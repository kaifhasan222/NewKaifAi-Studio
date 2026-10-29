# New Kaif Ai Studio: Project knowledge

---

# Brand: New Kaif Ai

Yeh file bharo, Claude har video mein isse follow karega. (TODO = tum bharo)

- **Channel:** New Kaif Ai (YouTube Shorts + Instagram Reels)
- **Content:** Tech/AI, Hinglish (Roman script)
- **Length:** 30-60 sec, 9:16
- **Tagline:** TODO
- **Tone:** TODO (jaise: dost jaisa, seedha, thoda funny, bina bakwaas)
- **Audience:** TODO (students? developers? beginners?)
- **Colors:** TODO (primary, accent, text)
- **Font (captions/titles):** TODO (`assets/fonts/` mein daalo)
- **Intro/outro line:** TODO
- **Hamesha daalo:** TODO (jaise "Follow for daily AI tips")
- **Kabhi mat daalo:** TODO

## Files jo `brand/` mein chahiye
- `photo.jpg` (clear, front-facing, achhi roshni)
- `voice.mp3` (apni awaaz, shaant jagah, mic ke paas)
- `logo.png` (optional)


---

# Script style guide (Hinglish shorts)

## Structure (30-60 sec, ~80-140 words)
1. **Hook (0-2s):** ek chhoti, dhamakedaar line. Sawaal, ajeeb fact ya "ye mat karo".
2. **Problem/Why (2-8s):** viewer ko kyun parwah honi chahiye.
3. **Meat (8-45s):** 2-4 chhote points, har point ek scene.
4. **Payoff + CTA (last 5s):** ek line ka nichod, phir follow/comment.

## Bhasha
- Roman Hinglish, bolchal wali. Chhote vaakya.
- English tech words waise hi (API, prompt, model), baaki Hindi/Urdu bolchal.
- Ek line = ek saans. Zyada lamba ho to todo.
- Jargon aaye to turant simple example.

## Hook formulas
- "Ye AI tool aapka [kaam] 10 minute mein kar dega."
- "99% log [cheez] galat use karte hain."
- "Aaj ke baad [purani cheez] ki zarurat nahi."
- "Maine [cheez] try ki, result dekho."

## Fact rules
- Har claim (naam, price, feature) search karke verify karo. Source `script.md` ke neeche likho.
- Pakka na ho to "shayad"/"abhi ke hisaab se" bolo ya point hata do.

## Script file format
```
# epNNN: <title>
Hook: ...
[Scene 1 | 0-4s] Voice: ... | Visual: ...
[Scene 2 | 4-9s] Voice: ... | Visual: ...
CTA: ...
Sources: ...
```


---

# Flow prompt template

Google Flow ke UI/options tumhare account ke hisaab se thode alag ho sakte hain. Yeh prompt ka *shape* hai.

## Har scene ka prompt
```
Subject: <kaun/kya, 1 line>
Action: <kya ho raha hai>
Setting: <jagah, background>
Camera: <close-up / medium / slow push-in / handheld / top-down>
Lighting & mood: <soft daylight / neon cyberpunk / clean studio>
Style: <realistic / 3D render / flat motion graphic>
Format: vertical 9:16
Duration: <3-6 sec>
Avoid: text/logos/watermarks in video, extra fingers, distorted faces
```

## Consistency ke liye
- Ek `STYLE:` line har scene mein copy-paste karo (same look).
- Character ho to same reference image / same description har scene mein.
- Screen par likha text Flow se mat banwao (aksar galat aata hai); text hum edit mein overlay karte hain.

## Output format (Claude `flow-prompts.md` mein aise likhega)
```
STYLE: <ek line, sab scenes ke liye>
Scene 1 (0-4s): <prompt>  -> file: raw-clips/epNNN_01.mp4
Scene 2 (4-9s): <prompt>  -> file: raw-clips/epNNN_02.mp4
```

## Background change
Pehle Flow prompt mein hi naya background likho. Ye na chale to subject alag karke (rembg) naye background par lagate hain, phir `episode.json` mein clip ki jagah wahi nayi file.


---

# Publishing guide: title, description, tags, hashtags

Har video ke liye Claude `episodes/epNNN/publish.md` banata hai (template: `episodes/_template/publish.md`). Video ki script/topic dekh ke likhta hai.

## Keyword research (har video se pehle)
- Claude web search karke dekhta hai: abhi us topic par kya trend kar raha hai, log kya search karte hain (YouTube/Google suggestions, Trends), competitors ke titles.
- **Hinglish + English dono** keywords: jaise "AI tools Hindi mein" aur "free AI tools". Indian audience dono tarah search karti hai.
- Search volume ya "viral guarantee" ka koi number banaya nahi jayega. Sirf jo search mein mila wahi.

