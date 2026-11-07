#!/usr/bin/env python3
"""
polish_voice.py - Kaif ki recording ko saaf aur "professional" sound dena.

Usage (project root se):
    python tools/polish_voice.py episodes/ep001/voice_raw.mp3 episodes/ep001/voice.mp3
    python tools/polish_voice.py raw.mp3 voice.mp3 --speed 1.05 --max-pause 0.6

Kya karta hai (sirf ffmpeg, koi naya install nahi):
  1. Lambi khamoshi chhoti: --max-pause se lamba gap utna hi reh jaata hai
     (planned ruk 0.4-0.6s bachi rehti hai). Shuru/aakhir 0.1s.
  2. Rumble hatana (80 Hz high-pass), halka noise reduction.
  3. EQ: 250 Hz par thoda kam (bhaari/boxy), 3.5 kHz par thoda zyada (saaf, aage).
  4. De-esser (sss kam), compressor (awaaz barabar aur paas).
  5. --speed: pitch badle bina thoda tez (1.03-1.08 shorts ke liye theek).
  6. Loudness -16 LUFS, true peak -1.5 dB (clipping khatam).

Dhyan do: yeh awaaz saaf karta hai, josh nahi daalta. Josh recording se aata hai
(Delivery card) ya voice_clone.py se. Pehle aur baad: tools/voice_report.py
"""
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr[-2000:])
    return r.stderr


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout
    return float(out.strip())


def speech_segments(path, threshold_db, min_silence):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af",
               f"silencedetect=noise={threshold_db}dB:d={min_silence}", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    total = duration(path)
    if len(ends) < len(starts):
        ends.append(total)
    silences = list(zip(starts, ends))
    segs, cur = [], 0.0
    for s, e in silences:
        if s > cur:
            segs.append([cur, s])
        cur = e
    if cur < total:
        segs.append([cur, total])
    return segs, silences, total


def tighten_filter(segs, silences, total, max_pause, edge=0.1):
    """Speech ke tukde rakho, beech ka gap max_pause tak."""
    keep = []
    for i, (s, e) in enumerate(segs):
        a = max(0.0, s - (edge if i == 0 else 0.0))
        b = e
        if i + 1 < len(segs):
            gap = segs[i + 1][0] - e
            b = e + min(gap, max_pause)
        else:
            b = min(total, e + edge)
        keep.append((a, b))
    expr = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in keep)
    return f"aselect='{expr}',asetpts=N/SR/TB"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--speed", type=float, default=1.0, help="1.0 = same. 1.05 = 5%% tez")
    ap.add_argument("--max-pause", type=float, default=0.6, help="isse lamba gap kaat ke itna (sec)")
    ap.add_argument("--no-tighten", action="store_true", help="khamoshi mat chhedo")
    ap.add_argument("--denoise", type=float, default=-25, help="afftdn noise floor dB (-20 zyada, -30 kam)")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        sys.exit(f"File nahi mili: {src}")
    if not 0.8 <= args.speed <= 1.25:
        sys.exit("--speed 0.8 se 1.25 ke beech rakho")

    chain = []
    if not args.no_tighten:
        segs, silences, total = speech_segments(src, -38, args.max_pause)
        if segs:
            chain.append(tighten_filter(segs, silences, total, args.max_pause))
    chain += [
        "highpass=f=80",
        f"afftdn=nf={args.denoise}",
        "equalizer=f=250:t=q:w=1.2:g=-2.5",
        "equalizer=f=3500:t=q:w=1.0:g=3",
        "equalizer=f=9000:t=h:w=2000:g=1.5",
        "deesser=i=0.4",
        "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3",
    ]
    if abs(args.speed - 1.0) > 1e-3:
        chain.append(f"atempo={args.speed:.3f}")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp) / "stage.wav"
        run(["ffmpeg", "-y", "-hide_banner", "-i", str(src), "-af", ",".join(chain),
             "-ar", "48000", "-ac", "1", str(stage)])
        # loudness 2-pass taaki -16 LUFS sahi aaye
        err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(stage), "-af",
                   "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=summary", "-f", "null", "-"])

        def val(name):
            return re.search(name + r":\s+([-+]?[\d.]+|-?inf)", err).group(1).lstrip("+")

        ln = ("loudnorm=I=-16:TP=-1.5:LRA=11:"
              f"measured_I={val('Input Integrated')}:measured_TP={val('Input True Peak')}:"
              f"measured_LRA={val('Input LRA')}:measured_thresh={val('Input Threshold')}:linear=true")
        codec = ["-c:a", "libmp3lame", "-b:a", "192k"] if out.suffix.lower() == ".mp3" else []
        run(["ffmpeg", "-y", "-hide_banner", "-i", str(stage), "-af", ln, "-ar", "48000"]
            + codec + [str(out)])

    print(f"Ban gaya: {out}  ({duration(src):.1f}s -> {duration(out):.1f}s)")
    print(f"Check: python tools/voice_report.py {src} {out}")


if __name__ == "__main__":
    main()
