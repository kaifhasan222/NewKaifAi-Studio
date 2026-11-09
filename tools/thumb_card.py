#!/usr/bin/env python3
"""
thumb_card.py - Clean, premium thumbnail text (1080x1920) on a ready image. Pillow (.venv).

Look: clean bold rounded sans (Poppins Bold), soft shadow (no thick black outline),
one phrase in a red highlight box, or premium gold text in a dark glossy box with a gold border.
Only the typography style is borrowed from popular tech thumbnails; no logos, faces or content copied.

Usage (project root se):
    .venv/bin/python tools/thumb_card.py episodes/ep011/thumb_card.json

thumb_card.json:
{
  "episode": "ep011",
  "options": {
    "A": {"image": "episodes/ep011/thumbs/gemini_real_v2.png",
          "shift_y": 180,              # image ko neeche khiskao (upar text ke liye jagah), default 0
          "top_shade": 0.75,           # upar kaala gradient (0..1), text saaf dikhe
          "blocks": [
            {"type": "plain", "text": "GALAT UPI?", "size": 130, "y": 250},
            {"type": "box", "text": "Paisa wapas kaise?", "size": 100, "y": 420, "fill": "#E11D2E", "rotate": -2},
            {"type": "gold", "text": "4 STEP", "size": 150, "y": 600}
          ]}
  }
}
Block keys: text, size, y (top), x ("center" ya px left), color (plain ke liye), fill (box), rotate (deg), max_w.
Output: output/<episode>_thumb_<K>.jpg + output/<episode>_thumbs_preview.jpg (safe-zone lines ke saath).
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FONT = "assets/fonts/Poppins-Bold.ttf"
GOLD_TOP, GOLD_BOT = (255, 236, 170), (214, 150, 40)


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def fit_font(text, size, max_w):
    while True:
        f = ImageFont.truetype(FONT, size)
        b = f.getbbox(text)
        if b[2] - b[0] <= max_w or size <= 40:
            return f, b
        size -= 4


def shadow_layer(mask, blur=14, offset=(0, 10), alpha=170):
    sh = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    a = mask.point(lambda v: v * alpha // 255)
    sh.putalpha(a)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out = Image.new("RGBA", (mask.size[0] + abs(offset[0]) * 2, mask.size[1] + abs(offset[1]) * 2), (0, 0, 0, 0))
    out.alpha_composite(sh, (abs(offset[0]) + offset[0], abs(offset[1]) + offset[1]))
    return out


def render_block(bl):
    """Return RGBA layer for one block (with padding for shadow)."""
    kind = bl.get("type", "plain")
    text = bl["text"]
    size = int(bl.get("size", 120))
    max_w = int(bl.get("max_w", 960))
    pad_x, pad_y = (int(size * 0.38), int(size * 0.18)) if kind != "plain" else (0, 0)
    f, b = fit_font(text, size, max_w - 2 * pad_x)
    tw, th = b[2] - b[0], b[3] - b[1]
    w, h = tw + 2 * pad_x, th + 2 * pad_y + int(size * 0.08)
    m = 40
    lay = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    tx, ty = m + pad_x - b[0], m + pad_y - b[1]
    if kind == "box":
        fill = hexrgb(bl.get("fill", "#E11D2E"))
        box = Image.new("L", lay.size, 0)
        ImageDraw.Draw(box).rounded_rectangle((m, m, m + w, m + h), int(h * 0.18), fill=255)
        lay.alpha_composite(shadow_layer(box, 16, (0, 12), 150).crop((0, 12, lay.size[0], lay.size[1] + 12)))
        d.rounded_rectangle((m, m, m + w, m + h), int(h * 0.18), fill=fill + (255,))
        d.text((tx, ty), text, font=f, fill=hexrgb(bl.get("color", "#FFFFFF")) + (255,))
    elif kind == "gold":
        box = Image.new("L", lay.size, 0)
        ImageDraw.Draw(box).rounded_rectangle((m, m, m + w, m + h), int(h * 0.22), fill=255)
        lay.alpha_composite(shadow_layer(box, 18, (0, 14), 170).crop((0, 14, lay.size[0], lay.size[1] + 14)))
        # dark glossy box: vertical gradient + gold border
        g = Image.new("RGBA", lay.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        for yy in range(h):
            k = yy / max(1, h - 1)
            c = tuple(int(a + (bb - a) * k) for a, bb in zip((40, 40, 46), (8, 8, 10)))
            gd.line([(m, m + yy), (m + w, m + yy)], fill=c + (255,))
        g.putalpha(Image.composite(g.getchannel("A"), Image.new("L", lay.size, 0), box))
        lay.alpha_composite(g)
        d.rounded_rectangle((m, m, m + w, m + h), int(h * 0.22), outline=GOLD_BOT + (255,), width=max(4, size // 28))
        # gold gradient text
        tm = Image.new("L", lay.size, 0)
        ImageDraw.Draw(tm).text((tx, ty), text, font=f, fill=255)
        grad = Image.new("RGBA", lay.size, (0, 0, 0, 0))
        gr = ImageDraw.Draw(grad)
        y0, y1 = ty + b[1], ty + b[3]
        for yy in range(lay.size[1]):
            k = min(1, max(0, (yy - y0) / max(1, y1 - y0)))
            c = tuple(int(a + (bb - a) * k) for a, bb in zip(GOLD_TOP, GOLD_BOT))
            gr.line([(0, yy), (lay.size[0], yy)], fill=c + (255,))
        grad.putalpha(tm)
        lay.alpha_composite(grad)
    else:  # plain: white bold + soft shadow
        tm = Image.new("L", lay.size, 0)
        ImageDraw.Draw(tm).text((tx, ty), text, font=f, fill=255)
        lay.alpha_composite(shadow_layer(tm, 12, (0, 8), 200).crop((0, 8, lay.size[0], lay.size[1] + 8)))
        col = hexrgb(bl.get("color", "#FFFFFF"))
        solid = Image.new("RGBA", lay.size, col + (255,))
        solid.putalpha(tm)
        lay.alpha_composite(solid)
    if bl.get("rotate"):
        lay = lay.rotate(bl["rotate"], resample=Image.BICUBIC, expand=True)
    return lay, m


def build(opt, out):
    src = Image.open(opt["image"]).convert("RGB")
    sc = max(W / src.width, H / src.height)
    src = src.resize((int(src.width * sc + 0.5), int(src.height * sc + 0.5)), Image.LANCZOS)
    src = src.crop(((src.width - W) // 2, 0, (src.width - W) // 2 + W, H))
    base = Image.new("RGB", (W, H), (8, 8, 12))
    sy = int(opt.get("shift_y", 0))
    base.paste(src, (0, sy))
    if sy > 0:  # upar ka khaali hissa: image ki top strip ko blur karke bharo
        strip = src.crop((0, 0, W, 40)).resize((W, sy)).filter(ImageFilter.GaussianBlur(30))
        base.paste(strip, (0, 0))
    img = base.convert("RGBA")
    shade = float(opt.get("top_shade", 0))
    if shade > 0:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        end = int(opt.get("shade_end", 820))
        for yy in range(end):
            a = int(255 * shade * (1 - yy / end) ** 1.4)
            gd.line([(0, yy), (W, yy)], fill=(6, 6, 10, a))
        img.alpha_composite(g)
    for bl in opt["blocks"]:
        lay, m = render_block(bl)
        x = bl.get("x", "center")
        px = (W - lay.width) // 2 if x == "center" else int(x) - m
        img.alpha_composite(lay, (px, int(bl["y"]) - m))
    img.convert("RGB").save(out, quality=93)
    print("->", out)


def preview(files, out):
    tiles = []
    for f in files:
        im = Image.open(f).convert("RGB")
        d = ImageDraw.Draw(im)
        d.rectangle((0, 240, W - 1, 1680), outline=(34, 211, 238), width=6)  # 3:4 grid box
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ov).rectangle((0, int(H * 0.75), W, H), fill=(220, 30, 30, 90))  # Shorts UI zone
        im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
        tiles.append(im.resize((360, 640)))
    sheet = Image.new("RGB", (360 * len(tiles), 640), (0, 0, 0))
    for k, t in enumerate(tiles):
        sheet.paste(t, (360 * k, 0))
    sheet.save(out, quality=90)
    print("Preview (cyan = 3:4 grid box, laal = Shorts UI zone) ->", out)


def main():
    cfg = json.loads(Path(sys.argv[1]).read_text())
    ep = cfg["episode"]
    outs = []
    for k, opt in cfg["options"].items():
        o = f"output/{ep}_thumb_{k}.jpg"
        build(opt, o)
        outs.append(o)
    preview(outs, f"output/{ep}_thumbs_preview.jpg")


if __name__ == "__main__":
    main()
