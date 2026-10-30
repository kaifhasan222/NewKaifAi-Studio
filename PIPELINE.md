# Daily pipeline: 1 short, kam se kam kaam

## Do tareeke se shuru kar sakte ho
- **Sirf topic:** "daily-short chalao, topic: ..." -> neeche ka flow.
- **Topic + reference video:** "is reference ke style mein banao" -> pehle `prompts/reference-style-workflow.md` (style-card), phir neeche ka flow.

## Do modes
- **Flow mode:** visuals Google Flow ke AI clips se.
- **Faceless mode:** Flow ka limit khatam ho to animation + awaaz + sound design (`prompts/faceless-mode.md`). Step 3 mein clips ka source badalta hai, baaki sab same.

| # | Step | Kaun | Tool | Output |
|---|---|---|---|---|
| 1 | Topic aur script (Hinglish, 30-60s) | Claude | `prompts/script-style-guide.md` | `episodes/epNNN/script.md` |
| 2 | Scene-wise Flow prompts | Claude | `prompts/flow-prompt-template.md` | `episodes/epNNN/flow-prompts.md` |
| 3 | Clips generate karna | Claude in Chrome ya tum | Google Flow | `raw-clips/epNNN_*.mp4` |
| 4 | Apni awaaz | Tum (ya existing voice mp3) | Phone/mic | `brand/voice.mp3` ya `episodes/epNNN/voice.mp3` |
| 5 | Captions | Claude | `make_captions.py` + Roman Hinglish cleanup | `episodes/epNNN/captions.srt` |
| 6 | Music/sfx chunna | Claude | `assets/` | `episode.json` mein entries |
| 7 | Assemble | Claude | `build_video.py` | `output/epNNN.mp4` |
| 8 | QA | Claude, phir tum | `check_video.py` | contact sheet + report |
| 9 | Title, description, tags, hashtags | Claude | `prompts/publishing-guide.md` | `episodes/epNNN/publish.md` |
| 10 | Approve, post | Tum | YouTube Shorts / Reels | Live |

## Rules
- **Hook pehle 2 second mein.** Overlay text + voice dono.
- Flow clips chhote rakho (3-6 sec ke scenes), edit mein jodte hain.
- Flow ka apna audio ho to use mute karte hain; voice aur music hum controlled mix karte hain.
- Music voice ke neeche (volume ~0.12, auto-ducking). SFX sirf transitions/emphasis par.
- Final loudness about -16 LUFS.
- **Tum hamesha final video dekhte ho.** Claude frames se check karta hai, par insaani nazar zaroori hai.
- Episode folder aur video files git mein nahi jaati. Sirf code, template, photo, music aur sfx. Remote personal GitHub `kaifhasan222`.

## Usage bachane ke tareeke (Claude Pro limit)
- Edit templates aur scripts se hota hai, Claude har baar naya code nahi likhta.
- Ek baar mein 3-5 episodes ke scripts + Flow prompts banwa lo (batch).
- Heavy browser automation kam karo; prompts batch mein paste karna sasta padta hai.
- Chat, Claude Code aur Cowork ek hi usage pool share karte hain.

## Phase plan
1. **Hafta 1:** 1 episode haath se poora (setup, test, templates thik karna).
2. **Hafta 2:** Batch scripts + prompts, edit script se.
3. **Hafta 3+:** Daily skill (`daily-short`) se ek-command flow.
4. **Baad mein (optional):** Remotion/HyperFrames motion graphics, background removal (rembg), thumbnails.
