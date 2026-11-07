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
| 1 | Topic & Script (Roman Hinglish, 30-60s) | AI | `prompts/script-style-guide.md` | `episodes/epNNN/script.md` |
| 1.5 | Script Review Loop | Kaif | Chat approval | Locked `script.md` |
| 2 | Scene-wise Flow Prompts | AI | `prompts/flow-prompt-template.md` | `episodes/epNNN/flow-prompts.md` |
| 3 | Clips generate karna | Kaif / Flow | Google Flow | `raw-clips/epNNN_*.mp4` |
| 4 | Apni Awaaz (Voiceover) | Kaif | Phone / Mic, Delivery card (`prompts/voice-delivery.md`) | `episodes/epNNN/voice_raw.mp3` |
| 4.1 | Awaaz check + polish | AI | `tools/voice_report.py`, `tools/polish_voice.py` | `episodes/epNNN/voice.mp3` |
| 4.3 | (Optional) Flow `@me` awaaz | AI | `tools/flow_voice.py` | `voice.mp3` (clips se, lip-sync same) |
| 4.2 | (Optional) Clone awaaz | AI + Kaif sunta hai | `tools/voice_clone.py` (Chatterbox, free) | `voice_takes/`, `voice.mp3` |
| 5 | Captions Generation | AI | `tools\make_captions.py` (Whisper) | `episodes/epNNN/captions.srt` |
| 6 | Music & SFX Config | AI | `assets/` | `episodes/epNNN/episode.json` |
| 7 | Video Assembly | AI | `py -3.12 tools\build_video.py` | `output/epNNN.mp4` |
| 8 | QA & Preview Check | AI + Kaif | `tools\check_video.py` | Contact sheet + report |
| 9 | Publishing Pack (`/content`) | AI | `prompts/publishing-guide.md` | `episodes/epNNN/publish.md` |
| 10 | Final Approval & Post | Kaif | YouTube Shorts / Reels | Live |

---

## Awaaz (professional sound)
Detail `prompts/voice-delivery.md`.
- Script mein har line ka `Delivery:` (pace, josh 1-5, zor, ruk) aur `Action:` (body language). Josh upar-neeche: hook 5, beech 3-4, CTA 2.
- **Raasta A (default):** Kaif delivery card dekh ke record karta hai (`voice_raw.mp3`). `python tools/voice_report.py episodes/epNNN/voice_raw.mp3`. FIX wali line dobara. Phir `python tools/polish_voice.py episodes/epNNN/voice_raw.mp3 episodes/epNNN/voice.mp3 --speed 1.05`.
- **Raasta B (clone):** `.venv-voice/bin/python tools/voice_clone.py episodes/epNNN/script.md --takes 3`, Kaif takes sunke `--use scene=take` chunta hai. Reference sirf Kaif ki josh wali recording `brand/voice_ref.wav`.
- **Raasta C:** zyada lines khud ki, galat lines clone se, phir polish.
- **Raasta D (Flow `@me`):** Flow prompt mein `Dialogue: @me says "..."`, Kaif clip mein khud bolta hai. `python tools/flow_voice.py episodes/epNNN/episode.json` usi clips se `voice.mp3` banata hai. Is par `--speed` ya khamoshi katna nahi.
- Clone sirf Kaif ki apni awaaz ka. Clone wali video par YouTube ka "altered/synthetic content" sawaal Kaif khud dekhe.

---

## Core Rules
- **Hook pehle 2 second mein.** Overlay text + voice dono. Visual punch zoom. Edit pe `assets/sfx/whoosh.mp3` time `0.0`, volume `0.4`.
- Flow clips chhote rakho (3-6 sec ke scenes), edit mein jodte hain.
- Bolne wali awaaz `voice.mp3`. Flow ki `@me` awaaz rakhni ho to `tools/flow_voice.py` clips se `voice.mp3` banata hai (lip-sync same); warna Flow audio mute. Music aur SFX sirf edit pe, voice file mein nahi.
- Music `assets/music/chill-tech-01.mp3`, volume `0.12`, voice pe auto-duck. Filler reaction SFX nahi.
- Final loudness about -16 LUFS.
- **Tum hamesha final video dekhte ho.** AI frames se check karta hai, par insaani nazar zaroori hai.
- Episode folder aur video files git mein nahi jaati. Sirf code, template, photo, music aur sfx. Remote personal GitHub `kaifhasan222`, author `kaifhasan222@gmail.com`.
