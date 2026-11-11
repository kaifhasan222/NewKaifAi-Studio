# Hook guide (pehle 3 second)

Har script se pehle yeh file padho. Hook kamzor hua to baaki video koi nahi dekhta.
Research: 11 Nov 2026 (sources neeche). ep001-ep013 ke hook ka audit bhi isi file mein.

## 1. Hook kyun sab kuch hai
- Viewer 1-3 second mein tay karta hai: rukna hai ya swipe. Reels par yeh aur jaldi hota hai, Shorts par thoda zyada setup chal jaata hai.
- YouTube Studio ka number: **Viewed vs swiped away**. Creators ka target 70-80%+ hota hai. 40-50% ho to hook hi dikkat hai. (YouTube ne koi official number nahi diya, yeh creators ka anubhav hai. Apne channel ke average se tulna karo.)
- Viewed zyada, par average % viewed kam: hook theek hai, beech ka hissa dheela hai.
- Instagram ke confirmed signal (Mosseri, Jan 2025): watch time, likes per reach, sends per reach. Hook ka kaam watch time bachana hai.
- Blog ke "35% zyada retention" jaise number unverified hain. Unhe sach maan ke script mat likho, apna data dekho.

## 2. Hook ke 4 hisse (charon ek saath, pehle 1.5 sec mein)
| Hissa | Kya ho | Is channel mein |
|---|---|---|
| **Visual** (frame 1) | Pehle frame se hi motion ya ajeeb cheez. Khaali ya dheere fade-in frame nahi. | Result/proof pehle dikhao: phata QR scan hota hua, "- Rs 5,000" udta hua, keypad par *99#. Kaif ho to chehra close-up + punch zoom. |
| **Text** (overlay) | 3-5 shabd, bade, 0.0s se screen par. | Voice ko dohrao mat, usse poora karo. Voice: "paisa lene ke liye PIN nahi lagta". Text: "PIN MAANGA = SCAM". Shorts/Reels ke button wale hisse se door. |
| **Voice** (pehli line) | 6-10 shabd, 2 second ke andar khatam. Pehle 3 shabd mein hi baat. | Devanagari `Voice:`. "Aaj", "is video mein", "kya aapko pata hai" se shuru nahi. |
| **Sound** | Ek saaf hit ya pop text ke saath. | `assets/sfx` se saaf hit ya boom, 0.3-0.4. Whoosh/glitch nahi. Detail `prompts/sound-design.md`. |

## 3. Hook ke 12 type
Har type ka formula aur is channel ke liye example. Example sirf dhaancha hai: fact script likhte waqt verify karo.

| # | Type | Formula | Example | Kab |
|---|---|---|---|---|
| 1 | **Result pehle (payoff first)** | Sabse kaam ki baat seedhi pehli line mein | "Bina internet UPI chalta hai. Bas *99# dabao." | How-to, trick, sarkari service |
| 2 | **Nuksaan / warning** | "[Yeh] kiya to [nuksaan]." | "QR scan karke paisa aata nahi. Jaata hai." | Scam, safety, galti |
| 3 | **Ulti baat (contrarian)** | Jo sab maante hain, uska ulta | "Background apps band karna battery bachata nahi, khaata hai." | Myth, tips |
| 4 | **Curiosity gap** | Ek ajeeb sach, wajah roko | "GPS ko internet chahiye hi nahi." | "Kaise kaam karta hai" explainer |
| 5 | **Number / specific** | Number + nateeja | "Tumhare naam par 9 SIM tak chal sakti hain. Check kiya?" | List, limit, paisa |
| 6 | **Seedha sawaal (haan/na)** | Aisa sawaal jiska jawab viewer ke paas ho | "Phone raat bhar charging par lagate ho?" | Aadat wale topic |
| 7 | **Proof / demo** | Bolne se pehle dikhao | (screen par kaam hota hua) "Yeh video bina camera ke bani hai." | AI tool, feature demo |
| 8 | **Kahani (1 line)** | Kisi ke saath hua + nuksaan, 2 sec mein | "Ek galat digit. 5,000 rupaye gaye." | Scam, galti, news |
| 9 | **Tum par ungli (callout)** | "Agar tum [yeh] ho/karte ho..." | "Agar tumhare phone mein yeh setting on hai, abhi band karo." | Setting, privacy |
| 10 | **Taaza khabar** | "Aaj se / is hafte se [badlav]" | "Is mahine se UPI ka yeh niyam badal gaya." | News, update (tareekh verify) |
| 11 | **Tulna / before-after** | Do cheezein aamne saamne | "10,000 ka phone vs 1 lakh ka phone. Farq sirf yahan hai." | Review, comparison |
| 12 | **Chhupi cheez (secret/hidden)** | "[Roz ki cheez] mein ek cheez hai jo 90% ko nahi pata" (number ho to verify) | "Har QR code ke kone mein 3 dabbe kyun hote hain?" | Roz ki cheez ka raaz |

