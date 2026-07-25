<#
  update.ps1 - Update the PvZ Fusion English APK WITHOUT losing your save.

  What it does:
    1. Backs up your save (playerData.json + LevelData) to a timestamped folder.
    2. Installs the new APK over the old one with `adb install -r` (keeps app data,
       so the save is preserved and the new English text auto-applies).
    3. Confirms the save survived; restores it from the backup if anything went wrong.

  Normal English -> English updates keep the save automatically (same signing key +
  the build-guid bump refreshes the text). This script is a safety net + one command.

  If you are switching FROM a differently-signed build (the original Chinese APK, or
  the very first v3.8.1 English release) install -r will fail with a signature error.
  Re-run with  -Clean  to do a safe uninstall -> install -> restore-save instead.

  Usage (PowerShell):
    powershell -ExecutionPolicy Bypass -File update.ps1 -Apk PvZ-Fusion-3.8.1-English.apk
    powershell -ExecutionPolicy Bypass -File update.ps1 -Apk PvZ-Fusion-3.8.1-English.apk -Clean

  Needs: Android platform-tools (adb) on PATH, or put adb.exe next to this script,
  or pass -Adb "C:\path\to\adb.exe". USB debugging must be ON.
#>
param(
  [string]$Apk = "",
  [string]$Adb = "",
  [switch]$Clean
)

$ErrorActionPreference = "Stop"
$PKG    = "com.LanPiaoPiao.PlantsVsZombiesRH"
$FILES  = "/sdcard/Android/data/$PKG/files"
$SAVE   = "$FILES/playerData.json"

function Find-Adb {
  param($hint)
  $cands = @()
  if ($hint) { $cands += $hint }
  $cands += @(
    "$PSScriptRoot\adb.exe",
    "$PSScriptRoot\platform-tools\adb.exe",
    "adb"
  )
  foreach ($c in $cands) {
    $cmd = Get-Command $c -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
  }
  throw "adb not found. Install Android platform-tools, or put adb.exe next to this script, or pass -Adb <path>."
}

# --- locate adb + apk ---
$Adb = Find-Adb $Adb
if (-not $Apk) {
  $newest = Get-ChildItem "$PSScriptRoot\*.apk" -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if ($newest) { $Apk = $newest.FullName }
}
if (-not $Apk -or -not (Test-Path $Apk)) {
  throw "APK not found. Pass -Apk <path-to.apk> (or put the .apk next to this script)."
}
Write-Host "adb: $Adb"
Write-Host "apk: $Apk"

# --- device ---
& $Adb start-server | Out-Null
Write-Host "Waiting for device (USB debugging must be ON, tap 'Allow' on the phone)..."
& $Adb wait-for-device
Write-Host "Device: $((& $Adb get-state).Trim())"

function Save-Exists {
  return ((& $Adb shell "if [ -f $SAVE ]; then echo YES; else echo NO; fi").Trim() -eq "YES")
}

# --- 1) backup ---
$stamp     = Get-Date -Format "yyyyMMdd-HHmmss"
$backupDir = Join-Path $PSScriptRoot "save-backups\$stamp"
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
$hadSave = Save-Exists
if ($hadSave) {
  & $Adb pull $SAVE (Join-Path $backupDir "playerData.json") | Out-Null
  # LevelData is optional
  & $Adb pull "$FILES/LevelData" $backupDir 2>$null | Out-Null
  Write-Host "Save backed up -> $backupDir"
} else {
  Write-Host "No existing save found (fresh install?) - nothing to back up."
}

# --- 2) install ---
if ($Clean) {
  Write-Host "Clean mode: uninstalling old build (save already backed up)..."
  & $Adb uninstall $PKG | Out-Null
  Write-Host "Installing $([IO.Path]::GetFileName($Apk)) ..."
  & $Adb install $Apk
  if ($LASTEXITCODE -ne 0) { throw "Install failed. Your save backup is safe in $backupDir." }
} else {
  Write-Host "Installing over the top (install -r, keeps save)..."
  $out = & $Adb install -r $Apk 2>&1
  $out | ForEach-Object { Write-Host "  $_" }
  if ($LASTEXITCODE -ne 0 -or ($out -match "Failure|INSTALL_FAILED")) {
    Write-Host ""
    Write-Host "install -r failed - this build is signed differently from the installed one"
    Write-Host "(normal the FIRST time you switch to this English build). Your save is backed up."
    Write-Host "Re-run with -Clean to uninstall + install + restore the save:"
    Write-Host "  powershell -ExecutionPolicy Bypass -File update.ps1 -Apk `"$Apk`" -Clean"
    exit 1
  }
}

# --- 3) verify / restore ---
if ($Clean) {
  # a clean install wipes app data; game must create files/ once before we push back
  Write-Host "Launching game once to create its data folder..."
  & $Adb shell monkey -p $PKG -c android.intent.category.LAUNCHER 1 | Out-Null
  Start-Sleep -Seconds 8
  & $Adb shell am force-stop $PKG | Out-Null
}

if ($hadSave) {
  if (Save-Exists -and -not $Clean) {
    Write-Host ""
    Write-Host "DONE - update installed and your save is intact." -ForegroundColor Green
  } else {
    Write-Host "Restoring save from backup..."
    & $Adb shell mkdir -p $FILES 2>$null | Out-Null
    & $Adb push (Join-Path $backupDir "playerData.json") $SAVE | Out-Null
    if (Test-Path (Join-Path $backupDir "LevelData")) {
      & $Adb push (Join-Path $backupDir "LevelData") "$FILES/" 2>$null | Out-Null
    }
    Write-Host ""
    Write-Host "DONE - update installed and save restored from backup." -ForegroundColor Green
  }
} else {
  Write-Host ""
  Write-Host "DONE - update installed (there was no prior save)." -ForegroundColor Green
}
Write-Host "Backup kept at: $backupDir"
