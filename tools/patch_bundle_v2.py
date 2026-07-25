"""Comprehensive translation pass v2.

Sources (all from the PC mod):
  - Almanac (structured, best quality): LawnStrings/ZombieStrings/DetailStrings
  - Master CN->EN dict: translation_strings + travel_buffs + tips_fs/tips_iz
    + plant/zombie names (from almanac CN->EN), applied to:
      * every non-almanac TextAsset's JSON string VALUES (exact match)
      * MonoBehaviour complete framed strings (exact match, length-safe splice)

Fixes:
  - Almanac font too big -> strip <size=..> tags (use component default, like the
    original Chinese which had none).

Textures replaced only when run with `--textures` (slow ASTC encode).

Usage: python patch_bundle_v2.py [--textures]   -> writes work/data.unity3d.v2
"""
import io
import os
import re
import sys
import glob
import json
import struct
import zipfile
import unicodedata
import UnityPy
from PIL import Image

APK = r"./pvzrh3.8.1.apk"
MOD = r"./PvZ_Fusion_Translator"
EN = MOD + r"/Localization/English"
TRANS = r"./translations"
OUT = r"./work/data.unity3d.v2"

WITH_TEXTURES = "--textures" in sys.argv
CJK = re.compile(r'[一-鿿㐀-䶿豈-﫿]')
SIZE_TAG = re.compile(r'</?size[^>]*>')
ALMANAC = ("LawnStrings", "ZombieStrings", "DetailStrings")
ALMANAC_SIZE = 12  # smaller than the game default so long English descriptions fit
# Make these display fonts render as a nicer font by copying a source font's FULL
# config (data + names + metrics + kerning) into them. Copying the whole config
# (not just m_FontData) avoids glyph-mapping bugs from mismatched m_FontNames/metrics.
FONT_SRC_NAME = "黑体"
# Font swap DISABLED: replacing a Font via UnityPy consistently corrupts a few glyphs
# (z->{, q->r, "->#) regardless of source font. Keep the game's original font (renders
# all characters correctly); readability is handled by ALMANAC_SIZE instead.
FONT_TARGETS = set()
FONT_COPY_FIELDS = [
    "m_FontData", "m_FontNames", "m_LineSpacing", "m_Ascent", "m_Descent",
    "m_KerningValues", "m_ConvertCase", "m_CharacterPadding", "m_CharacterSpacing",
    "m_PixelScale", "m_Tracking", "m_DefaultStyle", "m_FontRenderingMode",
    "m_AsciiStartOffset", "m_FontSize", "m_ShouldRoundAdvanceValue",
    "m_UseLegacyBoundsCalculation", "m_FallbackFonts",
]


def LJ(p):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def deaccent(s):
    """Accented Latin letters (a-circumflex, e-acute, n-tilde, ...) -> plain ASCII, since
    the game's CN font has no glyph for them (renders a box). Symbols (x, degree) and CJK kept."""
    if not isinstance(s, str):
        return s
    out = []
    for ch in s:
        if 0xC0 <= ord(ch) <= 0x24F and unicodedata.category(ch).startswith("L"):
            base = "".join(c for c in unicodedata.normalize("NFKD", ch) if ord(c) < 128)
            out.append(base if base else ch)
        else:
            out.append(ch)
    return "".join(out)


def strip_size(text):
    return SIZE_TAG.sub("", text) if isinstance(text, str) else text


def size_wrap(text):
    """Strip the mod's size tags and wrap in a smaller absolute size so long
    English almanac text fits the box (legacy uGUI Text: absolute size only)."""
    if not isinstance(text, str) or not text.strip():
        return text
    return f"<size={ALMANAC_SIZE}>{strip_size(text)}</size>"