**Stack karo:** sabse achha hook 2 type milata hai. Jaise Warning + Number: "Yeh 1 OTP diya, to poora account khaali."

## 4. Hamare purane hook mein kya galat tha (ep001-ep013)
1. **Asli baat der se aati hai.** ep007, ep008, ep009, ep011 mein Scene 1 sirf mahaul banata hai ("Mandi mein khade ho...") aur kaam ki baat Scene 2 mein, yaani 4-6 second par. Tab tak viewer ja chuka.
2. **Pehli line bahut lambi.** Zyada tar 13-20 shabd (ep010 mein 20+). Bolne mein 4-6 second. Hook 2 second mein khatam hona chahiye.
3. **"Aisa kaise?" wala ek hi formula.** ep002, ep003, ep004 teeno "X hota hai. Ye kaise?" Viewer ko koi nuksaan ya fayda nahi dikhta, isliye rukne ki wajah nahi.
4. **Scene 2 mein "Aaj poora tareeka / poora khel kholte hain".** ep004, ep005, ep006. Yeh intro hai, hook nahi. Hata do, seedha pehla point.
5. **"Ghabrao mat" baar baar.** ep007, ep011. Dar bana hi nahi tha to tasalli ka matlab nahi.
6. **Overlay voice ki copy hai**, aur har episode mein wahi whoosh + vine boom. Kuch naya nahi lagta.
7. **Viewer ka fayda saaf nahi.** "GPS kaise chalta hai" jaankari hai. "Jungle mein net nahi, phir bhi raasta aise milega" fayda hai.

| Ep | Purana hook | Dikkat | Behtar (type) |
|---|---|---|---|
| 001 | Sirf ek line, aur AI poori duniya bana deta hai. | Dava bada, saboot baad mein | (AI clip chalte hue) "Yeh camera se nahi bani. Ek line se bani." (7 Proof) |
| 002 | Phata hua QR code bhi scan ho jaata hai. Aisa kaise? | "Kaise" formula | (QR phaadte hue) "QR ko phaad do. Phir bhi scan hoga." (7 + 4) |
| 003 | Internet band hai, phir bhi map par location dikh rahi hai. Ye kaise? | Lamba, fayda nahi | "GPS ko internet chahiye hi nahi." (4) |
| 004 | Ek scan, aur kuch hi second mein payment poora. Par andar hota kya hai? | Lamba + Scene 2 intro | "2 second ka UPI payment. Peeche 4 jagah message jaata hai." (5, ginti verify) |
| 005 | Phone baar baar hang hota hai? Galti aksar phone ki nahi, hamari hoti hai. | Theek, par lamba | "Phone slow hai? Naya mat kharido." (3) |
| 006 | Bina camera, bina chehra dikhaye, bina ek rupaya lagaye, video banana hai? | 16 shabd | "Yeh video 0 rupaye mein bani. Bina camera." (7) |
| 007 | Mandi mein khade ho, paise dene hain, aur internet gayab. | Payoff Scene 2 mein | "Bina internet UPI chalta hai. Bas *99# dabao." (1) |
| 008 | Bike bechni hai, grahak bola QR scan karo, paise aa jayenge. | Payoff Scene 2 mein | "Paisa lene ke liye PIN kabhi nahi lagta." (2) |
| 009 | Bus mein phone chori, chor apni SIM daal ke chalayega. | Payoff Scene 2 mein | "Chori hua phone poore India mein band ho sakta hai. Ek form se." (1) |
| 010 | Roz phone ke saath 5 galtiyan jinko tum samajhdari samajhte ho. | 20+ shabd, phir "pehla myth" | Sabse chaunkane wale myth se seedha shuru (3) |
| 011 | Ek number galat dabaya, aur paanch hazaar kisi anjaan ke khaate mein. | Achhi kahani, par lambi | "Ek galat digit. 5,000 gaye. Wapas aise aayenge." (8 + 1) |
| 012 | Kya pata tumhare naam par koi aur SIM chala raha ho. | "Kya pata" kamzor | "Tumhare naam par kitni SIM chal rahi hain? 1 minute mein check." (5 + 9) |
| 013 | Ye dhundh nahi, zehreeli hawa hai (+ AQI ki paribhasha usi line mein) | Hook achha, line mein paribhasha jod di | "Yeh dhundh nahi hai. Zehar hai." Bas. Paribhasha Scene 2. (2) |

