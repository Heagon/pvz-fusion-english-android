"""Assemble the final (unsigned) APK from the patched artifacts.

Swaps the patched bundle + metadata into the source APK AND bumps the game's
`unity_app_guid` so the game re-extracts the metadata cache on an `adb install -r`
(an over-the-top install that KEEPS player saves) instead of requiring a save-wiping
clean install.

Why the unity_app_guid bump (the save-loss fix), VERIFIED on device 2026-07-26:
  global-metadata.dat (and the mscorlib resources) are stored DEFLATE-compressed in
  the APK, so on first launch Unity extracts them to
    /sdcard/Android/data/<pkg>/files/il2cpp/{Metadata,Resources}/
  and caches them, writing a marker file  il2cpp/unity.ver  whose contents equal the
  APK's  assets/bin/Data/unity_app_guid.  On later launches Unity re-extracts ONLY
  when  unity.ver != unity_app_guid.
  `install -r` keeps that external cache, so unless unity_app_guid changes the game
  keeps using the OLD (stale) metadata -> our new English code-strings never show
  without a clean install (uninstall), which wipes the external save (playerData.json
  lives in the same files/ dir).  Changing unity_app_guid makes unity.ver stale ->
  Unity re-extracts our new metadata + resources on the next launch, no uninstall,
  save preserved.

  NOTE: boot.config's `build-guid` does NOT gate this cache -- tested on device,
  changing only build-guid did nothing.  unity_app_guid is the real key.  We set
  unity_app_guid = md5(patched metadata) formatted as a UUID, so it changes iff the
  metadata changed (no needless re-extraction when only the bundle/textures change).
  We also bump build-guid to the same value (a harmless build identifier).

  data.unity3d is STORED (uncompressed) and mmap'd straight from the APK each launch,
  so bundle/almanac/texture changes already apply on a plain `install -r`.

Usage:
    python scripts/build_apk.py                 # -> work/unsigned.apk
    python scripts/build_apk.py path/to/out.apk # custom output path
"""
import hashlib
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import APK, WORK, OUT, META_OUT
from repack import repack_apk

BOOT_ENTRY = "assets/bin/Data/boot.config"
BUNDLE_ENTRY = "assets/bin/Data/data.unity3d"
META_ENTRY = "assets/bin/Data/Managed/Metadata/global-metadata.dat"
APPGUID_ENTRY = "assets/bin/Data/unity_app_guid"   # THE il2cpp extraction-cache key


def md5_to_uuid(h):
    """32-hex md5 -> 36-char UUID (8-4-4-4-12), same shape/length as unity_app_guid."""
    return "%s-%s-%s-%s-%s" % (h[0:8], h[8:12], h[12:16], h[16:20], h[20:32])


def bump_build_guid(boot_bytes, guid):
    """Return boot.config bytes with build-guid set to `guid` (32 hex chars)."""
    text = boot_bytes.decode("utf-8")
    if re.search(r"^build-guid=", text, re.M):
        text = re.sub(r"build-guid=[0-9a-fA-F]+", "build-guid=" + guid, text)
    else:
        text = text.rstrip("\n") + "\nbuild-guid=" + guid + "\n"
    return text.encode("utf-8")


def main(out_apk=None):
    out_apk = out_apk or os.path.join(WORK, "unsigned.apk")
    bundle = open(OUT, "rb").read()
    meta = open(META_OUT, "rb").read()

    h = hashlib.md5(meta).hexdigest()
    app_guid = md5_to_uuid(h)                       # the value that forces re-extract
    with zipfile.ZipFile(APK) as z:
        orig_boot = z.read(BOOT_ENTRY)
        old_app_guid = z.read(APPGUID_ENTRY).decode("utf-8", "replace")
    boot = bump_build_guid(orig_boot, h)

    replaced = repack_apk(APK, out_apk, {
        BUNDLE_ENTRY: bundle,
        META_ENTRY: meta,
        BOOT_ENTRY: boot,
        APPGUID_ENTRY: app_guid.encode("utf-8"),    # 36 bytes, same length as orig
    })

    print("unity_app_guid: %s -> %s" % (old_app_guid, app_guid))
    print("build-guid    -> %s" % h)
    print("replaced entries:", replaced)
    print("wrote %s (%s bytes)" % (out_apk, "{:,}".format(os.path.getsize(out_apk))))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
