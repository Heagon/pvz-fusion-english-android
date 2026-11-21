# Hướng Dẫn Cài Đặt / Installation Guide / 安装指南 (Android)

<p align="center">
  <a href="#-tiếng-việt"><b>🇻🇳 Tiếng Việt</b></a> •
  <a href="#-english"><b>🇬🇧 English</b></a> •
  <a href="#-简体中文"><b>🇨🇳 简体中文</b></a>
</p>

---

## 🇻🇳 Tiếng Việt

### Yêu cầu thiết bị
- Điện thoại hoặc máy tính bảng chạy **Android 8.0** trở lên.
- Vi xử lý kiến trúc **arm64-v8a** (hầu hết điện thoại từ năm 2018 trở lại đây).
- Bộ nhớ trống tối thiểu: khoảng **1.5 GB** (file APK khoảng ~600 MB, cần thêm bộ nhớ để giải nén cài đặt).

### Các bước cài đặt
1. **Tải file:** Tải file APK phiên bản mong muốn (**Bản Việt Hóa**, **English**, hoặc **Trung gốc**) từ mục [Releases](../../releases) về máy.
2. **Cài đặt đè (Giữ nguyên Save):**
   - **Đang chơi bản tải từ kho này:** Bấm cài đè trực tiếp (**không gỡ bản cũ**), toàn bộ tiến trình chơi được giữ nguyên.
   - **Lần đầu chuyển từ bản khác (bản ký khác key):** Nếu hệ thống báo "Ứng dụng chưa được cài đặt" do xung đột chữ ký, hãy sao lưu file save trước khi gỡ bản cũ (xem hướng dẫn [MIGRATION.md](MIGRATION.md)).
3. **Cấp quyền cài ứng dụng:**
   - Vào Cài đặt → Ứng dụng → Chọn Trình duyệt / Quản lý tệp → Bật **Cho phép cài đặt từ nguồn không xác định**.
4. **Mở file APK và bấm Cài đặt (Install).**
5. Mở game và trải nghiệm!

### Xử lý sự cố thường gặp
- **Lỗi màn hình đen hoặc hồi chiêu cây bất thường:** Đây là đặc tính của game gốc khi gặp định dạng khu vực không phù hợp; hãy đổi định dạng vùng/ngôn ngữ máy sang Tiếng Anh hoặc Tiếng Trung hoặc khởi động lại thiết bị.
- **Cảnh báo Google Play Protect:** Do đây là bản APK tùy chỉnh của cộng đồng, Play Protect có thể hiển thị cảnh báo. Bạn có thể chọn "Vẫn cài đặt" (Install anyway). File APK hoàn toàn an toàn và sạch 100%.

---

## 🇬🇧 English

### System Requirements
- Phone or tablet running **Android 8.0+**.
- **arm64-v8a** 64-bit CPU architecture.
- Free storage: at least **1.5 GB** available space.

### Installation Steps
1. **Download:** Grab your preferred APK (**Việt Hóa**, **English**, or **Original Chinese**) from the [Releases](../../releases) page.
2. **Install (Safe Update):**
   - **Updating / switching language within this repo:** Tap **Update / Install** directly over your existing app (**do NOT uninstall**). All game saves are automatically preserved.
   - **First time switching from a third-party APK:** If Android blocks installation due to different signatures, back up your `playerData.json` first, then uninstall and reinstall (see [MIGRATION.md](MIGRATION.md)).
3. **Allow Unknown Sources:**
   - Settings → Apps → (Your Browser / File Manager) → Enable **Install unknown apps**.
4. **Open the APK and tap Install.**
5. Launch and enjoy!

### Troubleshooting
- **Black screen / abnormal plant cooldowns:** This is a base game behavior when encountering non-standard locale formats. Switch system locale/region to English or Chinese, or restart your device.
- **Play Protect warning:** As with any fan-signed community APK, Google Play Protect may show a prompt. You can safely select "Install anyway".

---

## 🇨🇳 简体中文

### 系统要求
- **Android 8.0** 及以上系统的手机或平板电脑。
- **arm64-v8a** 64 位 CPU 架构（2018 年以后的主流安卓设备均支持）。
- 存储空间：预留至少 **1.5 GB** 剩余空间。

### 安装步骤
1. **下载安装包：** 在 [Releases](../../releases) 发布页面下载你需要的语言版本（**Việt Hóa 越化版**、**English 英文版** 或 **中文原版**）。
2. **覆盖安装（安全无损）：**
   - **从本项目先前版本更新或切换语言：** 直接点击**更新 / 安装**覆盖安装（**切勿卸载**），所有关卡进度与金币存档自动无损继承。
   - **首次从非本项目签名的其他第三方安装包迁移：** 若系统提示签名冲突，请先按照 [MIGRATION.md](MIGRATION.md) 备份 `playerData.json` 存档，再卸载旧版并安装本项目 APK。
3. **允许安装未知来源应用：**
   - 手机系统设置 → 应用管理 → 对应浏览器/文件管理器 → 开启**允许安装未知应用**。
4. **点击打开 APK 安装包并完成安装。**
5. 打开游戏，开始畅玩！

### 常见问题与解答
- **黑屏或植物冷却时间异常过长：** 此为原版游戏引擎在特定系统区域设置下的固有问题，可尝试将系统语言/区域临时设为中文或英文，或重启手机后重试。
- **Play Protect / 手机安全管家风险提示：** 因属于粉丝自制签名 APK，系统可能会提示非官方商店来源，选择“仍要安装”即可。安装包纯净无毒，请放心体验。
