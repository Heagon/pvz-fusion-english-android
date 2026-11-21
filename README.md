# Plants vs. Zombies: Fusion (Android) — English & Tiếng Việt

An **unofficial Android localization project** for *Plants vs. Zombies: Fusion* (植物大战僵尸融合版), made by statically applying community translations to the original Android APK — **no root, no PC, no runtime mod loader required.**

Currently offering both **English** and **Vietnamese (Tiếng Việt)** builds for:
- **v4.0.5.2 (Stable Release)**
- **v4.1 Preview (Half-Translated / Đang dịch dở)**

> ⚠️ **Fan-made & non-commercial.** This is a fan project. It is **not** affiliated with, endorsed by, or connected to the original game's developer, the translation teams, EA, or PopCap. All game content and translations belong to their respective creators — see **[Credits & Sources](#-credits--sources)**.

---

## 📥 Releases & Downloads

All builds are signed with the project's official release keystore and verified with Android Signature Scheme v1, v2, and v3. Save files are preserved across updates (`unity_app_guid` dynamic bump).

### 🌟 v4.0.5.2 (Latest Stable)
👉 **[View Release v4.0.5.2](../../releases/tag/v4.0.5.2)** | **[Bản riêng Tiếng Việt v4.0.5.2-vi](../../releases/tag/v4.0.5.2-vi)**

| Language | APK File | Size | SHA-256 Checksum |
| :--- | :--- | :--- | :--- |
| 🇬🇧 **English** | [`PvZ-Fusion-4.0.5.2-English.apk`](../../releases/download/v4.0.5.2/PvZ-Fusion-4.0.5.2-English.apk) | 599.5 MB | `aba29a346a6ecca587ce748b18568a12cfdbc4c990246d4ff35f7a4add4fb99c` |
| 🇻🇳 **Tiếng Việt** | [`PvZ-Fusion-4.0.5.2-Vietnamese.apk`](../../releases/download/v4.0.5.2/PvZ-Fusion-4.0.5.2-Vietnamese.apk) | 597.5 MB | `57d17659fff4147bd2f88458fe98f8c1f8065ed60a073fdc1fbd7fcba55039d5` |

---

### ⚡ v4.1 Preview (Half-Translated / Đang dịch dở)
👉 **[View Release v4.1-half-translate](../../releases/tag/v4.1-half-translate)** | **[Bản riêng Tiếng Việt v4.1-vi-half-translate](../../releases/tag/v4.1-vi-half-translate)**

> [!WARNING]
> **Half-Translate / Đang dịch dở:** Bản thử nghiệm sớm cho PvZ Fusion 4.1. Các nội dung mới (AutoChess Thám hiểm Tiến Hóa, thực vật Tối Thượng mới, bùa chú) đang được dịch tiếp tục từ tiếng Trung; các chuỗi chưa hoàn thiện sẽ tạm hiển thị tiếng Anh/bản dịch nháp để đảm bảo game không bị lỗi.

| Language | APK File | Size | SHA-256 Checksum |
| :--- | :--- | :--- | :--- |
| 🇬🇧 **English** | [`PvZ-Fusion-4.1-English-HalfTranslate.apk`](../../releases/download/v4.1-half-translate/PvZ-Fusion-4.1-English-HalfTranslate.apk) | 628.6 MB | `f9fd984f1647a442756a5021cdcddaa2bcf8fe9db8785a0ce9581e6768a865b2` |
| 🇻🇳 **Tiếng Việt** | [`PvZ-Fusion-4.1-Vietnamese-HalfTranslate.apk`](../../releases/download/v4.1-half-translate/PvZ-Fusion-4.1-Vietnamese-HalfTranslate.apk) | 626.7 MB | `83fad03cf196195727c6eaf540f299be9f2133cc41e778016c99dd420d0b6dd6` |

---

## 🇻🇳 Thông tin bản Tiếng Việt (Vietnamese Details)

- **Hỗ trợ 100% tiếng Việt có dấu:** Hệ thống tự động cấu hình font dự phòng `LiberationSans` trong asset bundle `data.unity3d`, giúp toàn bộ các ký tự có dấu (`ừ, ỡ, ệ, ằ, ú, ắ, â, ĩ, ô, ễ...`) hiển thị sắc nét, không bị lỗi mất ký tự hay ô vuông `[]`.
- **Việt hóa Sách Bách Khoa (Almanac):**
  - Đầy đủ 720/720 thực vật (bản 4.0.5.2) và 742/742 thực vật (bản 4.1).
  - Đầy đủ 235/235 zombie (bản 4.0.5.2) và 238/238 zombie (bản 4.1).
  - Đầy đủ 47/47 cơ chế (bản 4.0.5.2) và 48/48 cơ chế (bản 4.1, bao gồm Đinh ba Biển sâu).
- **Việt hóa Giao diện:** Toàn bộ menu, nút bấm, bảng kết thúc màn chơi, bảng chọn độ khó, HUD, thông báo trong trận và hệ thống bùa Thám hiểm (Travel Buffs).
- **Đồ họa:** Thay thế 38+ kết cấu hình ảnh menu sang tiếng Việt.
- **Giữ file lưu (Keep Save Data):** Cập nhật `unity_app_guid` tự động, cho phép cài đè trực tiếp mà không mất file lưu trữ tiến trình game (`playerData.json`).

---

## 📸 Screenshots

| Main menu | Almanac |
|---|---|
| ![Main menu](docs/screenshots/main-menu.png) | ![Almanac](docs/screenshots/almanac.png) |
| **Mechanics** | **Modifiers** |
| ![Mechanics](docs/screenshots/mechanics.png) | ![Modifiers](docs/screenshots/modifiers.png) |

---

## 📱 Installation Guide

1. Download the desired APK from the **[Releases](../../releases)** table above.
2. On Android, allow **"Install unknown apps"** for your browser / file manager if prompted.
3. Tap the APK file and select **Install / Update**.
4. **Upgrading from previous versions:**
   - If upgrading from an earlier release signed with our key, simply install over the top (`install -r`). Your save file is automatically preserved!
   - If switching from a different author's APK (different signature key), backup your `playerData.json` save file first (see **[docs/MIGRATION.md](docs/MIGRATION.md)**).

Requirements: **Android 8.0+**, **arm64-v8a** processor.

---

## 🙏 Credits & Sources

This project exists thanks to the dedicated work of the community:

| Role | Contributor | Links |
|---|---|---|
| **Original Game Creator** (*PvZ Fusion* / 植物大战僵尸融合版) | **LanPiaoPiao (蓝飘飘fly)** | [Bilibili](https://space.bilibili.com/3546619314178489) |
| **English Translation** | **PVZF‑Translation Team** | [GitHub](https://github.com/Teyliu/PVZF-Translation) · [Discord](https://discord.gg/DPAC5ZVJ8T) |
| **Vietnamese Translation (Bản Việt Hóa)** | **Team CBD & Team Bloom** | [PVZF-Translation / Vietnamese](https://github.com/Teyliu/PVZF-Translation) |
| **Android Porting & Automation** | **Heagon** | [GitHub Repo](https://github.com/Heagon/pvz-fusion-english-android) |

---

## ⚖️ License & Disclaimer

- *Plants vs. Zombies* is a registered trademark of **Electronic Arts / PopCap Games**.
- This project is an unofficial fan port, non-commercial, and free of charge. No monetisation or ads.
- Distributed "as is" with no warranty.
