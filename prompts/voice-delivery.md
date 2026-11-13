# Voice delivery: awaaz professional YouTuber jaisi

Dikkat: awaaz saaf hai par flat lagti hai. Har line ek hi zor se, ek hi sur mein, bina sochi-samjhi ruk ke.
Awaaz ka reference: 11 Nov 2026 se `brand/voice.mp3` (30 sec) aur clone ka reference `brand/voice_ref.wav` (10 sec, Hindi, josh wali) Kaif ke 3 Gemini videos ki awaaz se bane hain. Purani voice.mp3 git history mein hai (commit 09743b4). Naap: zor ka range 4.8 LU, pitch spread 8.9 semitone, yaani pehle (2.7 LU, 6 st) se zyada utaar-chadhaav.

Chaar raaste hain. Sab free hain aur isi project mein hain.

| Raasta | Kab | Tool |
|---|---|---|
| A. Khud record + polish | Roz ka default. Sabse asli lagta hai | Delivery card, `tools/polish_voice.py` |
| B. Clone awaaz | Record karne ka time na ho, ya ek line baar baar galat ho | `tools/voice_indic.py` (IndicF5, MIT) |
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
Model: IndicF5 (AI4Bharat), Hindi ke liye bana, MIT licence, free aur local. 12 Nov 2026 se Chatterbox ki jagah: Chatterbox 70 sec mein ~15 shabd galat bolta tha ("बंद" -> "बन", "तंदूर" -> "तंदूल") aur x1.35 speed-up se awaaz phone call jaisi dabti thi. Setup `SETUP.md` ke "Voice clone" mein.

1. **Reference (josh yahin se aata hai):** IndicF5 mein josh ka knob nahi, reference jaisa andaaz. Har josh ki Kaif ki recording `brand/refs/` mein (josh5, josh4, josh3, josh2, sawaal; text aur tareeka `brand/refs/RECORD.md`). Jo na ho uski jagah `brand/voice_ref.wav` + `brand/voice_ref.txt` (Gemini wali, sapaat). Reference ka text shabd-ba-shabd sahi ho, warna clone bigadta hai.
2. **Banao:** `.venv-indic/bin/python tools/voice_indic.py episodes/epNNN/script.md --takes 2`. Har take Whisper se suna jaata hai, script se sabse zyada milne wala chuna jaata hai (`voice_takes_indic/_scores.json`).
3. **Suno**, galat take ho to `--use 3=2,5=1`.
4. **Ek line dobara:** `--only 3 --seed 7`.
5. **Galat shabd:** tool ki `SPOKEN` list mein bolchaal wali spelling jodo (jaise "ऐप्स" -> "एप्स", warna "आप" bolta hai).
6. **Test ek line:** `--line "फ़ोन है, कुल्फ़ी नहीं।" --josh 2`.

Pace: model ki apni speed (tez 1.12 / normal 1.05 / dheema 0.95), phir halka atempo max x1.12.

### Clone kaisa hona chahiye (audit 11 Nov 2026)
Naap (ep012, ep013): clone **~153 shabd/min** bol raha tha, Shorts ke liye dheema. Zor ka range 1.7 LU aur pitch spread 5.9 st, yaani flat. Wajah teen thi: speed-up nahi tha, lagbhag har line `normal, josh 4` thi, aur `brand/voice_ref.wav` khud flat hai (zor ka range 2.8 LU).

Achha clone in 5 par pass ho:
| Cheez | Target | Kaise |
|---|---|---|
| Raftaar | tez 195, normal 180, dheema 160 shabd/min | Tool ab har take naap ke khud tez karta hai (pitch same). Aur tez: `--speed 1.1`. Purana tareeka: `--no-auto-speed` |
| Utaar-chadhaav | Pitch spread 7 st+, zor ka range 4 LU+ (`tools/voice_report.py`) | Script mein josh 2 se 5 tak sab ho, lagataar 3 line ek josh par nahi. Sawaal aur chhoti line likho |
| Kaif jaisa lage | Sun ke lage Kaif hi bol raha hai, robot nahi | Reference Hindi mein ho (language match), 10-15 sec, saaf, **josh wali**. Flat reference = flat clone |
| Saaf shabd | Koi extra shabd ya bakwaas tail nahi | `DHYAN:` wali line suno, `--only N --takes 3` se naya take |
| Har line ka best take | Takes mein se sabse saaf aur zinda | `--takes 2` (Whisper best chunta hai), sun ke `--use scene=take` |

**Sabse bada farq naye reference se aayega.** Kaif 12-15 sec ki nayi recording de (khade ho kar, muskura ke, 2 guna josh, ek sawaal + ek hairani + ek pakka fact), `brand/voice_ref.wav` mein. Bolne ke liye:
> क्या तुम्हें पता है, तुम्हारा फ़ोन रात को सोता नहीं? सच में! वो चुपके से चालीस ऐप से बातें करता है। और बैटरी? सुबह तक आधी। आज इसका पक्का इलाज बताता हूँ।


Hansi wali line: usse pehle `ruk 0.4`, line `dheema, josh 2` (deadpan), agli line phir `tez`. Detail `prompts/script-fun-simple.md`.

## 4. Flow `@me` awaaz (raasta D)
`@me` mein Kaif ki awaaz hai, `@me_photo` mein avatar.
1. Flow prompt: `Dialogue: @me says "<Voice line>" | Tone: energetic and fast` (josh 5), `confident` (josh 3-4), `calm and warm` (josh 1-2). Saath mein `CHARACTER:` line (`@me @me_photo ...`).
2. Ek clip = ek line.
3. `python tools/flow_voice.py episodes/epNNN/episode.json` -> `voice.mp3`, har clip ki awaaz unhi trim/transition ke saath, lip-sync same.
4. `python tools/voice_report.py episodes/epNNN/voice.mp3`. Galat shabd ya flat ho to wahi clip dobara Flow mein.
5. Is awaaz par `polish_voice.py --speed` ya khamoshi katna nahi (lip-sync toot jayega). `flow_voice.py` khud EQ aur loudness karta hai.

## Pakke rules
- Clone ka reference sirf `brand/voice_ref.wav` (Kaif ki chuni hui awaaz). Kisi aur asli insaan ki recording reference mein kabhi nahi, reference YouTuber ki bhi nahi.
- Reference video se sirf andaaz seekho: pace, ruk, josh ka graph. Unki awaaz, script ya lines copy nahi.
- Clone wali video upload karte waqt YouTube Studio ka "Altered or synthetic content" sawaal dhyan se padh ke Kaif khud jawab de.
- Channel par ek hi awaaz rahe: Kaif ki asli ya Kaif ka clone. Koi aur TTS voice nahi.
