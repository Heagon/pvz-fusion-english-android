# Sao Lưu & Chuyển Dữ Liệu Save / Save Data Migration / 存档备份与迁移指南

<p align="center">
  <a href="#vi-bản-việt-hóa"><b>[VI] Bản Việt Hóa</b></a> •
  <a href="#en-english"><b>[EN] English</b></a> •
  <a href="#zh-简体中文"><b>[ZH] 简体中文</b></a>
</p>

---

## [VI] Bản Việt Hóa

Khi bạn chuyển từ một file APK của nguồn khác (bị xung đột chữ ký số) sang bộ cài đặt này, hệ điều hành Android sẽ yêu cầu gỡ bản cũ. Vì vậy, bạn cần sao lưu file save trước khi gỡ.

### Vị trí file save trên điện thoại
```
/sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
*(Nếu trong thư mục có thêm thư mục `LevelData`, hãy sao lưu cả thư mục đó. Thư mục `il2cpp` chỉ là bộ nhớ đệm, có thể bỏ qua).*

### Cách sao lưu & Khôi phục

#### Cách 1: Thao tác trực tiếp trên điện thoại (Không cần máy tính)
1. Dùng ứng dụng quản lý tệp có quyền truy cập thư mục hệ thống (như **ZArchiver**, **MT Manager**, hoặc Trình quản lý tệp gốc của máy).
2. Tìm đến đường dẫn `Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/`.
3. Sao chép tệp `playerData.json` (và thư mục `LevelData` nếu có) ra thư mục an toàn khác (ví dụ `Download/` hoặc thẻ nhớ).
4. Gỡ cài đặt bản cũ, cài đặt file APK mới từ kho này.
5. Mở game mới lên 1 lần để hệ thống tự tạo thư mục dữ liệu, sau đó thoát game hoàn toàn.
6. Sao chép tệp `playerData.json` đã lưu ở bước 3 dán đè lại vào đường dẫn `Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/`.
7. Mở lại game: Toàn bộ thành quả cày cuốc đã trở lại đầy đủ!

#### Cách 2: Dùng máy tính qua cáp USB (ADB)
```bash
# 1. Kéo file save về máy tính
adb pull /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json

# 2. Gỡ bản cũ và cài bản mới
adb uninstall com.LanPiaoPiao.PlantsVsZombiesRH
adb install PvZ-Fusion-4.0.5.2-Vietnamese.apk

# 3. Mở game 1 lần rồi đóng, sau đó khôi phục save
adb push playerData.json /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```

---

## [EN] English

When switching from a third-party build signed with a different key, Android requires uninstalling the existing package. Because uninstalling wipes app storage, you must back up your save file first.

### Save File Location
```
/sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
*(If a `LevelData` folder is present, back it up as well. The `il2cpp` folder is temporary cache and can be ignored).*

### Backup & Restore Procedure

#### Method 1: On-Device (Using File Manager)
1. Use a capable file explorer that can access Android 11+ app data (e.g. **ZArchiver**, **MT Manager**, or your device's built-in File Manager).
2. Navigate to `Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/`.
3. Copy `playerData.json` (and `LevelData` if available) to a safe location such as `Download/`.
4. Uninstall the third-party APK, then install the new APK from this repository.
5. Launch the newly installed game once to let it initialize the `files/` directory, then close it completely.
6. Copy your backed-up `playerData.json` back into `Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/`.
7. Relaunch the game — all progress is fully restored!

#### Method 2: Via PC (ADB)
```bash
# 1. Pull save to computer
adb pull /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json

# 2. Reinstall
adb uninstall com.LanPiaoPiao.PlantsVsZombiesRH
adb install PvZ-Fusion-4.0.5.2-English.apk

# 3. Restore save
adb push playerData.json /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```

---

## [ZH] 简体中文

当从非本项目的其他第三方安装包（签名不一致）切换到本项目时，安卓系统会要求先卸载旧版本。由于卸载会清除应用数据目录，因此在卸载前备份存档至关重要。

### 存档文件存储路径
```
/sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
*(若该目录下存在 `LevelData` 文件夹，也请一同备份。`il2cpp` 文件夹为运行时缓存，无需备份)。*

### 备份与恢复步骤

#### 方法一：手机端直接操作（免电脑）
1. 使用具备 Android 11+ Data 目录访问权限的文件管理器（如 **MT 管理器**、**ZArchiver** 或手机自带文件管理应用）。
2. 进入路径：`Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/`。
3. 将 `playerData.json`（及可能存在的 `LevelData` 文件夹）复制备份到安全路径（如 `Download/` 目录）。
4. 卸载旧版游戏，安装本仓库发布的对应版本 APK。
5. 启动一次新安装的游戏以生成数据目录，随后彻底关闭游戏后台。
6. 将备份好的 `playerData.json` 覆盖复制回 `Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/` 目录下。
7. 重新进入游戏，存档与通关进度即可全部恢复！

#### 方法二：电脑端 ADB 命令行
```bash
# 1. 导出存档到电脑
adb pull /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json

# 2. 卸载旧版并安装新版
adb uninstall com.LanPiaoPiao.PlantsVsZombiesRH
adb install PvZ-Fusion-4.0.5.2-Chinese-Raw.apk

# 3. 恢复存档文件
adb push playerData.json /sdcard/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/playerData.json
```
