# Plants vs. Zombies: Fusion 3.8.1 — English (Android)

An **unofficial English build for Android** of *Plants vs. Zombies: Fusion*
(植物大战僵尸融合版) v3.8.1, made by statically applying the community English
translation to the game's Android APK so it runs in English on a phone — **no
root, no mod loader, no PC required.**

> ⚠️ **Fan-made & non-commercial.** This is a fan project. It is **not** affiliated
> with, endorsed by, or connected to the original game's developer, the translation
> team, EA, or PopCap. All game content and the English translation belong to their
> respective creators — see **[Credits & Sources](#-credits--sources)**. Please
> support the original creators and get the translation from their official channels.

---

## 📥 Download & Install

1. Go to the **[Releases](../../releases)** page and download the latest
   `PvZ-Fusion-3.8.1-English.apk`.
2. On your Android phone, allow **"Install unknown apps"** for your browser/file
   manager (Settings → Apps → your browser → Install unknown apps).
3. **If you already have any version of this game installed, uninstall it first**
   (the modified APK is signed with a different key and some changes only apply on
   a clean install).
4. Open the downloaded APK and tap **Install**.

Requirements: **Android 8+**, **arm64-v8a** device (most phones from ~2018 on).
Full steps: **[docs/INSTALL.md](docs/INSTALL.md)**.

---

## ✨ What's translated

- **Almanac** — all plant & zombie names, descriptions, and cost/recharge text
  (including 9 plants the PC translation had left in Chinese).
- **Mechanics & Modifiers almanac** — mechanic pages and all Odyssey buff / debuff /
  modifier ("词条") names and descriptions.
- **Menus & UI** — main menu, mode names, buttons, settings, dialogs (menu graphics
  swapped for the English textures from the PC translation).
- **In-game HUD & messages** — "Enemies", "Difficulty", "Adventure Lv.", wave/level
  banners, notifications, etc.
- **Odyssey / travel content** — route names, level tips, status messages
  (~1,300 extra strings translated for this build, since the PC mod didn't cover them).

Description font size is reduced so long entries fit on a phone screen.

### Known limitations
- A tiny amount of Chinese may remain (one rare zombie, a small "hotkey" label,
  some dynamically-composed number strings, and any artwork the translation team
  didn't provide an English version of).
- The in-game font is the game's **original** font. Swapping to a different font
  (e.g. Arial) triggered a character-rendering bug in this game engine, so the
  original font is kept (it renders every character correctly).

---

## 🙏 Credits & Sources

This build stands entirely on the work of others. **Please visit and support them:**

| Role | Who | Link |
|---|---|---|
| **Original game** (*PvZ Fusion* / 植物大战僵尸融合版) | **LanPiaoPiao (蓝飘飘fly)** & team | https://space.bilibili.com/3546619314178489 |
| **English translation** (PC mod, the source of all English text/textures) | **PVZF‑Translation team** | https://github.com/Teyliu/PVZF-Translation · Discord: https://discord.gg/DPAC5ZVJ8T |
| OG translation mod creator | **NaKune** | https://github.com/ArifRios1st/PVZ-Hyper-Fusion-Mod |
| Coding help / font implementation | **Climeron** | https://github.com/Climeron |
| Audio changing implementation | **TrevTV** | https://github.com/TrevTV/MelonLoader-AudioTools |
| Main‑menu music | **Rollerlhite** | https://www.youtube.com/watch?v=aBj1MfvnHPE |
| Game artist | **机鱼吐司 (Gfishtus)** | (see Discord) |
| Multi‑language PC package | **Blooms** | (see Discord) |

The English **strings, textures and fonts** come from the **PVZF‑Translation**
project. Their README explicitly asks that people credit them and download from
their **official GitHub repo** — so: **do not re‑host their PC translation, and if
you want the desktop version or the latest translation, get it from
https://github.com/Teyliu/PVZF-Translation and their Discord.**

Only the **Android packaging + the ~1,300 extra English strings** in
[`translations/`](translations/) are new to this repository.

See **[CREDITS.md](CREDITS.md)** for details.

---

## ⚖️ Legal / disclaimer

- *Plants vs. Zombies* is a trademark of **Electronic Arts / PopCap**. *PvZ Fusion*
  is an unofficial fan game; this English build is an unofficial fan port. This
  project is **not affiliated with EA, PopCap, the fan‑game developer, or the
  translation team.**
- Provided **free of charge, non‑commercial, "as is", with no warranty.** Do not
  sell it or put it behind ads/paywalls.
- If any original author asks for this to be taken down, it will be removed.
- You install and use this at your own risk.

---

## 🔒 Security notes

- The APK is signed with an **auto‑generated debug key** (standard for community
  builds). It is **not** signed with the original developer's key. Only download it
  from **this repo's Releases** — a debug‑signed APK can be re‑signed by anyone, so
  don't trust copies from random sites.
- This repository contains **no keystores, keys, or personal data** — only build
  scripts and translation JSON.
- The original Chinese APK and the PC translation files are **not** included here
  (they belong to their creators — get them from the links above).

---

## 🛠️ How it was built (reproduce)

The APK is produced by statically patching the original Chinese APK with the English
content — no runtime mod loader. Pipeline:

1. Extract `data.unity3d` (Unity IL2CPP asset bundle) and `global-metadata.dat`.
2. **Translate assets** (`tools/patch_bundle_v2.py`, uses [UnityPy](https://github.com/K0lb3/UnityPy)):
   replace almanac TextAssets, splice UI strings into MonoBehaviours, swap English
   menu textures.
3. **Translate code strings** (`tools/patch_metadata_v2.py`): rebuild the IL2CPP
   metadata string‑literal table so English of any length fits.
4. **Repack** (`tools/repack.py`) keeping 4‑byte alignment, then **sign**
   (v1+v2+v3) with [uber-apk-signer](https://github.com/patrickfav/uber-apk-signer).

Reproducing requires: Python 3 + UnityPy, Java 8+, the **original Chinese APK**, and
the **PC translation folder** (`PvZ_Fusion_Translator`) — both from the sources
above. See **[tools/README.md](tools/README.md)**.

---

*Made for the community. Big thanks to everyone credited above. 🌻*
