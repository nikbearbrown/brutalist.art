#!/usr/bin/env python3
"""Extract pixel mascots from a grid sprite sheet into tight transparent PNGs.

Usage:
  python3 extract_mascots.py <sheet.png> <out_dir> <cols> <name1,name2,...>
  python3 extract_mascots.py <sheet.png>              # defaults to the 6 emotions

Row-major names; rows = len(names)/cols. Knocks out the warm cream/shadow
background with a border-connected flood fill (scipy), preserving the mascot
body, enclosed highlights (white eyes, gear shine), and colour/tool accessories
(sparks, tears, gears, magnifiers, icons). Each cell's text label is cropped off.

Background key: "very light AND warm-ish" (min channel > 175 and R >= B-2). This
removes cream (~244) and its soft shadow but keeps medium-gray tools (~136) and
any cool-coloured bits (blue tears/'?').
"""
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage

EMOTIONS = ["shocked", "laughing", "furious", "crying", "suspicious", "smug"]

def passable_mask(rgb):
    # background = light AND warm-or-neutral. The warmth test (R >= B-2) keeps the
    # slightly-cool gray tools (gears, ~136/140/139) while removing cream (~244),
    # its soft shadow, and the faint neutral divider dots (~170) between cells.
    R, G, B = (rgb[..., i].astype(int) for i in range(3))
    return (np.minimum(np.minimum(R, G), B) > 150) & (R >= B - 2)

def label_top(cell_passable, bridge=6):
    """y of the TOP of the bottom-most content band (= the text label).

    Walks the bottom-most band up to its top, bridging vertical gaps up to
    `bridge` rows (thin serif rows inside the label can dip below threshold);
    stops at the wide empty gap that separates the label from the mascot.
    """
    solid = (~cell_passable).sum(axis=1) >= 6
    h = len(solid)
    idx = np.where(solid)[0]
    if len(idx) == 0:
        return int(h * 0.82)
    top = idx[-1]; i = len(idx) - 1
    while i > 0 and idx[i] - idx[i - 1] <= bridge:
        i -= 1; top = idx[i]
    return top if top > 0.30 * h else int(h * 0.82)

def knockout(region_rgb):
    p = passable_mask(region_rgb)
    lbl, _ = ndimage.label(p)
    border = (set(lbl[0, :]) | set(lbl[-1, :]) | set(lbl[:, 0]) | set(lbl[:, -1]))
    border.discard(0)
    bg = np.isin(lbl, list(border))
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    return np.dstack([region_rgb, alpha])

def trim(rgba, pad=6):
    ys, xs = np.where(rgba[..., 3] > 0)
    if len(xs) == 0:
        return rgba
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + 1 + pad, rgba.shape[0])
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + 1 + pad, rgba.shape[1])
    return rgba[y0:y1, x0:x1]

def main():
    sheet = sys.argv[1]
    out   = sys.argv[2] if len(sys.argv) > 2 else "assets/mascots"
    cols  = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    names = sys.argv[4].split(",") if len(sys.argv) > 4 else EMOTIONS
    rows  = (len(names) + cols - 1) // cols
    os.makedirs(out, exist_ok=True)
    arr = np.asarray(Image.open(sheet).convert("RGB"))
    H, W = arr.shape[:2]
    ch, cw = H // rows, W // cols
    ins = 5   # inset each cell to drop the surviving boundary divider dashes
    for i, name in enumerate(names):
        r, c = divmod(i, cols)
        cell = arr[r*ch+ins:(r+1)*ch-ins, c*cw+ins:(c+1)*cw-ins]
        # crop off the text label; clamp as a backstop against a merged band.
        cut = min(label_top(passable_mask(cell)), int(cell.shape[0] * 0.85))
        rgba = trim(knockout(cell[:cut]))
        Image.fromarray(rgba).save(os.path.join(out, f"{name}.png"))
        print(f"  {name:12s} {rgba.shape[1]}x{rgba.shape[0]}")

if __name__ == "__main__":
    main()
