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
