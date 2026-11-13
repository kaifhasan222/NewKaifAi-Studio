# New Kaif Ai Studio: instructions for the AI agent (Antigravity / any agent)

Project: YouTube Shorts + Instagram Reels channel "New Kaif Ai". Tech content, **Hinglish (Roman script)**, 30-60 sec, 9:16, 1080x1920.
Owner: Kaif. Uses his own photo and own recorded voice (`brand/`). Final approval hamesha Kaif ka.

## Shortcuts & Slash Commands
Jab bhi Kaif yeh shortcuts likhe, agent ko turant yeh workflow execute karna hai:
- **/start** (ya "start", "aaj ka video"): Interactive episode wizard shuru karo. Pehle Kaif se intake ke 5 sawaal poochho:
  1. **Topic:** Kaunsa topic par video banana hai? (Ya reference link/topic). Agar Kaif bole *"kuch topic nahi hai"*, *"auto kar do"*, ya *"tum decide karo"* -> internet se aaj ka trending AI/tech topic khud search karke select karo.
  2. **Motion Graphics Style:** `prompts/motion-styles.md` se (e.g. *Pop Info*, *Creator Motion Graphics*, *Clean Tech*, *Chalk Talk*, *Data Story*, *Software Walkthrough*) ya "Auto-pick".
  3. **Animation / Zoom Vibe:** Punch zoom & fast viral cuts, smooth zoom-in calm explainer, ya screen UI demo.
  4. **Audio / Voice Source:** Delivery card dekh ke phone se record (`episodes/epNNN/voice_raw.mp3`), apni awaaz ka clone (`tools/voice_indic.py`), ya brand/existing voice?
  5. **Visual Mode:** Google Flow clips ya Faceless animation.
  - Sawaal poochhne ke baad Roman Hinglish script ready karo.
- **/start auto**: Bina ruke sab kuch auto mode mein chalao: Trending AI news search karo, best motion style & zoom vibe choose karo, script aur prompts draft karke assemble karo.
- **Script Review & Revision Loop**: Script hamesha Roman Hinglish mein dikhao. Kaif se poochho: *"Script check karo. Changes chahiye ya lock karein?"* Agar Kaif changes bataye to uske mutabiq update karo; jab Kaif "Approved" ya "OK" bole tabhi production par aage badho.
- **/content** (ya **/publish**): Current episode ka SEO publishing pack generate karo (`episodes/epNNN/publish.md`): 3 high-CTR viral titles, YouTube description, tags, hashtags, pinned comment, aur Instagram Reels caption (copy-paste block format mein).
- **/edit**: Current episode ko rebuild karo `py -3.12 tools\build_video.py episodes\epNNN\episode.json` se (captions, music ducking, ya sfx adjustments ke baad).
- **/status**: Bataye current episode kaunsa hai aur kis step par hai (Script, Audio, Flow Prompts, Captions, Build, QA, Publish).

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
- Clone: hamesha `--takes 3`. Tool har take ko khud tez karta hai (tez 195 / normal 180 / dheema 160 shabd/min, aur tez `--speed 1.1`). Baad mein `tools/voice_report.py`: flat ho to script ka josh badlo ya naya take. Target `prompts/voice-delivery.md` -> "Clone kaisa hona chahiye".
- Har scene ke `Delivery:` mein `tez|normal|dheema, josh 1-5, zor "शब्द", ruk <sec>` aur alag `Action:` (body language). Josh upar-neeche ho. Detail `prompts/voice-delivery.md`.
- Awaaz: Kaif ki recording par `py -3.12 tools\voice_report.py`, phir `py -3.12 tools\polish_voice.py`. Clone chahiye to `.venv-indic/bin/python tools/voice_indic.py episodes/epNNN/script.md --takes 2` (IndicF5), reference sirf Kaif ki awaaz (`brand/refs/` ya `brand/voice_ref.wav` + `.txt`). Flow ki `@me` awaaz rakhni ho to `py -3.12 tools\flow_voice.py episodes\epNNN\episode.json` (lip-sync same).
- Kaif ka raw camera video `episodes/epNNN/raw-clips/` mein ho to `tools/cut_silence.py episodes/epNNN/episode.json --takes --fillers --dry-run` (faster-whisper wala python): best take, galat shuruaat, aa/umm kata. `cut_report.txt` Kaif ko dikhao, phir bina `--dry-run`, phir `tools/flow_voice.py`.
- Flow prompts: `prompts/flow-prompt-template.md` ke format mein, har scene alag. `@me` scene ke `Action:` mein script ka action aur josh.
- Edit: `py -3.12 tools\build_video.py episodes\epNNN\episode.json` (Kaif ke Windows PC par `py -3.12 tools\...` use karo kyunki `python` purana 3.8 hai; Mac par `python3`). Naya edit code mat likho jab tak tool ki kami na ho.
- Captions: `tools\make_captions.py`, phir text Roman Hinglish mein badlo, timings waise hi rakho.
- QA: `tools\check_video.py`, contact sheet dekho, dikkat likho (kata hua text, black frames, awaaz/music balance).
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
Kaif se Hinglish mein (Roman script), seedhi aur chhoti baat karo. Har episode ke baad: kya bana, kya assume kiya, kya check karna hai.

