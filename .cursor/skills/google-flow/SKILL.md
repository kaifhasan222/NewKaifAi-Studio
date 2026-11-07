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

- `@me` — Kaif ki awaaz aur avatar.
- `@me_photo` — Kaif ki photo (`me_photo.jpg`), chehra isi se banta hai.

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

- Video, vertical 9:16. Flow audio baad mein mute hota hai.
- Generated text aur brand logos mat maango. On-screen lines edit mein overlay hain.
- Save: `raw-clips/epNNN_01.mp4`, phir `02`, `03`, usi order mein.
