# New Kaif Ai Studio

Tech shorts (Hinglish, 30-60 sec) ka daily video pipeline: **Google Flow** se clips -> **Claude** se script/prompts/edit -> YouTube Shorts + Instagram Reels.

Cost: sirf Claude Pro. Baaki sab free tools (ffmpeg, Whisper, free music/sfx libraries). Flow tumhare paas pehle se hai.

## Quick start
1. `SETUP.md` follow karo (Mac ya Windows, 15 min).
2. `python tools/setup_check.py` chalao, sab OK aana chahiye.
3. `brand/` mein apna photo aur voice mp3 daalo, `brand/BRAND.md` bharo.
4. Claude Desktop mein is folder ko open karke bolo: **"daily-short chalao, topic: <topic>"**.
5. `PIPELINE.md` mein poora flow likha hai.

## Folder map
| Folder | Kya hai |
|---|---|
| `brand/` | Photo, voice, colors, font, channel identity |
| `prompts/` | Script style guide, Flow prompt template, Claude Project instructions |
| `episodes/` | Local episode folders. Git mein sirf `episodes/_template/` hai |
| `references/` | Reference videos. Git mein nahi |
| `raw-clips/` | Flow clips. Git mein nahi |
| `assets/` | Music, sfx, photos. Video files git mein nahi |
| `templates/` | Episode JSON example, motion graphics notes |
| `tools/` | `build_video.py`, `make_captions.py`, `check_video.py`, `analyze_reference.py`, `download_meme_sfx.py`, `setup_check.py` |
| `output/` | Final videos |
| `CLAUDE.md` | Claude ke liye standing instructions (Cowork / Claude Code padhta hai) |
| `.claude/skills/daily-short/` | Ek-command daily workflow skill |

## Abhi kya tested hai
`build_video.py`, `check_video.py` aur `analyze_reference.py` dummy video par test hue hain (9:16 crop, crossfade, voice + ducked music + sfx, captions, title overlay, loudness). `make_captions.py` (Whisper) aur Flow browser automation tumhare computer par pehli baar chalenge: pehle episode mein dekhna.

Sync: personal GitHub `kaifhasan222/NewKaifAi-Studio`, author `kaifhasan222 <kaifhasan222@gmail.com>`. Episode folders aur videos is repo mein commit nahi hote.

## Versions (checked 30 Oct 2026)

Python captions: `requirements.txt`. Baaki tools: `package.json` ka `studio` block. Install steps: `SETUP.md`.

| Tool | Version | File |
|---|---|---|
| faster-whisper | 1.2.1 | `requirements.txt` |
| numpy (captions, Python 3.9) | 2.0.2 | `requirements.txt` |
| ffmpeg | 9.0.2 | `package.json` |
| Node | 22.17.0 | `package.json` |
| yt-dlp | 2025.10.14 | `package.json` |
| HyperFrames | 0.8.216 | `package.json` |
| Earshot | 0.4.0 (Python 3.12, torch 2.15.0, numpy 2.5.4) | `package.json` |
| Real SFX | commit `edbefcb` (21 Oct 2026) | `package.json` |
| FFmpeg skill | 2.21.0 | `package.json` |
| Openverse | public API, no package | `package.json` |
