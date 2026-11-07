---
name: daily-short
description: Run the New Kaif Ai studio workflow to produce one Hinglish tech short (script, Flow or faceless visuals, edit, QA, publish pack). Triggered by "/start", "/start auto", "daily-short", "new episode", "aaj ka video", "/content", or "/edit".
---

# daily-short & Studio Workflow

## Commands & Triggers
- **/start** (or "aaj ka video", "new episode"): Triggers interactive intake questionnaire (Step 1).
- **/start auto**: Skips questions, automatically researches today's trending tech news, picks best motion style & zoom effect, and proceeds to script & flow prompts.
- **/content** (or **/publish**): Generates the complete publishing pack (`episodes/epNNN/publish.md`).
- **/edit**: Rebuilds the current episode video using `py -3.12 tools\build_video.py`.
- **/status**: Reports current progress of the episode.

---

## Workflow Steps

### Step 1: Interactive Intake (`/start`)
When `/start` is triggered, ask Kaif these 5 key questions:
1. **Topic:** What topic or reference link? (Or choose `Auto / Trending`).
2. **Motion Graphics Style:** From `prompts/motion-styles.md` (`Pop Info`, `Creator Motion Graphics`, `Clean Tech`, `Chalk Talk`, `Data Story`, `Software Walkthrough`) or `Auto`.
3. **Zoom & Animation Vibe:** Punch zoom & fast viral cuts, smooth zoom-in calm explainer, or UI demo.
4. **Voice / Audio Source:** Record on phone with the Delivery card (`episodes/epNNN/voice_raw.mp3`), clone of Kaif's own voice (`tools/voice_clone.py`), or brand/existing voice?
5. **Visual Mode:** Google Flow clips or Faceless animation (`prompts/faceless-mode.md`).

*Auto-Fallback:* If Kaif says "kuch topic nahi hai", "auto kar do", "tum decide karo", or enters `/start auto`:
- Search the web for current AI/tech news.
- Pick the most viral/relevant topic, best matching motion style, and zoom vibe.
- Announce what was picked and continue immediately.

### Step 2: Next Episode Setup
1. Find the next episode folder number in `episodes/` (e.g., `ep001`, `ep002`, ...).
2. Copy `episodes/_template/` to `episodes/epNNN/`.

### Step 3: Script Drafting & Review Loop
1. Write `episodes/epNNN/script.md` using `prompts/script-style-guide.md`:
   - Language: **Roman Hinglish**.
   - Length: 30-60 seconds.
   - Hook in the first 2 seconds (visual + voice).
   - `Voice:` is spoken Devanagari only. Separate `Delivery:` as `tez|normal|dheema, josh 1-5, zor "शब्द", ruk <sec>` and an `Action:` (body language matched to josh), per `prompts/voice-delivery.md`. Josh rises and falls: hook 5, middle 3-4, CTA 2. No filler reactions (`Aree`, `Achaa`, `Dekho`, `Matlab`, `Bas`).
   - Clear call to action (CTA) at the end.
2. **Review Loop:** Show the complete script to Kaif in chat.
   - Ask: *"Script check karo. Kya koi change chahiye ya approved hai?"*
   - If Kaif requests edits, revise `script.md`.
   - When Kaif confirms ("Approved", "OK", "theek hai"), proceed to asset generation.

### Step 4: Visuals & Audio Assets
1. **Flow Prompts:** Generate scene-by-scene prompts in `episodes/epNNN/flow-prompts.md` using `prompts/flow-prompt-template.md`. Put each scene's `Action:` and josh into the `@me` prompt's Action. `@me` is Kaif's voice, `@me_photo` is his avatar (face). Every clip that shows Kaif uses `@me @me_photo` plus the `CHARACTER:` line copied word for word, so the face stays the same; check each clip's face against `me_photo` and regenerate mismatches.
2. **Visual Clips:** Kaif generates clips in Google Flow (or browser automation) and puts them in `raw-clips/epNNN_01.mp4`, `epNNN_02.mp4`... (Or generate faceless assets if in Faceless mode).
3. **Voiceover:**
   - If Kaif records on phone: show him the Delivery card, save as `episodes/epNNN/voice_raw.mp3`, run `py -3.12 tools\voice_report.py episodes\epNNN\voice_raw.mp3`, ask for re-takes of FIX lines, then `py -3.12 tools\polish_voice.py episodes\epNNN\voice_raw.mp3 episodes\epNNN\voice.mp3 --speed 1.05`.
   - If Kaif wants the clone: `.venv-voice\Scripts\python tools\voice_clone.py episodes\epNNN\script.md --takes 3`, Kaif listens to `voice_takes\` and picks with `--use scene=take`. Reference is only Kaif's own recording (`brand/voice_ref.wav`), never anyone else's voice.
   - If Kaif wants the Flow `@me` voice: put `Dialogue: @me says "<Voice line>" | Tone: ...` in each Flow prompt, then `py -3.12 tools\flow_voice.py episodes\epNNN\episode.json` builds `voice.mp3` from the clips (lip-sync stays; no --speed or gap cutting).
   - If using existing brand audio: copy from `brand/voice.mp3`.

### Step 5: Captions & Assembly
1. **Captions:** Run `py -3.12 tools\make_captions.py episodes\epNNN\voice.mp3`. Verify and clean up text into Roman Hinglish while preserving timestamps (`captions.srt`).
2. **Config:** Fill `episodes/epNNN/episode.json` with clips, voice, music, sfx, captions, and overlays. Music edit-only: `assets/music/chill-tech-01.mp3` at 0.12. Hook zoom SFX: `assets/sfx/whoosh.mp3` at 0.0, volume 0.4. Do not bake music or SFX into `voice.mp3`.
3. **Build:** Run `py -3.12 tools\build_video.py episodes\epNNN\episode.json` to generate `output/epNNN.mp4`.

### Step 6: QA Review
1. Run `py -3.12 tools\check_video.py output\epNNN.mp4`.
2. Review the generated contact sheet for cut-off captions, black frames, and check audio balance (voice loud & clear, music ducked to ~0.12, -16 LUFS).
3. Report any issues and rebuild if needed.

### Step 7: Publishing Kit (`/content`)
Write `episodes/epNNN/publish.md` following `prompts/publishing-guide.md`:
- 3 Click-worthy viral title options.
- YouTube description with keywords from web search.
- SEO tags & hashtags.
- Pinned comment.
- Instagram Reel caption formatted in a copy-paste code block with appropriate emojis.
- Final upload checklist.

### Step 8: Final Report & Approval
- Give Kaif a summary of the generated video, file path, what was assumed, and what to verify.
- Kaif gives final approval and manually uploads to YouTube Shorts & Instagram Reels.
- **Git rules:** Never git-add `episodes/epNNN/` or `.mp4` video files. Push code/prompts only to `kaifhasan222`.
