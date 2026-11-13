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
.venv/bin/pip install pillow==12.3.0   # tools/thumb_card.py (thumbnail text)
```
Homebrew nahi hai to pehle brew.sh se install karo.

### Windows (PowerShell)
```
winget install Gyan.FFmpeg
winget install Python.Python.3.12
winget install OpenJS.NodeJS.LTS
pip install faster-whisper pillow==12.3.0
```
Install ke baad PowerShell band karke dobara kholo. Windows par `python3` ki jagah `python` use karo.

`node` sirf tab chahiye jab motion graphics ke liye Remotion use karo (optional).

### Sound tools (video fiki na lage)
Yeh project ke `requirements.txt` mein nahi hain. Dono machines par alag se lagte hain. Awaaz clone nahi karte (clone ke liye neeche "Voice clone"). Sound effects aur audio balance ke liye hain.

| Tool | Kahan | Note |
|---|---|---|
| Openverse | `https://api.openverse.org/v1/audio/` | Free sounds, API key nahi. Files `~/sounds` |
| Real SFX | `~/.claude/skills/real-sfx` | Skill. 78 CC0 UI sounds. `python3 scripts/setup.py check` |
| Earshot | `~/tools/earshot` | Python 3.12 venv (`uv python install 3.12`). `earshot doctor` |
| FFmpeg skill | `~/.claude/skills/ffmpeg-skill` | Local cuts, loudness, captions |

Mac par Homebrew likhne layak na ho to Python 3.12 `uv` se lo: `uv python install 3.12`. Earshot ke sunne wale models (~1.1 GB) pehli baar `earshot doctor --fetch` se aate hain.

### Voice clone (optional, free)
Kaif ki apni awaaz ka clone, `tools/voice_indic.py` ke liye. Model IndicF5 (AI4Bharat, MIT licence), Hindi ke liye bana. 12 Nov 2026 se Chatterbox ki jagah (Chatterbox Hindi shabd galat bolta tha). Alag venv `.venv-indic` isi folder mein (git mein nahi), ~3 GB disk (packages + model). Tested Python 3.11, Mac M-series.

```
uv python install 3.11
uv venv --python 3.11 .venv-indic
uv pip install --python .venv-indic -r requirements-indic.txt
```
Model gated hai (ek baar, Kaif khud): huggingface.co/ai4bharat/IndicF5 par "Agree and access repository", phir `.venv-indic/bin/hf auth login` aur terminal mein Read token paste. Token chat ya file mein nahi.
- Mac M1/M2/M3: GPU (MPS) apne aap, ek line ~35 sec.
- Windows NVIDIA GPU: CUDA wala torch chahiye, warna CPU par chalega (1 line ~70 sec).
- Reference: apni 10-15 sec josh wali saaf recording `brand/voice_ref.wav`. Guide `prompts/voice-delivery.md`.
- Output mein Resemble ka Perth watermark hota hai (sunai nahi deta).

## 3. Check
```
python tools/setup_check.py
```

## 4. Claude in Chrome (Flow automation ke liye, optional)
Chrome Web Store se "Claude" extension install karo. Pro par side panel abhi rollout mein ho sakta hai; na mile to manual mode use karo (Claude prompts deta hai, tum Flow mein paste karke clips download karte ho).

## 5. Free assets
`assets/ASSETS.md` dekho: music, sfx ke sources aur licence rules.

## Dono computers par kaam
Dono computers GitHub se sync hote hain. Remote sirf personal account hai: `https://github.com/kaifhasan222/NewKaifAi-Studio.git`. Commit author: `kaifhasan222 <kaifhasan222@gmail.com>` (is repo ka local git). Office account `kaifhasan1234` aur office email `kaif@roopya.com` se commit ya push mat karo. Push se pehle `gh auth status` mein `kaifhasan222` dikhna chahiye.

Git mein nahi jaata: `episodes/epNNN/` (poora episode), `raw-clips/`, `output/`, `references/`, aur koi bhi video (`.mp4`, `.mov`, `.webm`). Photo aur music/sfx (mp3) ja sakte hain. Blank template `episodes/_template/` git mein rehta hai.
