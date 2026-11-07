#!/usr/bin/env python3
"""
flow_voice.py - Flow clips mein jo @me ki awaaz hai, usi ko episode ki voice banana.

Jab Flow mein @me se clip banti hai, clip mein Kaif ki awaaz aur lip-sync dono hote hain.
build_video.py clips ki awaaz hata deta hai aur `voice` file lagata hai. Yeh tool har clip
se awaaz nikaal ke UNHI trim (start/duration) aur UNHI transition ke saath jodta hai jo
video mein lagte hain, taaki honth aur awaaz same second par rahein.

Usage (project root se):
    python tools/flow_voice.py episodes/ep001/episode.json
    python tools/flow_voice.py episodes/ep001/episode.json --out episodes/ep001/voice.mp3

Phir episode.json mein "voice": "episodes/ep001/voice.mp3" rakho aur build_video.py chalao.
Clip mein awaaz na ho (b-roll, motion graphic) to us hisse mein khamoshi aati hai.

Dhyan: is awaaz ko polish_voice.py se --speed ya khamoshi kaat ke mat chhedo, lip-sync toot jayega.
Yeh tool khud polish (EQ, compressor, -16 LUFS) bina timing badle karta hai.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SR = 48000


def probe(path, entries, stream=None):
    cmd = ["ffprobe", "-v", "error"]
    if stream:
        cmd += ["-select_streams", stream]
    cmd += ["-show_entries", entries, "-of", "csv=p=0", str(path)]
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr[-2000:])


def clip_audio(clip, idx, tmp):
    """Clip ki awaaz, video jaisa trim. Awaaz na ho to utni khamoshi."""
    f = clip["file"]
    if not Path(f).exists():
        sys.exit(f"Clip nahi mili: {f}")
    start = float(clip.get("start") or 0)
    dur = float(clip.get("duration") or 0) or float(probe(f, "format=duration")) - start
    out = Path(tmp) / f"a{idx:02d}.wav"
    has_audio = bool(probe(f, "stream=index", "a"))
    if has_audio:
        run(["ffmpeg", "-y", "-v", "error", "-i", f, "-af",
             f"atrim=start={start:.3f}:duration={dur:.3f},asetpts=PTS-STARTPTS,"
             f"apad=whole_dur={dur:.3f}", "-ar", str(SR), "-ac", "1", str(out)])
    else:
        run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-t", f"{dur:.3f}",
             "-i", f"anullsrc=r={SR}:cl=mono", str(out)])
    return out, dur, has_audio


def join(parts, durs, d, out):
    n = len(parts)
    inputs = []
    for p in parts:
        inputs += ["-i", str(p)]
    if n == 1:
        run(["ffmpeg", "-y", "-v", "error", *inputs, str(out)])
        return
    if d <= 0:
        chain = "".join(f"[{i}:a]" for i in range(n)) + f"concat=n={n}:v=0:a=1[a]"
    else:
        # video ka xfade overlap = audio ka acrossfade overlap, isliye timing same
        parts_f, last = [], "[0:a]"
        for i in range(1, n):
            lab = f"[x{i}]" if i < n - 1 else "[a]"
            parts_f.append(f"{last}[{i}:a]acrossfade=d={d}:c1=tri:c2=tri{lab}")
            last = lab
        chain = ";".join(parts_f)
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", chain, "-map", "[a]", str(out)])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode", help="episodes/epNNN/episode.json")
    ap.add_argument("--out", help="default: episode folder mein voice.mp3")
    ap.add_argument("--raw", action="store_true", help="polish mat karo, sirf jodo")
    args = ap.parse_args()

    cfg = json.loads(Path(args.episode).read_text(encoding="utf-8"))
    clips = cfg.get("clips") or []
    if not clips:
        sys.exit("episode.json mein clips nahi hain.")
    d = float((cfg.get("transition") or {"duration": 0.25}).get("duration", 0.25))
    out = Path(args.out) if args.out else Path(args.episode).resolve().parent / "voice.mp3"

    with tempfile.TemporaryDirectory() as tmp:
        parts, durs, silent = [], [], []
        for i, c in enumerate(clips):
            p, dur, has = clip_audio(c, i, tmp)
            parts.append(p)
            durs.append(dur)
            if not has:
                silent.append(c["file"])
        if d > 0 and any(x <= d for x in durs):
            sys.exit(f"Koi clip transition ({d}s) se chhoti hai. episode.json check karo.")
        joined = Path(tmp) / "joined.wav"
        join(parts, durs, d, joined)
        out.parent.mkdir(parents=True, exist_ok=True)
        if args.raw:
            codec = ["-c:a", "libmp3lame", "-b:a", "192k"] if out.suffix.lower() == ".mp3" else []
            run(["ffmpeg", "-y", "-v", "error", "-i", str(joined), *codec, str(out)])
        else:
            subprocess.run([sys.executable, str(ROOT / "tools" / "polish_voice.py"), str(joined), str(out),
                            "--no-tighten", "--denoise", "-30"], check=True, stdout=subprocess.DEVNULL)

    total = sum(durs) - d * (len(durs) - 1 if d > 0 else 0)
    print(f"Ban gaya: {out}  ({float(probe(out, 'format=duration')):.2f}s, video ~{total:.2f}s)")
    for f in silent:
        print(f"Note: {f} mein awaaz nahi thi, wahan khamoshi hai.")
    print(f'episode.json mein "voice": "{out.as_posix()}" rakho, phir build_video.py.')


if __name__ == "__main__":
    main()
