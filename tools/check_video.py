#!/usr/bin/env python3
"""
check_video.py - finished video ka quick QA.
Contact sheet (frames ek image mein), black-frame check, loudness, duration.

Usage: python tools/check_video.py output/ep001.mp4
Claude contact sheet image dekh ke gadbad pakadta hai; final approval tumhara.
"""
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
    sheet = video.with_suffix(".contact.jpg")

    info = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=width,height,r_frame_rate:format=duration",
                "-of", "default=nw=1", video]).stdout
    print(info.strip())

    # 1 frame har 3 second, 5 columns
    run(["ffmpeg", "-y", "-v", "error", "-i", video,
         "-vf", "fps=1/3,scale=216:-1,tile=5x4", "-frames:v", "1", "-q:v", "3", sheet])
    print(f"contact sheet -> {sheet}")

    black = run(["ffmpeg", "-i", video, "-vf", "blackdetect=d=0.3:pix_th=0.05",
                 "-an", "-f", "null", "-"]).stderr
    hits = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", black)
    print("black frames:", hits if hits else "none")

    loud = run(["ffmpeg", "-i", video, "-af", "ebur128=peak=true", "-vn", "-f", "null", "-"]).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", loud)
    if m:
        print(f"loudness: {m[-1]} LUFS  (target about -16)")


if __name__ == "__main__":
    main()
