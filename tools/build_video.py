#!/usr/bin/env python3
"""
build_video.py - Flow clips + voice + music + sfx + captions -> finished 9:16 short.

Usage (project root se chalao):
    python tools/build_video.py episodes/ep001/episode.json

Sab paths episode.json mein project root ke relative hote hain.
Full clip par optional "zoom": "punch" (hook snap-in), "slow" (dheema push-in) ya "tight" (seedha 1.12x, jump cut ke liye).
Har clip par optional "transition": us clip mein aane wala xfade type (jaise "smoothup", "circleopen"); duration global rehti hai.
Split clip ke "card" mein optional "theme": "clean" (Clean Tech: off-white bar, blue accent, dark title)
ya "chalk" (Chalk Talk: board green bar, yellow chalk accent, chalk-white title)
ya "creator" (Creator Motion Graphics: near-black bar, yellow accent, white title).
Top-level "logo": {"file": "brand/youtube/icon_round_240.png", "x": 842, "y": 1682, "w": 116} = channel icon, Gemini sparkle (center 900,1740) ke upar; clip par zoom se pehle lagta hai.
Overlay par "kinetic": true = bade Anton caps word-by-word slam; *shabd* yellow serif accent.
Mac aur Windows dono par chalta hai (sirf ffmpeg + Python chahiye).
"""
import json
import re
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


LOGO = None  # main() cfg["logo"] se bharta hai


def _logo_overlay(src, dst):
    """Channel icon ko [src] par overlay karke [dst] label deta hai (movie= source filter)."""
    lw = int(LOGO.get("w", 116))
    return (f"movie={Path(LOGO['file']).as_posix()},scale={lw}:{lw},format=rgba[lg];"
            f"{src}[lg]overlay={int(LOGO.get('x', 842))}:{int(LOGO.get('y', 1682))}:format=auto{dst}")


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


def _trim_prefix(start, dur, fps=30):
    """Keyframe seek nahi: mouth voice ke usi second par rahe.
    Pehle output fps par lao, phir trim: jump cut ke chhote tukde exact frames ke bante hain,
    warna 24fps source par har tukda thoda lamba/chhota hota hai aur video awaaz se khisakta hai."""
    return (f"fps={fps},trim=start={float(start or 0):.4f}:duration={float(dur):.4f},"
            "setpts=PTS-STARTPTS,")


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
    # "theme": "clean" = Clean Tech bar (off-white, blue accent, dark title).
    # "theme": "chalk" = Chalk Talk bar (board green, yellow chalk accent, chalk-white title). Default = dark + orange.
    bar_bg, accent, title_color = {
        "clean": ("0xF6F5F1", "0x2563EB", "0x111827"),
        "chalk": ("0x1F3B2D", "0xFACC15", "0xF1F5EE"),
        "creator": ("0x0B0B0D", "0xFFD60A", "0xF5F4F0"),
    }.get(card.get("theme"), ("0x070709", ORANGE, "white"))

    def tf(key, text):
        return _textfile(tmp, f"c{idx}_{key}.txt", text)

    graph = (
        f"[0:v]{_trim_prefix(clip.get('start'), dur)}"
        f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,"
        f"crop={w}:{bot_h}:(iw-{w})/2:36,fps={fps},setsar=1,format=yuv420p[face];"
        f"[1:v]scale={w}:{media_h}:force_original_aspect_ratio=increase,"
        f"crop={w}:{media_h},fps={fps},setsar=1,format=yuv420p[mv];"
        "[2:v]format=yuv420p"
        f",drawbox=x=0:y=0:w={w}:h=10:color={accent}:t=fill"
        + "," + _drawtext(FONT_DISPLAY, tf("kicker", card["kicker"]), 36, accent, "(w-text_w)/2", 40)
        + "," + _drawtext(FONT_DISPLAY, tf("title", title), title_size, title_color, "(w-text_w)/2", 92)
        + "[bar];[bar][mv]vstack=inputs=2[top];[top][face]vstack=inputs=2,format=yuv420p"
        + ("[vv];" + _logo_overlay("[vv]", "[v]") if LOGO else "[v]")
    )
    cmd = _src(clip)
    cmd += ["-stream_loop", "-1"]
    if card.get("media_start"):
        cmd += ["-ss", str(card["media_start"])]
    cmd += ["-t", f"{dur:.3f}", "-i", card["media"]]
    cmd += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", f"color=c={bar_bg}:s={w}x{bar_h}:r={fps}"]
    cmd += ["-filter_complex", graph, "-map", "[v]", "-frames:v", str(round(dur * fps))]  # +1 frame drift rokta hai
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
    cmd += ["-filter_complex", graph, "-map", "[v]", "-frames:v", str(round(dur * fps))]  # +1 frame drift rokta hai
    return _encode(cmd, out)


