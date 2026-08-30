#!/usr/local/bin/python3
"""Per-frame ink geometry + emboss structure for a sting.

The reference plate carries a strong global lighting gradient (a soft vignette
that alone accounts for sd~22). Subtracting a single page level therefore
measures the vignette, not the mark. So: HIGH-PASS each frame (subtract a heavy
Gaussian blur) and measure what is left, which is exactly the emboss edge
structure — highlight edge above zero, shadow edge below.
"""
import sys, glob, os, json
import numpy as np
from PIL import Image, ImageFilter

src, fps, dur = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
files = sorted(glob.glob(os.path.join(src, "*.png")))
rows = []
for i, f in enumerate(files):
    im = Image.open(f).convert('L')
    a = np.asarray(im).astype(np.float32)
    bg = np.asarray(im.filter(ImageFilter.GaussianBlur(24))).astype(np.float32)
    d = a - bg                                # high-passed: emboss only
    H, W = d.shape
    ad = np.abs(d)
    thr = 1.2                                 # ~0.5% of full range
    m = ad > thr
    frac = m.mean()
    if frac > 2e-4:
        ys, xs = np.nonzero(m)
        wgt = ad[m]
        x0, x1 = np.percentile(xs, [1.5, 98.5])
        y0, y1 = np.percentile(ys, [1.5, 98.5])
        cx = float((xs * wgt).sum() / wgt.sum() / W)
        cy = float((ys * wgt).sum() / wgt.sum() / H)
        w, h = (x1 - x0) / W, (y1 - y0) / H
        # rms radius of ink about its centroid -> scale proxy, robust to shape
        rr = np.sqrt(((xs / W - cx) ** 2 + (ys / H - cy) ** 2) * wgt).sum() / wgt.sum()
        rms = float(np.sqrt((((xs / W - cx) ** 2 + (ys / H - cy) ** 2) * wgt).sum() / wgt.sum()))
    else:
        cx = cy = w = h = rms = float('nan')
    hi = float(d[d > thr].sum() / (H * W))
    sh = float(-d[d < -thr].sum() / (H * W))
    rows.append(dict(n=i + 1, t=i / fps, p=(i / fps) / dur,
                     sd=float(d.std()), ink=float(frac * 100),
                     cx=cx, cy=cy, w=float(w), h=float(h), rms=rms,
                     hi=hi, sh=sh,
                     hmax=float(d.max()), smin=float(d.min())))
print(json.dumps(rows))
