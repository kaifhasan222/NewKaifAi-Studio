# New Kaif Ai Studio: instructions for Claude

Project: YouTube Shorts + Instagram Reels channel "New Kaif Ai". Tech content, **Hinglish (Roman script)**, 30-60 sec, 9:16, 1080x1920.
Owner: Kaif. Uses his own photo and own recorded voice (`brand/`). Final approval hamesha Kaif ka.

## Kaam karne ka tareeka
- Pehle `PIPELINE.md` aur `prompts/script-style-guide.md` padho.
- Naya episode: `episodes/_template/` copy karke `episodes/epNNN/` banao.
- Script se pehle motion style poochho (`prompts/motion-styles.md`, source [nafay3d.com](https://nafay3d.com)). Kaif "Pop Info" jaise naam bole to wahi look. "Jo achha ho" bole to tum style chuno, naam likho, phir banao. Unka prompt, music, ya voice copy mat karo.
- Scripts: `prompts/script-style-guide.md` follow karo. Facts ke liye search karo, andaza mat lagao. `Voice:` line seedhi Devanagari ho. `Delivery:` alag (tez, zor, ruk). Reaction filler mat likho (`Aree`, `Achaa`, `Dekho`). Vowel mat kheench.
- Hook: script se pehle `prompts/hook-guide.md` padho. 3 hook alag type ke likho, checklist par jaancho, ek chuno, `script.md` mein `Hook type:` aur `Hook options:` likho. Pehli line 10 shabd se kam, asli baat pehle 3 second mein, Scene 2 mein intro nahi. Pichhle 2 episode wala type dobara nahi.
- Script aasaan aur funny: `prompts/script-fun-simple.md`. Har line bachcha samjhe (pehle desi misaal, phir tech naam), 60 sec mein 2-3 halki hansi (hook/warning mein nahi, fact galat na ho), josh 2-5 upar-neeche. `script.md` mein `Seedhi baat:`, `Misaal:`, `Hansi:`.
- Ending: aakhri boli hui line topic par ek comment sawaal ho (viewer ki raay/POV, jawab 1-3 shabd mein). "Follow/like/subscribe karo" awaaz mein nahi, sirf end animation mein. Detail `prompts/script-style-guide.md` -> Ending.
- Sound: `prompts/sound-design.md` padho. 3 parat SFX animation se sync (detail pop/click, zor wale hit, aur har hansi par ek meme/viral sound), 60 sec mein 50-70. Whoosh/glitch/typing/riser/faaah/shocked nahi. Music `lofi-upbeat-raspberrymusic.mp3` 0.10 par (credit description mein). Awaaz ki khamoshi kati ho (0.35s se lambi chup nahi). Deliver se pehle earshot se takes aur final mix ka noise check.
- Visuals: `prompts/visual-assets.md`. Text ki jagah icon aur image: app ka naam = app ka icon (`assets/graphics/icons/`), kirdaar = Gemini se bana original cartoon (`assets/graphics/characters/`). Har scene mein kam se kam ek, aur har image hilti rahe (bob/wiggle/float). Asli insaan ki photo nahi (sirf Kaif ki).
- Clone: `.venv-indic/bin/python tools/voice_indic.py episodes/epNNN/script.md --takes 2` (IndicF5). Har take Whisper se sun ke best khud chunta hai, milan 0.85 se kam par DHYAN. Josh reference se aata hai (`brand/refs/`, `brand/refs/RECORD.md`), na ho to `brand/voice_ref.wav`. Galat shabd ko `SPOKEN` list mein bolchaal jaisa likho. Baad mein `tools/voice_report.py`. Target `prompts/voice-delivery.md` -> "Clone kaisa hona chahiye".
- Har scene ke `Delivery:` mein `tez|normal|dheema, josh 1-5, zor "शब्द", ruk <sec>` aur alag `Action:` (body language). Josh upar-neeche ho. Detail `prompts/voice-delivery.md`.
- Awaaz: Kaif ki recording par `tools/voice_report.py`, phir `tools/polish_voice.py`. Clone chahiye to `tools/voice_indic.py` (`.venv-indic` ke python se), reference sirf Kaif ki awaaz: `brand/refs/` (josh wali, Kaif ki recording) ya `brand/voice_ref.wav` + `.txt` (Gemini videos wali). Flow ki `@me` awaaz rakhni ho to pehle `.venv/bin/python tools/cut_silence.py episodes/epNNN/episode.json --whisper` (khamoshi wale hisse video se hi kaat ke jump cuts, lip-sync same), phir `tools/flow_voice.py episodes/epNNN/episode.json`.
- Kaif ka apna raw video (camera/phone): `episodes/epNNN/raw-clips/epNNN_01.mp4`... mein. Phir `.venv/bin/python tools/cut_silence.py episodes/epNNN/episode.json --takes --fillers --dry-run`: har line ka best take (script se milake, barabar ho to aakhri), galat shuruaat, "aa/umm" aur atka shabd katte hain. `cut_report.txt` Kaif ko dikhao, galat ho to clip par `"keep"`/`"cuts"`, phir bina `--dry-run`, phir `tools/flow_voice.py`.
- Flow prompts: `prompts/flow-prompt-template.md` ke format mein, har scene alag. `@me` scene ke `Action:` mein script ka action aur josh.
- Edit: `python tools/build_video.py episodes/epNNN/episode.json` (Windows par `python`, Mac par `python3`). Naya edit code mat likho jab tak tool ki kami na ho.
- Captions: `tools/make_captions.py`, phir text Roman Hinglish mein badlo, timings waise hi rakho.
- QA: `tools/check_video.py`, contact sheet dekho, dikkat likho (kata hua text, black frames, awaaz/music balance).
- Thumbnail: `prompts/thumbnail-guide.md`, `tools/make_thumbnail.py episodes/epNNN/thumb.json` se 3 options (A/B/C), Kaif chunta hai. Clean asli-chehra style: `.venv/bin/python tools/thumb_card.py episodes/epNNN/thumb_card.json` (Pillow).
- Har episode ke saath `publish.md` banao (title options, description, tags, hashtags, Instagram caption) `prompts/publishing-guide.md` ke hisaab se, keywords web search se.
- Post ka time: roz subah 8:30 AM aur shaam 5:30 PM IST (YouTube, aur IG/FB par bhi). Detail `prompts/publishing-guide.md` -> "Post ka time".
- Flow clips sirf project **me** mein. Awaaz ke liye `@me`, avatar (chehra) ke liye `@me_photo`; Kaif wale har clip mein dono saath, aur `flow-prompts.md` ki `CHARACTER:` line word-for-word taaki chehra har clip mein same rahe. Generate ke baad chehra `me_photo` se milao, na mile to dobara. Credit khatam ho to `newpub222@gmail.com` par switch karke wahi **me** project. Dono accounts khatam hon tab `prompts/faceless-mode.md`. Detail `.cursor/skills/google-flow/SKILL.md`. Login/password mat bharo.
- Agar Kaif topic + reference video de: `prompts/reference-style-workflow.md` follow karo. Style-card banao, Kaif se confirm karo, phir original video banao. Reference ka script/footage/music/voice kabhi copy mat karo.
- Music/sfx sirf `assets/` se, jinka licence `assets/ASSETS.md` ke hisaab se theek ho. Naya asset daalo to uska source aur licence `assets/LICENSES.md` mein likho.

## Mat karo
- Kaif ki awaaz ya chehra kisi aur ke saath na milao, na kisi aur ka misuse.
- Kisi aur ki awaaz clone mat karo (reference YouTuber ki bhi nahi). Clone reference sirf `brand/voice_ref.wav`.
- Copyrighted music ya clips use mat karo. Logo: sirf us app ka icon jiski video mein baat ho rahi hai, pehchan ke liye (`prompts/visual-assets.md`). Sarkari chinh aur kisi aur brand ka logo nahi.
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
- IndicF5 (AI4Bharat, MIT, Hindi), venv `.venv-indic/` (git mein nahi), packages `requirements-indic.txt`. Model gated: Hugging Face login Kaif khud karta hai. Setup `SETUP.md` -> Voice clone. Chatterbox (`tools/voice_clone.py`) 12 Nov 2026 ko hataya, uske sirf helper functions use hote hain.

## Sound tools (local, repo ke bahar)
- Openverse API (no key), Real SFX `~/.claude/skills/real-sfx`, Earshot `~/tools/earshot`, FFmpeg skill `~/.claude/skills/ffmpeg-skill`. Detail `AGENTS.md` mein.
