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
4. Decide mode: Flow, or faceless (`prompts/faceless-mode.md`) when Flow credits are out or the topic suits animation/screen demo. Write `script.md` (Hinglish, 30-60s, hook in first 2s, one idea, clear CTA) and `flow-prompts.md` using `prompts/flow-prompt-template.md`. Each `Voice:` line is what gets spoken: one natural reaction per scene (`Aree`, `Achaa`, `Dekho`, `Matlab`, `Bas`), written in `prompts/script-style-guide.md`. Do not stretch vowels. On-screen titles stay clean.
5. Generate clips in Google Flow if browser control is available; otherwise stop and ask Kaif to paste the prompts and put downloads in `raw-clips/` named `epNNN_01.mp4`, `epNNN_02.mp4`, ...
6. Make captions with `tools/make_captions.py`, rewrite to Roman Hinglish keeping timings.
7. Fill `episode.json` (clips, voice, music, sfx, captions, overlays) and run `tools/build_video.py`.
8. Run `tools/check_video.py`, look at the contact sheet, fix obvious issues, rebuild once.
9. Write `episodes/epNNN/publish.md` (titles, description, tags, hashtags, pinned comment, Instagram caption, upload checklist) per `prompts/publishing-guide.md`, keywords from web search. Channel "NEW KAIF AI" / @kaifhasan222, emojis per the guide's emoji rules, description and caption in copy-paste code blocks.
10. Report to Kaif: file path, what was assumed, what to check. Never post anything.
11. Do not git-add `episodes/epNNN/` or any video file. Photos and music/sfx may be committed. Push only to GitHub `kaifhasan222`.
