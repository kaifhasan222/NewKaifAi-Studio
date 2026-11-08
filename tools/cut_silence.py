#!/usr/bin/env python3
"""
cut_silence.py - Flow @me clips ki khamoshi kaat ke jump cuts banana (lip-sync same).

Dikkat: Flow clip 8 sec ki hoti hai, Kaif aksar 4-5 sec bolta hai. Shuru, beech aur aakhir ki
khamoshi video mein reh jaati thi. polish_voice.py ki gap-cutting Flow awaaz par nahi chal sakti
(honth aur awaaz alag ho jaate). Yeh tool VIDEO hi kaat deta hai: har clip ki awaaz mein bolne
wale hisse dhoondh ke usi clip ke chhote tukde (start/duration) bana deta hai. Phir
flow_voice.py aur build_video.py unhi tukdon se chalte hain, to awaaz aur honth saath rehte hain.

Usage (project root se):
    python tools/cut_silence.py episodes/ep004/episode.json
    python tools/cut_silence.py episodes/ep004/episode.json --gap 0.25 --pad 0.07 --db -32
    python tools/cut_silence.py episodes/ep004/episode.json --whisper   # .venv (faster-whisper) se

--whisper: Flow clip mein halki room-tone/hum ho to silencedetect khamoshi nahi pakadta. Yeh flag
Whisper ke word timestamps se pehle shabd se aakhri shabd tak hi rakhta hai, aur shabdon ke beech
lamba gap bhi kaatta hai.

Pehli baar original "clips" ko "clips_src" mein save karta hai. Dobara chalao to "clips_src" se
hi kaatta hai (tune karna safe). Clip par "nocut": true ho to woh clip waise hi rehti hai.
Clip par "cuts": [[a, b], ...] (clip ke seconds) = yeh hissa bhi hatao, jaise doharaya shabd.
Full clip ke jump cut par zoom badalta hai (normal <-> "tight"), taaki cut jhatka na lage.
Split clip mein upar wala card ruk ke dobara shuru nahi hota (card.media_start aage badhta hai).
Phir: python tools/flow_voice.py <episode.json>, phir build_video.py.
"""
import argparse
import copy
import json
import re
import subprocess
import sys
from pathlib import Path


