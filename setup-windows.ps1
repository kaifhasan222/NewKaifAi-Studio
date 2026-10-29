# New Kaif Ai Studio - Windows one-click setup
# Chalane ka tareeka: folder mein Shift+Right-click > "Open PowerShell window here", phir:
#   powershell -ExecutionPolicy Bypass -File .\setup-windows.ps1

$ErrorActionPreference = "Continue"
Set-Location -Path $PSScriptRoot

function Refresh-Path {
  $m = [System.Environment]::GetEnvironmentVariable("Path","Machine")
  $u = [System.Environment]::GetEnvironmentVariable("Path","User")
  $env:Path = "$m;$u"
}
function Has($cmd) { return [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }

Write-Host "`n=== New Kaif Ai Studio setup ===" -ForegroundColor Cyan

if (-not (Has "winget")) {
  Write-Host "winget nahi mila. Microsoft Store se 'App Installer' update karo, phir script dobara chalao." -ForegroundColor Red
  exit 1
}

if (-not (Has "ffmpeg")) {
  Write-Host "ffmpeg install ho raha hai..." -ForegroundColor Yellow
  winget install -e --id Gyan.FFmpeg --accept-package-agreements --accept-source-agreements
} else { Write-Host "ffmpeg: already installed" -ForegroundColor Green }

if (-not (Has "python")) {
  Write-Host "Python install ho raha hai..." -ForegroundColor Yellow
  winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
} else { Write-Host "python: already installed" -ForegroundColor Green }

if (-not (Has "node")) {
  Write-Host "Node.js install ho raha hai (optional, motion graphics ke liye)..." -ForegroundColor Yellow
  winget install -e --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
} else { Write-Host "node: already installed" -ForegroundColor Green }

Refresh-Path

if (Has "python") {
  Write-Host "faster-whisper install ho raha hai (captions ke liye)..." -ForegroundColor Yellow
  python -m pip install --upgrade pip
  python -m pip install faster-whisper
} else {
  Write-Host "Python PATH mein abhi nahi dikha. PowerShell band karke dobara kholo aur script phir chalao." -ForegroundColor Red
  exit 1
}

foreach ($d in "brand","assets\music","assets\sfx","assets\broll","assets\fonts","raw-clips","output","references","episodes") {
  New-Item -ItemType Directory -Force -Path $d | Out-Null
}

Write-Host "`n=== Check ===" -ForegroundColor Cyan
python tools\setup_check.py

Write-Host "`nAb brand\ mein photo.jpg aur voice.mp3 daalo, aur brand\BRAND.md bharo." -ForegroundColor Cyan
Write-Host "Agar ffmpeg 'missing' dikhe to PowerShell band karke dobara kholo aur 'python tools\setup_check.py' chalao." -ForegroundColor DarkYellow
