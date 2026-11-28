# 💾 Sao Lưu &amp; Chuyển Dữ Liệu Save · Save Data Migration · 存档备份与迁移

<p align="center">
  <a href="../README.vi.md"><b>← [VI] Trang Chủ Tiếng Việt</b></a> &nbsp;•&nbsp;
  <a href="../README.md"><b>← [EN] English Home</b></a> &nbsp;•&nbsp;
  <a href="../README.cn.md"><b>← [CN] 返回中文主页</b></a>
</p>

<p align="center">
  <a href="INSTALL.md">📖 Hướng Dẫn Cài Đặt (INSTALL)</a> &nbsp;•&nbsp;
  <a href="UPDATE.md">🔄 Cập Nhật &amp; Đổi Ngôn Ngữ (UPDATE)</a> &nbsp;•&nbsp;
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

Khi bạn chuyển **lần đầu tiên** từ một bản APK nguồn khác (khác chữ ký số) sang bộ cài đặt này, Android sẽ yêu cầu gỡ bản cũ. Vì gỡ cài đặt sẽ xóa thư mục dữ liệu của game, hãy làm theo hướng dẫn dưới đây để giữ trọn 100% tiến trình cày cuốc (**chỉ cần làm 1 lần duy nhất**; từ các lần cập nhật sau bạn chỉ việc cài đè).

### Vị trí tệp Save trên điện thoại
```text
/sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
*(Nếu có thêm thư mục `LevelData`, hãy sao chép cả thư mục đó. Thư mục `il2cpp` chỉ là bộ nhớ đệm hệ thống, không cần sao lưu).*

### Cách 1: Thực hiện ngay trên điện thoại (Không cần máy tính / Không cần Root)
1. Mở ứng dụng quản lý tệp hỗ trợ đọc `Android/data` trên Android 11+ (như **ZArchiver**, **MT Manager**, **MiXplorer**, hoặc trình Tệp mặc định của hãng máy).
2. Đi tới đường dẫn `Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/`.
3. **Sao chép `playerData.json`** (và thư mục `LevelData` nếu có) sang nơi an toàn ngoài thư mục đó (ví dụ `Download/`).
4. Gỡ cài đặt bản game cũ trên máy, sau đó cài đặt tệp APK mới tải từ kho này.
5. **Mở game mới lên 1 lần** tới màn hình Menu chính để game tự khởi tạo thư mục `files/`, rồi **đóng hẳn game**.
6. Sao chép tệp `playerData.json` từ `Download/` dán đè ngược lại vào `Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/`.
7. Mở lại game — toàn bộ cây, vàng và màn chơi đã quay trở lại 100%!

### Cách 2: Dùng máy tính qua cáp USB (`adb` — Ổn định trên mọi bản Android 11–15)
```bash
# 1. Sao lưu file save về máy tính TRƯỚC KHI gỡ bản cũ
adb pull /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json

# 2. Gỡ bản cũ và cài bản mới từ kho này
adb uninstall com.LanPiaoPiao.PlantsVsZombiesRH
adb install PvZ-Fusion-4.0.5.2-Vietnamese-B.0.1.apk

# 3. Mở game trên điện thoại 1 lần tới Menu rồi đóng hẳn, sau đó đẩy lại file save
adb push playerData.json /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```

---

<a id="en-english"></a>
## [EN] English

When switching **for the first time** from a third-party APK signed with a different key, Android requires uninstalling the old package first. Because uninstalling clears app storage, back up your save file beforehand (**one-time step** — all future updates within this repository install over the top automatically).

### Save File Path
```text
/sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
*(If a `LevelData` directory exists alongside it, back that up too. Ignore `il2cpp` — it is just runtime cache).*

### Method 1: On-Device Only (No PC / No Root)
1. Open a file manager capable of accessing `Android/data` on Android 11+ (such as **ZArchiver**, **MT Manager**, **MiXplorer**, or your OEM Files app).
2. Browse to `Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/`.
3. **Copy `playerData.json`** (and `LevelData` if present) to a safe folder like `Download/`.
4. Uninstall the old third-party app, then install the APK from this repository.
5. **Launch the game once** until it reaches the Main Menu (this creates the `files/` folder), then **force-close the game**.
6. Copy `playerData.json` from `Download/` back into `Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/`, overwriting if prompted.
7. Relaunch the game — 100% of your progress, coins, and unlocked plants are restored!

### Method 2: Via PC (`adb` — Reliable on Android 11–15)
```bash
# 1. Back up your save to PC BEFORE uninstalling
adb pull /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json

# 2. Replace the differently-signed package
adb uninstall com.LanPiaoPiao.PlantsVsZombiesRH
adb install PvZ-Fusion-4.0.5.2-English-B.0.1.apk

# 3. Launch the game once to the Main Menu, close it, then restore your save
adb push playerData.json /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```

---

<a id="cn-简体中文"></a>
## [CN] 简体中文

当您**首次**从非本仓库发布的其他安装包（签名不一致）切换到本项目时，安卓系统会要求先卸载旧版。由于卸载操作会一并清除应用数据目录，请在卸载前按以下步骤备份存档（**仅首次切换需要**，后续在本仓库内更新或换语言直接覆盖安装即可）。

### 本地存档文件路径
```text
/sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
*(若同目录下存在 `LevelData` 文件夹请一并备份；`il2cpp` 为运行缓存目录，无需备份)。*

### 方法一：手机端直接备份恢复（免电脑 / 免 Root）
1. 打开支持访问 Android 11+ `Android/data` 目录的文件管理器（如 **MT 管理器**、**ZArchiver**、**MiXplorer** 或品牌自带文件管理）。
2. 进入 `Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/`。
3. 将 **`playerData.json`**（及可能存在的 `LevelData` 文件夹）复制到外部安全位置（例如 `Download/` 目录）。
4. 卸载旧版应用，安装本仓库下载的新版 APK。
5. **启动一次新安装的游戏**直至进入主菜单（以自动初始化 `files/` 目录），随后**彻底划掉关闭游戏后台**。
6. 将备份好的 `playerData.json` 复制覆盖回 `Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/`。
7. 重新打开游戏，所有金币、植物与关卡进度即刻 100% 恢复！

### 方法二：使用电脑端 `adb` 命令（全安卓版本通用稳妥）
```bash
# 1. 卸载前先将存档拉取到电脑备份
adb pull /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json

# 2. 卸载旧签名包并安装本仓库 APK
adb uninstall com.LanPiaoPiao.PlantsVsZombiesRH
adb install PvZ-Fusion-4.0.5.2-Chinese-Raw-B.0.1.apk

# 3. 手机上启动一次游戏至主菜单后关闭，再推回存档
adb push playerData.json /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