def probe_dur(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def speech_regions(f, start, dur, db, min_sil):
    """[start, start+dur] ke andar bolne wale hisse (clip time mein)."""
    r = subprocess.run(
        ["ffmpeg", "-v", "info", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", f, "-vn",
         "-af", f"highpass=f=90,silencedetect=n={db}dB:d={min_sil}", "-f", "null", "-"],
        capture_output=True, text=True)
    sil, s0 = [], None
    for line in r.stderr.splitlines():
        m = re.search(r"silence_start: ([\d.]+)", line)
        if m:
            s0 = float(m.group(1))
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m and s0 is not None:
            sil.append((s0, float(m.group(1))))
            s0 = None
    if s0 is not None:
        sil.append((s0, dur))
    regs, cur = [], 0.0
    for a, b in sil:
        if a > cur:
            regs.append((cur, a))
        cur = max(cur, b)
    if cur < dur:
        regs.append((cur, dur))
    return [(start + a, start + b) for a, b in regs]


_WM = None


def word_spans(f, start, dur):
    """Whisper words [(a, b)] clip time mein. faster-whisper na ho to None."""
    global _WM
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None
    if _WM is None:
        _WM = WhisperModel("small", compute_type="int8")
    segs, _ = _WM.transcribe(f, language="hi", word_timestamps=True)
    ws = [(w.start, w.end) for sg in segs for w in (sg.words or [])]
    return [(a, b) for a, b in ws if b > start and a < start + dur]


def apply_words(regs, words, gap):
    """Regions ko pehle-aakhri shabd tak seemit karo, aur shabdon ke beech > gap wali khali jagah kaato."""
    if not words:
        return regs
    lo, hi = words[0][0] - 0.06, words[-1][1] + 0.1
    holes = [(b1 + 0.05, a2 - 0.05) for (_, b1), (a2, _) in zip(words, words[1:]) if a2 - b1 > gap + 0.12]
    out = []
    for a, b in regs:
        a, b = max(a, lo), min(b, hi)
        if b <= a:
            continue
        pieces = [(a, b)]
        for h0, h1 in holes:
            nxt = []
            for x, y in pieces:
                if h1 <= x or h0 >= y:
                    nxt.append((x, y))
                else:
                    if h0 > x:
                        nxt.append((x, h0))
                    if h1 < y:
                        nxt.append((h1, y))
            pieces = nxt
        out += pieces
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("--db", type=float, default=-32, help="is se dheemi awaaz = khamoshi (default -32)")
    ap.add_argument("--gap", type=float, default=0.28, help="is se lambi khamoshi kaato (sec, default 0.28)")
    ap.add_argument("--pad", type=float, default=0.07, help="har tukde ke dono taraf saans (sec)")
    ap.add_argument("--min", type=float, default=0.18, help="is se chhota tukda = shor, hatao")
    ap.add_argument("--tail", type=float, default=0.12, help="clip ki aakhri line ke baad thoda ruk (sec)")
    ap.add_argument("--fps", type=int, default=30, help="video fps (tukde isi grid par)")
    ap.add_argument("--whisper", action="store_true", help="Whisper word timing se bhi kaato (room tone wali clips)")
    args = ap.parse_args()

    path = Path(args.episode)
    cfg = json.loads(path.read_text(encoding="utf-8"))
    src = cfg.get("clips_src") or cfg["clips"]
    cfg["clips_src"] = src
    out, before, after = [], 0.0, 0.0
    for c in src:
        f = c["file"]
        start = float(c.get("start") or 0)
        dur = float(c.get("duration") or 0) or probe_dur(f) - start
        before += dur
        if c.get("nocut"):
            out.append(copy.deepcopy(c))
            after += dur
            continue
        regs = speech_regions(f, start, dur, args.db, args.gap)
        if args.whisper:
            ws = word_spans(f, start, dur)
            if ws is None:
                sys.exit("--whisper ke liye faster-whisper chahiye (.venv/bin/python se chalao)")
            regs = apply_words(regs, ws, args.gap)
        for h0, h1 in c.get("cuts", []):
            nxt = []
            for x, y in regs:
                if h1 <= x or h0 >= y:
                    nxt.append((x, y))
                else:
                    if h0 > x:
                        nxt.append((x, h0))
                    if h1 < y:
                        nxt.append((h1, y))
            regs = nxt
        regs = [(a, b) for a, b in regs if b - a >= args.min]
        if not regs:
            print(f"  {Path(f).name}: awaaz nahi mili, clip waise hi rakhi")
            out.append(copy.deepcopy(c))
            after += dur
            continue
        # pad + merge overlapping
        padded = []
        for k, (a, b) in enumerate(regs):
            a = max(start, a - args.pad)
            b = min(start + dur, b + (args.tail if k == len(regs) - 1 else args.pad))
            # manual cut ke andar pad mat failao
            for h0, h1 in c.get("cuts", []):
                if h0 <= a + args.pad <= h1 + 1e-6:
                    a = h1
                if h0 - 1e-6 <= b - args.pad <= h1:
                    b = h0
            if padded and a <= padded[-1][1]:
                padded[-1] = (padded[-1][0], b)
            else:
                padded.append((a, b))
        card_t = float((c.get("card") or {}).get("media_start") or 0)
        # frame grid par align: har tukda poore frames ka ho, warna ~45 tukdon mein video
        # awaaz se khisak jaata hai (lip-sync aur captions bigadte hain)
        padded = [(round(a * args.fps) / args.fps, round(b * args.fps) / args.fps) for a, b in padded]
        padded = [(a, b) for a, b in padded if b - a >= 2 / args.fps]
        for k, (a, b) in enumerate(padded):
            seg = copy.deepcopy(c)
            seg["start"] = round(a, 4)
            seg["duration"] = round(b - a, 4)
            if k > 0:
                seg.pop("transition", None)
                if seg.get("layout") != "split":
                    # jump cut: zoom badlo taaki cut "edit" lage, galti nahi
                    seg["zoom"] = "tight" if k % 2 == 1 else None
                    if seg["zoom"] is None:
                        seg.pop("zoom")
            if seg.get("card") and seg["card"].get("media"):
                seg["card"]["media_start"] = round(card_t, 3)
            card_t += b - a
            out.append(seg)
            after += b - a
        print(f"  {Path(f).name}: {dur:.2f}s -> {sum(b - a for a, b in padded):.2f}s ({len(padded)} tukde)")
    cfg["clips"] = out
    path.write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Khamoshi kati: {before:.1f}s -> {after:.1f}s. Ab: python tools/flow_voice.py {path.as_posix()}")


if __name__ == "__main__":
    sys.exit(main())
