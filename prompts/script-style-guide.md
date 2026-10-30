# Script style guide (Hinglish shorts)

## Structure (30-60 sec, ~80-140 words)
1. **Hook (0-2s):** ek chhoti, dhamakedaar line. Sawaal, ajeeb fact ya "ye mat karo".
2. **Problem/Why (2-8s):** viewer ko kyun parwah honi chahiye.
3. **Meat (8-45s):** 2-4 chhote points, har point ek scene.
4. **Payoff + CTA (last 5s):** ek line ka nichod, phir follow/comment.

## Bhasha
- Roman Hinglish, bolchal wali. Chhote vaakya.
- English tech words waise hi (API, prompt, model), baaki Hindi/Urdu bolchal.
- Ek line = ek saans. Zyada lamba ho to todo.
- Jargon aaye to turant simple example.

## Voice line (jo awaaz bolegi)
`Voice:` wahi text hai jo screen par awaaz banegi. Seedha paragraph mat likho. Aise likho jaise Kaif dost ko samjha raha ho, beech mein reaction ke saath.

- Har scene mein **ek** interjection. Har sentence mein nahi, warna natak lagega.
- Interjection alag chhota tukda ho, phir baat. "..." ka matlab chhoti rukawat.
- Kaunsa reaction kab:
  - Hook / shock: `Aree!` ya `Suno!`
  - Samajh aaya: `Achaa...`
  - Screen dikhao: `Dekho,`
  - Simple banao: `Matlab`
  - Nichod: `Bas.`
  - CTA seedha rahe. Optional: `Ek kaam karo,`
- Vowel mat kheench (`Areeeeee`, `Achaaaaa`). Awaaz ka tool repeat par atak jaata hai ya line kaat deta hai. Josh tool ke emotion setting se aayega, spelling se nahi.
- On-screen title aur card saaf rakho (`YOU SHOT FIRST`, `SIGNAL DELAY`). "Aree" sirf voice aur caption mein.

Flat: `Ye koi hack nahi hai. Signal jaane mein time lagta hai.`
Bolne layak: `Aree, ye koi hack nahi hai. Dekho, signal jaane mein thoda time lagta hai.`

## Hook formulas
- "Ye AI tool aapka [kaam] 10 minute mein kar dega."
- "99% log [cheez] galat use karte hain."
- "Aaj ke baad [purani cheez] ki zarurat nahi."
- "Maine [cheez] try ki, result dekho."

## Fact rules
- Har claim (naam, price, feature) search karke verify karo. Source `script.md` ke neeche likho.
- Pakka na ho to "shayad"/"abhi ke hisaab se" bolo ya point hata do.

## Script file format
```
# epNNN: <title>
Hook: ...
[Scene 1 | 0-4s] Voice: Aree! ... | Visual: ...
[Scene 2 | 4-9s] Voice: ... | Visual: ...
CTA: ...
Sources: ...
```
