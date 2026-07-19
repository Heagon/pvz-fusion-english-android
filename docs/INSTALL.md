# Install guide (Android)

## Requirements
- Android **8.0+** phone/tablet.
- **arm64-v8a** CPU (basically any phone from ~2018 onward).
- ~1.2 GB free space (the APK is ~555 MB; it needs room to install).

## Steps
1. **Download** `PvZ-Fusion-3.8.1-English.apk` from the
   [Releases](../../releases) page onto your phone.
2. **Uninstall any existing copy** of the game first.
   > Important: this build is signed with a different key than other copies, so it
   > can't install "over" them; and some text (the code-level strings) only shows in
   > English after a clean install.
3. **Allow install from unknown sources** for the app you'll open the APK with:
   - Settings → Apps → (your browser / Files app) → **Install unknown apps** → Allow.
4. Open the APK (from the browser's downloads, or a file manager) → **Install**.
5. Launch **Plants vs. Zombies RH** and play in English. 🌻

## Troubleshooting
- **"App not installed" / parse error:** make sure you fully uninstalled the old
  version, and that your device is 64-bit (arm64-v8a).
- **Black screen or very long plant cooldowns:** set your phone's language/region to
  English (US) or Chinese, or reboot and retry (this is a quirk of the base game).
- **Some text is still Chinese:** expected in a few rare spots (see the README's
  "Known limitations"). It doesn't affect gameplay.
- **Play Protect warning:** because it's a fan-signed APK, Google Play Protect may
  warn you. You can choose to install anyway (you downloaded it from this repo's
  Releases). This APK is not malware, but as with any sideloaded app, only install it
  from the official Releases page here.

## Save data
Progress is stored in the app's own data. Uninstalling deletes it, so back up if you
care about your save (there is no cloud sync).
