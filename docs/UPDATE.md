# 🔄 Cập Nhật &amp; Đổi Ngôn Ngữ Không Mất Save · Safe Updates · 无损更新指南

<p align="center">
  <a href="../README.vi.md"><b>← [VI] Trang Chủ Tiếng Việt</b></a> &nbsp;•&nbsp;
  <a href="../README.md"><b>← [EN] English Home</b></a> &nbsp;•&nbsp;
  <a href="../README.cn.md"><b>← [CN] 返回中文主页</b></a>
</p>

<p align="center">
  <a href="INSTALL.md">📖 Hướng Dẫn Cài Đặt (INSTALL)</a> &nbsp;•&nbsp;
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

> [!IMPORTANT]
> **Quy Tắc Vàng:** Luôn bấm **Cài đặt đè / Cập nhật (Install / Update)** — **TUYỆT ĐỐI KHÔNG bấm Gỡ cài đặt (Uninstall)**.

Tệp lưu tiến trình chơi của bạn nằm tại:
```text
/sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
Trên Android, chỉ có thao tác **Gỡ cài đặt (Uninstall)** mới khiến hệ điều hành xóa sạch thư mục dữ liệu trên.

### Cơ chế bảo toàn Save trong bộ cài đặt này
- **Đồng nhất chữ ký số (Unified Release Keystore):** Cả 3 bản APK (**`[VI] Bản Việt Hóa`**, **`[EN] English`**, **`[CN] Trung Gốc`**) ở mọi phiên bản (`v4.0.5.2`, `v4.1`...) đều được ký bằng cùng một khóa phát hành chính thức.
- **Tự động làm mới bộ nhớ đệm ngôn ngữ (`unity_app_guid`):** Mỗi bản phát hành được tự động gán mã định danh `unity_app_guid` riêng theo mã băm dữ liệu dịch thuật. Khi bạn cài đè, game tự nhận biết bản mới và giải nén lại văn bản ngôn ngữ mới ngay lần mở đầu tiên mà không đụng chạm tới `playerData.json`.
- **Đổi ngôn ngữ bất kỳ lúc nào:** Đang chơi `[EN]` muốn sang `[VI]` (hoặc về `[CN]` gốc)? Chỉ cần tải APK ngôn ngữ muốn đổi và bấm **Cập nhật đè** — xong trong 10 giây, giữ nguyên 100% cây cối và tiền vàng!

---

<a id="en-english"></a>
## [EN] English

> [!IMPORTANT]
> **The Golden Rule:** Always **install over the top (in-place Update)** — **NEVER tap Uninstall**.

Your entire profile and progress live at:
```text
/sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
Uninstalling the app is the *only* action that causes Android to delete this external app-data folder.

### How Lossless Switching Works
- **Unified Release Keystore:** Every build in this repository (**`[EN] English`**, **`[VI] Bản Việt Hóa`**, and **`[CN] Chinese Raw`**) across all versions (`v4.0.5.2`, `v4.1`, and future releases) shares the exact same signing key.
- **Automatic Metadata Cache Refresh (`unity_app_guid`):** Unity IL2CPP caches `global-metadata.dat` inside `files/il2cpp/` keyed by `unity_app_guid`. Our build pipeline updates `unity_app_guid` automatically whenever strings change, forcing a clean metadata re-extraction on first launch while leaving `playerData.json` completely untouched.
- **Instant Language Switching:** Simply download another edition's APK (e.g., `[EN]` → `[VI]` or `[CN]`) and tap **Update / Install** over your existing installation.

---

<a id="cn-简体中文"></a>
## [CN] 简体中文

> [!IMPORTANT]
> **黄金准则：** 升级版本或切换语言时，请始终**直接覆盖安装（点击更新）**——**切勿点击卸载**。

您的全部通关进度与图鉴解锁数据均保存在：
```text
/sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
在安卓系统中，**只有执行“卸载”操作才会导致系统清空上述目录中的存档文件**。

### 无损更新与跨语言切换机制
- **全系共享同一官方签名 (Unified Release Keystore)：** 本仓库的所有安装包（**`[CN] 中文原版`**、**`[VI] 越化版`**、**`[EN] 英文版`**）在所有版本间均采用同一签名证书打包。
- **自动刷新本地化元数据缓存 (`unity_app_guid`)：** 构建管线会根据每次注入的文本动态生成唯一 `unity_app_guid`。覆盖安装后首次启动时，引擎会自动识别并重新释放最新语言的 `global-metadata.dat` 缓存，无需手动清理数据，更不会触碰 `playerData.json`。
- **随时自由互切语言：** 想从英文版或越化版切回原汁原味的蓝飘飘fly中文原版？直接下载对应 APK 点击“更新”覆盖安装即可，100% 完整继承进度！