# ---------------- master CN->EN dict ----------------
def build_master():
    d = {}

    def add(cn, en):
        if isinstance(cn, str) and isinstance(en, str) and en and cn != en and CJK.search(cn):
            d.setdefault(cn, deaccent(en))

    ts = LJ(f"{EN}/Strings/translation_strings.json") or {}
    for k, v in ts.items():
        if isinstance(v, str) and not k.strip().startswith("---") and not v.strip().endswith("-------"):
            add(k, v)
    cnb, enb = LJ(f"{MOD}/Dumps/travel_buffs.json") or {}, LJ(f"{EN}/Strings/travel_buffs.json") or {}

    def walk(a, b):
        if isinstance(a, dict) and isinstance(b, dict):
            for k in a:
                if k in b:
                    walk(a[k], b[k])
        elif isinstance(a, str) and isinstance(b, str):
            add(a, b)
    walk(cnb, enb)
    for f in ("tips_fs", "tips_iz"):
        cnt, ent = LJ(f"{MOD}/Dumps/{f}.json") or {}, LJ(f"{EN}/Strings/{f}.json") or {}
        for k, v in cnt.items():
            if k in ent and isinstance(v, str):
                add(v, ent[k])
    # plant & zombie names (CN dump -> EN translate), by id
    lc, le = LJ(f"{MOD}/Dumps/LawnStrings.json"), LJ(f"{EN}/Almanac/LawnStringsTranslate.json")
    if lc and le:
        eb = {p["seedType"]: p for p in le["plants"]}
        for p in lc["plants"]:
            e = eb.get(p["seedType"])
            if e and "name" in e:
                add(p.get("name", ""), e["name"])
    zc, ze = LJ(f"{MOD}/Dumps/ZombieStrings.json"), LJ(f"{EN}/Almanac/ZombieStringsTranslate.json")
    if zc and ze:
        eb = {z["theZombieType"]: z for z in ze["zombies"]}
        for z in zc["zombies"]:
            e = eb.get(z["theZombieType"])
            if e and "name" in e:
                add(z.get("name", ""), e["name"])
    # supplement: my own translations (level/odyssey/buff strings the mod lacked)
    sup = LJ(f"{TRANS}/supplement.json") or {}
    for k, v in sup.items():
        add(k, v)
    # detail titles + types (Mechanics almanac headers)
    dt = LJ(f"{TRANS}/detail_titles_en.json") or {}
    for k, v in dt.get("titles", {}).items():
        add(k, v)
    for k, v in dt.get("types", {}).items():
        add(k, v)
    # 9 plants the mod didn't translate -> names into dict too
    nine = LJ(f"{TRANS}/nine_plants_en.json") or {}
    for st, p in nine.items():
        pass  # names handled in almanac merge; nothing to add to text dict
    # changelog popup body (one big MonoBehaviour framed string, shown every launch).
    # Key = the game's EXACT 3.8.1 Chinese (translations/changelog_cn.txt) since the mod's
    # 3.8 Dumps/changelog.txt differs; value = the team's official English changelog.
    cl_cn = os.path.join(TRANS, "changelog_cn.txt")
    cl_en = os.path.join(EN, "Strings", "changelog.txt")
    if os.path.exists(cl_cn) and os.path.exists(cl_en):
        with open(cl_cn, encoding="utf-8") as f:
            cn_cl = f.read()
        with open(cl_en, encoding="utf-8") as f:
            en_cl = f.read()
        add(cn_cl, en_cl)
    return d


# ---------------- almanac merge ----------------
def merge_array(cn_text, en_json, arr_key, id_key, fields):
    cn = json.loads(cn_text)
    by = {x[id_key]: x for x in en_json[arr_key]}
    tr = kept = 0
    for e in cn[arr_key]:
        s = by.get(e.get(id_key))
        if s is None:
            kept += 1
            continue
        for f in fields:
            if f in s:
                e[f] = deaccent(size_wrap(s[f]) if f in ("introduce", "info") else strip_size(s[f]))
        tr += 1
    return json.dumps(cn, ensure_ascii=False), tr, kept


