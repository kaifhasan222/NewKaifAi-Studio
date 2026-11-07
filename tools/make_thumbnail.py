#!/usr/bin/env python3
"""
make_thumbnail.py - Shorts/Reels thumbnail (1080x1920) options A/B/C, sirf ffmpeg.

Usage (project root se):
    python3 tools/make_thumbnail.py episodes/ep001/thumb.json
    python3 tools/make_thumbnail.py --frames episodes/ep001/raw-clips/ep001_01.mp4   # frame chunne ka contact sheet

thumb.json:
{
  "episode": "ep001",
  "options": {
    "A": {"layout": "face", "face": {"file": "...mp4", "t": 0.4, "zoom": 1.1, "y": 0.0},
          "lines": [{"text": "EK LINE =", "color": "white"}, {"text": "DUNIYA?", "color": "yellow", "size": 260}]},
    "B": {"layout": "split", "media": {"file": "...mp4", "t": 5.5}, "face": {...}, "lines": [...]},
    "C": {"layout": "before_after", "before": {"file": "...", "t": 1}, "after": {"file": "...", "t": 6},
          "face": {...}, "lines": [...]},
    "D": {"layout": "image", "image": {"file": "episodes/ep001/thumbs/flow_1.png"}, "text_y": 1150,
          "lines": [...]}      # Flow se bani bina-text image + text (MrBeast-style flow)
  }
}
face.zoom: >1 andar zoom; face.y: -0.2..0.2 frame ko upar/neeche khiskao. top_h: upar wale visual ki height (default 860). Rules: prompts/thumbnail-guide.md
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

W, H = 1080, 1920
FONT = "assets/fonts/BebasNeue-Regular.ttf"
COLORS = {"white": "white", "yellow": "0xFACC15", "cyan": "0x22D3EE", "orange": "0xFF5A1F"}
NAVY = "0x0B1020"


def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode:
        sys.exit("FFMPEG ERROR:\n" + r.stderr[-2500:])


def grab(src, t, w, h, out, zoom=1.0, y=0.0):
    """Clip ke ek frame ko w x h mein cover-crop karta hai."""
    zw, zh = int(w * zoom), int(h * zoom)
    oy = f"(ih-{h})/2+{y}*ih"
    vf = (f"scale={zw}:{zh}:force_original_aspect_ratio=increase,"
          f"crop={w}:{h}:(iw-{w})/2:max(0\\,min(ih-{h}\\,{oy}))")
    run(["ffmpeg", "-y", "-v", "error", "-ss", t, "-i", src, "-frames:v", 1, "-vf", vf, out])


def text_filters(lines, tmp, y0, key):
    """Har line alag drawtext, center, mota border. Return (filters, end_y)."""
    fs, y = [], y0
    for i, ln in enumerate(lines):
        size = int(ln.get("size", 200))
        tf = Path(tmp) / f"{key}_{i}.txt"
        tf.write_text(ln["text"], encoding="utf-8")
        col = COLORS.get(ln.get("color", "white"), ln.get("color", "white"))
        fs.append(f"drawtext=fontfile={FONT}:textfile={tf.as_posix()}:fontsize={size}:fontcolor={col}:"
                  f"borderw={max(8, size // 18)}:bordercolor=black:shadowx=0:shadowy=8:shadowcolor=black@0.6:"
                  f"x=(w-text_w)/2:y={y}")
        y += int(size * 0.92)
    return fs, y


def build(opt, key, tmp, out):
    lay = opt["layout"]
    f = opt.get("face", {})
    layers, filt = [], []
    if lay == "image":
        # Flow/AI se bani poori 9:16 image (bina text), upar text. Text middle third mein.
        img = opt["image"]
        bg = Path(tmp) / f"{key}_img.png"
        if str(img["file"]).lower().endswith((".mp4", ".mov")):
            grab(img["file"], img.get("t", 0), W, H, bg, img.get("zoom", 1.0), img.get("y", 0.0))
        else:
            run(["ffmpeg", "-y", "-v", "error", "-i", img["file"], "-vf",
                 f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", bg])
        layers.append(bg)
        ty = opt.get("text_y", 1150)
        tx, end_y = text_filters(opt["lines"], tmp, ty, key)
        if opt.get("text_bar", False):
            filt.append(f"drawbox=x=0:y={ty - 40}:w={W}:h={end_y - ty + 90}:color=black@0.4:t=fill")
        graph = ",".join(["[0:v]format=rgb24"] + filt + tx) + "[v]"
    elif lay == "face":
        grab(f["file"], f["t"], W, H, Path(tmp) / f"{key}_face.png", f.get("zoom", 1.0), f.get("y", 0.0))
        layers.append(Path(tmp) / f"{key}_face.png")
        filt.append("[0:v]format=rgb24")
        # chehra upar hota hai, text chest par (grid box ke andar, Shorts UI zone se upar)
        ty = opt.get("text_y", 1000)
        tx, end_y = text_filters(opt["lines"], tmp, ty, key)
        filt.append(f"drawbox=x=0:y={ty - 50}:w={W}:h={end_y - ty + 110}:color=black@0.45:t=fill")
        graph = ",".join(filt + tx) + "[v]"
    else:
        top_h = int(opt.get("top_h", 860))
        grab(f["file"], f["t"], W, H - top_h, Path(tmp) / f"{key}_face.png", f.get("zoom", 1.0), f.get("y", 0.0))
        if lay == "split":
            m = opt["media"]
            grab(m["file"], m["t"], W, top_h, Path(tmp) / f"{key}_top.png", m.get("zoom", 1.0), m.get("y", 0.0))
            layers += [Path(tmp) / f"{key}_top.png", Path(tmp) / f"{key}_face.png"]
            top = "[0:v]format=rgb24[top]"
            fi = 1
        else:  # before_after
            for side in ("before", "after"):
                s = opt[side]
                grab(s["file"], s["t"], W // 2 - 6, top_h, Path(tmp) / f"{key}_{side}.png", s.get("zoom", 1.0))
            layers += [Path(tmp) / f"{key}_before.png", Path(tmp) / f"{key}_after.png",
                       Path(tmp) / f"{key}_face.png"]
            atf = Path(tmp) / f"{key}_arrow.txt"
            atf.write_text(">", encoding="utf-8")
            top = (f"[0:v][1:v]hstack=inputs=2,pad={W}:{top_h}:(ow-iw)/2:0:color={NAVY},format=rgb24,"
                   f"drawbox=x={W // 2 - 70}:y={top_h // 2 - 70}:w=140:h=140:color=0xFACC15:t=fill,"
                   f"drawtext=fontfile={FONT}:textfile={atf.as_posix()}:fontsize=170:fontcolor=black:"
                   f"x=(w-text_w)/2:y={top_h // 2}-text_h/2[top]")
            fi = 2
        tx, _ = text_filters(opt["lines"], tmp, opt.get("text_y", top_h - 200), key)
        graph = (f"{top};[top][{fi}:v]vstack=inputs=2,format=rgb24,"
                 f"drawbox=x=0:y={top_h - 230}:w={W}:h=470:color=black@0.55:t=fill,"
                 f"drawbox=x=0:y={top_h - 4}:w={W}:h=8:color=0xFF5A1F:t=fill,"
                 + ",".join(tx) + "[v]")
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for p in layers:
        cmd += ["-i", p]
    cmd += ["-filter_complex", graph, "-map", "[v]", "-frames:v", 1, "-q:v", 2, out]
    run(cmd)


def preview(files, out):
    """Har option ke upar 3:4 grid crop aur Shorts UI zone dikhata hai, side by side."""
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for p in files:
        cmd += ["-i", p]
    n = len(files)
    parts = []
    for i in range(n):
        parts.append(f"[{i}:v]drawbox=x=0:y=240:w={W}:h=1440:color=0x22D3EE:t=6,"
                     f"drawbox=x=0:y=1536:w={W}:h={H - 1536}:color=red@0.35:t=fill,scale=360:-1[p{i}]")
    graph = ";".join(parts) + ";" + "".join(f"[p{i}]" for i in range(n)) + f"hstack=inputs={n}[v]"
    cmd += ["-filter_complex", graph, "-map", "[v]", "-frames:v", 1, "-q:v", 3, out]
    run(cmd)


def frames_sheet(clip):
    out = Path("output") / (Path(clip).stem + "_frames.jpg")
    out.parent.mkdir(exist_ok=True)
    vf = ("fps=4,scale=216:-1,drawtext=fontfile=" + FONT +
          ":text='%{pts\\:hms}':x=6:y=6:fontsize=30:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=8x4")
    run(["ffmpeg", "-y", "-v", "error", "-i", clip, "-vf", vf, "-frames:v", 1, out])
    print(f"Frames sheet -> {out}  (har 0.25s, upar time likha hai)")


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--frames":
        return frames_sheet(sys.argv[2])
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    ep = cfg["episode"]
    Path("output").mkdir(exist_ok=True)
    outs = []
    with tempfile.TemporaryDirectory() as tmp:
        for key, opt in cfg["options"].items():
            out = Path("output") / f"{ep}_thumb_{key}.jpg"
            build(opt, key, tmp, out)
            outs.append(out)
            print(f"{key} -> {out}")
    prev = Path("output") / f"{ep}_thumbs_preview.jpg"
    preview(outs, prev)
    print(f"Preview (cyan = 3:4 grid box, laal = Shorts UI zone) -> {prev}")


if __name__ == "__main__":
    main()
