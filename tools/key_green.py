#!/usr/bin/env python3
"""
key_green.py - Gemini ke hare (#00FF00) background wali image se kirdaar kaat ke PNG banana.

Usage (project root se):
    .venv/bin/python tools/key_green.py ~/Downloads/Gemini_Generated_Image_x.png assets/graphics/characters/chor.png

Kya karta hai (Pillow + numpy):
  1. Hara rang transparent (green key), kinaron par halka fade.
  2. Despill: kinaron ki hari jhalak hatana.
  3. Sirf sabse bada hissa rakhta hai, taaki kone ka Gemini sparkle ya chhote dhabbe hat jaayein.
  4. Khaali jagah kaat ke 900px tak chhota.
Rule: prompts/visual-assets.md
"""
import argparse

import numpy as np
from PIL import Image, ImageFilter


def largest_blob(mask):
    """mask (bool) ka sabse bada juda hua hissa. scipy na ho to mask waisa hi."""
    try:
        from scipy import ndimage
    except ImportError:
        return mask
    lab, n = ndimage.label(mask)
    if n <= 1:
        return mask
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    return lab == (1 + int(np.argmax(sizes)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--max", type=int, default=900, help="lambi taraf zyada se zyada kitne px")
    args = ap.parse_args()

    a = np.asarray(Image.open(args.src).convert("RGB")).astype("float32")
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    dom = g - np.maximum(r, b)
    alpha = np.clip(1 - (dom - 25) / 70, 0, 1)
    keep = largest_blob(alpha > 0.5)
    # bade hisse ke paas wale kinare rakho, door ke dhabbe hatao
    near = np.asarray(Image.fromarray((keep * 255).astype("uint8")).filter(ImageFilter.MaxFilter(9))) > 0
    alpha = alpha * near
    g2 = np.minimum(g, np.maximum(r, b) + 12)
    out = Image.fromarray(np.dstack([r, g2, b, alpha * 255]).astype("uint8"), "RGBA")
    out.putalpha(out.getchannel("A").filter(ImageFilter.GaussianBlur(1.2)))
    out = out.crop(out.getbbox())
    out.thumbnail((args.max, args.max))
    out.save(args.out)
    print(f"-> {args.out} {out.size}")


if __name__ == "__main__":
    main()
