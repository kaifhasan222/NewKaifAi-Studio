# Daily pipeline: 1 short, kam se kam kaam

## Shortcuts & Quick Commands
- **/start** (ya "aaj ka video", "new episode"): Interactive wizard shuru hota hai. Agent pehle 5 intake questions poochhega:
  1. Topic (ya "auto / trending")
  2. Motion Graphics Style (`prompts/motion-styles.md`)
  3. Zoom / Camera Vibe (Punch zoom & fast cuts, smooth calm zoom, UI focus)
  4. Audio Source (Delivery card ke saath phone recording `voice_raw.mp3`, apni awaaz ka clone, ya existing voice)
  5. Visual Mode (Google Flow vs Faceless)
- **/start auto**: Bina ruke auto-mode: trending tech news web search karke script, flow prompts aur config khud decide karke draft karega.
- **/content** (ya **/publish**): Episode ka complete SEO pack banata hai (`episodes/epNNN/publish.md`) - 3 title options, tags, hashtags, pinned comment, aur copy-paste Instagram Reel caption.
- **/edit**: `py -3.12 tools\build_video.py episodes\epNNN\episode.json` re-run karke video render karega.
- **/status**: Batayega episode abhi kis step par hai (Script, Audio, Clips, Edit, QA, Publish).

---

