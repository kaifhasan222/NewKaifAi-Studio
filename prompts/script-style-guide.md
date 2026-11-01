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

- Tez / normal / dheema: hook tez, beech normal, CTA dheema.
- Zor: ek keyword tez aur thoda upar. Poori line chillao mat.
- Ruk: voice line mein comma chhoti ruk, full stop lambi ruk. "Pause" shabd mat likho.
- Sample Kaif ki energetic recording ho, 6-10 second, bina music. Shaant padhai wali file hook pe mat do.

Flat: `ये कोई हैक नहीं है सिग्नल जाने में समय लगता है`
Bolne layak: `ये कोई हैक नहीं है। सिग्नल जाने में थोड़ा समय लगता है।` Delivery: pehli line tez, pehla shabd zor. Poori ruk. Doosri line normal.

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
[Scene 1 | 0-2s] Voice: ... | Delivery: tez, pehla shabd zor | Visual: punch zoom
[Scene 2 | 2-8s] Voice: ... | Delivery: normal, fact ke baad ruk | Visual: ...
CTA: ...
Sources: ...
```
