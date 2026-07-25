"""Assemble the final (unsigned) APK from the patched artifacts, and bump the game's
`unity_app_guid` so an over-the-top update (`adb install -r`) refreshes the English
text while KEEPING player saves.

Why the unity_app_guid bump (the save-loss fix), verified on device:
  global-metadata.dat (and the mscorlib resources) are stored DEFLATE-compressed in
  the APK, so on first launch Unity extracts them to
    /sdcard/Android/data/<pkg>/files/il2cpp/{Metadata,Resources}/
  and caches them, writing a marker  il2cpp/unity.ver  =  the APK's
  assets/bin/Data/unity_app_guid.  Later launches re-extract ONLY when
  unity.ver != unity_app_guid.  `install -r` keeps that cache, so unless
  unity_app_guid changes the game keeps the OLD (stale) metadata -> the new English
  code-strings never show without a clean install (uninstall), which wipes the
  external save (playerData.json is in the same files/ dir).  Changing unity_app_guid
  makes unity.ver stale -> Unity re-extracts our new metadata on the next launch, no
  uninstall, save preserved.
  (boot.config's build-guid does NOT gate this cache -- tested; unity_app_guid does.)
  We set unity_app_guid = md5(patched metadata) as a UUID so it changes iff the
  metadata changed.  data.unity3d is STORED/mmap'd from the APK, so bundle/texture
  changes already apply on a plain `install -r`.

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
APPGUID_ENTRY = "assets/bin/Data/unity_app_guid"   # THE il2cpp extraction-cache key


def md5_to_uuid(h):
    """32-hex md5 -> 36-char UUID (8-4-4-4-12), same shape/length as unity_app_guid."""
    return "%s-%s-%s-%s-%s" % (h[0:8], h[8:12], h[12:16], h[16:20], h[20:32])


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
    h = hashlib.md5(meta).hexdigest()
    app_guid = md5_to_uuid(h)
    with zipfile.ZipFile(ORIG) as z:
        boot = bump_build_guid(z.read(BOOT_ENTRY), h)
        old_app_guid = z.read(APPGUID_ENTRY).decode("utf-8", "replace")
    replaced = repack_apk(ORIG, out_apk, {
        BUNDLE_ENTRY: bundle,
        META_ENTRY: meta,
        BOOT_ENTRY: boot,
        APPGUID_ENTRY: app_guid.encode("utf-8"),   # 36 bytes, same length as orig
    })
    print("unity_app_guid: %s -> %s" % (old_app_guid, app_guid))
    print("build-guid    ->", h)
    print("replaced entries:", replaced)
    print("wrote %s (%s bytes)" % (out_apk, "{:,}".format(os.path.getsize(out_apk))))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else OUT_APK)
