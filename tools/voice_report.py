#!/usr/bin/env python3
"""
voice_report.py - awaaz kitni flat hai, number mein batata hai.

Usage (project root se):
    python tools/voice_report.py episodes/ep001/voice_raw.mp3
    python tools/voice_report.py brand/voice.mp3 episodes/ep001/voice.mp3   # pehle vs baad

Kya naapta hai:
  - Loudness (LUFS) aur loudness range (LRA): zor kitna upar-neeche hota hai
  - Pitch spread (semitone): awaaz kitni upar-neeche jaati hai
  - Pause: kitne, sabse lamba, aur 0.3s se lambe kitne
  - True peak: clipping hai ya nahi

Delivery ke liye RAW recording (polish se pehle) naapo. polish_voice.py compressor
lagata hai, isliye uske baad LRA kam aana normal hai; wahan sirf loudness aur peak dekho.
Thresholds andaze ke liye hain (rough guide), kaan se sunna phir bhi zaroori hai.
Sirf ffmpeg + numpy chahiye.
"""
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

SR = 16000


def ffmpeg_stats(path):
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
           "-af", "ebur128=peak=true,silencedetect=noise=-35dB:d=0.2", "-f", "null", "-"]
    err = subprocess.run(cmd, capture_output=True, text=True).stderr
    summary = err[err.rfind("Summary:"):]

    def grab(label):
        m = re.search(label + r":\s+(-?[\d.]+)", summary)
        return float(m.group(1)) if m else None

    pauses = [float(x) for x in re.findall(r"silence_duration: ([\d.]+)", err)]
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    total = int(dur.group(1)) * 3600 + int(dur.group(2)) * 60 + float(dur.group(3)) if dur else 0
    # shuru aur aakhir ki khamoshi pause nahi hai
    inner = [p for p, s in zip(pauses, starts) if s > 0.05 and s + p < total - 0.05]
    return {"lufs": grab("I"), "lra": grab("LRA"), "peak": grab("Peak"),
            "pauses": inner, "duration": total}


def pitch_stats(path):
    with tempfile.TemporaryDirectory() as tmp:
        wav_path = Path(tmp) / "p.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-ac", "1",
                        "-ar", str(SR), str(wav_path)], check=True)
        with wave.open(str(wav_path)) as w:
            x = np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768.0
    frame, hop = int(0.04 * SR), int(0.01 * SR)
    lo, hi = SR // 350, SR // 70
    f0 = []
    for i in range(0, len(x) - frame, hop):
        s = x[i:i + frame]
        if np.sqrt((s ** 2).mean()) < 0.02:
            continue
        s = s - s.mean()
        c = np.correlate(s, s, "full")[frame - 1:]
        k = lo + int(np.argmax(c[lo:hi]))
        if c[k] > 0.45 * c[0]:
            f0.append(SR / k)
    if len(f0) < 20:
        return None
    f0 = np.array(f0)
    st = 12 * np.log2(f0 / np.median(f0))
    return {"median_hz": float(np.median(f0)),
            "spread": float(np.percentile(st, 90) - np.percentile(st, 10))}


def verdict(ok, good, bad):
    return ("OK   " + good) if ok else ("FIX  " + bad)


def report(path):
    a = ffmpeg_stats(path)
    p = pitch_stats(path)
    pauses = a["pauses"]
    long_p = [x for x in pauses if x >= 0.3]
    print(f"\n== {path}  ({a['duration']:.1f}s)")
    print(f"Loudness      {a['lufs']} LUFS")
    lra = a["lra"] or 0
    print(f"Zor ka range  {lra:.1f} LU   " + verdict(
        lra >= 4, "zor upar-neeche ho raha hai",
        "flat: keyword par zor do, hook tez/upar, CTA dheema"))
    if p:
        print(f"Pitch spread  {p['spread']:.1f} st (median {p['median_hz']:.0f} Hz)   " + verdict(
            p["spread"] >= 7, "awaaz mein utaar-chadhaav hai",
            "kam utaar-chadhaav: sawaal par upar, fact par neeche jao"))
    longest = max(pauses) if pauses else 0
    print(f"Pause         {len(pauses)} total, {len(long_p)} >= 0.3s, sabse lamba {longest:.2f}s   " + verdict(
        len(long_p) >= max(1, round(a["duration"] / 12)),
        "sochi-samjhi ruk hai",
        "fact/reveal ke baad 0.4-0.7s ruko"))
    peak = a["peak"] if a["peak"] is not None else -99
    print(f"True peak     {peak:.1f} dBFS   " + verdict(
        peak <= -1.0, "clipping nahi", "clipping: mic se thoda door ya gain kam, phir polish_voice.py"))
    if pauses and a["duration"] and sum(pauses) / a["duration"] > 0.25:
        print("Note          khamoshi 25% se zyada: polish_voice.py lambe gap chhote karega")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for f in sys.argv[1:]:
        if not Path(f).exists():
            sys.exit(f"File nahi mili: {f}")
        report(f)
    print("\nYeh number andaza hain. Final faisla kaan se.")


if __name__ == "__main__":
    main()
