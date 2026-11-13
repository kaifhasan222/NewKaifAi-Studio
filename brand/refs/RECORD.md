# Clone ke liye emotion wali recordings (Kaif, baaki hai)

IndicF5 mein josh ka knob nahi hai. Jaisi reference awaaz, waisa hi andaaz. Isliye har josh ki alag recording.
`tools/voice_indic.py` har scene ke `Delivery:` ka josh dekh ke yahin se reference chunta hai. Jo file nahi hai,
uski jagah `brand/voice_ref.wav` (Gemini wali awaaz) lagti hai.

Kaise record karo: phone voice memo, shaant kamra, mic munh ke paas, 8-12 sec, ek hi take mein.
**Likhe hue shabd bilkul wahi bolo** (model ko reference ka text chahiye; ek shabd badla to clone bigadta hai).
Emotion 2 guna karke bolo. Kuch badal ke bola to `<naam>.txt` mein wahi likh do jo bola.

| File (is folder mein) | Kaisa bolna | Text |
|---|---|---|
| `josh5.m4a` | Hairani, zor se, tez | क्या?! सच में? ये तो बिल्कुल उल्टा निकला! मुझे भी यकीन नहीं हुआ, लेकिन यही सच है। अब ध्यान से सुनो! |
| `josh4.m4a` | Josh se, tez, kaam ki baat | सुनो, ये बात बहुत काम की है। ज़्यादातर लोग यहीं गलती करते हैं, और फ़ोन की बैटरी खराब कर देते हैं। |
| `josh3.m4a` | Dost jaisa, aaram se | चलो अब आराम से समझते हैं कि अंदर असल में होता क्या है। बात बिल्कुल सीधी है। |
| `josh2.m4a` | Dheema, deadpan, muskura ke (mazaak) | सोते हुए बच्चे को बार बार उठाओगे, तो वो और रोएगा। फ़ोन भी बिल्कुल ऐसा ही है। |
| `sawaal.m4a` | Sawaal, aakhir mein awaaz upar | इन पाँच में से तुम कितनी करते थे? कमेंट में नंबर ज़रूर लिखना। |

`.wav`, `.m4a`, `.mp3` sab chalega. Josh 1 wali line `josh2` se, sawaal (`sur upar` ya `?` wali aakhri line) `sawaal` se.