def _zoom(kind, w, h, fps):
    """Full clips par motion. "punch" = shuru mein 0.3s ka zoom-in snap, "slow" = dheema push-in."""
    if not kind:
        return ""
    n = max(1, int(0.3 * fps))
    if kind == "tight":  # jump cut: seedha andar, zoompan ki zaroorat nahi
        cw, ch = int(w / 1.12) // 2 * 2, int(h / 1.12) // 2 * 2
        return f",crop={cw}:{ch}:(iw-{cw})/2:(ih-{ch})/2*0.7,scale={w}:{h},setsar=1"
    z = {"punch": f"if(lt(on,{n}),1.16-0.16*on/{n},1)", "slow": "min(1+0.0009*on,1.12)"}[kind]
    return (f",zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d=1:s={w}x{h}:fps={fps}")


def render_clip(clip, idx, w, h, fps, tmp):
    """Har clip ko 1080x1920, same fps, bina audio ke convert karta hai."""
    out = tmp / f"clip{idx}.mp4"
    if clip.get("layout") == "split":
        return render_split(clip, idx, w, h, fps, tmp)
    dur = float(clip.get("duration") or 0)
    trim = _trim_prefix(clip.get("start"), dur) if dur else ""
    vf = (f"{trim}scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h},"
          f"setsar=1,fps={fps},format=yuv420p")
    tail = _zoom(clip.get("zoom"), w, h, fps)
    if clip.get("label"):
        tf = _textfile(tmp, f"lab{idx}.txt", clip["label"])
        tail += "," + _drawtext(FONT_DISPLAY, tf, 54, "white", "(w-text_w)/2", 188)
        tail += ":box=1:boxcolor=0x111111@0.9:boxborderw=18"
    if LOGO:
        # icon zoom se pehle: Gemini ka sparkle zoom ke saath khisakta hai, icon uske saath khisakta hai
        graph = f"[0:v]{vf}[b];" + _logo_overlay("[b]", "[o]") + ";[o]null" + tail + "[v]"
        cmd = _src(clip) + ["-filter_complex", graph, "-map", "[v]"]
    else:
        cmd = _src(clip) + ["-vf", vf + tail]
    return _encode(cmd, out)


def join_clips(files, trans, tmp, types=None):
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
                f"{last}[{i}:v]xfade=transition={(types or [None] * n)[i] or trans.get('type', 'fade')}:"
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


def _kinetic_line(o):
    """Creator style: har shabd 0.13s ke gap par slam (1.45x -> 1x), *shabd* = yellow serif accent."""
    per = float(o.get("per", 0.13))
    words = o["text"].split()
    parts = []
    for k, wd in enumerate(words):
        t0 = int(k * per * 1000)
        acc = wd.startswith("*") and wd.endswith("*")
        wd = wd.strip("*")
        look = "\\fnDM Serif Display\\i1\\c&H0AD6FF&\\fs146" if acc else "\\fnAnton\\i0\\c&HF0F4F5&\\fs132"
        parts.append(
            f"{{{look}\\alpha&HFF&\\fscx145\\fscy145"
            f"\\t({t0},{t0 + 1},\\alpha&H00&)\\t({t0},{t0 + 170},0.6,\\fscx100\\fscy100)}}{wd}"
        )
    y = {"top": 250, "middle": 860, "bottom": 1250}.get(o.get("position", "top"), 250)
    return (f"Dialogue: 1,{ass_time(o['start'])},{ass_time(o['end'])},Kin,,0,0,{y},,"
            f"{{\\fad(0,200)}}" + " ".join(parts))


