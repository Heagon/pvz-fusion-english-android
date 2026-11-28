# 📋 Build History & Release Changelog · Lịch Sử Bản Build (`B.x.y`)

<p align="center">
  <a href="README.vi.md"><b>← [VI] Trang Chủ Tiếng Việt</b></a> &nbsp;•&nbsp;
  <a href="README.md"><b>← [EN] English Home</b></a> &nbsp;•&nbsp;
  <a href="README.cn.md"><b>← [CN] 返回中文主页</b></a> &nbsp;•&nbsp;
  <a href="CREDITS.md"><b>👥 Credits &amp; Sources</b></a> &nbsp;•&nbsp;
  <a href="https://github.com/Heagon/pvz-fusion-english-android/releases"><b>📦 All GitHub Releases</b></a>
</p>

---

## 🏷️ Build Naming & Immutable Release Policy · Quy Tắc Đánh Số Bản Build

Every Android APK published in this repository carries an explicit, immutable build identifier (`B.<major>.<minor>`) so players can immediately distinguish newer builds from older ones, inspect exact fixes, and roll back cleanly if a regression is ever found:

- **APK Filename Format:** `<GameName>-<GameVersion>-<Language/Variant>-B.<major>.<minor>.apk`
  - Example: `PvZ-Fusion-4.1-Vietnamese-HalfTranslate-B.0.1.apk`
- **GitHub Release Tag Format:** `<base-tag>-B.<major>.<minor>` (e.g., `v4.1-half-translate-B.0.1`, `v4.0.5.2-B.0.1`, `v3.9-B.0.1`, `v3.8.1-B.0.1`)
- **Versioning Rules:**
  - **`B.0.1`** — Initial baseline build for a given upstream game version.
  - **`B.0.2`, `B.0.3`, ...** — Bug fixes, crash hotfixes, translation updates, or UI/texture refinements for the same game version.
  - **`B.1.0`, ...** — Major overhaul/milestone for the same game version.
  - Resets to **`B.0.1`** when the upstream *PvZ: Fusion* version updates (e.g., `4.1` → `4.2`).
- **Immutable Releases (No Overwriting) & Save-Safe Rollback:** Every build receives its **own dedicated GitHub Release** — existing releases are **never overwritten** (`--clobber` prohibited). All releases share the same official Release Keystore and dynamic `unity_app_guid`, so upgrading (`B.0.1 → B.0.2`), switching languages (`[VI] ↔ [EN] ↔ [CN]`), or rolling back (`B.0.2 → B.0.1`) via in-place **Update (never uninstall)** preserves 100% of your `playerData.json` save data.

---

## 📦 Complete Build Timeline (Newest First)