## Motion Style Selection
Script se pehle Kaif se poochho: kaunsa style. List [nafay3d.com](https://nafay3d.com) se hai, detail `prompts/motion-styles.md`.
- Creator Motion Graphics, Chalk Talk, Clean Tech, Software Walkthrough, Data Story, Warm Canvas, Pop Info.
- Kaif ek naam bole to wahi banao. "Jo achha ho" ya "auto" bole to tum topic ke hisaab se ek style chuno, naam batao, phir banao.

---

## Do Modes
- **Flow mode:** visuals Google Flow ke AI clips se (`raw-clips/epNNN_*.mp4`).
- **Faceless mode:** Dono Flow accounts (`kaifhasan222` aur `newpub222@gmail.com`) ke credits khatam hon, ya topic animation/screen demo ke layak ho, tab `prompts/faceless-mode.md`. Ek account ke credits khatam hon to pehle doosre account ke project **me** mein jao. `@me` avatar/awaaz, `@me_photo` photo.

---

## Pipeline Steps Table

| # | Step | Kaun | Tool | Output |
|---|---|---|---|---|
| 0 | Intake & Setup (`/start`) | Kaif + AI | Chat Q&A | Episode folder `episodes/epNNN/` |
| 1 | Topic & Script (Roman Hinglish, 30-60s) | AI | `prompts/script-style-guide.md`, `prompts/hook-guide.md`, `prompts/script-fun-simple.md` | `episodes/epNNN/script.md` |
| 1.5 | Script Review Loop | Kaif | Chat approval | Locked `script.md` |
| 2 | Scene-wise Flow Prompts | AI | `prompts/flow-prompt-template.md` | `episodes/epNNN/flow-prompts.md` |
| 3 | Clips generate karna | Kaif / Flow | Google Flow | `raw-clips/epNNN_*.mp4` |
| 4 | Apni Awaaz (Voiceover) | Kaif | Phone / Mic, Delivery card (`prompts/voice-delivery.md`) | `episodes/epNNN/voice_raw.mp3` |
| 4.1 | Awaaz check + polish | AI | `tools/voice_report.py`, `tools/polish_voice.py` | `episodes/epNNN/voice.mp3` |
| 4.4 | (Optional) Kaif ka raw camera video | AI + Kaif report dekhta hai | `tools/cut_silence.py --takes --fillers --dry-run`, phir bina dry-run, phir `tools/flow_voice.py` | best take + filler kata, `cut_report.txt` |
| 4.3 | (Optional) Flow `@me` awaaz | AI | `tools/cut_silence.py --whisper`, phir `tools/flow_voice.py` | jump cuts + `voice.mp3` (lip-sync same) |
| 4.2 | (Optional) Clone awaaz | AI + Kaif sunta hai | `tools/voice_indic.py` (IndicF5, free) | `voice_takes_indic/`, `voice.mp3`, `voice_parts.json` |
| 5 | Captions Generation | AI | `tools\make_captions.py` (Whisper) | `episodes/epNNN/captions.srt` |
| 6 | Music & SFX Config | AI | `assets/` | `episodes/epNNN/episode.json` |
| 7 | Video Assembly | AI | `py -3.12 tools\build_video.py` | `output/epNNN.mp4` |
| 8 | QA & Preview Check | AI + Kaif | `tools\check_video.py` | Contact sheet + report |
| 8.5 | Thumbnail A/B/C | AI + Kaif chunta hai | `tools/make_thumbnail.py`, `prompts/thumbnail-guide.md` | `output/epNNN_thumb_A/B/C.jpg` |
| 9 | Publishing Pack (`/content`) | AI | `prompts/publishing-guide.md` | `episodes/epNNN/publish.md` |
| 10 | Final Approval & Post | Kaif | YouTube Shorts / Reels | Live |

---

## Awaaz (professional sound)
Detail `prompts/voice-delivery.md`.
- Script mein har line ka `Delivery:` (pace, josh 1-5, zor, ruk) aur `Action:` (body language). Josh upar-neeche: hook 5, beech 3-4, aakhri comment sawaal 3. Follow/like/subscribe sirf end animation mein, bola nahi jaata.
- **Raasta A (default):** Kaif delivery card dekh ke record karta hai (`voice_raw.mp3`). `python tools/voice_report.py episodes/epNNN/voice_raw.mp3`. FIX wali line dobara. Phir `python tools/polish_voice.py episodes/epNNN/voice_raw.mp3 episodes/epNNN/voice.mp3 --speed 1.05`.
- **Raasta B (clone):** `.venv-indic/bin/python tools/voice_indic.py episodes/epNNN/script.md --takes 2` (IndicF5, Hindi). Har take Whisper se sun ke best khud chunta hai; Kaif sunke `--use scene=take` se badal sakta hai. Josh har scene ke josh wali reference se (`brand/refs/RECORD.md`). Reference sirf Kaif ki awaaz.
- **Raasta C:** zyada lines khud ki, galat lines clone se, phir polish.
- **Raasta D (Flow `@me`):** Flow prompt mein `Dialogue: @me says "..."`, Kaif clip mein khud bolta hai. `python tools/flow_voice.py episodes/epNNN/episode.json` usi clips se `voice.mp3` banata hai. Is par `--speed` ya khamoshi katna nahi.
- **Raasta E (apna camera video):** Kaif scene-wise ya ek lamba take record karke `episodes/epNNN/raw-clips/` mein daalta hai (9:16). Galti ho to wahi line dobara bol do, rukna mat. `.venv/bin/python tools/cut_silence.py episodes/epNNN/episode.json --takes --fillers --dry-run` report deta hai: har line ke takes (RAKHA/KATA), "aa/umm", atke shabd, script se bahar wala hissa (EXTRA; `--drop-extra` se kata). Kaif report dekhe, galat ho to clip par `"keep": [[a, b]]` ya `"cuts"`, phir bina `--dry-run`, phir `tools/flow_voice.py`. Whisper medium (~1.5 GB, pehli baar download).
- Clone sirf Kaif ki apni awaaz ka. Clone wali video par YouTube ka "altered/synthetic content" sawaal Kaif khud dekhe.

---

## Core Rules
- **Hook pehle 2 second mein** (`prompts/hook-guide.md`): 3 option alag type ke, ek chuno. Pehli line 10 shabd se kam, asli baat pehle. Overlay text + voice dono, text voice ki copy nahi. Visual punch zoom ya proof shot. Hook par ek saaf hit/boom (whoosh nahi), `prompts/sound-design.md`.
- Flow clips chhote rakho (3-6 sec ke scenes), edit mein jodte hain.
- Bolne wali awaaz `voice.mp3`. Flow ki `@me` awaaz rakhni ho to `tools/flow_voice.py` clips se `voice.mp3` banata hai (lip-sync same); warna Flow audio mute. Music aur SFX sirf edit pe, voice file mein nahi.
- Sound `prompts/sound-design.md` se: music `assets/music/lofi-upbeat-raspberrymusic.mp3` volume `0.10` (credit zaroori), voice pe auto-duck; 3 parat SFX, har hansi par meme sound; awaaz ki khamoshi kati ho.
- Final loudness about -16 LUFS.
- **Tum hamesha final video dekhte ho.** AI frames se check karta hai, par insaani nazar zaroori hai.
- Episode folder aur video files git mein nahi jaati. Sirf code, template, photo, music aur sfx. Remote personal GitHub `kaifhasan222`, author `kaifhasan222@gmail.com`.
