# Same statistics on reference frames and our frames. Usage: python3 -I analysis/measure.py
# Image stats at 540x960, caption band (58-78 % of height) masked on BOTH sets so they stay comparable.
# Motion: 60 consecutive frames per reference sheet (10x6 grid of 180x320) vs our video sampled the same way.
import glob, json, subprocess, os, numpy as np
from PIL import Image
REF = "/home/user/RCTRIPS/.claude/skills/cartoon-3d-short/references"
VID = "out/final2/whale_short_v4.mp4"; OUT = "analysis/data"; os.makedirs(OUT, exist_ok=True)
def srgb2lin(x): return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
def stats(rgb):
    a = np.asarray(rgb.convert("RGB").resize((540, 960)), float) / 255
    m = np.ones(a.shape[:2], bool); m[int(.58 * 960):int(.78 * 960)] = False
    Y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    mx, mn = a.max(2), a.min(2); S = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    ink = (Y < 0.10) & m
    g = Y.copy(); lap = np.abs(4 * g[1:-1, 1:-1] - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:])
    rg, yb = a[..., 0] - a[..., 1], 0.5 * (a[..., 0] + a[..., 1]) - a[..., 2]
    colorful = np.hypot(rg[m].std(), yb[m].std()) + 0.3 * np.hypot(rg[m].mean(), yb[m].mean())
    gx = np.abs(np.diff(g, axis=1))[:-1, :]; gy = np.abs(np.diff(g, axis=0))[:, :-1]
    edges = ((gx + gy) > 0.12)[m[:-1, :-1]].mean()
    # detail: share of 16x16 tiles with real texture (local std > .04) -> "busy / rich" frame
    t = g[:960 // 16 * 16, :540 // 16 * 16].reshape(60, 16, 33, 16).std(axis=(1, 3)); tm = m[::16, ::16][:60, :33]
    hue = np.degrees(np.arctan2(np.sqrt(3) * (a[..., 1] - a[..., 2]), 2 * a[..., 0] - a[..., 1] - a[..., 2])) % 360
    hh = np.histogram(hue[m & (S > .25)], bins=12, range=(0, 360))[0]; fam = int((hh > 0.04 * max(1, hh.sum())).sum())
    return dict(Ymed=float(np.median(Y[m])), Yp5=float(np.percentile(Y[m & ~ink], 5)), Yp95=float(np.percentile(Y[m], 95)),
                Smed=float(np.median(S[m])), colorful=float(colorful), ink=float(ink.mean() / m.mean()),
                sharp=float(lap[m[1:-1, 1:-1]].mean()), edges=float(edges), detail=float((t[tm] > .04).mean()), hues=fam)
def summ(rows):
    k = rows[0].keys(); return {x: (round(float(np.median([r[x] for r in rows])), 4), round(float(np.percentile([r[x] for r in rows], 25)), 4), round(float(np.percentile([r[x] for r in rows], 75)), 4)) for x in k}
ref = [stats(Image.open(p)) for p in sorted(glob.glob(REF + "/frames/*.jpg"))]
os.makedirs("analysis/ours", exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VID, "-vf", "fps=1,scale=540:960", "analysis/ours/o_%03d.jpg"], check=True)
ours = [stats(Image.open(p)) for p in sorted(glob.glob("analysis/ours/o_*.jpg"))]
# ---- motion: sub-pixel phase correlation between consecutive 180x320 frames (centre 70 % to avoid caption / borders)
def pc(a, b):
    A, B = np.fft.fft2(a * win), np.fft.fft2(b * win); R = A * np.conj(B); R /= np.abs(R) + 1e-9
    r = np.fft.ifft2(R).real; y, x = np.unravel_index(r.argmax(), r.shape)
    def sub(c, n, ax):
        l, cc, rr = [r[(y + (d if ax == 0 else 0)) % r.shape[0], (x + (d if ax == 1 else 0)) % r.shape[1]] for d in (-1, 0, 1)]
        den = l - 2 * cc + rr; o = 0.5 * (l - rr) / den if abs(den) > 1e-9 else 0
        v = c + o; return v - n if v > n / 2 else v
    return np.hypot(sub(y, r.shape[0], 0), sub(x, r.shape[1], 1)), float(r.max())
H0, W0 = 224, 180; win = np.outer(np.hanning(H0), np.hanning(W0))
def crop(f): return f[16:16 + H0]  # rows 16-240 of 320: above the caption band
def motion(frames):
    sp, cuts = [], 0
    for a, b in zip(frames, frames[1:]):
        d = np.abs(a - b).mean()
        if d > 0.12: cuts += 1; continue
        s, _ = pc(crop(a), crop(b)); sp.append(s * 4)  # px at 720 width (180 -> 720 = x4)
    sp = np.array(sp); return dict(hold=float((sp < 0.3).mean()), drift=float(((sp >= 0.3) & (sp < 2)).mean()), move=float((sp >= 2).mean()), med=float(np.median(sp)), cuts=cuts, n=len(frames))
refm = []
for p in sorted(glob.glob(REF + "/sheets/*.jpg")):
    s = np.asarray(Image.open(p).convert("L"), float) / 255
    refm.append(motion([s[r * 320:(r + 1) * 320, c * 180:(c + 1) * 180] for r in range(6) for c in range(10)]))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VID, "-vf", "scale=180:320,format=gray", "-f", "rawvideo", "analysis/ours/all.gray"], check=True)
raw = np.fromfile("analysis/ours/all.gray", np.uint8).reshape(-1, 320, 180).astype(float) / 255
ourm = [motion(list(raw[i:i + 60])) for i in range(0, len(raw) - 60, 60)]
def msum(ms): return {k: round(float(np.median([m[k] for m in ms])), 3) for k in ("hold", "drift", "move", "med")} | {"cuts_per_2s": round(float(np.mean([m["cuts"] for m in ms])), 2)}
res = dict(image=dict(ref=summ(ref), ours=summ(ours), n_ref=len(ref), n_ours=len(ours)), motion=dict(ref=msum(refm), ours=msum(ourm), n_ref=len(refm), n_ours=len(ourm)))
json.dump(res, open(OUT + "/compare.json", "w"), indent=1)
print("metric        ref med [IQR]              ours med [IQR]")
for k in res["image"]["ref"]: print(f'{k:10s} {str(res["image"]["ref"][k]):28s} {res["image"]["ours"][k]}')
print("motion ref ", res["motion"]["ref"]); print("motion ours", res["motion"]["ours"])
