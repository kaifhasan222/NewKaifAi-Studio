# Script style guide (Hinglish shorts)

## Structure (30-60 sec, ~80-140 words)
1. **Hook (0-2s):** pehli line 10 shabd se kam, 2 second mein khatam, asli baat pehle 3 shabd mein. Type aur niyam `prompts/hook-guide.md` se. Scene 2 mein "aaj poora tareeka" jaisa intro nahi, seedha pehla point.
2. **Problem/Why (2-8s):** viewer ko kyun parwah honi chahiye.
3. **Meat (8-45s):** 2-4 chhote points, har point ek scene.
4. **Payoff + comment sawaal (last 5s):** ek line ka nichod, phir aakhri boli hui line viewer se uski raay poochhe (neeche "Ending"). Follow/like/subscribe bola nahi jaata, sirf animation mein.

## Bhasha
- Overlay, title aur caption Roman Hinglish. `Voice:` line Devanagari Hindi. Detail neeche.
- Bolchal wali. Chhote vaakya.
- English tech words waise hi (API, prompt, model), baaki Hindi/Urdu bolchal.
- Ek line = ek saans. Zyada lamba ho to todo.
- Jargon aaye to turant simple example.

## Voice line (jo awaaz bolegi)
`Voice:` wahi text hai jo awaaz banegi. Sirf yahi line Devanagari Hindi mein likho. Baaki script, overlay, title aur caption Roman Hinglish mein rahenge.

- Likhne ka andaaz dost jaisa aur aasaan ho, jaise Kaif kisi bachche ko samjha raha ho: har concept ek desi misaal se, aur har 15-20 sec mein ek halki hansi. Poora guide `prompts/script-fun-simple.md`. Filler nahi.
- Reaction filler mat likho: Aree, Achaa, Dekho, Suno, Matlab, Bas. Na voice mein, na caption mein.
- Tech word Devanagari mein likho, taaki awaaz ka tool atke nahi: गिट, गिटहब, कमिट, पुश.
- Ek line ek saans. Vowel mat kheench. Josh spelling se nahi aata.

## Delivery (awaaz mein nahi jaata)
Har scene ke saath `Delivery:` likho. Yeh generator ke liye hai. Text box mein sirf `Voice:` jaata hai.

Poora guide (recording tips, clone): `prompts/voice-delivery.md`. `tools/voice_clone.py` yahi shabd padhta hai, isliye inhi shabdon mein likho:

- **Pace:** `tez` / `normal` / `dheema`. Hook tez, beech normal, aakhri comment sawaal normal.
- **Josh 1-5:** `josh 5` hook, `josh 3-4` beech, `josh 2-3` CTA. Har line ek hi number par mat rakho, upar-neeche hona chahiye.
- **Zor:** `zor "शब्द"`, ek line mein ek shabd. Woh shabd thoda upar aur lamba. Poori line chillao mat.
- **Ruk:** `ruk 0.5` = line ke baad 0.5 sec chup. Fact/reveal ke baad 0.4-0.7, hook ke baad 0.3. Voice line ke andar comma chhoti ruk, full stop lambi. "Pause" shabd voice mein mat likho.
- **Sur (optional):** `upar` sawaal/hairani, `neeche` pakka fact.
- Clone ke liye reference Kaif ki energetic recording ho, 10-15 second, bina music (`brand/voice_ref.wav`). Shaant padhai wali file mat do.

Flat: `ये कोई हैक नहीं है सिग्नल जाने में समय लगता है`
Bolne layak: `ये कोई हैक नहीं है।` Delivery: `tez, josh 5, zor "हैक", ruk 0.3`. Phir `सिग्नल जाने में थोड़ा समय लगता है।` Delivery: `normal, josh 3, zor "समय", sur neeche, ruk 0.5`.

