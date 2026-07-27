#!/usr/bin/env python3
"""Extract the 6 emotion mascots from a 3x2 sprite sheet into tight transparent PNGs.

Usage: python3 extract_mascots.py <sheet.png> [out_dir]

Knocks out the warm cream/shadow background with a border-connected flood fill
(scipy label), so it preserves the mascot body, enclosed white eyes, and the
floating colour accents (sparks, sweat, '?', sparkle) and cool bits (blue tears).
Each emotion's text label is cropped off first.
"""
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage

NAMES = [["shocked", "laughing", "furious"],
         ["crying", "suspicious", "smug"]]

def passable_mask(rgb):
    R, G, B = (rgb[..., i].astype(int) for i in range(3))
    # warm light = cream / beige shadow / neutral white; NOT cool (blue) or saturated
    return (R > 140) & (G > 140) & (B > 140) & (R + 8 >= B)

def label_top(cell_passable):
    """y (within cell) of the top of the bottom-most content band = the text label."""
    content_rows = (~cell_passable).sum(axis=1)
    empty = content_rows < 6
    h = len(empty)
    y = h - 1
    while y >= 0 and empty[y]:
        y -= 1                       # skip bottom margin
    while y >= 0 and not empty[y]:
        y -= 1                       # skip the label band
    top = y + 1
    return top if top > 220 else int(h * 0.82)   # guard against merged bands

def knockout(region_rgb):
    """Return RGBA with border-connected warm-light background made transparent."""
    p = passable_mask(region_rgb)
    lbl, _ = ndimage.label(p)                    # 4-connectivity
    border = set(lbl[0, :]) | set(lbl[-1, :]) | set(lbl[:, 0]) | set(lbl[:, -1])
    border.discard(0)
    bg = np.isin(lbl, list(border))
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    return np.dstack([region_rgb, alpha])

def trim(rgba):
    ys, xs = np.where(rgba[..., 3] > 0)
    if len(xs) == 0:
        return rgba
    pad = 6
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + 1 + pad, rgba.shape[0])
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + 1 + pad, rgba.shape[1])
    return rgba[y0:y1, x0:x1]

def main():
    sheet = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "assets/mascots"
    os.makedirs(out, exist_ok=True)
    arr = np.asarray(Image.open(sheet).convert("RGB"))
    H, W = arr.shape[:2]
    ch, cw = H // 2, W // 3
    saved = []
    for r in range(2):
        for c in range(3):
            cell = arr[r*ch:(r+1)*ch, c*cw:(c+1)*cw]
            cut = label_top(passable_mask(cell))         # drop the label text
            region = cell[:cut]
            rgba = trim(knockout(region))
            name = NAMES[r][c]
            Image.fromarray(rgba, "RGBA").save(os.path.join(out, f"{name}.png"))
            saved.append((name, rgba.shape[1], rgba.shape[0]))
            print(f"  {name:11s} {rgba.shape[1]}x{rgba.shape[0]}")
    return saved

if __name__ == "__main__":
    main()
