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


FONT_DISPLAY = "assets/fonts/BebasNeue-Regular.ttf"
FONT_BODY = "assets/fonts/Poppins-Bold.ttf"
ORANGE = "0xFF5A1F"
CARD_BG = "0x141416"
MUTED = "0xB5B5B5"


def _textfile(tmp, name, text):
    path = tmp / name
    path.write_text(text, encoding="utf-8")
    return path.as_posix()


def _drawtext(font, textfile, size, color, x, y):
    return (
        f"drawtext=fontfile={font}:textfile={textfile}:fontsize={size}:"
        f"fontcolor={color}:x={x}:y={y}:expansion=none"
    )


def _encode(cmd, out):
    cmd += ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", out]
    run(cmd)
    return out


def _trim_prefix(start, dur):
    """Keyframe seek nahi: mouth voice ke usi second par rahe."""
    return f"trim=start={float(start or 0):.3f}:duration={float(dur):.3f},setpts=PTS-STARTPTS,"


def _src(clip):
    return ["ffmpeg", "-y", "-v", "error", "-i", clip["file"]]


def render_media_split(clip, idx, w, h, fps, tmp):
    """Upar b-roll ya motion graphic, neeche wahi face jo us second bol raha hai."""
    out = tmp / f"clip{idx}.mp4"
    dur = float(clip["duration"])
    card = clip["card"]
    top_h = 1040
    bot_h = h - top_h
    bar_h = 230
    media_h = top_h - bar_h
    title = card["title"]
    title_size = 118 if len(title) <= 8 else 84

    def tf(key, text):
        return _textfile(tmp, f"c{idx}_{key}.txt", text)

    graph = (
        f"[0:v]{_trim_prefix(clip.get('start'), dur)}"
        f"scale={w}:{h}:force_original_aspect_ratio=increase,"
        f"crop={w}:{bot_h}:(iw-{w})/2:36,fps={fps},setsar=1,format=yuv420p[face];"
        f"[1:v]scale={w}:{media_h}:force_original_aspect_ratio=increase,"
        f"crop={w}:{media_h},fps={fps},setsar=1,format=yuv420p[mv];"
        "[2:v]format=yuv420p"
        f",drawbox=x=0:y=0:w={w}:h=10:color={ORANGE}:t=fill"
        + "," + _drawtext(FONT_DISPLAY, tf("kicker", card["kicker"]), 36, ORANGE, "(w-text_w)/2", 40)
        + "," + _drawtext(FONT_DISPLAY, tf("title", title), title_size, "white", "(w-text_w)/2", 92)
        + "[bar];[bar][mv]vstack=inputs=2[top];[top][face]vstack=inputs=2,format=yuv420p[v]"
    )
    cmd = _src(clip)
    cmd += ["-stream_loop", "-1"]
    if card.get("media_start"):
        cmd += ["-ss", str(card["media_start"])]
    cmd += ["-t", f"{dur:.3f}", "-i", card["media"]]
    cmd += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", f"color=c=0x070709:s={w}x{bar_h}:r={fps}"]
    cmd += ["-filter_complex", graph, "-map", "[v]"]
    return _encode(cmd, out)


