# Flow prompt template

Google Flow ke UI/options tumhare account ke hisaab se thode alag ho sakte hain. Yeh prompt ka *shape* hai.

## Har scene ka prompt
```
Subject: <kaun/kya, 1 line>
Action: <kya ho raha hai. @me wale scene mein script ki `Action:` line + josh, jaise "leans toward camera, points finger, raised eyebrows, energetic">
Setting: <jagah, background>
Camera: <hook = fast punch-in zoom; baaki close-up / medium / slow push-in>
Lighting & mood: <soft daylight / neon cyberpunk / clean studio>
Style: <realistic / 3D render / flat motion graphic>
Format: vertical 9:16
Duration: <3-6 sec>
Avoid: text/logos/watermarks in video, extra fingers, distorted faces
```

## Kahan banao
- Sirf Google Flow project **me** ke andar. Naya project nahi.
- Avatar ya awaaz ke liye `@me`, chehre ke liye `@me_photo`. Kaif wale har scene mein dono saath: `@me @me_photo`. Dono usi project mein add hon.
- Credit khatam ho to `newpub222@gmail.com` par switch karke wahi **me** project. Detail `.cursor/skills/google-flow/SKILL.md`.

## Body language (Kaif professional YouTuber jaisa dikhe)
Script ki `Action:` line aur `josh` se Flow ka `Action:` English mein likho:
| Josh | Flow Action words |
|---|---|
| 5 (hook) | leans toward camera, points at viewer, raised eyebrows, quick hand gesture, energetic expression |
| 3-4 (points) | counts on fingers, explains with open hands, small nod, confident smile |
| 1-2 (CTA) | relaxed posture, warm smile, slight nod, steady eye contact |

- Ek scene mein ek hi action. Haath frame ke andar rahein (extra fingers se bachne ke liye haath simple rakho).
- Hamesha "looks directly into the camera" likho, YouTuber wali eye contact.
- Flow ka audio mute hota hai, awaaz `voice.mp3` se aati hai. Isliye action utna hi lamba ho jitni line (3-6 sec).

## Consistency ke liye
- Ek `STYLE:` line har scene mein copy-paste karo (same look).
- Kaif wale har scene ka `Subject:` = upar wali `CHARACTER:` line, word-for-word:
  `@me @me_photo, same face as @me_photo, same hairstyle, same outfit: <ek outfit>, looks directly into the camera`
- Chehra apne shabdon mein describe mat karo (umar, daadhi, baal). Sirf "same face as @me_photo".
- Ek episode = ek outfit, ek STYLE, ek background family. Soft front light, close-up/medium shot, chehra dhaka na ho, frame mein sirf Kaif.
- Generate ke baad har clip ka chehra `me_photo` se milao. Na mile to dobara chalao, mismatch clip edit mein mat daalo. Detail `.cursor/skills/google-flow/SKILL.md`.
- Screen par likha text Flow se mat banwao (aksar galat aata hai); text hum edit mein overlay karte hain.

## Output format (Claude `flow-prompts.md` mein aise likhega)
```
STYLE: <ek line, sab scenes ke liye>
CHARACTER: @me @me_photo, same face as @me_photo, same hairstyle, same outfit: <outfit>, looks directly into the camera
Scene 1 (0-4s): <CHARACTER line> + <prompt>  -> file: raw-clips/epNNN_01.mp4
Scene 2 (4-9s): <CHARACTER line> + <prompt>  -> file: raw-clips/epNNN_02.mp4
```

## Background change
Pehle Flow prompt mein hi naya background likho. Ye na chale to subject alag karke (rembg) naye background par lagate hain, phir `episode.json` mein clip ki jagah wahi nayi file.
