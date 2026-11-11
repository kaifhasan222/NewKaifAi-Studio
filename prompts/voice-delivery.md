# Voice delivery: awaaz professional YouTuber jaisi

Dikkat: awaaz saaf hai par flat lagti hai. Har line ek hi zor se, ek hi sur mein, bina sochi-samjhi ruk ke.
`brand/voice.mp3` ka naap (7 Nov 2026): zor ka range 2.7 LU (flat), pitch spread 6 semitone, peak +0.3 dB (clipping).

Chaar raaste hain. Sab free hain aur isi project mein hain.

| Raasta | Kab | Tool |
|---|---|---|
| A. Khud record + polish | Roz ka default. Sabse asli lagta hai | Delivery card, `tools/polish_voice.py` |
| B. Clone awaaz | Record karne ka time na ho, ya ek line baar baar galat ho | `tools/voice_clone.py` (Chatterbox, MIT) |
| C. Mix | Zyada lines khud ki, 1-2 line clone se theek | Dono |
| D. Flow `@me` | Clip mein Kaif khud bole, Flow wali awaaz hi rakhni ho | `Dialogue:` Flow prompt mein, `tools/flow_voice.py` |

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
Hook sabse upar. Har point ke shuru mein thoda upar, fact par neeche. Reveal se pehle ek ruk. Aakhri line comment sawaal ho, saaf aur sur upar. Follow/subscribe bola nahi jaata, animation mein dikhta hai.

Example:
```
[Scene 1 | 0-2s] Voice: ये कोई हैक नहीं है। | Delivery: tez, josh 5, zor "हैक", ruk 0.3 | Action: camera ki taraf jhuk ke, ungli se mana | Visual: punch zoom
[Scene 2 | 2-7s] Voice: सिग्नल जाने में थोड़ा समय लगता है, बस इतनी सी बात है। | Delivery: normal, josh 3, zor "समय", sur neeche, ruk 0.5 | Action: haath se "thoda" ka ishara | Visual: ...
[Scene 6 | 50-55s] Voice: तुम्हारे साथ कभी ऐसा हुआ है? कमेंट में बताओ। | Delivery: normal, josh 3, sur upar, ruk 0.2 | Action: muskura ke camera ki taraf ishara | Visual: ...
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

`josh` model ke "exaggeration" knob ko badalta hai (1=0.3 ... 5=0.9). `tez/dheema` pace badalte hain. Ek shabd par zor model control nahi karta. Woh zaroori ho to woh line khud record karo (raasta C).

### Clone kaisa hona chahiye (audit 11 Nov 2026)
Naap (ep012, ep013): clone **~153 shabd/min** bol raha tha, Shorts ke liye dheema. Zor ka range 1.7 LU aur pitch spread 5.9 st, yaani flat. Wajah teen thi: speed-up nahi tha, lagbhag har line `normal, josh 4` thi, aur `brand/voice_ref.wav` khud flat hai (zor ka range 2.8 LU).

Achha clone in 5 par pass ho:
| Cheez | Target | Kaise |
|---|---|---|
| Raftaar | tez 195, normal 180, dheema 160 shabd/min | Tool ab har take naap ke khud tez karta hai (pitch same). Aur tez: `--speed 1.1`. Purana tareeka: `--no-auto-speed` |
| Utaar-chadhaav | Pitch spread 7 st+, zor ka range 4 LU+ (`tools/voice_report.py`) | Script mein josh 2 se 5 tak sab ho, lagataar 3 line ek josh par nahi. Sawaal aur chhoti line likho |
| Kaif jaisa lage | Sun ke lage Kaif hi bol raha hai, robot nahi | Reference Hindi mein ho (language match), 10-15 sec, saaf, **josh wali**. Flat reference = flat clone |
| Saaf shabd | Koi extra shabd ya bakwaas tail nahi | `DHYAN:` wali line suno, `--only N --takes 3` se naya take |
| Har line ka best take | 3 take mein se sabse zinda | Hamesha `--takes 3`, phir `--use scene=take` |

**Sabse bada farq naye reference se aayega.** Kaif 12-15 sec ki nayi recording de (khade ho kar, muskura ke, 2 guna josh, ek sawaal + ek hairani + ek pakka fact), `brand/voice_ref.wav` mein. Bolne ke liye:
> क्या तुम्हें पता है, तुम्हारा फ़ोन रात को सोता नहीं? सच में! वो चुपके से चालीस ऐप से बातें करता है। और बैटरी? सुबह तक आधी। आज इसका पक्का इलाज बताता हूँ।

Model ke knob (Chatterbox docs): exaggeration 0.5 default, zyada josh ke liye 0.7+ aur cfg_weight ~0.3; temperature 0.8 default. Tool mein yeh `josh` aur pace se set hote hain.

Hansi wali line: usse pehle `ruk 0.4`, line `dheema, josh 2` (deadpan), agli line phir `tez`. Detail `prompts/script-fun-simple.md`.

## 4. Flow `@me` awaaz (raasta D)
`@me` mein Kaif ki awaaz hai, `@me_photo` mein avatar.
1. Flow prompt: `Dialogue: @me says "<Voice line>" | Tone: energetic and fast` (josh 5), `confident` (josh 3-4), `calm and warm` (josh 1-2). Saath mein `CHARACTER:` line (`@me @me_photo ...`).
2. Ek clip = ek line.
3. `python tools/flow_voice.py episodes/epNNN/episode.json` -> `voice.mp3`, har clip ki awaaz unhi trim/transition ke saath, lip-sync same.
4. `python tools/voice_report.py episodes/epNNN/voice.mp3`. Galat shabd ya flat ho to wahi clip dobara Flow mein.
5. Is awaaz par `polish_voice.py --speed` ya khamoshi katna nahi (lip-sync toot jayega). `flow_voice.py` khud EQ aur loudness karta hai.

## Pakke rules
- Clone **sirf Kaif ki apni awaaz** ka. Kisi aur ki recording reference mein kabhi nahi, reference YouTuber ki bhi nahi.
- Reference video se sirf andaaz seekho: pace, ruk, josh ka graph. Unki awaaz, script ya lines copy nahi.
- Clone wali video upload karte waqt YouTube Studio ka "Altered or synthetic content" sawaal dhyan se padh ke Kaif khud jawab de.
- Channel par ek hi awaaz rahe: Kaif ki asli ya Kaif ka clone. Koi aur TTS voice nahi.
