# Updating without losing your save

**Short version:** once you are on an English build from this repo, every later English
update **installs over the top and keeps your save automatically** — do **not** uninstall.

Your save lives in the app's own data folder:
```
/sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
Uninstalling is the *only* thing that deletes it. So the rule is simple: **update in
place, never uninstall.**

---

## Which situation are you in?

### A) You already have an English build from this repo → future English update
*(e.g. this 3.8.1 → a newer 3.8.1 build, or 3.8.1 → 3.9)*

Just install the new APK over the old one. **Your save is kept.** No PC needed.

- **Phone only:** download the new `PvZ-Fusion-…-English.apk`, open it, tap **Update/Install**
  (Android installs it over the existing app). Launch — progress and the new English text
  are both there.
- Every build from this repo is signed with the **same key**, so Android allows the
  in-place update; and the APK carries a fresh **build-guid**, which makes the game refresh
  its English code-strings on the next launch — **no uninstall, no cleared save.**

> Don't tap "uninstall" out of habit. In-place update = save kept. Uninstall = save gone.

### B) First time switching *to* this English build
*(you currently have the original **Chinese** APK, or the very first v3.8.1 English release
that was signed with a different key)*

This one time only, Android can't install over the top (different signing key), so you must
uninstall first — which deletes the save unless you back it up. It's a single file, so this
is easy and **no root is needed**. Follow **[MIGRATION.md](MIGRATION.md)** (back up →
uninstall → install → restore). After this, you're in situation A forever.

---

## Easiest safe update with a PC (one command)

If you have a PC with `adb`, the included **[../tools/update.ps1](../tools/update.ps1)**
backs up your save, installs the update, and restores the save if anything goes wrong:

```powershell
# normal update (English -> English): keeps the save, refreshes the text
powershell -ExecutionPolicy Bypass -File tools\update.ps1 -Apk PvZ-Fusion-3.8.1-English.apk

# first switch from a differently-signed build (situation B): safe uninstall+restore
powershell -ExecutionPolicy Bypass -File tools\update.ps1 -Apk PvZ-Fusion-3.8.1-English.apk -Clean
```
(USB debugging must be ON. Put `adb.exe` next to the script or have platform-tools on PATH.)

## Manual update with a PC (adb)

```
# situation A — keep save automatically:
adb install -r PvZ-Fusion-3.8.1-English.apk

# always safe — back up first, then update:
adb pull /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
adb install -r PvZ-Fusion-3.8.1-English.apk
# (only if the save ever disappears:)
adb push playerData.json /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```

---

## FAQ

- **Do I need to clear the `il2cpp` cache anymore?** No. Older notes said metadata only
  updated after a clean install; the build now changes its `build-guid` each release, so the
  game re-extracts the English metadata by itself on the next launch after an in-place update.
- **Will my coins/levels survive?** Yes — they're all in `playerData.json`, which an
  in-place update never touches. (Verified on Android 13.)
- **Is there a cloud save?** No. Keep a copy of `playerData.json` somewhere safe if it matters
  to you.
- **"App not installed" when updating?** You're likely in situation B (different signing key)
  — use `-Clean` / MIGRATION.md this one time.
