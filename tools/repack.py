"""Rebuild an APK from a source APK, optionally replacing some entries.

- Copies every entry from src_apk to out_apk, preserving compress_type.
- Drops old signature files (META-INF/*.SF/*.RSA/*.DSA/MANIFEST.MF) so it can be re-signed.
- 4-byte-aligns STORED (uncompressed) entries' data offset (like `zipalign -f 4`),
  which Android API 30+ requires for resources.arsc and Unity needs for mmap'd data.unity3d.
- Entries whose name is a key in `replacements` get the new bytes instead.
"""
import zipfile
import sys

ALIGN = 4


def _is_old_sig(name):
    if not name.startswith("META-INF/"):
        return False
    base = name.rsplit("/", 1)[-1].upper()
    return base == "MANIFEST.MF" or base.endswith((".SF", ".RSA", ".DSA"))


def repack_apk(src_apk, out_apk, replacements=None):
    replacements = replacements or {}
    replaced = []
    with zipfile.ZipFile(src_apk, "r") as zin, zipfile.ZipFile(out_apk, "w") as zout:
        for info in zin.infolist():
            name = info.filename
            if _is_old_sig(name):
                continue
            if name in replacements:
                data = replacements[name]
                replaced.append(name)
            else:
                data = zin.read(name)
            zi = zipfile.ZipInfo(name, date_time=info.date_time)
            zi.compress_type = info.compress_type
            zi.external_attr = info.external_attr
            zi.internal_attr = info.internal_attr
            zi.create_system = info.create_system
            if zi.compress_type == zipfile.ZIP_STORED:
                offset = zout.fp.tell()  # where this local header will start
                nlen = len(name.encode("utf-8"))
                pad = (ALIGN - (offset + 30 + nlen) % ALIGN) % ALIGN
                zi.extra = b"\x00" * pad
            zout.writestr(zi, data)
    return replaced


if __name__ == "__main__":
    r = repack_apk(sys.argv[1], sys.argv[2])
    print("repacked ->", sys.argv[2])
    print("replaced entries:", r)