def merge_details(cn_text, en_map, titles=None, types=None):
    titles = titles or {}
    types = types or {}
    cn = json.loads(cn_text)
    tr = kept = 0
    for e in cn.get("details", []):
        t = e.get("title")
        if t in en_map:
            e["text"] = deaccent(size_wrap(en_map[t]))
            tr += 1
        else:
            kept += 1
        if t in titles:
            e["title"] = titles[t]
        if e.get("type") in types:
            e["type"] = types[e["type"]]
    return json.dumps(cn, ensure_ascii=False), tr, kept


# ---------------- dict apply to TextAsset json values ----------------
def translate_values(obj, d, stat):
    if isinstance(obj, dict):
        return {k: translate_values(v, d, stat) for k, v in obj.items()}
    if isinstance(obj, list):
        return [translate_values(x, d, stat) for x in obj]
    if isinstance(obj, str) and obj in d:
        stat[0] += 1
        return d[obj]
    return obj


# ---------------- dict apply to MonoBehaviour framed strings ----------------
def splice_object(data, dict_pats):
    matches = []
    for pat, en_b, cn_len in dict_pats:
        start = 0
        while True:
            i = data.find(pat, start)
            if i < 0:
                break
            start = i + 1
            if i % 4 != 0:
                continue
            pad = (4 - (i + 4 + cn_len) % 4) % 4
            if data[i + 4 + cn_len: i + 4 + cn_len + pad] != b"\x00" * pad:
                continue
            matches.append((i, cn_len, en_b))
    if not matches:
        return data, 0
    matches.sort(key=lambda m: m[0], reverse=True)
    buf = bytearray(data)
    for i, cn_len, en_b in matches:
        old_end = i + 4 + cn_len + ((4 - (i + 4 + cn_len) % 4) % 4)
        new_pad = (4 - (i + 4 + len(en_b)) % 4) % 4
        buf[i:old_end] = struct.pack('<i', len(en_b)) + en_b + b"\x00" * new_pad
    return bytes(buf), len(matches)


def build_tex_map():
    m = {}
    for p in glob.glob(f"{EN}/Textures/**/*.png", recursive=True) + glob.glob(f"{EN}/Sprites/**/*.png", recursive=True):
        m[os.path.splitext(os.path.basename(p))[0]] = p
    return m


