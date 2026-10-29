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
| `episodes/` | Har video ka folder (script, captions, episode.json) |
| `references/` | Reference videos aur unka style-card/analysis |
| `raw-clips/` | Flow se download kiye clips |
| `assets/` | Music, sound effects, b-roll, fonts |
| `templates/` | Episode JSON example, motion graphics notes |
| `tools/` | `build_video.py`, `make_captions.py`, `check_video.py`, `analyze_reference.py`, `setup_check.py` |
| `output/` | Final videos |
| `CLAUDE.md` | Claude ke liye standing instructions (Cowork / Claude Code padhta hai) |
| `.claude/skills/daily-short/` | Ek-command daily workflow skill |

## Abhi kya tested hai
`build_video.py`, `check_video.py` aur `analyze_reference.py` dummy video par test hue hain (9:16 crop, crossfade, voice + ducked music + sfx, captions, title overlay, loudness). `make_captions.py` (Whisper) aur Flow browser automation tumhare computer par pehli baar chalenge: pehle episode mein dekhna.