## Action (body language, Flow avatar aur recording dono ke liye)
Har scene ke saath `Action:` likho: Kaif camera par kya kare. Josh ke hisaab se:
- josh 5: camera ki taraf jhukna, ungli se point, bhaun uthana, tez haath.
- josh 3-4: haath se ginti (1, 2, 3), "chhota/bada" ka ishara, halka sir hilana.
- josh 1-2: seedha khade, muskaan, halka nod.
Ek scene mein ek hi action. Zor wale shabd par action. Flow prompt ke `Action:` mein yahi jaata hai.

## Ending (zaroori)
- **Aakhri `Voice:` line = comment sawaal**, isi video ke topic par, viewer ka apna POV ya anubhav poochho. "Comment karo" bol sakte ho.
- **"Follow karo", "like karo", "subscribe karo" awaaz mein nahi.** Yeh sirf end animation mein dikhe (subscribe + follow + like card, ek saaf pop/click SFX). `Visual:` mein likho.
- Sawaal ka jawab 1-3 shabd mein aa sake: A ya B, haan ya na, ek number, ya "tumhare saath hua?".
  - Achha: "तुम्हारे शहर का एक्यूआई आज कितना है? कमेंट करो।" / "तुम्हारे साथ कभी ऐसा स्कैम हुआ? कमेंट में बताओ।" / "तुम्हें क्या लगता है, फ़ोन रात भर चार्ज करना सही है या गलत?"
  - Bekaar: "Video kaisi lagi comment karo." / "Like, share, subscribe karo."
- Sawaal sachcha ho, jhagda karane wala nahi (dharm, rajneeti nahi). Delivery: `normal, josh 3, sur upar`.
- `CTA:` line mein likho: `Comment sawaal: ... | Animation: subscribe + follow + like`.

## Aasaan + funny (zaroori)
`prompts/script-fun-simple.md` padho. Chhota nichod:
- Bachche wala test: har line 10 saal ka bachcha samjhe. Pehle misaal (chai, tiffin, cricket, mummy), phir tech naam.
- 60 sec mein 2-3 halki hansi. Hook aur warning/step wali line mein nahi. Mazaak fact ko galat na kare.
- Josh 2 se 5 tak sab aaye, lagataar 3 line ek hi josh par nahi. Hansi se pehle `ruk 0.4`, hansi `dheema, josh 2`.

## Hook (zaroori)
Poora guide: `prompts/hook-guide.md` (12 type, checklist, purane hook ka audit). Script se pehle padho.
- Har script ke liye **3 hook, teeno alag type ke** likho, checklist par jaancho, sabse mazboot chuno.
- Pichhle 2 episode wala hook type dobara nahi. "X kaise hota hai?" aakhri option.
- Hook ke 4 hisse saath: frame 1 visual (motion/proof), overlay text (3-5 shabd, voice ki copy nahi), voice, ek saaf SFX.
- Video ke 40-50% par ek rehook line. Aakhri line pehli line se jude (loop).

## Fact rules
- Har claim (naam, price, feature) search karke verify karo. Source `script.md` ke neeche likho.
- Pakka na ho to "shayad"/"abhi ke hisaab se" bolo ya point hata do.

## Script file format
```
# epNNN: <title>
Seedhi baat: <topic ek line mein, bachche ke liye>
Misaal: <concept = roz ki cheez>
Hansi: <kis scene mein, kaunsa tareeqa>
Hook type: <number + naam, prompts/hook-guide.md se>
Hook: ...
Hook options: A) ... B) ... C) ...
Hook text (overlay): <3-5 shabd>
Hook visual (frame 1): ...
[Scene 1 | 0-2s] Voice: ... | Delivery: tez, josh 5, zor "...", ruk 0.3 | Action: ... | Visual: punch zoom
[Scene 2 | 2-8s] Voice: ... | Delivery: normal, josh 3, zor "...", ruk 0.5 | Action: ... | Visual: ...
CTA: Comment sawaal: <topic par viewer ki raay> | Animation: subscribe + follow + like (bola nahi jaata)
Sources: ...
```