## Kaif ka setup (Windows)
- Project folder: `F:\Video_generator_NewKaifAi_studio`. ffmpeg, node, faster-whisper installed. Python: `py -3.12`.
- `brand/photo.jpg` aur `brand/voice.mp3` maujood hain. `assets/` mein original (synthesized) music + sfx hain.
- Kaam shuru karne se pehle `py -3.12 tools\setup_check.py` chalao.
- Koi bhi install ya delete se pehle Kaif se puchho.

## Git
- Remote: `https://github.com/kaifhasan222/NewKaifAi-Studio.git` (personal). Office GitHub `kaifhasan1234` par commit ya push nahi.
- Commit author hamesha personal: `kaifhasan222 <kaifhasan222@gmail.com>`. Is repo ka local git author yahi hai. Mac ka global git (`kaif@roopya.com`) mat badlo, aur us email se is repo mein commit mat karo. Push se pehle `gh auth status` mein account `kaifhasan222` hona chahiye.
- Git mein nahi: episode folders (`episodes/epNNN/`), raw clips, final videos, koi bhi `.mp4` / `.mov` / `.webm`.
- Git mein theek: code, prompts, `episodes/_template/`, `brand/photo.jpg`, `brand/voice.mp3`, `assets/` ki music aur sfx (mp3), photos.
- Nayi dependency add ho to `requirements.txt` (clone ke liye `requirements-indic.txt`), `SETUP.md`, `README.md`, `CLAUDE.md` aur yeh file update karo.
- `.venv-indic/` (clone model ka venv) git mein nahi.
- Thumbnail text card: `.venv/bin/python tools/thumb_card.py episodes/epNNN/thumb_card.json` (Pillow 12.3.0, `requirements.txt`). Asli chehra (Gemini edit of `brand/photo.jpg`) + clean text, detail `prompts/thumbnail-guide.md`.

## Voice clone (local, isi repo mein)
- IndicF5 (AI4Bharat, MIT licence), Hindi. Venv `.venv-indic`, packages `requirements-indic.txt`. Model gated (Hugging Face login Kaif khud). Setup `SETUP.md` -> Voice clone. Mac GPU par ~35 sec/line, CPU par ~70.

## Sound tools (local, repo ke bahar)
Video fiki lage to yeh tools use karo. Yeh awaaz badalte nahi. Cuts par sound effects lagate hain.
- Openverse: `https://api.openverse.org/v1/audio/` (key nahi). Downloads `~/sounds`.
- Real SFX: `~/.claude/skills/real-sfx` (78 CC0 UI sounds). Library: `~/sounds`.
- Earshot: `~/tools/earshot` (Python 3.12 venv). `earshot doctor` healthy. Sunne wale models (~1.1 GB) pehli listen par download hote hain.
- FFmpeg skill: `~/.claude/skills/ffmpeg-skill` (audio balance, local).