## 5. Hook ke niyam (checklist)
Har hook in 8 par pass ho:
1. Pehli `Voice:` line **10 shabd se kam**, 2 second mein khatam.
2. Pehle **3 shabd** mein hi topic ya nuksaan/fayda. Shuruaat mein "Aaj", "Is video mein", "Kya aapko pata hai", "Dosto", naam ya channel intro nahi.
3. **3 second ke andar** viewer ko pata ho: video kis baare mein hai aur mujhe kya milega.
4. **"Tum"** se baat. Viewer ki jeb, phone, paisa, suraksha.
5. **Specific:** number, rupaya, naam (*99#, 9 SIM, 5,000). "Bahut log", "kuch cheezein" nahi.
6. **Frame 1:** motion + bada text 0.0s se. Text voice ki copy nahi.
7. **Scene 2 intro nahi.** Hook ke turant baad pehla kaam ka point ya wajah.
8. **Sach.** Hook ka vaada video mein poora ho. Jhootha shock nahi (CLAUDE.md: claim verify).

## 6. Script likhte waqt process
1. Topic ke liye **3 hook likho, teeno alag type ke** (section 3 se).
2. Har ek ko section 5 ki checklist par jaancho. Sabse mazboot chuno.
3. `script.md` mein likho:
   ```
   Hook type: <number + naam, jaise 2 Warning + 5 Number>
   Hook: <chuna hua>
   Hook options: A) ... B) ... C) ...
   Hook text (overlay): <3-5 shabd>
   Hook visual (frame 1): <kya dikhta hai>
   ```
4. **Type ghumao:** pichhle 2 episode wala type dobara nahi. "X kaise hota hai?" tabhi jab koi aur type na bane.
5. Kaif ko report mein teeno option dikhao, taaki woh badal sake.

## 7. Hook ke baad bhi (retention)
- **Rehook:** video ke 40-50% par ek chhoti line jo aage ka vaada kare: "Par asli khatra teesra hai." Lambi (60s+) video mein do baar.
- **Sabse achhi baat aakhir ke liye mat bachao.** Ek mazboot point pehle 10 second mein.
- **Loop ending:** aakhri line aisi ho jo pehli line se jud jaaye, taaki replay ho. Aakhri boli line comment sawaal ho (viewer ki raay), 2-3 second. Follow/subscribe sirf animation mein.
- Har 2-3 second mein visual badle (cut, zoom, naya card).

## 8. Naapo aur seekho
Post ke 48 ghante baad neeche likho. 5 episode ke baad dekho kaun sa type jeet raha hai, usi ko zyada banao.

| Ep | Hook type | Viewed vs swiped (YT) | Avg % viewed | IG 3s / watch time | Seekh |
|---|---|---|---|---|---|
| | | | | | |

## Sources
- YouTube Help, analytics ki paribhasha: https://support.google.com/youtube/answer/12220281
- Viewed vs swiped away (koi official benchmark nahi): https://www.creatoressentials.com/glossary/viewed-vs-swiped-away/
- Shorts analytics, 70-90% viewed range: https://www.socialmediaexaminer.com/how-to-analyze-your-youtube-shorts/
- Shorts retention benchmarks: https://www.bytecap.io/research/youtube-shorts-retention-benchmarks
- Instagram signals (watch time, likes, sends): https://buffer.com/resources/instagram-algorithms/
- Hook types aur 3-second hold: https://www.opus.pro/blog/youtube-shorts-hook-formulas
- Hook categories: https://dev.to/wedgemethoddev/the-7-hook-categories-behind-every-viral-video-4771
- Pattern interrupt, visual 1.5s: https://virvid.ai/blog/hooks-pattern-interrupts-viral-openers-in-2026
- Platform ke hisaab se hook timing: https://ugccopilot.ai/blog/viral-hooks-that-convert/
- Slow intro/greeting ki galti: https://www.capcut.com/create/short-form-video-hooks-first-3-second-patterns
- Payoff der se dene ki galti: https://jellymarketing.ca/blog/stop-the-scroll-in-3-seconds-secrets-to-high-performing-short-form-video-hooks/
- India Shorts hooks: https://www.truefan.ai/blogs/youtube-shorts-attention-grabbing-hooks-tips
