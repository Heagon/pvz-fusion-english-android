# Cập Nhật Không Mất Save / Updating Without Losing Save / 无损更新与存档保留指南

<p align="center">
  <a href="#vi-bản-việt-hóa"><b>[VI] Bản Việt Hóa</b></a> •
  <a href="#en-english"><b>[EN] English</b></a> •
  <a href="#zh-简体中文"><b>[ZH] 简体中文</b></a>
</p>

---

## [VI] Bản Việt Hóa

**Quy tắc vàng:** Luôn luôn **cài đặt đè (Install / Update), tuyệt đối không gỡ cài đặt**.

File save của bạn nằm tại đường dẫn:
```
/sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
Thao tác gỡ cài đặt (Uninstall) là nguyên nhân duy nhất làm hệ điều hành Android xóa thư mục dữ liệu trên.

### Cơ chế hoạt động trong bộ cài đặt này
- Tất cả các bản APK (**[VI] Bản Việt Hóa**, **[EN] English**, **[ZH] Trung gốc**) trong kho đều được ký cùng một **Release Keystore duy nhất**.
- Mỗi lần có bản dịch mới hoặc cập nhật tài nguyên, hệ thống tự động sinh mã định danh nội bộ mới (`unity_app_guid`). Khi bạn cài đè, game sẽ tự động giải nén dữ liệu ngôn ngữ mới mà không cần xóa ứng dụng.
- **Để đổi ngôn ngữ:** Bạn chỉ cần tải file APK của ngôn ngữ muốn đổi (ví dụ đang ở [EN] English muốn qua [VI] Bản Việt Hóa) và bấm **Cài đặt cập nhật đè**. Save game được bảo toàn 100%!

---

## [EN] English

**The Golden Rule:** Always **install over the top (in-place update); NEVER uninstall**.

Your save game file is located at:
```
/sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
Uninstalling the app is the *only* action that causes Android to wipe this data directory.

### How It Works in This Suite
- All APK builds (**[VI] Bản Việt Hóa**, **[EN] English**, and **[ZH] Chinese Raw**) in this repository share the exact same official **Release Keystore**.
- Whenever a translation is updated, the internal `unity_app_guid` is dynamically updated. Android detects the update and cleanly extracts new localization assets on first launch.
- **To switch language:** Simply download your desired language APK (e.g. switching from [EN] English to [VI] Bản Việt Hóa) and tap **Update / Install** over the top. All coins, unlocked plants, and stage progress remain 100% intact!

---

## [ZH] 简体中文

**核心原则：** 始终直接**覆盖安装更新，切勿卸载游戏**。

您的游戏本地存档路径为：
```
/sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
在安卓系统中，**只有点击“卸载”操作才会导致系统清空该目录下的存档**。

### 本项目的技术保障机制
- 本仓库发布的所有 APK（**[VI] 越化版**、**[EN] English 英文版**、**[ZH] 中文原版**）均采用相同的**官方签名证书 (Release Keystore)**。
- 每次版本更新与资源注入均会动态更新内部版本标识（`unity_app_guid`），游戏启动时会自动重新加载最新本地化文本，无需清理缓存或重置应用。
- **无损切换语言：** 当你想从 [EN] 英文版切换到 [VI] 越化版或 [ZH] 中文原版时，只需下载对应 APK 直接点击“更新”，关卡进度、植物图鉴与金币数据 100% 完整继承！
