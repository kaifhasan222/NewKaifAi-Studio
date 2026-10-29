#!/usr/bin/env python3
"""
make_captions.py - voice mp3 se short-form captions (.srt) banata hai (free, local, Whisper).

Setup (ek baar):   pip install faster-whisper
Usage:             python tools/make_captions.py brand/voice.mp3 episodes/ep001/captions.srt
Optional:          --lang hi   (default: hi)   ya   --lang en
                   --words 4   (ek caption mein max words, default 4)

Note: Hindi mode aksar Devanagari deta hai. Hinglish (Roman) chahiye to Claude se kaho:
"captions.srt ka text Roman Hinglish mein badlo, timings mat chhedna."
"""
import argparse
import subprocess
from pathlib import Path
import numpy as np


def load_audio(path, sampling_rate=16000):
    cmd = [
        "ffmpeg", "-nostdin", "-threads", "0", "-i", str(path),
        "-f", "s16le", "-ac", "1", "-ar", str(sampling_rate), "-"
    ]
    res = subprocess.run(cmd, capture_output=True, check=True)
    return np.frombuffer(res.stdout, np.int16).flatten().astype(np.float32) / 32768.0


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("out")
    ap.add_argument("--lang", default="hi")
    ap.add_argument("--words", type=int, default=4)
    ap.add_argument("--model", default="small")
    a = ap.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise SystemExit("faster-whisper install karo:  pip install faster-whisper")

    model = WhisperModel(a.model, compute_type="int8")
    audio_data = load_audio(a.audio)
    segments, _ = model.transcribe(audio_data, language=a.lang, word_timestamps=True)
    words = [w for seg in segments for w in (seg.words or [])]

    blocks = []
    for i in range(0, len(words), a.words):
        chunk = words[i:i + a.words]
        text = " ".join(w.word.strip() for w in chunk)
        blocks.append((chunk[0].start, chunk[-1].end, text))

    lines = []
    for n, (s, e, text) in enumerate(blocks, 1):
        lines += [str(n), f"{srt_time(s)} --> {srt_time(e)}", text, ""]
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(blocks)} captions -> {a.out}")


if __name__ == "__main__":
    main()
