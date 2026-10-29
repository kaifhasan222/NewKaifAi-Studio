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
