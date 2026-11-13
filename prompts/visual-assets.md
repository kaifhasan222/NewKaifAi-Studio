# Visuals: icon aur image, sirf text nahi

Kaif (11 Nov 2026): "Text ki jagah icon aur photo use karo, jaise WhatsApp ka icon, chacha ki image. Aur image hilni chahiye."
Motion scenes banane se pehle padho. Namoona: `episodes/ep014/motion/mg.py` (`sprite()` helper).

## 1. Niyam
- **Jis cheez ka naam bolo, uski tasveer dikhao.** App ka naam = app ka icon. Insaan/kirdaar (chacha, mummy, dukaandar, thag) = uski image. Cheez (SIM, chaabi, phone) = drawing ya image.
- **Har scene mein kam se kam ek icon ya image.** Sirf text wala scene tabhi jab hook ka bada slam ho.
- Text chhota rakho: icon ke neeche 1-3 shabd ka label. Poora vaakya caption mein hai, screen par dobara mat likho.
- **Har image hile.** Pehle pop-in, phir rukti nahi: `bob` (upar-neeche), `wiggle` (halka ghoomna), `float` (dono), `pulse` (saans), `shake` (jhatka, stamp/galti par). Ek scene ke icons alag `phase` par hilen taaki saath na hilen.
- Hansi wali line par kirdaar ki image zaroor (meme sound ke saath, `prompts/sound-design.md`).

## 2. App icons
- Source: Simple Icons (https://simpleicons.org, SVG CC0). File: `assets/graphics/icons/app_<naam>.png` (512px, brand rang ka gol-kone wala dabba + glyph).
- Naya icon:
  ```
  curl -o x.svg https://cdn.jsdelivr.net/npm/simple-icons@13/icons/<naam>.svg
  qlmanage -t -s 512 -o . x.svg        # Mac: kaala glyph, safed background
  ```
  phir Pillow se mask bana ke brand rang ke dabbe par chipkao (ep014 mein kiya hua hai). Naam aur source `assets/LICENSES.md` mein.
- **Kab chalega:** sirf us app ko pehchanne ke liye jiski baat ho rahi hai (news/explainer). Icon ka rang ya shape mat bigaado.
- **Kab nahi:** aisa na lage ki app ya company ne video banayi ya support kiya. Thumbnail mein kisi app ka icon mukhya cheez na ho. Sarkari chinh (Ashok stambh, DoT, RBI, police) nahi. Bank ya company ka logo scam wale scene mein "yeh company thag hai" jaisa na dikhe.
- Trademark us company ka hi rehta hai. Koi company hatane ko kahe to hata do.

## 3. Kirdaar aur photo jaisi image
- Gemini (Kaif ka Pro, Chrome mein gemini.google.com) se **naya, original cartoon kirdaar**. Prompt ka dhaancha:
  `Create an image: an original friendly cartoon character of <kaun, umar, kapde, haath mein kya, chehre ka bhaav>. 3D animated-movie cartoon style, waist-up, centered. Plain solid pure green (#00FF00) background with nothing else in it. No text, no logos, no watermark. Square 1:1.`
- Download karo, `.venv/bin/python tools/key_green.py <download.png> assets/graphics/characters/<naam>.png` se hara background hatao (green key + despill + Gemini sparkle hatana), `assets/graphics/characters/<naam>.png` mein rakho (raw file repo mein nahi, bhaari hoti hai). Dobara kaam aane wale kirdaar yahin rakho (chacha ban chuka hai).
- **Asli insaan ki photo nahi** (sirf Kaif ki apni, `brand/photo.jpg`). Celebrity, neta, kisi film/cartoon ka kirdaar nahi. Stock photo ke asli chehre ko mazaak ka patra mat banao.
- Asli cheezon ki photo/footage (sheher, smog, phone): Pexels/Pixabay, licence `assets/LICENSES.md` mein.
- AI image wali video par YouTube "Altered or synthetic content" aur Instagram "AI info" Kaif dekhe.

## 4. Check
- Contact sheet mein dekho: har scene mein icon/image hai, kuch kata nahi, caption ke neeche nahi chhupa.
- Kirdaar wale scene ke 3-4 frame nikal ke dekho ki image sach mein hil rahi hai.
