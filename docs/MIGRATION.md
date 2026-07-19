# Keep your save when switching to this English build

Switching **from another build** (e.g. the original Chinese APK) **to this English
build** needs a one-time uninstall, because the two are signed with different keys —
and uninstalling deletes the save. But the save is a **single file in normal storage**,
so you can just back it up and put it back. **No root needed** (tested on Android 13).

Good news:
- The save is fully compatible (same game), so your Chinese-version progress works here.
- This is **one-time**. Future **English → English** updates (e.g. 3.8.1 → 3.9) are signed
  with the same key, so they install over the top and **keep your save automatically**.

Package name (same for all builds): `com.LanPiaoPiao.PlantsVsZombiesRH`

## Where the save is  ✅ verified
```
/sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
(`playerData.json` is your whole profile: progress, coins, unlocks. If the folder also
has a `LevelData` folder, back that up too. The `il2cpp` folder is just cache — ignore it.)

---

## Method A — With a PC (adb)  ✅ easiest & reliable, works on Android 11–14, no root

1. On the phone: **Developer options → USB debugging → ON**, plug into the PC, install
   [platform-tools](https://developer.android.com/tools/releases/platform-tools) so you have `adb`.
2. **Back up your save (do this BEFORE uninstalling):**
   ```
   adb pull /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
   ```
   (optional, if it exists:)
   ```
   adb pull /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/LevelData
   ```
3. **Switch builds:**
   ```
   adb uninstall com.LanPiaoPiao.PlantsVsZombiesRH
   adb install PvZ-Fusion-3.8.1-English.apk
   ```
4. **Launch the game once**, let it reach the menu, then fully close it (this creates the
   `files` folder).
5. **Restore your save:**
   ```
   adb push playerData.json /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
   ```
   (and `adb push LevelData /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/` if you backed it up)
6. Open the game — your progress is back. 🎉  *(Verified: profile, coins and level progress carry over.)*

---

## Method B — Phone only (file manager)  ⚠️ easy on Android ≤10, needs a capable file manager on 11+

1. In a file manager, open
   `Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/` and **copy `playerData.json`**
   (and the `LevelData` folder if present) somewhere safe, e.g. `Download/`.
2. Uninstall the old game, install `PvZ-Fusion-3.8.1-English.apk`, launch it once, then close it.
3. **Copy `playerData.json` back** into
   `Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/`, overwriting.

On **Android 11+**, the built-in Files app usually can't open other apps' `Android/data`
folders. Use one that can (**MT Manager**, **ZArchiver**, **MiXplorer**, or your phone
maker's own Files app), or use Method A. Rooted phones can copy it freely.

---

## Notes
- Always back up **before** uninstalling — uninstalling is what deletes the save.
- Keep a copy of `playerData.json` somewhere safe; there is **no cloud save**.
- If the game ever won't launch after restoring, delete the `il2cpp` cache folder in the
  same `files/` directory (it's regenerated on next launch) and try again.
