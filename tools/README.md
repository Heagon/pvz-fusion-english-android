# Build tools

Reference scripts used to produce the English APK. They are provided for
transparency and reproducibility. **They are not needed to *play*** — just download
the finished APK from Releases.

## What you need to reproduce
- **Python 3** with `UnityPy` and `Pillow`:  `pip install UnityPy pillow`
- **Java 8+** (to run uber-apk-signer)
- **Android platform-tools** (`adb`, optional `zipalign`)
- [`uber-apk-signer.jar`](https://github.com/patrickfav/uber-apk-signer/releases)
- The **original Chinese APK** `pvzrh3.8.1.apk` (from the game's official channels)
- The **PC translation folder** `PvZ_Fusion_Translator/` (from
  https://github.com/Teyliu/PVZF-Translation)

> The original APK and the PC translation are **not** included in this repo — they
> belong to their creators. Bring your own copies and place them next to the scripts
> (see the path constants near the top of each script and edit them for your setup).

## Scripts
| File | Purpose |
|---|---|
| `repack.py` | Rebuild an APK from the original, replacing entries, keeping 4-byte alignment; strips old signatures for re-signing. |
| `patch_bundle_v2.py` | Main asset patcher: almanac merge (+ font-size wrap + the 9 extra plants), UI string splice into MonoBehaviours, English texture swap. Run with `--textures` for the full build. |
| `patch_metadata_v2.py` | Rebuild-based IL2CPP `global-metadata.dat` string-literal patcher (allows English of any length): HUD, buffs/modifiers, messages. |
| `patch_metadata.py` | Older safe in-place metadata patcher (only same-or-shorter English). Kept for reference. |
| `patch_bundle_full.py`, `patch_bundle_phase1.py`, `patch_bundle_spike.py` | Earlier iterations, kept for history. |
| `build.sh` | Repack + sign helper. |

## Rough flow
```bash
# 1) translate the asset bundle (with English menu textures)
python patch_bundle_v2.py --textures        # -> work/data.unity3d.v2

# 2) translate the code string-literals
python patch_metadata_v2.py global-metadata.orig.dat global-metadata.v2.dat

# 3) repack both into the APK, then sign
python - <<'PY'
from repack import repack_apk
repack_apk("pvzrh3.8.1.apk", "unsigned.apk", {
  "assets/bin/Data/data.unity3d": open("work/data.unity3d.v2","rb").read(),
  "assets/bin/Data/Managed/Metadata/global-metadata.dat": open("global-metadata.v2.dat","rb").read(),
})
PY
java -jar uber-apk-signer.jar -a unsigned.apk --skipZipAlign -o out/

# 4) install (clean install, so the metadata changes take effect)
adb uninstall com.LanPiaoPiao.PlantsVsZombiesRH
adb install out/unsigned-debugSigned.apk
```

Note: **metadata changes only appear after a clean install** — the app caches the
extracted `global-metadata.dat`, so `adb install -r` keeps the old one.
