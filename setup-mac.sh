#!/usr/bin/env bash
# New Kaif Ai Studio - Mac one-click setup
# Chalane ka tareeka: Terminal mein folder ke andar:  bash setup-mac.sh
set -u
cd "$(dirname "$0")"

echo "=== New Kaif Ai Studio setup ==="

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew nahi mila. Pehle https://brew.sh se install karo, phir ye script dobara chalao."
  exit 1
fi

for pkg in ffmpeg python node; do
  if brew list "$pkg" >/dev/null 2>&1; then echo "$pkg: already installed"; else brew install "$pkg"; fi
done

pip3 install --upgrade pip --break-system-packages 2>/dev/null || pip3 install --upgrade pip
pip3 install faster-whisper --break-system-packages 2>/dev/null || pip3 install faster-whisper

mkdir -p brand assets/music assets/sfx assets/broll assets/fonts raw-clips output references episodes

echo "=== Check ==="
python3 tools/setup_check.py

echo "Ab brand/ mein photo.jpg aur voice.mp3 daalo, aur brand/BRAND.md bharo."
