# New Kaif Ai Studio: instructions for Claude

Project: YouTube Shorts + Instagram Reels channel "New Kaif Ai". Tech content, **Hinglish (Roman script)**, 30-60 sec, 9:16, 1080x1920.
Owner: Kaif. Uses his own photo and own recorded voice (`brand/`). Final approval hamesha Kaif ka.

## Kaam karne ka tareeka
- Pehle `PIPELINE.md` aur `prompts/script-style-guide.md` padho.
- Naya episode: `episodes/_template/` copy karke `episodes/epNNN/` banao.
- Script se pehle motion style poochho (`prompts/motion-styles.md`, source [nafay3d.com](https://nafay3d.com)). Kaif "Pop Info" jaise naam bole to wahi look. "Jo achha ho" bole to tum style chuno, naam likho, phir banao. Unka prompt, music, ya voice copy mat karo.
- Scripts: `prompts/script-style-guide.md` follow karo. Facts ke liye search karo, andaza mat lagao. `Voice:` line seedhi Devanagari ho. `Delivery:` alag (tez, zor, ruk). Reaction filler mat likho (`Aree`, `Achaa`, `Dekho`). Vowel mat kheench.
- Har scene ke `Delivery:` mein `tez|normal|dheema, josh 1-5, zor "शब्द", ruk <sec>` aur alag `Action:` (body language). Josh upar-neeche ho. Detail `prompts/voice-delivery.md`.
- Awaaz: Kaif ki recording par `tools/voice_report.py`, phir `tools/polish_voice.py`. Clone chahiye to `tools/voice_clone.py` (`.venv-voice` ke python se), reference sirf Kaif ki apni awaaz. Flow ki `@me` awaaz rakhni ho to `tools/flow_voice.py episodes/epNNN/episode.json` (lip-sync same).
- Flow prompts: `prompts/flow-prompt-template.md` ke format mein, har scene alag. `@me` scene ke `Action:` mein script ka action aur josh.
- Edit: `python tools/build_video.py episodes/epNNN/episode.json` (Windows par `python`, Mac par `python3`). Naya edit code mat likho jab tak tool ki kami na ho.
- Captions: `tools/make_captions.py`, phir text Roman Hinglish mein badlo, timings waise hi rakho.
- QA: `tools/check_video.py`, contact sheet dekho, dikkat likho (kata hua text, black frames, awaaz/music balance).
- Thumbnail: `prompts/thumbnail-guide.md`, `tools/make_thumbnail.py episodes/epNNN/thumb.json` se 3 options (A/B/C), Kaif chunta hai.
- Har episode ke saath `publish.md` banao (title options, description, tags, hashtags, Instagram caption) `prompts/publishing-guide.md` ke hisaab se, keywords web search se.
- Flow clips sirf project **me** mein. Awaaz ke liye `@me`, avatar (chehra) ke liye `@me_photo`; Kaif wale har clip mein dono saath, aur `flow-prompts.md` ki `CHARACTER:` line word-for-word taaki chehra har clip mein same rahe. Generate ke baad chehra `me_photo` se milao, na mile to dobara. Credit khatam ho to `newpub222@gmail.com` par switch karke wahi **me** project. Dono accounts khatam hon tab `prompts/faceless-mode.md`. Detail `.cursor/skills/google-flow/SKILL.md`. Login/password mat bharo.
- Agar Kaif topic + reference video de: `prompts/reference-style-workflow.md` follow karo. Style-card banao, Kaif se confirm karo, phir original video banao. Reference ka script/footage/music/voice kabhi copy mat karo.
- Music/sfx sirf `assets/` se, jinka licence `assets/ASSETS.md` ke hisaab se theek ho. Naya asset daalo to uska source aur licence `assets/LICENSES.md` mein likho.

## Mat karo
- Kaif ki awaaz ya chehra kisi aur ke saath na milao, na kisi aur ka misuse.
- Kisi aur ki awaaz clone mat karo (reference YouTuber ki bhi nahi). Clone reference sirf Kaif ki recording.
- Copyrighted music, clips ya logos use mat karo.
- Flow ya kisi site par login/password khud mat bharo; Kaif khud login karta hai.
- Bina Kaif ke approve kiye kuch publish/post mat karo.
- Claims (tool ka naam, feature, price) bina verify kiye video mein mat daalo.
- `episodes/epNNN/` aur koi bhi video file git mein mat daalo. Photo aur music/sfx chalenge. Push sirf personal GitHub `kaifhasan222` par. Office account `kaifhasan1234` par push mat karo.

## Output style
Kaif se Hinglish mein, seedhi aur chhoti baat karo. Har episode ke baad: kya bana, kya assume kiya, kya check karna hai.

## Git
- Remote: `https://github.com/kaifhasan222/NewKaifAi-Studio.git` (personal). Office GitHub `kaifhasan1234` par commit ya push nahi.
- Commit author hamesha personal: `kaifhasan222 <kaifhasan222@gmail.com>`. Is repo ka local git author yahi hai. Mac ka global git (`kaif@roopya.com`) mat badlo, aur us email se is repo mein commit mat karo. Push se pehle `gh auth status` mein account `kaifhasan222` hona chahiye.
- Git mein nahi: episode folders, raw clips, final videos, koi bhi video file.
- Git mein theek: code, prompts, `episodes/_template/`, photo, music, sfx.
- Nayi dependency add ho to `requirements.txt`, `SETUP.md`, `README.md`, `AGENTS.md` aur yeh file update karo.

## Voice clone (local, isi repo mein)
- Chatterbox Multilingual (Resemble AI, MIT), venv `.venv-voice/` (git mein nahi), packages `requirements-voice.txt`. Model ~3 GB pehli baar Hugging Face se. Setup `SETUP.md` -> Voice clone.

## Sound tools (local, repo ke bahar)
- Openverse API (no key), Real SFX `~/.claude/skills/real-sfx`, Earshot `~/tools/earshot`, FFmpeg skill `~/.claude/skills/ffmpeg-skill`. Detail `AGENTS.md` mein.
