# Script: bachche ko samajh aaye + beech beech mein hansi

Har script se pehle padho (hook ke liye `prompts/hook-guide.md`). Research: 11 Nov 2026, sources neeche.
Dikkat jo Kaif ne batayi: script aur awaaz boring lagti hai, kitaab jaisi. Hal: har baat ek desi misaal se, aur beech beech mein ek halki hansi.

## 1. Bachche wala test (ELI5)
Har line par poochho: **10 saal ka bachcha ya dadi yeh sun ke samjhegi?** Nahi to dobara likho.

1. **Ek concept = ek misaal.** Paribhasha mat do, tulna do. Ek achhi tulna kai lines ki samjhaish se tez sikhati hai.
2. **Misaal ghar aur gali se:** chai, tiffin, dabba, auto, cricket, mummy, school, kirana dukaan, shaadi, train, pados wali aunty. Videsh wali misaal nahi.
3. **Pehle misaal, phir naam.** "Hawa ki marksheet hoti hai. Usko AQI kehte hain." Ulta nahi.
4. **Kathin shabd aaye to usi line mein aasaan matlab**, ya shabd hi hata do. Full form (Air Quality Index) tabhi jab kaam ki ho.
5. **Number ko cheez banao.** "30 percent" nahi, "har 10 mein se 3". "5 GB" nahi, "lagbhag 1000 photo".
6. **Ek line mein ek hi baat.** 6-12 shabd. "Aur", "jo ki", "jisse" se judi lambi line todo.
7. **"Tum" se baat karo**, viewer ki apni zindagi: tumhara phone, tumhari jeb, tumhari mummy.
8. **Chhoti kahani > list.** Ek kirdaar (Pappu, chacha, dukaandar) ke saath kuch hota hai, usi se baat samjhao.

| Boring (kitaab) | Aasaan (bachcha samjhe) |
|---|---|
| AQI yaani Air Quality Index, ek number jo batata hai hawa kitni saaf hai. | Hawa ki bhi marksheet hoti hai. Naam hai AQI. Bas yahan zyada number laana buri baat hai. |
| GPS satellite se signal lekar location nikalta hai. | Upar 4 satellite tumhe awaaz dete hain. Kiski awaaz kitni der mein aayi, usi se pata chalta hai tum kahan khade ho. |
| QR code mein error correction hota hai. | QR code ek hi baat teen-chaar baar likh ke rakhta hai. Ek jagah phat jaaye, doosri se padh leta hai. |
| UPI transaction NPCI ke through route hota hai. | Tumhara bank aur dukaandar ka bank seedhe baat nahi karte. Beech mein ek daakiya hai, NPCI. |

Misaal sach ke kareeb ho. Jo misaal fact ko galat kar de, woh mat likho (CLAUDE.md: claim verify).

## 2. Hansi (beech beech mein, zabardasti nahi)
- **Kitni:** har 15-20 second mein ek halki hansi. 60 sec ki video mein 2-3. Hook aur asli warning/step wali line mein mazaak nahi.
- **Kahan:** kisi fact ke turant baad, ya do point ke beech. Rehook (40-50%) par ek achhi jagah hai.
- **Chhoti:** ek line, 5-10 shabd. Mazaak samjhana pade to hata do.

Hansi ke 6 tareeqe:
| Tareeqa | Example |
|---|---|
| Badha-chadha ke (exaggeration) | "Phone itna garam, upar roti sek lo." |
| Ghar ghar ki kahani (relatable) | "Mummy ko lagta hai wifi band karne se bijli ka bill kam aayega." |
| Apna mazaak (self-roast) | "Maine bhi 3 saal yahi galti ki. Haan, main hi tha woh." |
| Ajeeb tulna | "Yeh password utna hi surakshit hai jitna darwaze par likha 'chaabi gamle ke neeche hai'." |
| Cheez ko insaan banana | "Tumhara phone raat ko sota nahi. Chupke se 40 app se gappe maarta hai." |
| Callback (pehli hansi ko aakhir mein dobara) | Shuru mein roti wali baat, aakhri sawaal par: "Tumhara phone kitna garam hota hai? Comment karo. Aur roti mat sekna." |

**Hansi ki delivery (clone/recording ke liye):** mazaak se pehle `ruk 0.4`, mazaak wali line `dheema, josh 2` ya `normal, josh 3` (seedhe chehre se, deadpan), uske baad agli line phir `tez, josh 4-5`. Yahi upar-neeche awaaz ko boring hone se bachata hai.

**Mat karo:**
- Dharm, jaati, rajneeti, kisi ke rang-roop, ling ya gareebi par mazaak nahi. Kisi asli insaan ya brand ki beizzati nahi.
- Scam ke shikaar ka mazaak nahi. Scammer ka uda sakte ho.
- Mazaak fact ko galat na kare, aur viewer use sach na samajh le.
- Reaction filler ab bhi nahi (`Aree`, `Achaa`, `Dekho`, `Matlab`, `Bas`). Hansi line ke matlab se aaye, awaazon se nahi. Vowel mat kheencho.
- Har hansi wali line ke punch par ek meme/viral sound (vine-boom, anime-wow, cha-ching, cough). Noisy wale nahi. Detail `prompts/sound-design.md`.

## 3. Boring se bachne ke aur tareeqe
- **Awaaz ka graph hile:** lagataar 3 line ek hi `josh` par nahi. Poori video mein josh 2 se 5 tak sab aaye.
- **Sawaal poochho** beech mein: "Ab socho, yeh paisa gaya kahan?" Sawaal par sur apne aap upar jaata hai.
- **Line ki lambai badlo:** do chhoti, ek lambi. "Ruko. Yeh scam hai. Aur isme sabse pehle wahi phanste hain jo sabse zyada padhe likhe hain."
- **Bolne jaisi bhasha.** Likh ke zor se padho. Zubaan atke to line badlo.
- Har point ke baad chhota "to ab kya karein" (fayda), sirf jaankari nahi.

## 4. Script likhte waqt process
1. Pehle topic ko **ek line mein bachche ko samjhao**. Yahi video ki reedh hai. `script.md` mein `Seedhi baat:` likho.
2. Har concept ke liye misaal chuno, `Misaal:` mein likho (kaunsi cheez = kaunsi cheez).
3. 2-3 hansi ki jagah tay karo, `Hansi:` mein scene number ke saath.
4. Scene likho. Phir poori script par section 1 ka test aur section 3 ka josh graph check.

```
Seedhi baat: <ek line, bachche ke liye>
Misaal: AQI = hawa ki marksheet; N95 = chhanni
Hansi: Scene 4 (ajeeb tulna), Scene 9 (callback)
```

## Sources
- ELI5 se explainer likhna: https://www.clipatize.com/blog/how-to-eli5-your-explainer-video/
- Saaf, bachche jaisi bhasha par bharosa: https://explainerd.com/?p=1225
- Ek tulna kai paragraph se tez: https://www.teleprompter.com/tools/explainer-video-script-generator
- Kathin topic: kirdaar ki kahani + ek-do mazaak: https://truscribe.com/blog/how-to-write-a-script-for-a-complex-topic
- Hansi + jaankari saath: https://breadnbeyond.com/articles/explainer-video-script
- Kaan ke liye likhna, chhoti-lambi line: https://vidiq.com/es/blog/post/write-youtube-video-script/
- Kahani se yaad rehna (number pakka nahi, secondary source): https://www.wyzowl.com/storytelling-in-explainer-videos.html
