"""Phase-0 spike: surgically change ONE Chinese string in the LawnStrings
TextAsset (Peashooter's name) to English, then repack the bundle with LZ4.
Minimal edit to isolate: does a UnityPy-written bundle load correctly in-game?
"""
import io
import zipfile
import UnityPy

APK = r"./pvzrh3.8.1.apk"
OUT = r"./work/data.unity3d.patched"
BUNDLE = "assets/bin/Data/data.unity3d"

OLD = '"name": "豌豆射手"'   # first occurrence = base Peashooter (seedType 0)
NEW = '"name": "Peashooter"'

with zipfile.ZipFile(APK) as z:
    raw = z.read(BUNDLE)
env = UnityPy.load(io.BytesIO(raw))

patched = 0
for o in env.objects:
    if o.type.name == "TextAsset":
        d = o.read()
        if str(d.m_Name) == "LawnStrings":
            s = d.m_Script if isinstance(d.m_Script, str) else bytes(d.m_Script).decode("utf-8", "surrogateescape")
            assert OLD in s, "target string not found in LawnStrings"
            s2 = s.replace(OLD, NEW, 1)          # change ONLY the first (base Peashooter)
            d.m_Script = s2
            d.save()
            patched += 1
            print("Peashooter names left:", s2.count("豌豆射手"), " 'Peashooter' occurrences:", s2.count("Peashooter"))
            break

assert patched == 1, f"expected 1 patch, got {patched}"
data = env.file.save(packer="lz4")
with open(OUT, "wb") as f:
    f.write(data)
print(f"patched={patched}  wrote {OUT}  ({len(data):,} bytes)")

# sanity: reload the patched bundle and confirm the change is really in it
env2 = UnityPy.load(OUT)
for o in env2.objects:
    if o.type.name == "TextAsset":
        d = o.read()
        if str(d.m_Name) == "LawnStrings":
            s = d.m_Script if isinstance(d.m_Script, str) else bytes(d.m_Script).decode("utf-8", "surrogateescape")
            print("verify in repacked bundle -> contains NEW name:", NEW in s)
            break
