# New Kaif Ai Studio: instructions for the AI agent (Antigravity / any agent)

Project: YouTube Shorts + Instagram Reels channel "New Kaif Ai". Tech content, **Hinglish (Roman script)**, 30-60 sec, 9:16, 1080x1920.
Owner: Kaif. Uses his own photo and own recorded voice (`brand/`). Final approval hamesha Kaif ka.

## Kaam karne ka tareeka
- Pehle `PIPELINE.md` aur `prompts/script-style-guide.md` padho.
- Naya episode: `episodes/_template/` copy karke `episodes/epNNN/` banao.
- Script se pehle motion style poochho (`prompts/motion-styles.md`, source [nafay3d.com](https://nafay3d.com)). Kaif "Pop Info" jaise naam bole to wahi look. "Jo achha ho" bole to tum style chuno, naam likho, phir banao. Unka prompt, music, ya voice copy mat karo.
- Scripts: `prompts/script-style-guide.md` follow karo. Facts ke liye search karo, andaza mat lagao.
- Flow prompts: `prompts/flow-prompt-template.md` ke format mein, har scene alag.
- Edit: `python tools/build_video.py episodes/epNNN/episode.json` (Kaif ke Windows PC par `py -3.12 tools\...` use karo kyunki `python` purana 3.8 hai; Mac par `python3`). Naya edit code mat likho jab tak tool ki kami na ho.
- Captions: `tools/make_captions.py`, phir text Roman Hinglish mein badlo, timings waise hi rakho.
- QA: `tools/check_video.py`, contact sheet dekho, dikkat likho (kata hua text, black frames, awaaz/music balance).
- Har episode ke saath `publish.md` banao (title options, description, tags, hashtags, Instagram caption) `prompts/publishing-guide.md` ke hisaab se, keywords web search se.
- Flow limit khatam ho ya topic animation ke layak ho to `prompts/faceless-mode.md` follow karo.
- Agar Kaif topic + reference video de: `prompts/reference-style-workflow.md` follow karo. Style-card banao, Kaif se confirm karo, phir original video banao. Reference ka script/footage/music/voice kabhi copy mat karo.
- Music/sfx sirf `assets/` se, jinka licence `assets/ASSETS.md` ke hisaab se theek ho. Naya asset daalo to uska source aur licence `assets/LICENSES.md` mein likho.

## Mat karo
- Kaif ki awaaz ya chehra kisi aur ke saath na milao, na kisi aur ka misuse.
- Copyrighted music, clips ya logos use mat karo.
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
- Nayi dependency add ho to `requirements.txt`, `SETUP.md`, `README.md` aur yeh file update karo.

## Sound tools (local, repo ke bahar)
Video fiki lage to yeh tools use karo. Yeh awaaz badalte nahi. Cuts par sound effects lagate hain.
- Openverse: `https://api.openverse.org/v1/audio/` (key nahi). Downloads `~/sounds`.
- Real SFX: `~/.claude/skills/real-sfx` (78 CC0 UI sounds). Library: `~/sounds`.
- Earshot: `~/tools/earshot` (Python 3.12 venv). `earshot doctor` healthy. Sunne wale models (~1.1 GB) pehli listen par download hote hain.
- FFmpeg skill: `~/.claude/skills/ffmpeg-skill` (audio balance, local).
