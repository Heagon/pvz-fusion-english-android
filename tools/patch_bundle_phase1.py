"""Phase 1: translate the three almanac TextAssets to English by merging the
PC mod's English localization onto the Chinese data (keeping Chinese for any
entry the translation doesn't cover, so nothing goes missing).

- LawnStrings   : merge by seedType        (plants[])
- ZombieStrings : merge by theZombieType   (zombies[])
- DetailStrings : map English text by the Chinese title key (details[])

Writes work/data.unity3d.phase1 (LZ4-packed).
"""
import io
import json
import zipfile
import UnityPy

APK = r"./pvzrh3.8.1.apk"
EN = r"./PvZ_Fusion_Translator/Localization/English"
OUT = r"./work/data.unity3d.phase1"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def merge_array(cn_text, en_json, arr_key, id_key, fields):
    """Overlay en fields onto cn entries matched by id_key. Return (new_text, n_tr, n_kept)."""
    cn = json.loads(cn_text)
    en_by_id = {x[id_key]: x for x in en_json[arr_key]}
    n_tr = n_kept = 0
    for entry in cn[arr_key]:
        eid = entry.get(id_key)
        src = en_by_id.get(eid)
        if src is None:
            n_kept += 1
            continue
        for fld in fields:
            if fld in src:
                entry[fld] = src[fld]
        n_tr += 1
    return json.dumps(cn, ensure_ascii=False), n_tr, n_kept


def merge_details(cn_text, en_map):
    """DetailStrings: en_map is {chinese_title: english_text}. Replace text by title."""
    cn = json.loads(cn_text)
    n_tr = n_kept = 0
    for entry in cn.get("details", []):
        title = entry.get("title")
        if title in en_map:
            entry["text"] = en_map[title]
            n_tr += 1
        else:
            n_kept += 1
    return json.dumps(cn, ensure_ascii=False), n_tr, n_kept


lawn_en = load_json(f"{EN}/Almanac/LawnStringsTranslate.json")
zomb_en = load_json(f"{EN}/Almanac/ZombieStringsTranslate.json")
det_en = load_json(f"{EN}/Almanac/DetailStringsTranslate.json")

with zipfile.ZipFile(APK) as z:
    raw = z.read("assets/bin/Data/data.unity3d")
env = UnityPy.load(io.BytesIO(raw))

report = {}
for o in env.objects:
    if o.type.name != "TextAsset":
        continue
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
    report[name] = (tr, kept)

print("translation report (translated, kept-chinese):")
for k, v in report.items():
    print(f"  {k}: translated={v[0]}  kept_cn={v[1]}")

data = env.file.save(packer="lz4")
with open(OUT, "wb") as f:
    f.write(data)
print(f"wrote {OUT} ({len(data):,} bytes)")

# sanity reload
env2 = UnityPy.load(OUT)
for o in env2.objects:
    if o.type.name == "TextAsset":
        d = o.read()
        if str(d.m_Name) == "LawnStrings":
            s = d.m_Script if isinstance(d.m_Script, str) else bytes(d.m_Script).decode("utf-8", "surrogateescape")
            print("reload check: 'Peashooter' in LawnStrings:", '"name": "Peashooter"' in s,
                  " | 'Sunflower':", '"name": "Sunflower"' in s)
            break
