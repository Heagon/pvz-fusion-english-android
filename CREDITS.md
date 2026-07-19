# Credits & Sources

This English Android build would not exist without the following people and projects.
Everything except the Android packaging and the extra strings in [`translations/`](translations/)
is their work. Please support them directly.

## Original game
- **Plants vs. Zombies: Fusion** (植物大战僵尸融合版) — a fan game by
  **LanPiaoPiao (蓝飘飘fly)** and team.
  - Developer: https://space.bilibili.com/3546619314178489
- Game artist: **机鱼吐司 (Gfishtus)**.

## English translation (the source of all English text, textures & fonts)
- **PVZF-Translation** — the community English translation project.
  - **Official GitHub: https://github.com/Teyliu/PVZF-Translation**
  - Discord: https://discord.gg/DPAC5ZVJ8T
  - Their notice: *the translation is fan-made (Google Translate + AI + community
    input) and unofficial; get it only from their official GitHub, and credit them.*
- Contributors named in the translation's README:
  - **NaKune** — OG translation mod creator — https://github.com/ArifRios1st/PVZ-Hyper-Fusion-Mod
  - **Climeron** — coding help / font-changing implementation — https://github.com/Climeron
  - **TrevTV** — audio-changing implementation — https://github.com/TrevTV/MelonLoader-AudioTools
  - **Rollerlhite** — new main-menu music — https://www.youtube.com/watch?v=aBj1MfvnHPE
- **Blooms** — packaged the multi-language PC beta this build was made from.

## Tools used
- [UnityPy](https://github.com/K0lb3/UnityPy) — read/write Unity asset bundles.
- [uber-apk-signer](https://github.com/patrickfav/uber-apk-signer) — zipalign + APK signing.
- [Android platform-tools](https://developer.android.com/tools/releases/platform-tools) — adb.

## What is original to this repository
- The Android static-patching pipeline (`tools/`).
- ~1,300 extra English strings + the 9 missing plants + Mechanics-page titles
  (`translations/`), translated for this build because the PC mod didn't cover them.

If you are one of the authors above and want changes or a takedown, please open an
issue — it will be honored.
