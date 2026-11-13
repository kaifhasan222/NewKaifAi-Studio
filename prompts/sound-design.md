# Sound design: SFX, meme sound, music, khamoshi

Har edit se pehle padho. Kaif ki shikayat (11 Nov 2026, ep014 pehla version): "lagta hai bas video bana di, detailing nahi. Funny jagah viral sound nahi, music theek nahi, awaaz ki khamoshi kati nahi."
Yeh file sound ke saare rule ek jagah rakhti hai. Koi doosri file isse takraaye to yeh file sahi hai.

## 1. Awaaz: khamoshi kaato (har awaaz par, clone par bhi)
- Clone: `tools/voice_clone.py` khud kaat-ta hai. Line ke baad aam ruk 0.18s tak, script mein `ruk 0.4+` (hansi/reveal se pehle) 0.28s tak, line ke andar ki lambi chup 0.1s. Band karna ho: `--no-tighten`.
- Flow `@me` awaaz: `tools/cut_silence.py --whisper`. Kaif ka raw camera video: `tools/cut_silence.py --takes --fillers` (best take + aa/umm). Kaif ki recording: `tools/polish_voice.py` (`--max-pause`).
- Episode ki `make_episode.py` timing ke liye `voice_clone.take_af()` hi use kare, taaki scene ki lambai awaaz se mile.
- Check: `ffmpeg -i voice.mp3 -af silencedetect=noise=-38dB:d=0.35 -f null -`. 0.35s se lambi koi chup nahi honi chahiye.
- Har chune hue take par earshot: "a noisy distorted crackling buzzy voice" ka z 2.5 ya zyada ho to take badlo.

## 2. SFX ki 3 parat (teeno chahiye, tabhi "detailing" lagti hai)
| Parat | Kab | Kaunsi file | Volume |
|---|---|---|---|
| **Detail** | Screen par har cheez jo aaye: text slam, pill, card, tick, button | `pop-01`, `click-01`, `ding-01`, `ui/select`, `ui/snap`, `ui/success` | 0.20-0.30 |
| **Zor (impact)** | Hook, bada number, stamp, reveal, rehook | `hit-01`, `boom-cinematic`, `impact-cinematic`, `sting-dramatic` | 0.28-0.40 |
| **Meme / viral** | Har hansi wali line ka punch, aur 1-2 bade reveal | `vine-boom`, `anime-wow`, `cha-ching`, `cough-01`, `heartbeat-2` | 0.38-0.55 |

Niyam:
- **Har hansi wali line par ek meme sound zaroor**, theek punch word par. 60 sec mein 2-4 meme sound. Ek hi meme sound ek video mein do baar nahi.
- **Sync animation se, andaze se nahi.** SFX ka time wahi ho jis pal cheez screen par aati hai (mg.py ka `t0`; scene stretch ho to `t0 / k`). `make_episode.py` mein `"a1.4"` format.
- **Ghanapan:** 60 sec mein 50-70 SFX (ep004: 42, ep013: 43, ep014: 71). Koi 3 second bina sound ke na jaaye.
- **Mana hai (Kaif ko noise lagta hai):** `error-glitch`, `ui/typing`, `whoosh*`, `ui/swipe`, `riser*`, `faaah`, `shocked-sound`. Purana `dun-dun` bhi nahi.
- Naya meme sound chahiye: `python3 tools/download_meme_sfx.py`, phir earshot se noise check, source aur licence `assets/LICENSES.md` mein. Gaane ya film ka tukda nahi.

## 3. Background music
- `assets/music/chill-tech-01.mp3` sirf 24 sec ka loop hai (loudness range 1 LU), 60 sec mein 3 baar dohrata hai. **Default nahi.**
- Default: `assets/music/lofi-upbeat-raspberrymusic.mp3`, volume **0.10**, voice par auto-duck. Licence CC BY 4.0: description mein credit zaroori:
  `Music: "Lofi Hip Hop Upbeat" by raspberrymusic (CC BY 4.0, Wikimedia Commons)`
- Naya track: Pixabay Music / YouTube Audio Library se, 60 sec+ lamba, licence `assets/LICENSES.md` mein.
- Kaif post karte waqt app se trending sound khud jodta hai (dheema, 5-15%).

## 4. Deliver se pehle check (earshot)
1. `tools/check_video.py`: loudness -14 se -16 LUFS, black frames nahi.
2. earshot match final mp4 par: "a digital glitch buzz or static noise" aur "a noisy distorted crackling voice" dono z 2.5 se neeche. Hansi wale hisse alag se bhi.
3. `publish.md` ke QA mein number likho. Kaif ko saaf batao: "maine naapa hai, suna nahi".

## 5. Yeh rule pehle kyun toote (ep014 v1)
- Memory ki ek line ("noisy SFX mat lagao, clean pop/click/hit") ko zyada kheench ke saare meme sound hata diye, jabki mana sirf glitch/typing/whoosh the. Poori memory file nahi padhi, jisme likha tha ki Kaif ko naye viral sound chahiye.
- Khamoshi kaatne wala tool (`cut_silence.py`) sirf Flow clip ke liye tha. Clone ke raaste mein `--no-tighten` laga tha, isliye kuch nahi kata.
- Music ka rule khud `chill-tech-01` kehta tha.
Ab teeno is file aur tool mein theek hain.