def render_split(clip, idx, w, h, fps, tmp):
    """Upar dark stat-card, neeche face. Reference jaisa split, apna content."""
    if clip.get("card", {}).get("media"):
        return render_media_split(clip, idx, w, h, fps, tmp)
    out = tmp / f"clip{idx}.mp4"
    dur = float(clip["duration"])
    card = clip["card"]
    top_h = 1040
    bot_h = h - top_h
    title = card["title"]
    title_size = 148 if len(title) <= 7 else 108
    sub_y = 128 + title_size + 6
    cards_y = sub_y + 64
    foot = card.get("foot")
    foot_h = 118 if foot else 0
    foot_gap = 28 if foot else 0
    bottom_pad = 40
    cards_h = top_h - cards_y - bottom_pad - foot_h - foot_gap
    gap = 36
    cw = (w - gap * 3) // 2

    def tf(key, text):
        return _textfile(tmp, f"c{idx}_{key}.txt", text)

    graph = (
        f"[0:v]{_trim_prefix(clip.get('start'), dur)}"
        f"scale={w}:{h}:force_original_aspect_ratio=increase,"
        f"crop={w}:{bot_h}:(iw-{w})/2:36,fps={fps},setsar=1,format=yuv420p[face];"
        "[1:v]format=yuv420p"
        f",drawbox=x=0:y=0:w={w}:h=10:color={ORANGE}:t=fill"
        + "," + _drawtext(FONT_DISPLAY, tf("kicker", card["kicker"]), 38, ORANGE, "(w-text_w)/2", 48)
        + "," + _drawtext(FONT_DISPLAY, tf("title", title), title_size, "white", "(w-text_w)/2", 112)
        + "," + _drawtext(FONT_BODY, tf("sub", card["subtitle"]), 32, MUTED, "(w-text_w)/2", sub_y)
    )
    boxes = (
        (gap, "left_value", "left_label"),
        (gap * 2 + cw, "right_value", "right_label"),
    )
    for x, vk, lk in boxes:
        val = card[vk]
        vsize = 92 if len(val) <= 4 else 58 if len(val) <= 8 else 42
        graph += (
            f",drawbox=x={x}:y={cards_y}:w={cw}:h={cards_h}:color={CARD_BG}:t=fill"
            f",drawbox=x={x}:y={cards_y}:w={cw}:h=8:color={ORANGE}:t=fill"
            + "," + _drawtext(FONT_DISPLAY, tf(vk, val), vsize, ORANGE, f"{x}+({cw}-text_w)/2", f"{cards_y}+({cards_h}/2)-{vsize}")
            + "," + _drawtext(FONT_BODY, tf(lk, card[lk]), 28, "white", f"{x}+({cw}-text_w)/2", f"{cards_y}+({cards_h}/2)+18")
        )
    if foot:
        fy = cards_y + cards_h + foot_gap
        graph += (
            f",drawbox=x={gap}:y={fy}:w={w - gap * 2}:h={foot_h}:color={CARD_BG}:t=fill"
            f",drawbox=x={gap}:y={fy}:w=8:h={foot_h}:color={ORANGE}:t=fill"
            + "," + _drawtext(FONT_DISPLAY, tf("foot", foot), 52, "white", "(w-text_w)/2", fy + 32)
        )
    graph += "[top];[top][face]vstack=inputs=2,format=yuv420p[v]"
    cmd = _src(clip)
    cmd += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", f"color=c=0x070709:s={w}x{top_h}:r={fps}"]
    cmd += ["-filter_complex", graph, "-map", "[v]"]
    return _encode(cmd, out)


def render_clip(clip, idx, w, h, fps, tmp):
    """Har clip ko 1080x1920, same fps, bina audio ke convert karta hai."""
    out = tmp / f"clip{idx}.mp4"
    if clip.get("layout") == "split":
        return render_split(clip, idx, w, h, fps, tmp)
    dur = float(clip.get("duration") or 0)
    trim = _trim_prefix(clip.get("start"), dur) if dur else ""
    vf = (f"{trim}scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
          f"setsar=1,fps={fps},format=yuv420p")
    if clip.get("label"):
        tf = _textfile(tmp, f"lab{idx}.txt", clip["label"])
        vf += "," + _drawtext(FONT_DISPLAY, tf, 54, "white", "(w-text_w)/2", 188)
        vf += ":box=1:boxcolor=0x111111@0.9:boxborderw=18"
    cmd = _src(clip) + ["-vf", vf]
    return _encode(cmd, out)


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
        files = [render_clip(c, i, w, h, cfg["fps"], tmp) for i, c in enumerate(cfg["clips"])]
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
