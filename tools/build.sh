#!/usr/bin/env bash
# Build a signed APK. Usage: bash build.sh <label>
# Set REPACK_SRC to an already-repacked/patched apk to just align+sign it;
# otherwise it repacks the ORIGINAL APK (path taken from scripts/config.py) verbatim.
set -e
PROJ="."
# original APK path comes from config.py (single source of truth) so this never goes
# stale across game versions (3.8.1 -> 3.9 -> ...).
ORIG="$(python -c "import sys; sys.path.insert(0, '$PROJ/scripts'); import config; print(config.APK)")"
LABEL="${1:-baseline}"
OUT="$PROJ/output/$LABEL"
rm -rf "$OUT"; mkdir -p "$OUT"

SRC="${REPACK_SRC:-$ORIG}"
echo "[build] repack $SRC -> unsigned.apk (aligned)"
python "$PROJ/scripts/repack.py" "$SRC" "$OUT/unsigned.apk"

# uber-apk-signer.jar: allow override via $SIGNER; else prefer tools/, then the
# english-build tools dir (the workspace itself has no tools/ folder).
SIGNER="${SIGNER:-$PROJ/tools/uber-apk-signer.jar}"
[ -f "$SIGNER" ] || SIGNER="$PROJ/../english-build/tools/uber-apk-signer.jar"
echo "[build] sign (v1+v2+v3, skip zipalign - already aligned) using $SIGNER"
java -jar "$SIGNER" -a "$OUT/unsigned.apk" --skipZipAlign -o "$OUT"

echo "[build] result:"
ls -la "$OUT"/*.apk
