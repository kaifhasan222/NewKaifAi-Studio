# Thumbnail / cover guide (Shorts + Reels)

Har episode ke saath 3 thumbnail options (A/B/C) bante hain, Kaif ek chunta hai. Tool: `tools/make_thumbnail.py`, config `episodes/epNNN/thumb.json`.

## Size aur safe zones
- Canvas **1080x1920** (9:16), JPG.
- **Grid safe box:** beech ka 1080x1440 (y 240 se 1680). Instagram profile grid 3:4 mein crop karta hai, isliye text aur chehra isi box mein.
- **Neeche 20% (y 1536 se neeche) khali:** Shorts/Reels ka title, caption aur buttons wahan aate hain.
- Upar ~200px mein bhi kuch zaroori nahi (status bar, search).

## Design rules
- **Text 2-4 shabd**, bahut bada (Bebas Neue 180-280px), har line ek rang: white + ek line highlight yellow `#FACC15`. Mota black border (borderw 10-14) taaki kisi bhi background par padha jaye.
- **Chehra** frame ka 35-45%, expression saaf: hairaan, muskaan, ishara. Blur ya aadhi band aankh wala frame nahi.
- **Ek idea:** jo video ka hook hai wahi thumbnail. 1 visual + 1 text, zyada cheezein nahi.
- **Contrast:** text ke peeche dark gradient/bar. Brand colors `brand/BRAND.md` (navy `#0B1020`, cyan `#22D3EE`, yellow `#FACC15`) aur video ka orange `#FF5A1F`.
- **Claim sach:** thumbnail ka text video mein poora hona chahiye. Misleading clickbait, fake numbers, kisi aur ka logo/chehra nahi.

## Layouts (`layout` in thumb.json)
- `face`: poore frame mein Kaif, text upar.
- `split`: upar visual (b-roll / motion still), neeche Kaif ka chehra, beech mein text.
- `before_after`: upar do stills (pehle -> baad) arrow ke saath, neeche chehra, beech mein text.
- `image`: Flow (Image mode, `@me_photo`) se bani bina-text 9:16 image, upar text. Bold MrBeast-jaisa look ke liye yahi best: skill `.claude/skills/video-thumbnail` (strategy, 4 concepts, desire loop) + `brand-style.md`.

## Flow
1. Frame chunna: `python3 tools/make_thumbnail.py --frames episodes/epNNN/raw-clips/epNNN_01.mp4` har 0.25s ka contact sheet banata hai (timestamps ke saath). Khuli aankh, strong expression, sharp frame chuno.
2. `episodes/epNNN/thumb.json` mein A/B/C likho (dekho ep001).
3. `python3 tools/make_thumbnail.py episodes/epNNN/thumb.json` -> `output/epNNN_thumb_A.jpg` ... aur `output/epNNN_thumbs_preview.jpg` (3:4 grid crop + Shorts UI zone ke saath).
4. Preview dekho: text kata to nahi, chehra grid box mein hai, neeche UI zone khali hai.
5. Kaif chunta hai, `publish.md` mein likho: "Thumbnail: A/B/C, chuna hua: __".

## Upload
- **Instagram Reels:** "Edit cover" mein chuna hua JPG upload karo, grid preview check karo.
- **YouTube Shorts:** video ka frame chunna safe hai. Custom image ka option app mein ho to wahi JPG. Hook frame video ke pehle second mein bhi rakh sakte ho.

## Bold look: Flow se custom image
Skill `video-thumbnail` ke prompt template se concept likho, `brand-style.md` jodo, text mat banwao. Shorts safe zones: upar 12%, neeche 25%, right 15% khali.

## Optional: Flow se custom photo
Video frame kaafi na lage to Flow (project **me**, Image mode) mein `@me_photo` ke saath expressive pose. Credits lagte hain, pehle Kaif se ok. Chehra `me_photo` se milao.
