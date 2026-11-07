# Script style guide (Hinglish shorts)

## Structure (30-60 sec, ~80-140 words)
1. **Hook (0-2s):** ek chhoti, dhamakedaar line. Sawaal, ajeeb fact ya "ye mat karo".
2. **Problem/Why (2-8s):** viewer ko kyun parwah honi chahiye.
3. **Meat (8-45s):** 2-4 chhote points, har point ek scene.
4. **Payoff + CTA (last 5s):** ek line ka nichod, phir follow/comment.

## Bhasha
- Overlay, title aur caption Roman Hinglish. `Voice:` line Devanagari Hindi. Detail neeche.
- Bolchal wali. Chhote vaakya.
- English tech words waise hi (API, prompt, model), baaki Hindi/Urdu bolchal.
- Ek line = ek saans. Zyada lamba ho to todo.
- Jargon aaye to turant simple example.

## Voice line (jo awaaz bolegi)
`Voice:` wahi text hai jo awaaz banegi. Sirf yahi line Devanagari Hindi mein likho. Baaki script, overlay, title aur caption Roman Hinglish mein rahenge.

- Likhne ka andaaz seedha aur professional ho, jaise Kaif camera pe explain kar raha ho. Dosti wala filler nahi.
- Reaction filler mat likho: Aree, Achaa, Dekho, Suno, Matlab, Bas. Na voice mein, na caption mein.
- Tech word Devanagari mein likho, taaki awaaz ka tool atke nahi: गिट, गिटहब, कमिट, पुश.
- Ek line ek saans. Vowel mat kheench. Josh spelling se nahi aata.

## Delivery (awaaz mein nahi jaata)
Har scene ke saath `Delivery:` likho. Yeh generator ke liye hai. Text box mein sirf `Voice:` jaata hai.

Poora guide (recording tips, clone): `prompts/voice-delivery.md`. `tools/voice_clone.py` yahi shabd padhta hai, isliye inhi shabdon mein likho:

- **Pace:** `tez` / `normal` / `dheema`. Hook tez, beech normal, CTA dheema.
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

## Hook formulas
- "Ye AI tool aapka [kaam] 10 minute mein kar dega."
- "99% log [cheez] galat use karte hain."
- "Aaj ke baad [purani cheez] ki zarurat nahi."
- "Maine [cheez] try ki. Result yeh raha."

## Fact rules
- Har claim (naam, price, feature) search karke verify karo. Source `script.md` ke neeche likho.
- Pakka na ho to "shayad"/"abhi ke hisaab se" bolo ya point hata do.

## Script file format
```
# epNNN: <title>
Hook: ...
[Scene 1 | 0-2s] Voice: ... | Delivery: tez, josh 5, zor "...", ruk 0.3 | Action: ... | Visual: punch zoom
[Scene 2 | 2-8s] Voice: ... | Delivery: normal, josh 3, zor "...", ruk 0.5 | Action: ... | Visual: ...
CTA: ...
Sources: ...
```
