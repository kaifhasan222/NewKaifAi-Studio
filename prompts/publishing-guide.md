# Publishing guide: title, description, tags, hashtags

Har video ke liye Claude `episodes/epNNN/publish.md` banata hai (template: `episodes/_template/publish.md`). Video ki script/topic dekh ke likhta hai.
Channel name: **NEW KAIF AI** (YouTube), Instagram handle **@kaifhasan222**. Har description/caption ke CTA mein yahi naam.
Sample (achha bana hua): `episodes/ep001/publish.md`. Episode folder git mein nahi jata, isliye pattern neeche likha hai.

## Skill
`.claude/skills/youtube-seo-optimizer` (Mode E Shorts) se package banao, phir is guide ke rules lagao.

## Keyword research (har video se pehle)
- Claude web search karke dekhta hai: abhi us topic par kya trend kar raha hai, log kya search karte hain (YouTube/Google suggestions, Trends), competitors ke titles.
- **Hinglish + English dono** keywords: jaise "AI tools Hindi mein" aur "free AI tools". Indian audience dono tarah search karti hai.
- Gaming topic ho to log jo problem type karte hain woh shabd pakdo ("bullet not registering", "lag problem", "ping problem").
- Search volume ya "viral guarantee" ka koi number banaya nahi jayega. Sirf jo search mein mila wahi.

## Emoji rules
- Title: 1 emoji, beech ya end mein (shuru mein nahi, keyword pehle aana chahiye).
- Description / caption: har point ke aage 1 emoji (📶 ⚡ 🎯 🧱 👀 🏆 💬 🔔). Zyada mat bharo, padhne mein aasaan rahe.
- Hashtags aur YouTube "Tags" box mein emoji **nahi** (wahan kaam nahi karte). Emoji wale hashtag mat banao.
- Pinned comment: 2-3 emoji, sawaal ke saath.

## YouTube Shorts
- **Title:** 3 options, pehla recommended. 40-70 characters, main keyword shuru mein, hook (sawaal ya shock) + 1 emoji + `#Shorts`. Misleading clickbait nahi (video mein jo hai wahi title mein).
- **Description:** code block mein do taaki Kaif seedha copy kare.
  1. Pehli 1-2 line: hook + main keyword (YouTube pehli lines search aur preview mein dikhata hai).
  2. 3-5 bullet points with emoji: video ke main points, keywords naturally.
  3. Ek punch line (video ka takeaway).
  4. CTA: "💬 comment ..." + "🔔 ... NEW KAIF AI ko Subscribe karo!"
  5. End mein 3-5 hashtags, `#Shorts` pehla.
- **Hashtags:** 3-5 relevant. YouTube par 15 se zyada ho jayein to sab ignore ho sakte hain.
- **Tags (backend):** 10-12 keywords, comma se alag, code block mein (Hinglish + English, ek `new kaif ai`). Emoji nahi.
- **Pinned comment:** ek sawaal jo comments laye, options ke saath (jaise "20ms 🟢 | 60ms 🟡 | 100ms+ 🔴").

## Instagram Reels
- **On-screen cover text:** 3-5 shabd + 1 emoji. Cover image: `prompts/thumbnail-guide.md`.
- **Caption:** code block mein. Pehli line hook (keyword ke saath) + emoji, 3-4 emoji points, ek punch line, phir CTA: comment 💬, save/share 📌, "🔔 Follow @kaifhasan222".
- **Hashtags:** 8-10, alag code block: 2 broad (#tech #gaming), 4-5 niche (#bgmiindia #techinhindi), 1 brand (#newkaifai).
- Caption mein hi keywords likho (search/discovery ke liye).

## Upload checklist (publish.md ke end mein)
- Title mein `#Shorts`, video 9:16. Shorts aur Reels dono 3 min tak allow karte hain.
- AI label: voice clone ya realistic AI person/scene ho to YouTube "Altered or synthetic content" = Yes, Instagram "AI info" on.
- Post Kaif khud karega. Claude kuch post nahi karta.

## Rules
- Hashtag sirf relevant. Unrelated trending hashtag mat chipkao.
- Title/thumbnail ka claim video mein poora hona chahiye.
- Claims (price, feature, tick-rate jaise number) verify karo, source `publish.md` ke neeche.

## Output format
Dekho `episodes/_template/publish.md`.

## Trending / viral sound (Kaif ka rule, 9 Nov 2026)
- Sound sirf platform ke apne option se: Instagram "Add audio" (Trending tab), YouTube Shorts "Add sound" / Studio Editor Audio. Koi gaana download karke mp4 mein mix MAT karo (copyright claim / mute).
- Sound hamesha dheema: voice (original audio) 100%, platform sound ~5-15%. Awaaz saaf sunai deni chahiye.
- Volume set kiye bina direct post ya schedule MAT karo.
- Web par sound ya volume ka option na mile to post mat karo. Kaif ko sound ka naam batao: "Ye sound lagao, volume kam kar dena", aur woh app se post kare.
- Ek hi trending sound baar-baar mat lagao (spam signal).

## Delivery default (Kaif ka rule, 9 Nov 2026)
- Claude khud post/schedule NAHI karega. Video + thumbnail WhatsApp par Kaif ke apne chat "Kaif Jio (You)" mein **Document** ki tarah bhejo (quality compress na ho), saath mein publish.md ke copy-paste text (title, description, tags, IG caption, hashtags, pinned comment).
- Music wali video hi bhejo (bina-music version nahi chahiye). Kaif post karte waqt app se trending music khud jodta hai.
- Sirf jab Kaif bole "post kardo", tab Claude khud post kare.

## Thumbnail video ke andar (Kaif, 9 Nov 2026)
- WhatsApp delivery wali video ke shuru mein chuna hua thumbnail 0.4 sec ka frame lagao, aur wahi jpg cover art (attached_pic) embed karo. File: `output/epNNN_with_thumb.mp4`. Kaif app mein cover ke liye pehla frame chun sake.