| Release Tag | Build | Date (UTC) | Channel | APK Files, Sizes &amp; SHA-256 | Summary of Changes / Fixes |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **[`v4.1-half-translate-B.0.1`](https://github.com/Heagon/pvz-fusion-english-android/releases/tag/v4.1-half-translate-B.0.1)** | **`B.0.1`** | `2026-11-27` | 🟡 **Preview** | • [`PvZ-Fusion-4.1-Vietnamese-HalfTranslate-B.0.1.apk`](https://github.com/Heagon/pvz-fusion-english-android/releases/download/v4.1-half-translate-B.0.1/PvZ-Fusion-4.1-Vietnamese-HalfTranslate-B.0.1.apk) (`628,964,262` B)<br>&nbsp;&nbsp;`sha256:81606687f29b864e7a01de6510ae036c3aed30a3871cc3c27bb81c10ee23a2cb`<br>• [`PvZ-Fusion-4.1-English-HalfTranslate-B.0.1.apk`](https://github.com/Heagon/pvz-fusion-english-android/releases/download/v4.1-half-translate-B.0.1/PvZ-Fusion-4.1-English-HalfTranslate-B.0.1.apk) (`628,804,521` B)<br>&nbsp;&nbsp;`sha256:04b8de0ba0a45eca878f6eea6a4c7c2d6d92aeae58d737a2916ed95a72b359f9`<br>• [`PvZ-Fusion-4.1-Chinese-Raw-B.0.1.apk`](https://github.com/Heagon/pvz-fusion-english-android/releases/download/v4.1-half-translate-B.0.1/PvZ-Fusion-4.1-Chinese-Raw-B.0.1.apk) (`620,178,332` B)<br>&nbsp;&nbsp;`sha256:3144746c552455b88db28eedfa20777099ecdb9736ac679bbbe70cd4113cb5fd` | 100% Vietnamese v4.1 localization (+3,837 strings, 742 plants / 238 zombies / 48 mechanics, 176 Travel Buffs, 48/48 VI textures, AutoChess/Tycoon/Magic Brush/Shooting); +994 EN v4.1 UI strings; **fixed Android 13 / Nubia `TalentNode` NUL-key startup crash (`SIGTRAP`)** and hardened binary splicer. ([Release Notes](RELEASE_NOTES-4.1-HalfTranslate.md)) |
| **[`v4.0.5.2-B.0.1`](https://github.com/Heagon/pvz-fusion-english-android/releases/tag/v4.0.5.2-B.0.1)** | **`B.0.1`** | `2026-11-21` | 🟢 **Latest Stable** | • [`PvZ-Fusion-4.0.5.2-Vietnamese-B.0.1.apk`](https://github.com/Heagon/pvz-fusion-english-android/releases/download/v4.0.5.2-B.0.1/PvZ-Fusion-4.0.5.2-Vietnamese-B.0.1.apk) (`599,616,431` B)<br>&nbsp;&nbsp;`sha256:78f23a7265cbdffcab5d888958efb995c42f4a91f18e86f91bea1f543204260b`<br>• [`PvZ-Fusion-4.0.5.2-English-B.0.1.apk`](https://github.com/Heagon/pvz-fusion-english-android/releases/download/v4.0.5.2-B.0.1/PvZ-Fusion-4.0.5.2-English-B.0.1.apk) (`599,718,829` B)<br>&nbsp;&nbsp;`sha256:f923f9abada8bdccab606f63fb3f78a9854cf0bb86fa06d68c3863629bc5a8c5`<br>• [`PvZ-Fusion-4.0.5.2-Chinese-Raw-B.0.1.apk`](https://github.com/Heagon/pvz-fusion-english-android/releases/download/v4.0.5.2-B.0.1/PvZ-Fusion-4.0.5.2-Chinese-Raw-B.0.1.apk) (`591,096,732` B)<br>&nbsp;&nbsp;`sha256:51a084faf0eac1a8d633f7e4f0749441655a3d909df8befb71cc70d82fe0739a` | Complete tri-lingual v4.0.5.2 suite (`[VI]` / `[EN]` / `[CN]` Raw), 720 plants / 235 zombies / 47 mechanics, 48 localized UI textures per language, `LiberationSans` accented Vietnamese font, unified save-preserving Release Keystore &amp; `unity_app_guid`. ([Release Notes](RELEASE_NOTES-4.0.5.2.md)) |
| **[`v3.9-B.0.1`](https://github.com/Heagon/pvz-fusion-english-android/releases/tag/v3.9-B.0.1)** | **`B.0.1`** | `2026-08-31` | Archived | • [`PvZ-Fusion-3.9-English-B.0.1.apk`](https://github.com/Heagon/pvz-fusion-english-android/releases/download/v3.9-B.0.1/PvZ-Fusion-3.9-English-B.0.1.apk) (`575,933,352` B)<br>&nbsp;&nbsp;`sha256:8d26c9fc0cc8b449408b903d1c68d0abf90ad71f06a548097e3cd21ce5d66bed` | Rebased English Android APK on *PvZ: Fusion 3.9* with full Almanac, Mechanics, Modifiers, Odyssey buffs, English menu textures, and save-preserving Release Keystore. |
| **[`v3.8.1-B.0.1`](https://github.com/Heagon/pvz-fusion-english-android/releases/tag/v3.8.1-B.0.1)** | **`B.0.1`** | `2026-07-19` | Archived | • [`PvZ-Fusion-3.8.1-English-B.0.1.apk`](https://github.com/Heagon/pvz-fusion-english-android/releases/download/v3.8.1-B.0.1/PvZ-Fusion-3.8.1-English-B.0.1.apk) (`555,059,804` B)<br>&nbsp;&nbsp;`sha256:9a27c575590aec1d47c79f36b0aaf4bf3618e28d41ab0d2f726d7fb88c70b8c4` | Initial English Android APK for *PvZ: Fusion 3.8.1* introducing the unified save-preserving Release Keystore and localized English update changelog popup. |

---

## 👥 Credits, Official Sources &amp; Copyright Attribution

- **Complete Credits &amp; Official Sources Page:** **[`CREDITS.md`](https://github.com/Heagon/pvz-fusion-english-android/blob/main/CREDITS.md)** ([`[VI] Tiếng Việt`](https://github.com/Heagon/pvz-fusion-english-android/blob/main/CREDITS.md#vi-bản-việt-hóa) · [`[EN] English`](https://github.com/Heagon/pvz-fusion-english-android/blob/main/CREDITS.md#en-english) · [`[CN] 简体中文`](https://github.com/Heagon/pvz-fusion-english-android/blob/main/CREDITS.md#cn-简体中文))
- **Original Game (*Plants vs. Zombies: Fusion* / 植物大战僵尸融合版):** **LanPiaoPiaofly (蓝飘飘fly)** ([Official Bilibili](https://space.bilibili.com/3546619314178489)), **Gfishtus (机鱼吐司)**, **LanDie (蓝蝶)**, **MengLuo (梦珞)** &amp; original team.
- **Multi-Language Mod &amp; English Localization (*PVZF-Translation*):** **[PVZF-Translation](https://github.com/Teyliu/PVZF-Translation)** · **[Translator Mod Source](https://github.com/Teyliu/PVZFusionTranslation)** · **[Discord](https://discord.gg/DPAC5ZVJ8T)** · **[Online Almanac](https://carroti4ch.itch.io/almanac)** (`Mamoru-kun`, `NaKune`, `Climeron`, `Teyliu`, `Cassidy`, `JustNull`, `Dakosha`, `TrevTV`, `Rollerlhite`, `Roaoming`, `Shel`, `flexyj`, `CarrotD1scord`, `Xabdi`, `The Blooms Community` — licensed under **[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)**).
- **Vietnamese Localization (`Bản Việt Hóa`):** **Team CBD &amp; Team Bloom** · `Shion`, `Cryda`, `JustNull` · v4.0.5.2 &amp; v4.1 Android completion by **Heagon**.
- **Android Static Porting &amp; Open-Source Tools:** **Heagon** ([pvz-fusion-english-android](https://github.com/Heagon/pvz-fusion-english-android)); prior community Android ports by **silvershadow** ([pvzf-android-translation](https://github.com/silvershadowkat/pvzf-android-translation)) &amp; **Joseph Franci**; tools: [UnityPy](https://github.com/K0lb3/UnityPy), [fontTools](https://github.com/fonttools/fonttools), [Pillow](https://python-pillow.org/), [Liberation Fonts](https://github.com/liberationfonts/liberation-fonts), [uber-apk-signer](https://github.com/patrickfav/uber-apk-signer).
- **Trademark &amp; Non-Commercial Notice:** *Plants vs. Zombies* is a registered trademark of **Electronic Arts Inc. (EA) / PopCap Games** ([ea.com](https://www.ea.com/games/plants-vs-zombies)). This project is **100% free, ad-free, and non-commercial**; all original rights belong to their respective owners.
