---
name: google-flow
description: >-
  Generate New Kaif Ai clips in Google Flow. Use when making Flow videos,
  avatars, @me, @me_photo, switching Flow accounts, or when Flow credits run out.
---

# Google Flow

Kaif ka Flow pehle se login hai. Password mat bharo.

## Project

Sirf existing project **me** ke andar kaam karo. Naya project mat banao. Episode ka naam project ka naam nahi hai.

Primary project: `https://flow.google.com/project/1e11e2a3-ffc0-4a2d-ade0-6c54ca3c4e21` (account `kaifhasan222@gmail.com`). Isme `Me` avatar aur `me_photo.jpg` pehle se hain. Prompt mein chip `@Me` aur `@me_photo` lagao.

## Tags

Prompt box mein yeh tags tab likho jab kaam unpar depend kare:

- `@me` — Kaif ki **awaaz**. Clip mein Kaif bole to yeh tag.
- `@me_photo` — Kaif ka **avatar** (`me_photo.jpg`), chehra isi se banta hai.

**Jis bhi clip mein Kaif dikhe, dono tags saath likho: `@me @me_photo`.** Sirf ek tag se chehra badal sakta hai.

Dono tags project **me** mein hone chahiye. Missing hon to pehle Flow mein add karo (photo ke liye `brand/photo.jpg` upload karke naam `me_photo`), phir clip generate karo.

## Chehra har clip mein same (consistency)

1. `flow-prompts.md` ke upar ek `CHARACTER:` line likho aur har Kaif wale scene mein **word-for-word** copy karo:
   `CHARACTER: @me @me_photo, same face as @me_photo, same hairstyle, same outfit: <ek outfit, poore episode ke liye>, looks directly into the camera`
2. Chehre ko apne shabdon mein describe mat karo (umar, daadhi, baal, rang). Sirf "same face as @me_photo". Naya description chehra badal deta hai.
3. Ek episode = ek outfit, ek background family, ek `STYLE:` line. Beech mein mat badlo.
4. Lighting soft aur saamne se, chehra frame ke beech mein, close-up ya medium shot. Side profile, door ka shot, chehra dhaka (haath, mic, cap, chashma) mat maango.
5. Ek clip mein sirf Kaif. Koi doosra insaan ya bheed nahi.
6. Generate ke baad har clip ka chehra `me_photo` se milao. Na mile (alag shakal, alag baal, alag kapde) to wahi prompt dobara chalao. Mismatch clip edit mein mat daalo.
7. Dono accounts (`kaifhasan222`, `newpub222`) ke **me** project mein wahi `me_photo.jpg` aur wahi `Me` avatar ho, taaki account badalne par chehra na badle.

## Accounts

1. Jo account abhi open ho, usi **me** project se shuru karo.
2. Credit ya limit khatam dikhe to account `newpub222@gmail.com` par switch karo. Wahan bhi project **me** kholo. `@me` aur `@me_photo` wahan bhi hone chahiye. Na hon to add karo.
3. Dono accounts ke credits khatam hon, tab `prompts/faceless-mode.md`. Beech mein top-up mat karo.

## Clip

- Video, vertical 9:16.
- Generated text aur brand logos mat maango. On-screen lines edit mein overlay hain.
- Save: `raw-clips/epNNN_01.mp4`, phir `02`, `03`, usi order mein.

## Awaaz @me se (Flow wali Kaif ki awaaz)

Kaif ki awaaz `@me` mein hai. Clip mein Kaif khud bole aur wahi awaaz final video mein rahe:
1. Prompt mein bolne wali line do, script ki `Voice:` line (Devanagari) waise hi:
   `Dialogue: @me says "<Voice line>" | Tone: <josh ke hisaab se: energetic and fast / confident / calm and warm>`
2. Ek clip = ek line, 3-6 sec. Line lambi ho to do clip.
3. Download ke baad: pehle `.venv/bin/python tools/cut_silence.py episodes/epNNN/episode.json --whisper` (clip ki khamoshi video se hi kaatta hai), phir `python tools/flow_voice.py episodes/epNNN/episode.json`. Har clip ki awaaz unhi trim aur transition ke saath judti hai, lip-sync nahi tootta. Output `voice.mp3`.
4. `python tools/voice_report.py episodes/epNNN/voice.mp3` se check. Galat shabd ya flat line ho to wahi clip dobara.
5. Is awaaz par `polish_voice.py --speed` ya uski gap-cutting mat chalao, lip-sync toot jayega. Khamoshi sirf `tools/cut_silence.py` se kaato.
6. Flow policy error: "पिन डालो", "पिन डाला", "बैंक पिन चेक" jaisi lines (paise/PIN daalne ka hukm) fail hoti hain. Matlab wahi rakho, line naram karo (ep004 notes).

Flow ki awaaz na rakhni ho to clip ka audio mute rehta hai aur `voice.mp3` Kaif ki recording ya clone se aata hai (`prompts/voice-delivery.md`).
