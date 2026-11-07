# Voice delivery: awaaz professional YouTuber jaisi

Dikkat: awaaz saaf hai par flat lagti hai. Har line ek hi zor se, ek hi sur mein, bina sochi-samjhi ruk ke.
`brand/voice.mp3` ka naap (7 Nov 2026): zor ka range 2.7 LU (flat), pitch spread 6 semitone, peak +0.3 dB (clipping).

Teen raaste hain. Teeno free hain aur isi project mein hain.

| Raasta | Kab | Tool |
|---|---|---|
| A. Khud record + polish | Roz ka default. Sabse asli lagta hai | Delivery card, `tools/polish_voice.py` |
| B. Clone awaaz | Record karne ka time na ho, ya ek line baar baar galat ho | `tools/voice_clone.py` (Chatterbox, MIT) |
| C. Mix | Zyada lines khud ki, 1-2 line clone se theek | Dono |

Teeno ke baad check: `python tools/voice_report.py <file>`. Delivery naapne ke liye RAW recording do.

## 1. Delivery card (script mein har line ke saath)
Format `[Scene N | a-bs] Voice: ... | Delivery: ... | Action: ... | Visual: ...`

`Delivery:` mein sirf yeh shabd:
- **Pace:** `tez` / `normal` / `dheema`
- **Josh 1-5:** `josh 5` hook, `josh 3-4` beech mein, `josh 2-3` CTA. Poori video ek hi number par na ho.
- **Zor:** `zor "शब्द"`: ek line mein ek hi shabd. Woh shabd thoda upar aur thoda lamba bolo, chillao mat.
- **Ruk:** `ruk 0.5`: line ke baad kitne second chup. Fact ya reveal ke baad 0.4-0.7. Hook ke baad 0.3.
- **Sur (optional):** `upar` (sawaal, hairani) / `neeche` (pakka fact, nichod).

Energy ka graph aisa ho:
```
josh 5  ■                                  
josh 4  ■     ■           ■               
josh 3  ■  ■  ■  ■     ■  ■              ■
josh 2  ■  ■  ■  ■  ■  ■  ■  ■        ■  ■
        hook  why   point1 point2 reveal  CTA
```
Hook sabse upar. Har point ke shuru mein thoda upar, fact par neeche. Reveal se pehle ek ruk. CTA dheema aur saaf.

Example:
```
[Scene 1 | 0-2s] Voice: ये कोई हैक नहीं है। | Delivery: tez, josh 5, zor "हैक", ruk 0.3 | Action: camera ki taraf jhuk ke, ungli se mana | Visual: punch zoom
[Scene 2 | 2-7s] Voice: सिग्नल जाने में थोड़ा समय लगता है, बस इतनी सी बात है। | Delivery: normal, josh 3, zor "समय", sur neeche, ruk 0.5 | Action: haath se "thoda" ka ishara | Visual: ...
[Scene 6 | 50-55s] Voice: ऐसी रोज़ की एआई टिप के लिए फॉलो करो। | Delivery: dheema, josh 2, ruk 0.2 | Action: muskura ke halka sir hilana | Visual: ...
```

## 2. Khud record karna (raasta A)
1. **Khade ho kar bolo.** Baith ke awaaz dab jaati hai.
2. **Muskura ke bolo.** Muskaan awaaz mein sunai deti hai, khaas kar hook aur CTA par.
3. **2 guna josh.** Mic aur compressor josh ko aadha kar dete hain. Jo tumhe "thoda zyada" lage, recording mein woh normal lagega.
4. **Line by line, 3 take.** Har line ke 3 take lo: ek normal, ek zyada josh wala, ek tez. Edit mein best rakhte hain.
5. **Zor wala shabd haath ke saath.** Us shabd par haath ya sir hilao. Awaaz apne aap upar jaati hai.
6. **Ruk ko gino.** `ruk 0.5` = man mein "ek". Sharmao mat, edit mein chhota ho sakta hai, bada nahi.
7. **Mic se ek baalisht door**, shaant kamra, pankha band. Clipping na ho.
8. File: `episodes/epNNN/voice_raw.mp3`.

Phir:
```
python tools/voice_report.py episodes/epNNN/voice_raw.mp3
python tools/polish_voice.py episodes/epNNN/voice_raw.mp3 episodes/epNNN/voice.mp3 --speed 1.05
```
Windows par `python` ki jagah `py -3.12`. Report "FIX" bole to woh line dobara record karo, polish josh nahi daal sakta.

## 3. Clone awaaz (raasta B)
Model: Chatterbox Multilingual (Resemble AI), Hindi bhi bolta hai, MIT licence, free aur local. Setup `SETUP.md` ke "Voice clone" mein.

1. **Reference:** apni hi 10-15 sec ki **josh wali** saaf recording `brand/voice_ref.wav` mein (music nahi, ek hi insaan). Clone wahi andaaz leta hai, isliye flat reference do to flat clone milega.
2. **Banao:**
   ```
   .venv-voice/bin/python tools/voice_clone.py episodes/epNNN/script.md --takes 3
   ```
   Windows: `.venv-voice\Scripts\python tools\voice_clone.py episodes\epNNN\script.md --takes 3`
3. **Suno** `episodes/epNNN/voice_takes/`. Har scene ka best take chuno:
   ```
   .venv-voice/bin/python tools/voice_clone.py episodes/epNNN/script.md --use 1=2,3=3
   ```
4. **Ek line dobara:** `--only 3 --takes 3`.
5. **Test ek line:** `--line "ये कोई हैक नहीं है।" --josh 5 --pace tez`.

`josh` model ke "exaggeration" knob ko badalta hai (1=0.3 ... 5=1.0). `tez/dheema` pace badalte hain. Ek shabd par zor model control nahi karta. Woh zaroori ho to woh line khud record karo (raasta C).

## Pakke rules
- Clone **sirf Kaif ki apni awaaz** ka. Kisi aur ki recording reference mein kabhi nahi, reference YouTuber ki bhi nahi.
- Reference video se sirf andaaz seekho: pace, ruk, josh ka graph. Unki awaaz, script ya lines copy nahi.
- Clone wali video upload karte waqt YouTube Studio ka "Altered or synthetic content" sawaal dhyan se padh ke Kaif khud jawab de.
- Channel par ek hi awaaz rahe: Kaif ki asli ya Kaif ka clone. Koi aur TTS voice nahi.
