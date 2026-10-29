#!/usr/bin/env python3
"""
analyze_reference.py - reference video ka STYLE nikalta hai (content copy karne ke liye nahi).

Usage:  python tools/analyze_reference.py references/my-ref.mp4

Banata hai (references/<naam>_analysis/ folder mein):
  - frames.jpg      : har ~1 sec ka ek frame (max 30) ek image mein
  - stats.json      : duration, size, cuts ki ginti, average shot length, cut timings, loudness
  - audio.wav       : voice ke liye (make_captions.py se transcript nikalne ke liye)
Phir Claude frames.jpg dekh ke + transcript padh ke `style-card.md` likhta hai.
"""
import json
import re
import subprocess
import sys
from pathlib import Path


def run(cmd):
    return subprocess.run([str(c) for c in cmd], capture_output=True, text=True)


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    video = Path(sys.argv[1])
    out = video.parent / f"{video.stem}_analysis"
    out.mkdir(parents=True, exist_ok=True)

    p = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height,r_frame_rate:format=duration",
             "-of", "json", video])
    meta = json.loads(p.stdout)
    dur = float(meta["format"]["duration"])
    st = meta["streams"][0]

    # scene cuts
    r = run(["ffmpeg", "-i", video, "-vf", "select='gt(scene,0.3)',showinfo",
             "-an", "-f", "null", "-"])
    cuts = [round(float(x), 2) for x in re.findall(r"pts_time:([\d.]+)", r.stderr)]

    # frames: ~1 per second, max 30
    step = max(1.0, dur / 30)
    run(["ffmpeg", "-y", "-v", "error", "-i", video,
         "-vf", f"fps=1/{step:.2f},scale=216:-1,tile=6x5",
         "-frames:v", "1", "-q:v", "3", out / "frames.jpg"])

    # audio + loudness
    run(["ffmpeg", "-y", "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000", out / "audio.wav"])
    loud = run(["ffmpeg", "-i", video, "-af", "ebur128", "-vn", "-f", "null", "-"]).stderr
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", loud)

    stats = {
        "file": str(video),
        "duration_sec": round(dur, 1),
        "size": f"{st['width']}x{st['height']}",
        "fps": st["r_frame_rate"],
        "cuts": len(cuts),
        "avg_shot_length_sec": round(dur / (len(cuts) + 1), 2),
        "cut_times": cuts,
        "loudness_lufs": float(lufs[-1]) if lufs else None,
    }
    (out / "stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(json.dumps(stats, indent=2))
    print(f"\nFiles -> {out}")


if __name__ == "__main__":
    main()
