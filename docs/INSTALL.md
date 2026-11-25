# 📖 Hướng Dẫn Cài Đặt · Installation Guide · 安装指南 (Android)

<p align="center">
  <a href="../README.vi.md"><b>← [VI] Trang Chủ Tiếng Việt</b></a> &nbsp;•&nbsp;
  <a href="../README.md"><b>← [EN] English Home</b></a> &nbsp;•&nbsp;
  <a href="../README.cn.md"><b>← [CN] 返回中文主页</b></a>
</p>

<p align="center">
  <a href="UPDATE.md">🔄 Cập Nhật &amp; Đổi Ngôn Ngữ (UPDATE)</a> &nbsp;•&nbsp;
  <a href="MIGRATION.md">💾 Sao Lưu &amp; Chuyển Save (MIGRATION)</a> &nbsp;•&nbsp;
  <a href="../CREDITS.md">👥 Đội Ngũ (CREDITS)</a>
</p>

<p align="center">
  <a href="#vi-bản-việt-hóa"><b>[VI] Bản Việt Hóa</b></a> &nbsp;|&nbsp;
  <a href="#en-english"><b>[EN] English</b></a> &nbsp;|&nbsp;
  <a href="#cn-简体中文"><b>[CN] 简体中文</b></a>
</p>

---

<a id="vi-bản-việt-hóa"></a>
## [VI] Bản Việt Hóa

### 1. Cấu hình thiết bị yêu cầu
- Điện thoại hoặc máy tính bảng chạy **Android 8.0** trở lên.
- Vi xử lý 64-bit kiến trúc **`arm64-v8a`** (hầu hết điện thoại từ năm 2018 trở lại đây đều hỗ trợ).
- Bộ nhớ trống tối thiểu: khoảng **1.5 GB** (tệp APK nặng ~600–630 MB, cần thêm dung lượng trống để hệ thống giải nén khi cài đặt).

