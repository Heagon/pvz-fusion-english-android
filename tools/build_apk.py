"""Assemble the final (unsigned) APK from the patched artifacts, and bump the
`build-guid` so an over-the-top update (`adb install -r`) keeps player saves.

Why the build-guid bump (the save-loss fix):
  global-metadata.dat is stored DEFLATE-compressed in the APK, so on first launch
  Unity extracts it to  /sdcard/Android/data/<pkg>/files/il2cpp/Metadata/  and
  caches it there, keyed by boot.config's `build-guid`.  `install -r` keeps that
  external cache -> the game keeps using the OLD (stale) metadata unless the guid
  changes. A clean install would refresh it but also wipe the save (which lives in
  the same files/ dir). Setting build-guid = md5(patched metadata) makes the game
  re-extract our new English metadata on the next launch after an `install -r` --
  no uninstall, save preserved.
  (data.unity3d is STORED/mmap'd from the APK, so bundle/texture changes already
  apply on a plain `install -r`.)

Usage:
    python build_apk.py                 # -> unsigned.apk
"""
import hashlib
import os
import re
import sys
import zipfile

from repack import repack_apk

# edit these paths for your setup
ORIG = r"./pvzrh3.8.1.apk"                 # original Chinese APK
BUNDLE = r"./work/data.unity3d.v2"         # from patch_bundle_v2.py
META = r"./work/global-metadata.v2.dat"    # from patch_metadata_v2.py
OUT_APK = r"./unsigned.apk"

BOOT_ENTRY = "assets/bin/Data/boot.config"
BUNDLE_ENTRY = "assets/bin/Data/data.unity3d"
META_ENTRY = "assets/bin/Data/Managed/Metadata/global-metadata.dat"


def bump_build_guid(boot_bytes, guid):
    text = boot_bytes.decode("utf-8")
    if re.search(r"^build-guid=", text, re.M):
        text = re.sub(r"build-guid=[0-9a-fA-F]+", "build-guid=" + guid, text)
    else:
        text = text.rstrip("\n") + "\nbuild-guid=" + guid + "\n"
    return text.encode("utf-8")


def main(out_apk=OUT_APK):
    meta = open(META, "rb").read()
    bundle = open(BUNDLE, "rb").read()
    guid = hashlib.md5(meta).hexdigest()
    with zipfile.ZipFile(ORIG) as z:
        boot = bump_build_guid(z.read(BOOT_ENTRY), guid)
    replaced = repack_apk(ORIG, out_apk, {
        BUNDLE_ENTRY: bundle,
        META_ENTRY: meta,
        BOOT_ENTRY: boot,
    })
    print("build-guid ->", guid)
    print("replaced entries:", replaced)
    print("wrote %s (%s bytes)" % (out_apk, "{:,}".format(os.path.getsize(out_apk))))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else OUT_APK)
