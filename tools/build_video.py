#!/usr/bin/env python3
"""
build_video.py - Flow clips + voice + music + sfx + captions -> finished 9:16 short.

Usage (project root se chalao):
    python tools/build_video.py episodes/ep001/episode.json

Sab paths episode.json mein project root ke relative hote hain.
Mac aur Windows dono par chalta hai (sirf ffmpeg + Python chahiye).
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULTS = {
    "size": "1080x1920",
    "fps": 30,
    "transition": {"type": "fade", "duration": 0.25},  # duration 0 = hard cut
    "tail": 0.6,  # voice ke baad extra seconds
    "music_volume": 0.12,
    "caption_style": (
        "Fontname=Arial,Fontsize=16,Bold=1,PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,Outline=1.6,Shadow=0,Alignment=2,MarginV=70"
    ),
    "loudness": "I=-16:TP=-1.5:LRA=11",
}


def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR:\n" + r.stderr[-2500:])
        sys.exit(1)
    return r


def duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", path])
    return float(r.stdout.strip())


def normalize(clip, idx, w, h, fps, tmp):
    """Har clip ko 1080x1920, same fps, bina audio ke convert karta hai."""
    out = tmp / f"clip{idx}.mp4"
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if clip.get("start"):
        cmd += ["-ss", clip["start"]]
    cmd += ["-i", clip["file"]]
    if clip.get("duration"):
        cmd += ["-t", clip["duration"]]
    vf = (f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
          f"setsar=1,fps={fps},format=yuv420p")
    cmd += ["-vf", vf, "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "17", out]
    run(cmd)
    return out


def join_clips(files, trans, tmp):
    out = tmp / "joined.mp4"
    n = len(files)
    if n == 1:
        return files[0]
    d = float(trans.get("duration", 0))
    durs = [duration(f) for f in files]
    inputs = []
    for f in files:
        inputs += ["-i", f]
    if d <= 0:
        chain = "".join(f"[{i}:v]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
    else:
        parts, last, acc = [], "[0:v]", durs[0]
        for i in range(1, n):
            lab = f"[x{i}]" if i < n - 1 else "[v]"
            parts.append(
                f"{last}[{i}:v]xfade=transition={trans.get('type', 'fade')}:"
                f"duration={d}:offset={acc - d:.3f}{lab}"
            )
            last = lab
            acc += durs[i] - d
        chain = ";".join(parts)
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", chain, "-map", "[v]",
         "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", out])
    return out


def ass_time(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def write_overlays_ass(overlays, w, h, path):
    """Title/hook text overlays (animated fade) ASS subtitle file ke through."""
    head = (
        f"[Script Info]\nScriptType: v4.00+\nPlayResX: {w}\nPlayResY: {h}\n\n"
        "[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,"
        "BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,"
        "Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n"
        "Style: Top,Arial,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,5,0,8,60,60,260,1\n"
        "Style: Mid,Arial,110,&H0000D7FF,&H0000D7FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,6,0,5,60,60,0,1\n\n"
        "[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n"
    )
    lines = []
    for o in overlays:
        style = "Mid" if o.get("position") == "middle" else "Top"
        text = o["text"].replace("\n", "\\N")
        lines.append(
            f"Dialogue: 0,{ass_time(o['start'])},{ass_time(o['end'])},{style},,0,0,0,,"
            f"{{\\fad(250,250)}}{text}"
        )
    path.write_text(head + "\n".join(lines) + "\n", encoding="utf-8")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    cfg = {**DEFAULTS, **json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))}
    w, h = (int(x) for x in cfg["size"].split("x"))
    out = Path(cfg["output"])
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp_overlay = Path(".build_overlays.ass")  # cwd mein rakhte hain: Windows path/colon issue se bachne ke liye

    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        print("1/3 clips normalize kar raha hoon...")
        files = [normalize(c, i, w, h, cfg["fps"], tmp) for i, c in enumerate(cfg["clips"])]
        print("2/3 clips jod raha hoon...")
        video = join_clips(files, cfg["transition"], tmp)
        vdur = duration(video)

        voice = cfg.get("voice")
        total = duration(voice) + cfg["tail"] if voice else vdur

        # ---- video filter chain: pad -> overlays -> captions
        vf = []
        if total > vdur:
            vf.append(f"tpad=stop_mode=clone:stop_duration={total - vdur + 0.1:.3f}")
        if cfg.get("overlays"):
            write_overlays_ass(cfg["overlays"], w, h, tmp_overlay)
            vf.append(f"subtitles={tmp_overlay.as_posix()}")
        if cfg.get("captions"):
            vf.append(
                f"subtitles={Path(cfg['captions']).as_posix()}:force_style='{cfg['caption_style']}'"
            )
        vchain = "[0:v]" + (",".join(vf) if vf else "null") + "[vout]"

        # ---- audio graph: voice + ducked music + sfx
        inputs = ["-i", video]
        achain, mix = [], []
        idx = 1
        fmt = "aformat=sample_rates=44100:channel_layouts=stereo"
        if voice:
            inputs += ["-i", voice]
            achain.append(f"[{idx}:a]{fmt},apad,asplit=2[vo][vsc]")  # apad: tail mein music chalta rahe
            mix.append("[vo]")
            idx += 1
        music = cfg.get("music")
        if music:
            inputs += ["-stream_loop", "-1", "-i", music["file"]]
            mv = music.get("volume", cfg["music_volume"])
            achain.append(f"[{idx}:a]{fmt},volume={mv}[mu]")
            if voice:  # voice bolte waqt music apne aap dheemi
                achain.append("[mu][vsc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=450[mud]")
                mix.append("[mud]")
            else:
                mix.append("[mu]")
            idx += 1
        for k, s in enumerate(cfg.get("sfx", [])):
            inputs += ["-i", s["file"]]
            ms = int(s["at"] * 1000)
            achain.append(f"[{idx}:a]{fmt},volume={s.get('volume', 0.8)},adelay={ms}|{ms}[s{k}]")
            mix.append(f"[s{k}]")
            idx += 1

        cmd = ["ffmpeg", "-y", "-v", "error", *inputs]
        if mix:
            n = len(mix)
            graph = ";".join(
                [vchain] + achain
                + [f"{''.join(mix)}amix=inputs={n}:duration=longest:dropout_transition=0,"
                   f"volume={n},loudnorm={cfg['loudness']}[aout]"]
            )
            cmd += ["-filter_complex", graph, "-map", "[vout]", "-map", "[aout]"]
        else:
            cmd += ["-filter_complex", vchain, "-map", "[vout]"]
        cmd += ["-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
        print("3/3 final render (captions + audio mix)...")
        run(cmd)

    tmp_overlay.unlink(missing_ok=True)
    print(f"Done -> {out}  ({total:.1f}s)")


if __name__ == "__main__":
    main()