def write_overlays_ass(overlays, w, h, path):
    """Title/hook text overlays (animated fade) ASS subtitle file ke through."""
    head = (
        f"[Script Info]\nScriptType: v4.00+\nPlayResX: {w}\nPlayResY: {h}\n\n"
        "[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,"
        "BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,"
        "Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n"
        "Style: Top,Arial,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,5,0,8,60,60,260,1\n"
        "Style: Mid,Arial,110,&H0000D7FF,&H0000D7FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,6,0,5,60,60,0,1\n"
        "Style: Kin,Anton,132,&H00F0F4F5,&H00F0F4F5,&H000D0B0B,&H99000000,0,0,0,0,100,100,1,0,1,7,4,8,50,50,250,1\n\n"
        "[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n"
    )
    lines = []
    for o in overlays:
        if o.get("kinetic"):
            lines.append(_kinetic_line(o))
            continue
        style = "Mid" if o.get("position") == "middle" else "Top"
        text = o["text"].replace("\n", "\\N")
        lines.append(
            f"Dialogue: 0,{ass_time(o['start'])},{ass_time(o['end'])},{style},,0,0,0,,"
            f"{{\\fad(150,250)\\fscx70\\fscy70\\t(0,180,\\fscx100\\fscy100)}}{text}"
        )
    path.write_text(head + "\n".join(lines) + "\n", encoding="utf-8")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    cfg = {**DEFAULTS, **json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))}
    global LOGO
    LOGO = cfg.get("logo")
    w, h = (int(x) for x in cfg["size"].split("x"))
    out = Path(cfg["output"])
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp_overlay = Path(".build_overlays.ass")  # cwd mein rakhte hain: Windows path/colon issue se bachne ke liye

    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        print("1/3 clips normalize kar raha hoon...")
        files = [render_clip(c, i, w, h, cfg["fps"], tmp) for i, c in enumerate(cfg["clips"])]
        print("2/3 clips jod raha hoon...")
        video = join_clips(files, cfg["transition"], tmp, [c.get("transition") for c in cfg["clips"]])
        vdur = duration(video)

        voice = cfg.get("voice")
        total = duration(voice) + cfg["tail"] if voice else vdur

        # ---- video filter chain: pad -> overlays -> captions
        vf = []
        if total > vdur:
            vf.append(f"tpad=stop_mode=clone:stop_duration={total - vdur + 0.1:.3f}")
        if cfg.get("overlays"):
            write_overlays_ass(cfg["overlays"], w, h, tmp_overlay)
            vf.append(f"subtitles={tmp_overlay.as_posix()}:fontsdir=assets/fonts")
        if cfg.get("captions"):
            cap = Path(cfg["captions"])
            # .ass apna style laata hai (pill, yellow word). .srt par purana force_style.
            if cap.suffix.lower() == ".ass":
                vf.append(f"subtitles={cap.as_posix()}:fontsdir=assets/fonts")
            else:
                vf.append(f"subtitles={cap.as_posix()}:force_style='{cfg['caption_style']}'")
        vchain = "[0:v]" + (",".join(vf) if vf else "null") + "[vout]"


        # ---- audio graph: voice + ducked music + sfx
        inputs = ["-i", video]
        achain, mix = [], []
        idx = 1
        fmt = "aformat=sample_rates=44100:channel_layouts=stereo"
        music = cfg.get("music")
        if voice:
            inputs += ["-i", voice]
            if music:  # [vsc] sirf music ducking ke liye; bina music ke split ka output khaali reh jaata
                achain.append(f"[{idx}:a]{fmt},apad,asplit=2[vo][vsc]")  # apad: tail mein music chalta rahe
            else:
                achain.append(f"[{idx}:a]{fmt},apad[vo]")
            mix.append("[vo]")
            idx += 1
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
        cmd += ["-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
        print("3/3 final render (captions + audio mix)...")
        run(cmd)

    tmp_overlay.unlink(missing_ok=True)
    fix_loudness(out, cfg["loudness"])
    print(f"Done -> {out}  ({total:.1f}s)")


def fix_loudness(out, spec):
    """Bahut saare SFX ke saath single-pass loudnorm target se hat jaata hai (jaise -13 LUFS).
    Final file naap ke audio par seedha gain + limiter, video copy (dobara encode nahi)."""
    target = float(re.search(r"I=(-?[\d.]+)", spec).group(1))
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(out), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    if not m:
        return
    got = float(m[-1])
    if abs(got - target) <= 1.0:
        return
    gain = target - got
    tmpf = Path(out).with_suffix(".loud.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-i", out, "-c:v", "copy",
         "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:attack=5:release=50",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", tmpf])
    tmpf.replace(out)
    print(f"loudness {got:.1f} -> ~{target:.0f} LUFS (gain {gain:+.1f} dB)")


if __name__ == "__main__":
    main()
