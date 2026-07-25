# Install guide (Android)

## Requirements
- Android **8.0+** phone/tablet.
- **arm64-v8a** CPU (basically any phone from ~2018 onward).
- ~1.2 GB free space (the APK is ~555 MB; it needs room to install).

## Steps
1. **Download** `PvZ-Fusion-3.8.1-English.apk` from the
   [Releases](../../releases) page onto your phone.
2. **If you already have the game installed, decide how to install:**
   - **Coming from the original Chinese APK (or a build not from this repo):** you must
     **uninstall it first** (it's signed with a different key). Uninstalling deletes your
     save, so **back it up first** — see **[MIGRATION.md](MIGRATION.md)**.
   - **Already on an English build from this repo (updating):** **do NOT uninstall.** Just
     install this APK **over the top** — your save is kept automatically. See
     **[UPDATE.md](UPDATE.md)**.
   - **Fresh phone (game not installed):** nothing to do, continue.
3. **Allow install from unknown sources** for the app you'll open the APK with:
   - Settings → Apps → (your browser / Files app) → **Install unknown apps** → Allow.
4. Open the APK (from the browser's downloads, or a file manager) → **Install**.
5. Launch **Plants vs. Zombies RH** and play in English. 🌻

## Troubleshooting
- **"App not installed" / parse error:** if you're switching from the Chinese APK or a
  non-repo build, uninstall it first (back up your save — see [MIGRATION.md](MIGRATION.md)).
  Also check your device is 64-bit (arm64-v8a). When *updating* an English build from this
  repo, don't uninstall — install over the top ([UPDATE.md](UPDATE.md)).
- **Black screen or very long plant cooldowns:** set your phone's language/region to
  English (US) or Chinese, or reboot and retry (this is a quirk of the base game).
- **Some text is still Chinese:** expected in a few rare spots (see the README's
  "Known limitations"). It doesn't affect gameplay.
- **Play Protect warning:** because it's a fan-signed APK, Google Play Protect may
  warn you. You can choose to install anyway (you downloaded it from this repo's
  Releases). This APK is not malware, but as with any sideloaded app, only install it
  from the official Releases page here.

## Save data
Progress is stored in the app's own data (`playerData.json`). **Updating** an English build
from this repo keeps it automatically (install over the top — see [UPDATE.md](UPDATE.md)).
Only **uninstalling** deletes it, so back up before you uninstall (there is no cloud sync —
see [MIGRATION.md](MIGRATION.md)).
