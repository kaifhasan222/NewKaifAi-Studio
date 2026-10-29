# New Kaif Ai Studio: instructions for Claude

Project: YouTube Shorts + Instagram Reels channel "New Kaif Ai". Tech content, **Hinglish (Roman script)**, 30-60 sec, 9:16, 1080x1920.
Owner: Kaif. Uses his own photo and own recorded voice (`brand/`). Final approval hamesha Kaif ka.

## Kaam karne ka tareeka
- Pehle `PIPELINE.md` aur `prompts/script-style-guide.md` padho.
- Naya episode: `episodes/_template/` copy karke `episodes/epNNN/` banao.
- Scripts: `prompts/script-style-guide.md` follow karo. Facts ke liye search karo, andaza mat lagao.
- Flow prompts: `prompts/flow-prompt-template.md` ke format mein, har scene alag.
- Edit: `python tools/build_video.py episodes/epNNN/episode.json` (Windows par `python`, Mac par `python3`). Naya edit code mat likho jab tak tool ki kami na ho.
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

## Output style
Kaif se Hinglish mein, seedhi aur chhoti baat karo. Har episode ke baad: kya bana, kya assume kiya, kya check karna hai.
