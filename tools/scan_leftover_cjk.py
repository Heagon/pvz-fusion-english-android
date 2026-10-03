"""Audit: list every Chinese string still left AFTER patching, so the gaps can be
translated. Scans work/global-metadata.v2.dat (IL2CPP string literals) and
work/data.unity3d.v2 (TextAsset JSON values + MonoBehaviour framed strings).

Usage: python scan_leftover_cjk.py   -> work/leftover/{metadata,textasset,mono}.json
"""
import os
import re
import json
import struct
import UnityPy
from config import WORK, META_OUT, OUT

CJK = re.compile(r'[一-鿿㐀-䶿]')
DST = os.path.join(WORK, "leftover")


def metadata_literals(path):
    gm = open(path, "rb").read()
    tOff, tSize = struct.unpack_from("<II", gm, 8)
    dOff = struct.unpack_from("<I", gm, 16)[0]
    out = {}
    for i in range(tSize // 8):
        ln, di = struct.unpack_from("<II", gm, tOff + i * 8)
        s = gm[dOff + di: dOff + di + ln].decode("utf-8", "replace")
        if CJK.search(s):
            out.setdefault(s, i)
    return out


def walk_values(obj, acc, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            walk_values(v, acc, f"{path}/{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_values(v, acc, f"{path}[{i}]")
    elif isinstance(obj, str) and CJK.search(obj):
        acc.append((path, obj))


def framed_strings(data):
    """Unity-serialized strings: int32 len, utf8, pad to 4. Yield CJK ones."""
    i, n = 0, len(data)
    while i + 4 <= n:
        ln = struct.unpack_from("<i", data, i)[0]
        if 2 < ln < 20000 and i + 4 + ln <= n:
            try:
                s = data[i + 4: i + 4 + ln].decode("utf-8")
            except UnicodeDecodeError:
                s = None
            if s and CJK.search(s):
                yield i, s
                i += 4 + ln + ((4 - ln % 4) % 4)
                continue
        i += 4


def main():
    os.makedirs(DST, exist_ok=True)
    meta = metadata_literals(META_OUT)
    print("metadata CJK literals:", len(meta))
    json.dump(meta, open(f"{DST}/metadata.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

    env = UnityPy.load(open(OUT, "rb").read())
    ta, mono = {}, {}
    for o in env.objects:
        tn = o.type.name
        if tn == "TextAsset":
            d = o.read()
            s = d.m_Script if isinstance(d.m_Script, str) else bytes(d.m_Script).decode("utf-8", "replace")
            if not CJK.search(s):
                continue
            try:
                acc = []
                walk_values(json.loads(s.lstrip("﻿")), acc)
                ta[str(d.m_Name)] = acc
            except Exception:
                ta[str(d.m_Name)] = [("<raw>", s[:3000])]
        elif tn == "MonoBehaviour":
            hits = [s for _, s in framed_strings(o.get_raw_data())]
            if hits:
                mono[str(o.path_id)] = hits
    print("TextAssets with CJK:", len(ta), "values:", sum(len(v) for v in ta.values()))
    print("MonoBehaviours with CJK:", len(mono), "unique strings:", len({s for v in mono.values() for s in v}))
    json.dump(ta, open(f"{DST}/textasset.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    json.dump(mono, open(f"{DST}/mono.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)


if __name__ == "__main__":
    main()
