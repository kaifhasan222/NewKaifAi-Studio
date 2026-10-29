# Setup (Mac + Windows)

## Sabse aasaan: one-click script
- **Windows:** folder mein PowerShell kholo, phir `powershell -ExecutionPolicy Bypass -File .\setup-windows.ps1`
- **Mac:** Terminal mein folder ke andar `bash setup-mac.sh`

Script ffmpeg, Python, Node, faster-whisper install karke `setup_check.py` chala deta hai. Neeche wale steps sirf manual tareeka hain.

## 1. Claude Desktop
claude.ai/download se install karo, Claude Pro account se login. Is folder (`new-kaif-ai-studio`) ko Cowork/Claude Code mein open karo.

## 2. Tools

### Mac (Terminal)
```
brew install ffmpeg python node
pip3 install faster-whisper
```
Homebrew nahi hai to pehle brew.sh se install karo.

### Windows (PowerShell)
```
winget install Gyan.FFmpeg
winget install Python.Python.3.12
winget install OpenJS.NodeJS.LTS
pip install faster-whisper
```
Install ke baad PowerShell band karke dobara kholo. Windows par `python3` ki jagah `python` use karo.

`node` sirf tab chahiye jab motion graphics ke liye Remotion use karo (optional).

## 3. Check
```
python tools/setup_check.py
```

## 4. Claude in Chrome (Flow automation ke liye, optional)
Chrome Web Store se "Claude" extension install karo. Pro par side panel abhi rollout mein ho sakta hai; na mile to manual mode use karo (Claude prompts deta hai, tum Flow mein paste karke clips download karte ho).

## 5. Free assets
`assets/ASSETS.md` dekho: music, sfx ke sources aur licence rules.

## Dono computers par kaam
Folder ko Google Drive/OneDrive/GitHub (private repo) se sync rakho. `raw-clips/` aur `output/` bade hote hain, `.gitignore` unhe git se bahar rakhta hai.
