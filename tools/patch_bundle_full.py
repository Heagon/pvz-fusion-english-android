"""Full pass: translate everything we can statically into English, in one bundle.

A) Almanac TextAssets (LawnStrings/ZombieStrings/DetailStrings) — merge English
   over Chinese by id (keeps Chinese for entries the mod didn't translate).
B) UI strings in MonoBehaviours — splice the mod's translation_strings.json
   English over the Chinese, matched as *complete* Unity-framed strings
   ([int32 len][utf8][align4]) with safety validators, so length can change.

Writes work/data.unity3d.full (LZ4).
"""
import io
import json
import struct
import re
import os
import glob
import zipfile
import UnityPy
from PIL import Image

APK = r"./pvzrh3.8.1.apk"
EN = r"./PvZ_Fusion_Translator/Localization/English"
OUT = r"./work/data.unity3d.full"

CJK = re.compile(r'[一-鿿㐀-䶿]')


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


# ---------- A) almanac merge ----------
def merge_array(cn_text, en_json, arr_key, id_key, fields):
    cn = json.loads(cn_text)
    en_by_id = {x[id_key]: x for x in en_json[arr_key]}
    tr = kept = 0
    for entry in cn[arr_key]:
        src = en_by_id.get(entry.get(id_key))
        if src is None:
            kept += 1
            continue
        for fld in fields:
            if fld in src:
                entry[fld] = src[fld]
        tr += 1
    return json.dumps(cn, ensure_ascii=False), tr, kept


def merge_details(cn_text, en_map):
    cn = json.loads(cn_text)
    tr = kept = 0
    for entry in cn.get("details", []):
        t = entry.get("title")
        if t in en_map:
            entry["text"] = en_map[t]
            tr += 1
        else:
            kept += 1
    return json.dumps(cn, ensure_ascii=False), tr, kept


# ---------- B) UI dict ----------
def build_ui_dict():
    ts = load_json(f"{EN}/Strings/translation_strings.json")
    d = {}
    for k, v in ts.items():
        if not isinstance(v, str):
            continue
        if k.strip().startswith("---") or v.strip().endswith("-------"):
            continue
        if not CJK.search(k):        # only Chinese keys
            continue
        if v == "":
            continue
        d[k] = v
    d["关闭"] = "Close"              # override: standalone 关闭 is usually a Close button
    return d


def splice_object(data, dict_pats):
    """Return (new_bytes, n) splicing all safe framed matches. data is bytes."""
    matches = []  # (idx, cn_bytes_len, en_bytes)
    for cn_b, (pat, en_b) in dict_pats.items():
        start = 0
        while True:
            i = data.find(pat, start)
            if i < 0:
                break
            start = i + 1
            # validators
            if i % 4 != 0:
                continue
            cn_len = len(cn_b)
            end = i + 4 + cn_len
            pad = (4 - (i + 4 + cn_len) % 4) % 4
            if data[end:end + pad] != b"\x00" * pad:   # real string padding is zero
                continue
            matches.append((i, cn_len, en_b))
    if not matches:
        return data, 0
    # apply right-to-left so earlier offsets stay valid
    matches.sort(key=lambda m: m[0], reverse=True)
    buf = bytearray(data)
    n = 0
    for i, cn_len, en_b in matches:
        old_end = i + 4 + cn_len + ((4 - (i + 4 + cn_len) % 4) % 4)
        new_pad = (4 - (i + 4 + len(en_b)) % 4) % 4
        new_field = struct.pack('<i', len(en_b)) + en_b + b"\x00" * new_pad
        buf[i:old_end] = new_field
        n += 1
    return bytes(buf), n


def build_texture_map():
    """name (no ext) -> png path, for mod English textures/sprites."""
    m = {}
    for p in glob.glob(f"{EN}/Textures/**/*.png", recursive=True) + glob.glob(f"{EN}/Sprites/**/*.png", recursive=True):
        m[os.path.splitext(os.path.basename(p))[0]] = p
    return m


def main():
    lawn_en = load_json(f"{EN}/Almanac/LawnStringsTranslate.json")
    zomb_en = load_json(f"{EN}/Almanac/ZombieStringsTranslate.json")
    det_en = load_json(f"{EN}/Almanac/DetailStringsTranslate.json")
    ui = build_ui_dict()
    dict_pats = {k.encode(): (struct.pack('<i', len(k.encode())) + k.encode(), v.encode())
                 for k, v in ui.items()}
    print(f"UI dict pairs: {len(ui)}")

    tex_map = build_texture_map()
    tex_cache = {}
    print(f"mod textures: {len(tex_map)}")

    with zipfile.ZipFile(APK) as z:
        raw = z.read("assets/bin/Data/data.unity3d")
    env = UnityPy.load(io.BytesIO(raw))

    almanac_report = {}
    ui_objs = 0
    ui_sites = 0
    tex_replaced = 0
    tex_names = set()
    for o in env.objects:
        tn = o.type.name
        if tn == "Texture2D":
            d = o.read()
            nm = str(d.m_Name)
            if nm in tex_map:
                if nm not in tex_cache:
                    tex_cache[nm] = Image.open(tex_map[nm]).convert("RGBA")
                img = tex_cache[nm]
                if (d.m_Width, d.m_Height) == img.size:
                    d.image = img
                    d.save()
                    tex_replaced += 1
                    tex_names.add(nm)
            continue
        if tn == "TextAsset":
            d = o.read()
            name = str(d.m_Name)
            if name not in ("LawnStrings", "ZombieStrings", "DetailStrings"):
                continue
            s = d.m_Script if isinstance(d.m_Script, str) else bytes(d.m_Script).decode("utf-8", "surrogateescape")
            if name == "LawnStrings":
                new, tr, kept = merge_array(s, lawn_en, "plants", "seedType", ["name", "introduce", "info", "cost"])
            elif name == "ZombieStrings":
                new, tr, kept = merge_array(s, zomb_en, "zombies", "theZombieType", ["name", "introduce", "info"])
            else:
                new, tr, kept = merge_details(s, det_en)
            d.m_Script = new
            d.save()
            almanac_report[name] = (tr, kept)
        elif tn == "MonoBehaviour":
            data = o.get_raw_data()
            new, n = splice_object(data, dict_pats)
            if n:
                o.set_raw_data(new)
                ui_objs += 1
                ui_sites += n

    print("almanac:", almanac_report)
    print(f"UI splice: objects={ui_objs} sites={ui_sites}")
    print(f"textures replaced: {tex_replaced} objects, {len(tex_names)} distinct names")

    out = env.file.save(packer="lz4")
    with open(OUT, "wb") as f:
        f.write(out)
    print(f"wrote {OUT} ({len(out):,} bytes)")

    # reload validation
    env2 = UnityPy.load(OUT)
    checks = {"LawnStrings_Peashooter": False, "UI_Settings": False, "UI_UpdateLog": False}
    for o in env2.objects:
        if o.type.name == "TextAsset":
            d = o.read()
            if str(d.m_Name) == "LawnStrings":
                s = d.m_Script if isinstance(d.m_Script, str) else bytes(d.m_Script).decode("utf-8", "surrogateescape")
                checks["LawnStrings_Peashooter"] = '"name": "Peashooter"' in s
        elif o.type.name == "MonoBehaviour":
            data = o.get_raw_data()
            if b"Settings" in data and struct.pack('<i', 8) + b"Settings" in data:
                checks["UI_Settings"] = True
    print("reload checks:", checks)


if __name__ == "__main__":
    main()
