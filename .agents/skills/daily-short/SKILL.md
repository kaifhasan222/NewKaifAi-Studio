---
name: daily-short
description: Run the New Kaif Ai daily workflow to produce one Hinglish tech short (script, Flow or faceless visuals, edit, QA, publish pack). Use when the user says "daily-short", "new episode", "aaj ka video", gives a topic, or gives a topic plus a reference video to match in style.
---

# daily-short

1. Read `AGENTS.md`, `PIPELINE.md`, `prompts/script-style-guide.md`.
2. Pick the next episode number from `episodes/` and copy `episodes/_template/` to `episodes/epNNN/`.
3. If a reference video is given, follow `prompts/reference-style-workflow.md` first: analyze it, write a style-card, get Kaif's OK. Copy the style only, never the content.
   If no topic is given, propose 3 topics (search the web for current tech news first) and wait for a choice.
   Before the script, ask which motion style from `prompts/motion-styles.md` (https://nafay3d.com). Wait for a name such as Pop Info. If Kaif says to pick whatever fits the video, choose one style, say which and why, then continue. Do not copy that site's prompt text, music, or voice.
4. Decide mode: Flow, or faceless (`prompts/faceless-mode.md`) when Flow credits are out or the topic suits animation/screen demo. Write `script.md` (Hinglish, 30-60s, hook in first 2s, one idea, clear CTA) and `flow-prompts.md` using `prompts/flow-prompt-template.md`. Each `Voice:` line is only what gets spoken, in Devanagari, with a separate `Delivery:` in the form `tez|normal|dheema, josh 1-5, zor "शब्द", ruk <sec>` and an `Action:` (body language matched to josh) per `prompts/script-style-guide.md` and `prompts/voice-delivery.md`. Josh must rise and fall across the video: hook 5, middle 3-4, CTA 2. Put the scene's `Action:` and josh into the `@me` Flow prompt's Action. `@me` is Kaif's voice, `@me_photo` is his avatar (face). Every clip that shows Kaif uses `@me @me_photo` plus the `CHARACTER:` line from `flow-prompts.md` copied word for word, so the face stays the same; check each clip's face against `me_photo` and regenerate mismatches (`.cursor/skills/google-flow/SKILL.md`). No filler reactions (`Aree`, `Achaa`, `Dekho`, `Matlab`, `Bas`). Do not stretch vowels. On-screen titles stay clean.
5. Generate clips in Google Flow if browser control is available; otherwise stop and ask Kaif to paste the prompts and put downloads in `raw-clips/` named `epNNN_01.mp4`, `epNNN_02.mp4`, ...
5.5. Voice: ask Kaif to record `episodes/epNNN/voice_raw.mp3` using the Delivery card, run `tools/voice_report.py` on it, ask for re-takes of FIX lines, then `tools/polish_voice.py voice_raw.mp3 voice.mp3 --speed 1.05`. If Kaif wants the clone, run `tools/voice_clone.py episodes/epNNN/script.md --takes 3` with the `.venv-voice` Python, let Kaif pick takes with `--use scene=take`. If Kaif wants the Flow `@me` voice, put `Dialogue: @me says "<Voice line>" | Tone: ...` in each Flow prompt, then run `tools/flow_voice.py episodes/epNNN/episode.json` to build `voice.mp3` from the clips (lip-sync stays; no --speed or gap cutting). The clone reference is only Kaif's own recording (`brand/voice_ref.wav`), never anyone else's voice.
6. Make captions with `tools/make_captions.py`, rewrite to Roman Hinglish keeping timings.
7. Fill `episode.json` (clips, voice, music, sfx, captions, overlays) and run `tools/build_video.py`. Music is edit-only: `assets/music/chill-tech-01.mp3` at volume 0.12. Hook zoom SFX is `assets/sfx/whoosh.mp3` at 0.0, volume 0.4. Do not put music or SFX inside `voice.mp3`.
8. Run `tools/check_video.py`, look at the contact sheet, fix obvious issues, rebuild once.
9. Write `episodes/epNNN/publish.md` (titles, description, tags, hashtags, pinned comment, Instagram caption, upload checklist) per `prompts/publishing-guide.md`, keywords from web search. Channel "NEW KAIF AI" / @kaifhasan222, emojis per the guide's emoji rules, description and caption in copy-paste code blocks.
10. Report to Kaif: file path, what was assumed, what to check. Never post anything.
11. Do not git-add `episodes/epNNN/` or any video file. Photos and music/sfx may be committed. Push only to GitHub `kaifhasan222`.
