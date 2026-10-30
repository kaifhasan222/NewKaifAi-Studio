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

### Sound tools (video fiki na lage)
Yeh project ke `requirements.txt` mein nahi hain. Dono machines par alag se lagte hain. Awaaz clone nahi karte. Sound effects aur audio balance ke liye hain.

| Tool | Kahan | Note |
|---|---|---|
| Openverse | `https://api.openverse.org/v1/audio/` | Free sounds, API key nahi. Files `~/sounds` |
| Real SFX | `~/.claude/skills/real-sfx` | Skill. 78 CC0 UI sounds. `python3 scripts/setup.py check` |
| Earshot | `~/tools/earshot` | Python 3.12 venv (`uv python install 3.12`). `earshot doctor` |
| FFmpeg skill | `~/.claude/skills/ffmpeg-skill` | Local cuts, loudness, captions |

Mac par Homebrew likhne layak na ho to Python 3.12 `uv` se lo: `uv python install 3.12`. Earshot ke sunne wale models (~1.1 GB) pehli baar `earshot doctor --fetch` se aate hain.

## 3. Check
```
python tools/setup_check.py
```

## 4. Claude in Chrome (Flow automation ke liye, optional)
Chrome Web Store se "Claude" extension install karo. Pro par side panel abhi rollout mein ho sakta hai; na mile to manual mode use karo (Claude prompts deta hai, tum Flow mein paste karke clips download karte ho).

## 5. Free assets
`assets/ASSETS.md` dekho: music, sfx ke sources aur licence rules.

## Dono computers par kaam
Dono computers GitHub se sync hote hain. Remote sirf personal account hai: `https://github.com/kaifhasan222/NewKaifAi-Studio.git`. Office account `kaifhasan1234` par push mat karo.

Git mein nahi jaata: `episodes/epNNN/` (poora episode), `raw-clips/`, `output/`, `references/`, aur koi bhi video (`.mp4`, `.mov`, `.webm`). Photo aur music/sfx (mp3) ja sakte hain. Blank template `episodes/_template/` git mein rehta hai.
