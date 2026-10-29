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