def main():
    master = build_master()
    # overrides: ambiguity, missing translations, and shorter text to avoid button overflow
    master["关闭"] = "Close"
    master["查看草坪"] = "View Lawn"
    master["切换手套"] = "Toggle Glove"
    master["机制图鉴"] = "Mechanics"   # was "Mechanics Almanac" -> overflowed
    master["词条图鉴"] = "Modifiers"   # was "Modifier Almanac" -> overflowed
    # highest-priority overrides (category shortenings, button-overflow fixes, etc.)
    for k, v in (LJ(f"{TRANS}/overrides.json") or {}).items():
        if not k.startswith("_"):
            master[k] = v
    print("master dict:", len(master))
    dict_pats = [(struct.pack('<i', len(k.encode())) + k.encode(), v.encode(), len(k.encode()))
                 for k, v in master.items()]

    lawn_en = LJ(f"{EN}/Almanac/LawnStringsTranslate.json")
    zomb_en = LJ(f"{EN}/Almanac/ZombieStringsTranslate.json")
    det_en = LJ(f"{EN}/Almanac/DetailStringsTranslate.json")
    # inject my translations for the 9 plants the mod omitted
    nine = LJ(f"{TRANS}/nine_plants_en.json") or {}
    have = {p["seedType"] for p in lawn_en["plants"]}
    for st, p in nine.items():
        if int(st) not in have:
            lawn_en["plants"].append({"seedType": int(st), **p})
    detail_titles = LJ(f"{TRANS}/detail_titles_en.json") or {"titles": {}, "types": {}}
    tex_map = build_tex_map() if WITH_TEXTURES else {}
    tex_cache = {}

    with zipfile.ZipFile(APK) as z:
        raw = z.read("assets/bin/Data/data.unity3d")
    env = UnityPy.load(io.BytesIO(raw))

    # grab source font config (to copy into the target display fonts)
    font_src = None
    for o in env.objects:
        if o.type.name == "Font":
            tt = o.read_typetree()
            if tt.get("m_Name") == FONT_SRC_NAME:
                font_src = dict(tt)  # full clone incl. m_Texture/m_DefaultMaterial
                break

    alm = {}
    ta_val = [0]
    ta_hit = 0
    ui_objs = ui_sites = 0
    tex_n = 0
    font_n = 0
    for o in env.objects:
        tn = o.type.name
        if tn == "Font":
            d = o.read()
            nm = str(d.m_Name)
            if nm in FONT_TARGETS and font_src is not None:
                tt = o.read_typetree()
                for k, v in font_src.items():
                    tt[k] = v            # keep this object's m_Texture/m_DefaultMaterial/path_id
                o.save_typetree(tt)
                font_n += 1
            continue
        if tn == "Texture2D":
            if not WITH_TEXTURES:
                continue
            d = o.read()
            nm = str(d.m_Name)
            if nm in tex_map:
                if nm not in tex_cache:
                    tex_cache[nm] = Image.open(tex_map[nm]).convert("RGBA")
                img = tex_cache[nm]
                if (d.m_Width, d.m_Height) == img.size:
                    d.image = img
                    d.save()
                    tex_n += 1
            continue
        if tn == "TextAsset":
            d = o.read()
            name = str(d.m_Name)
            s = d.m_Script if isinstance(d.m_Script, str) else bytes(d.m_Script).decode("utf-8", "surrogateescape")
            if name == "LawnStrings":
                new, tr, kept = merge_array(s, lawn_en, "plants", "seedType", ["name", "introduce", "info", "cost"])
                alm[name] = (tr, kept)
                d.m_Script = new
                d.save()
            elif name == "ZombieStrings":
                new, tr, kept = merge_array(s, zomb_en, "zombies", "theZombieType", ["name", "introduce", "info"])
                alm[name] = (tr, kept)
                d.m_Script = new
                d.save()
            elif name == "DetailStrings":
                new, tr, kept = merge_details(s, det_en, detail_titles.get("titles", {}), detail_titles.get("types", {}))
                alm[name] = (tr, kept)
                d.m_Script = new
                d.save()
            else:
                if CJK.search(s):
                    try:
                        j = json.loads(s)
                    except Exception:
                        continue
                    st = [0]
                    j2 = translate_values(j, master, st)
                    if st[0]:
                        d.m_Script = json.dumps(j2, ensure_ascii=False)
                        d.save()
                        ta_hit += 1
                        ta_val[0] += st[0]
        elif tn == "MonoBehaviour":
            data = o.get_raw_data()
            if b'\xe4' not in data and b'\xe5' not in data and b'\xe6' not in data and b'\xe7' not in data \
               and b'\xe8' not in data and b'\xe9' not in data:
                continue  # no common CJK lead byte -> skip
            new, n = splice_object(data, dict_pats)
            if n:
                o.set_raw_data(new)
                ui_objs += 1
                ui_sites += n

    print("almanac:", alm)
    print(f"fonts replaced: {font_n}")
    print(f"TextAsset value-translations: {ta_val[0]} values in {ta_hit} assets")
    print(f"MonoBehaviour splice: objects={ui_objs} sites={ui_sites}")
    if WITH_TEXTURES:
        print(f"textures replaced: {tex_n}")

    out = env.file.save(packer="lz4")
    with open(OUT, "wb") as f:
        f.write(out)
    print(f"wrote {OUT} ({len(out):,} bytes)")


if __name__ == "__main__":
    main()
