#!/usr/bin/env bash
# Build a signed APK. Usage: bash build.sh <label>
# Set REPACK_SRC to an already-repacked/patched apk to just align+sign it;
# otherwise it repacks the original APK verbatim (baseline).
set -e
PROJ="."
ORIG="./pvzrh3.8.1.apk"
LABEL="${1:-baseline}"
OUT="$PROJ/output/$LABEL"
rm -rf "$OUT"; mkdir -p "$OUT"

SRC="${REPACK_SRC:-$ORIG}"
echo "[build] repack $SRC -> unsigned.apk (aligned)"
python "$PROJ/scripts/repack.py" "$SRC" "$OUT/unsigned.apk"

echo "[build] sign (v1+v2+v3, skip zipalign - already aligned)"
java -jar "$PROJ/tools/uber-apk-signer.jar" -a "$OUT/unsigned.apk" --skipZipAlign -o "$OUT"

echo "[build] result:"
ls -la "$OUT"/*.apk