### 2. Các bước cài đặt chuẩn
1. **Tải tệp APK:** Chọn phiên bản mong muốn (**`[VI] Bản Việt Hóa`**, **`[EN] English`**, hoặc **`[CN] Trung Gốc`**) từ [Trang Chủ Tiếng Việt](../README.vi.md#downloads) hoặc mục [Releases](https://github.com/Heagon/pvz-fusion-english-android/releases).
2. **Kiểm tra tình trạng máy hiện tại:**
   - **Đang dùng bản tải từ kho này:** Bấm **Cài đặt đè / Cập nhật (Update)** trực tiếp (**tuyệt đối không gỡ bản cũ**) để giữ nguyên 100% dữ liệu chơi.
   - **Lần đầu chuyển từ APK nguồn khác sang:** Nếu Android báo *"Ứng dụng chưa được cài đặt"* do xung đột chữ ký số, hãy sao lưu tệp `playerData.json` trước khi gỡ bản cũ theo hướng dẫn tại **[MIGRATION.md](MIGRATION.md#vi-bản-việt-hóa)**.
3. **Cấp quyền cài đặt tệp APK (nếu cài lần đầu):**
   - Vào **Cài đặt → Ứng dụng → Trình duyệt / Quản lý tệp** → Bật **Cho phép cài đặt ứng dụng không rõ nguồn gốc**.
4. **Mở tệp APK vừa tải và bấm Cài đặt (Install).**
5. Mở game và tận hưởng!

### 3. Xử lý sự cố thường gặp
> [!TIP]
> **Lỗi màn hình đen hoặc thời gian hồi chiêu cây lâu bất thường:** Đây là lỗi cố hữu của engine game gốc khi hệ thống điện thoại dùng định dạng số thập phân dấu phẩy (`,`). Cách khắc phục: chuyển tạm ngôn ngữ/khu vực máy sang **English (United States)** hoặc **Chinese**, hoặc khởi động lại thiết bị rồi vào lại game.

> [!NOTE]
> **Cảnh báo Google Play Protect:** Vì các bản APK cộng đồng được ký bằng chứng chỉ riêng ngoài Play Store, Play Protect có thể hiện hộp thoại nhắc nhở. Bấm **Chi tiết khác (More details) → Vẫn cài đặt (Install anyway)** — tệp cài đặt hoàn toàn sạch, không quảng cáo, mã nguồn đóng gói công khai tại [`tools/`](../tools/README.md).

---

<a id="en-english"></a>
## [EN] English

### 1. System Requirements
- Android phone or tablet running **Android 8.0+**.
- **`arm64-v8a`** 64-bit CPU architecture.
- Free storage: at least **1.5 GB** available space (~600–630 MB APK + extraction headroom).

### 2. Step-by-Step Installation
1. **Download APK:** Grab your preferred edition (**`[EN] English`**, **`[VI] Bản Việt Hóa`**, or **`[CN] Chinese Raw`**) from the [Main README](../README.md#downloads) or [Releases](https://github.com/Heagon/pvz-fusion-english-android/releases) page.
2. **Install Safely:**
   - **Updating or switching language within this suite:** Tap **Update / Install** directly over your existing app (**do NOT uninstall**). All progress is automatically preserved.
   - **First time switching from an external APK:** If Android blocks installation due to a signature conflict, back up `playerData.json` before uninstalling the old package — see **[MIGRATION.md](MIGRATION.md#en-english)**.
3. **Allow Unknown Apps (first-time sideloading):**
   - **Settings → Apps → (Your Browser / File Manager)** → Enable **Install unknown apps**.
4. **Open the APK and tap Install.**
5. Launch and enjoy!

### 3. Troubleshooting
> [!TIP]
> **Black screen on launch or abnormal plant cooldowns:** A known upstream game bug triggered by locales that format decimals with commas (`,`). Temporarily set your device language/region to **English (US)** or **Chinese**, or reboot your device.

> [!NOTE]
> **Google Play Protect prompt:** Standard Android prompt for community-signed APKs distributed outside Google Play. Tap **More details → Install anyway**. All build scripts are open-source in [`tools/`](../tools/README.md).

---

<a id="cn-简体中文"></a>
## [CN] 简体中文

### 1. 系统配置要求
- 运行 **Android 8.0** 及以上系统的手机或平板电脑。
- **`arm64-v8a`** 64 位处理器架构（2018 年后的主流安卓设备均支持）。
- 存储空间：建议预留至少 **1.5 GB** 可用空间（APK 约 600–630 MB，系统安装需额外解压空间）。

### 2. 安装步骤
1. **下载安装包：** 前往 [中文主页](../README.cn.md#downloads) 或 [Releases](https://github.com/Heagon/pvz-fusion-english-android/releases) 下载所需版本（**`[CN] 中文原版`**、**`[VI] 越化版`** 或 **`[EN] 英文版`**）。
2. **安全安装方式：**
   - **本仓库版本升级或切换语言：** 直接点击 **更新 / 安装** 覆盖安装（**切勿卸载旧版**），所有存档自动无损继承。
   - **首次从其他第三方签名安装包迁移：** 若提示签名不一致冲突，请先参照 **[MIGRATION.md](MIGRATION.md#cn-简体中文)** 备份 `playerData.json`，再卸载旧版并安装本包。
3. **开启未知来源安装权限：**
   - 手机 **设置 → 应用管理 → 对应浏览器或文件管理器** → 开启 **允许安装未知应用**。
4. **打开下载好的 APK 并点击安装。**
5. 启动游戏即可畅玩！

### 3. 常见问题排查
> [!TIP]
> **启动黑屏或植物冷却时间异常漫长：** 此为原版引擎在部分欧洲/越南等使用逗号（`,`）作为小数点的系统区域下的固有兼容性问题。将手机系统语言/区域切换为**中文**或**英文（美国）**，或重启手机后即可恢复正常。

> [!NOTE]
> **Play Protect / 手机安全管家提示：** 由于属于非应用商店分发的社区自签名 APK，系统可能弹出未知来源提醒，选择 **“了解详情 → 仍要安装 / 继续安装”** 即可。构建工具链完全开源于 [`tools/`](../tools/README.md)。