## YouTube Shorts
- **Title:** 3 options. 40-60 characters, main keyword shuru mein, hook ke saath. Misleading clickbait nahi (video mein jo hai wahi title mein).
- **Description:** pehli 1-2 line mein keyword + hook, phir 2-3 line summary, phir CTA (follow/subscribe), end mein 3-5 hashtags. `#Shorts` daalo.
- **Hashtags:** 3-5 relevant. YouTube par 15 se zyada ho jayein to sab ignore ho sakte hain.
- **Tags (backend):** 8-12 keywords (Hinglish + English). Asar kam hota hai, par daalne mein dikkat nahi.
- **Pinned comment:** ek sawaal jo comments laye ("Aapko kaun sa tool chahiye?").

## Instagram Reels
- **On-screen cover text:** 3-5 shabd.
- **Caption:** pehli line hook (keyword ke saath), 2-3 line value, last mein CTA.
- **Hashtags:** 5-10 mix: 2 broad (#tech #ai), 3-4 niche (#aitoolshindi), 1-2 apne brand ke (#newkaifai).
- Caption mein hi keywords likho (search/discovery ke liye).

## Rules
- Hashtag sirf relevant. Unrelated trending hashtag mat chipkao.
- Title/thumbnail ka claim video mein poora hona chahiye.
- Agar video mein realistic AI-generated person/scene hai to YouTube/Instagram ka AI-content label option check karo aur zarurat ho to on karo.
- Claims (price, feature) verify karo, source `publish.md` ke neeche.

## Output format
Dekho `episodes/_template/publish.md`.


---

# Faceless mode (jab Google Flow ka limit khatam ho jaye)

Flow ke bina bhi video banega: **animation + awaaz + sound design**, bina chehre ke. Edit tool (`build_video.py`) wahi rehta hai, sirf clips ka source badalta hai.

## Kab switch karna hai
- Flow credits/limit khatam, ya
- Topic aisa hai jisme AI video ki jagah animation/screen demo behtar dikhega (tools, code, charts, steps).

## Visuals ke sources (priority order)
1. **Motion graphics scenes:** animated text (kinetic typography), step cards, charts, counters, UI mockups, typing code animation. Remotion (React, tum jaante ho) ya HyperFrames se clip render karo (`templates/motion-graphics/README.md`).
2. **Screen recordings:** tool ka asli demo (tech channel ke liye sabse trust wala). Tum record karo, Claude trim/zoom/caption karta hai.
3. **Free stock b-roll:** Pexels/Pixabay/Mixkit (`assets/ASSETS.md`, licence check).
4. **Still images + slow zoom (Ken Burns):** tumhare banaye ya free licence ke images.

## Awaaz
- Pehli pasand: **tumhari apni awaaz** (`voice.mp3`), brand consistent rehta hai.
- Agar roz record nahi kar sakte: free TTS (jaise edge-tts, unofficial hai, kabhi band ho sakta hai) ya koi aur tool. Quality aur terms pehle check karo, aur channel par ek hi voice rakho.

## Sound design (faceless mein aur zaroori)
- Har scene change par halka whoosh/swipe.
- Text aane par pop/click. Reveal se pehle riser, reveal par hit.
- Background music voice ke neeche (~0.12, auto-ducking, tool karta hai).
- Silence ka bhi use: hook ke baad 0.3s ruk kar.

## Pace (retention)
- Har 2-4 sec par kuch badle (scene, zoom, text).
- Pehle 2 sec mein bada hook text + voice.
- Captions bade, 3-4 shabd ek baar mein.
- Ek scene = ek point.

## Faceless episode ka flow
1. Script (same style guide) + scene list: har scene ke saath visual type likho (motion / screen / stock / still).
2. Motion scenes render -> `raw-clips/epNNN_NN.mp4`; screen recordings aur stock bhi wahin.
3. `episode.json` mein clips, voice, music, sfx, captions, overlays.
4. `build_video.py`, phir `check_video.py`.
5. `publish.md` banao.

## Abhi kya ready hai, kya nahi
Ready: assemble, transitions, captions, overlays, music/sfx mix, QA.
Abhi nahi bana: Remotion starter project (animated scenes ke templates). Ye faceless mode ka agla step hai, jab chaho tab banate hain.


---

# Topic + reference video -> uske style mein apna video

Tum Claude ko do cheezein doge: **(1) topic**, **(2) reference video** (jis style mein banana hai). Claude style samjhega aur **tumhare topic ka original video** banayega.

## Rule: style lo, content nahi
Copy hoga: structure, pace, hook ka tareeka, text style, sound design ka andaaz, color mood.
Copy nahi hoga: unka script, footage, music, voice, logo, edits frame-by-frame. Sab kuch apna aur original.

## Reference kaise doge
- **Best:** video file `references/` folder mein daalo (khud record ki hui ya jo tumhe use karne ka haq ho). Claude tool se frames, cuts, loudness, transcript nikalta hai.
- **Sirf link:** Claude YouTube/Instagram video download nahi karta aur video dekh nahi sakta. Link se title/description/transcript padh sakta hai (jahan available), ya tum 3-5 screenshots + 2 line description do.

## Steps
1. `python tools/analyze_reference.py references/<file>.mp4` (frames.jpg, stats.json, audio.wav).
2. Transcript: `python tools/make_captions.py references/<file>_analysis/audio.wav references/<file>_analysis/transcript.srt`
3. Claude `frames.jpg` dekh ke aur stats padh ke **style-card** banata hai: `references/<naam>_style-card.md` (neeche ka format).
4. Tum style-card dekh ke bologe: "theek hai" ya kya badalna hai.
5. Claude tumhare topic par **naya script** likhta hai us structure mein.
6. Mode chuno: **Flow** (AI clips) ya **Faceless** (`prompts/faceless-mode.md`).
7. Build -> QA -> `publish.md`. Tum approve karke post karte ho.

## Style-card format
```
# Style card: <reference naam>
- Length / format:
- Hook (pehle 2s): kya hota hai, kaisa text/awaaz
- Structure: hook -> ... -> CTA (second ke saath)
- Pace: average shot length, kitne cuts, zoom/motion kab
- Visuals: type (AI video / animation / screen / stock), color mood, camera feel
- Text on screen: font style, size, position, animation, kab aata hai
- Captions: style, kitne shabd ek saath, highlight
- Audio: voice ka tone/speed, music mood, volume, sfx kab (whoosh/pop/riser)
- Transitions: type aur kitni baar
- Jo hum apnayenge: ...
- Jo hum apna banayenge (copy nahi): ...
```

## Note
Sirf cuts ki ginti pe bharosa mat karo: crossfade/dissolve cuts ke roop mein detect nahi hote. Frames dekhna zaroori hai.


---

# Daily pipeline: 1 short, kam se kam kaam

## Do tareeke se shuru kar sakte ho
- **Sirf topic:** "daily-short chalao, topic: ..." -> neeche ka flow.
- **Topic + reference video:** "is reference ke style mein banao" -> pehle `prompts/reference-style-workflow.md` (style-card), phir neeche ka flow.

## Do modes
- **Flow mode:** visuals Google Flow ke AI clips se.
- **Faceless mode:** Flow ka limit khatam ho to animation + awaaz + sound design (`prompts/faceless-mode.md`). Step 3 mein clips ka source badalta hai, baaki sab same.

| # | Step | Kaun | Tool | Output |
|---|---|---|---|---|
| 1 | Topic aur script (Hinglish, 30-60s) | Claude | `prompts/script-style-guide.md` | `episodes/epNNN/script.md` |
| 2 | Scene-wise Flow prompts | Claude | `prompts/flow-prompt-template.md` | `episodes/epNNN/flow-prompts.md` |
| 3 | Clips generate karna | Claude in Chrome ya tum | Google Flow | `raw-clips/epNNN_*.mp4` |
| 4 | Apni awaaz | Tum (ya existing voice mp3) | Phone/mic | `brand/voice.mp3` ya `episodes/epNNN/voice.mp3` |
| 5 | Captions | Claude | `make_captions.py` + Roman Hinglish cleanup | `episodes/epNNN/captions.srt` |
| 6 | Music/sfx chunna | Claude | `assets/` | `episode.json` mein entries |
| 7 | Assemble | Claude | `build_video.py` | `output/epNNN.mp4` |
| 8 | QA | Claude, phir tum | `check_video.py` | contact sheet + report |
| 9 | Title, description, tags, hashtags | Claude | `prompts/publishing-guide.md` | `episodes/epNNN/publish.md` |
| 10 | Approve, post | Tum | YouTube Shorts / Reels | Live |

## Rules
- **Hook pehle 2 second mein.** Overlay text + voice dono.
- Flow clips chhote rakho (3-6 sec ke scenes), edit mein jodte hain.
- Flow ka apna audio ho to use mute karte hain; voice aur music hum controlled mix karte hain.
- Music voice ke neeche (volume ~0.12, auto-ducking). SFX sirf transitions/emphasis par.
- Final loudness about -16 LUFS.
- **Tum hamesha final video dekhte ho.** Claude frames se check karta hai, par insaani nazar zaroori hai.

## Usage bachane ke tareeke (Claude Pro limit)
- Edit templates aur scripts se hota hai, Claude har baar naya code nahi likhta.
- Ek baar mein 3-5 episodes ke scripts + Flow prompts banwa lo (batch).
- Heavy browser automation kam karo; prompts batch mein paste karna sasta padta hai.
- Chat, Claude Code aur Cowork ek hi usage pool share karte hain.

## Phase plan
1. **Hafta 1:** 1 episode haath se poora (setup, test, templates thik karna).
2. **Hafta 2:** Batch scripts + prompts, edit script se.
3. **Hafta 3+:** Daily skill (`daily-short`) se ek-command flow.
4. **Baad mein (optional):** Remotion/HyperFrames motion graphics, background removal (rembg), thumbnails.

