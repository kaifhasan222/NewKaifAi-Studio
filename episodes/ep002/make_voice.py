#!/usr/bin/env python3
"""Clone Kaif's voice (brand/voice.mp3) into the ep002 Hindi lines. Local, free: Chatterbox."""
import os
from pathlib import Path

import torch
import torchaudio as ta

os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

from chatterbox.mtl_tts import ChatterboxMultilingualTTS

ROOT = Path(__file__).resolve().parent
REF = ROOT / "voice-lines" / "ref.wav"
OUT = ROOT / "voice-lines"

LINES = [
    "Microsoft में करीब साठ हज़ार लोगों को नौकरी छोड़ने का ऑफ़र मिला है।",
    "यह सीधी छंटनी नहीं है। खुद हटने का ऑफ़र है। कुल स्टाफ में से करीब सत्ताईस प्रतिशत लोग इस लिस्ट में हैं।",
    "ऑफ़र चार देशों में है। भारत, अमेरिका, ब्रिटेन और कनाडा। सिर्फ लेवल सत्तर या उससे नीचे, और सिर्फ चुनिंदा टीमों के लिए।",
    "भारत में एक दिसंबर तक जवाब देना है। जो हाँ कहेगा, वह इकतीस दिसंबर को कंपनी छोड़ देगा।",
    "हर टीम को यह ऑफ़र नहीं मिला। मार्केटिंग, सेल्स और सिक्योरिटी की कई टीमें इस लिस्ट से बाहर हैं।",
    "रिपोर्ट्स के हिसाब से, डेटा सेंटर और एआई चिप्स पर इस साल करीब एक सौ पचहत्तर अरब डॉलर का प्लान है। इसलिए टीम का खर्च घटाया जा रहा है।",
    "आदमी खुद चुन सकता है। सबको निकाला नहीं जा रहा। यह सही है या गलत? कमेंट करो, और रोज़ टेक अपडेट्स के लिए फॉलो करो।",
]


def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print("device", device, flush=True)
    model = ChatterboxMultilingualTTS.from_pretrained(device)
    print("model ready", model.sr, flush=True)
    for i, text in enumerate(LINES, start=1):
        wav = model.generate(
            text,
            language_id="hi",
            audio_prompt_path=str(REF),
            exaggeration=0.35,
            cfg_weight=0.5,
            temperature=0.7,
        )
        path = OUT / f"line{i:02d}.wav"
        ta.save(str(path), wav, model.sr)
        print(f"saved {path.name} {wav.shape[-1] / model.sr:.2f}s", flush=True)


if __name__ == "__main__":
    main()
