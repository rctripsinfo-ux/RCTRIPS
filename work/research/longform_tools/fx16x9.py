# fx16x9.py in.mp4 out.json -- 30 fps forensic pass for 16:9 flat-colour animation (Yellow-Dude style).
# Per frame: diff, brightness, sharpness, background colour, foreground bbox/area/centre, global shift (phase correlation),
# red / green / glow pixel shares. Then events: cut, dissolve, slide, scale/zoom, pan/whip, dim, flash, blur, bg-colour change, red/green blink.
import json, subprocess, sys, numpy as np, cv2
src, out = sys.argv[1:3]; Wd, Hd = 320, 180
p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", src, "-vf", f"fps=30,scale={Wd}:{Hd}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
R = []; prev = None; prevg = None; n = 0
while True:
    b = p.stdout.read(Wd * Hd * 3)
    if len(b) < Wd * Hd * 3: break
    f = np.frombuffer(b, np.uint8).reshape(Hd, Wd, 3); g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV); H_, S_, V_ = [hsv[..., k].astype(np.int16) for k in range(3)]
    border = np.concatenate([f[:6].reshape(-1, 3), f[-6:].reshape(-1, 3), f[:, :6].reshape(-1, 3), f[:, -6:].reshape(-1, 3)])
    bg = np.median(border, 0)
    fg = np.abs(f.astype(np.int16) - bg).sum(2) > 45; ys, xs = np.where(fg)
    box = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) > 30 else None
    red = ((H_ < 8) | (H_ > 170)) & (S_ > 120) & (V_ > 90); grn = (H_ > 40) & (H_ < 85) & (S_ > 100) & (V_ > 90)
    glow = (V_ > 235) & (S_ < 50) & ~(np.abs(f.astype(np.int16) - bg).sum(2) < 20)
    r = dict(i=n, diff=float(np.abs(g - prevg).mean()) if prevg is not None else 0.0, bright=float(V_.mean()),
             sharp=float(cv2.Laplacian(g, cv2.CV_32F).var()), bg=[int(x) for x in bg], area=float(fg.mean()), box=box,
             red=float(red.mean()), green=float(grn.mean()), glow=float(glow.mean()))
    if prevg is not None:
        (dx, dy), resp = cv2.phaseCorrelate(prevg, g); r.update(dx=round(dx, 2), dy=round(dy, 2), resp=round(resp, 3))
    R.append(r); prevg = g; n += 1
N = len(R); ev = []
def add(kind, a, b, **k): ev.append(dict(kind=kind, t0=round(a / 30, 2), t1=round(b / 30, 2), frames=b - a + 1, **k))
i = 1
while i < N:  # change events: group consecutive frames with diff > 0.8
    if R[i]["diff"] > 0.8:
        j = i
        while j + 1 < N and R[j + 1]["diff"] > 0.8: j += 1
        seg = R[i:j + 1]; L = j - i + 1; pk = max(x["diff"] for x in seg)
        sx = sum(x.get("dx", 0) for x in seg); sy = sum(x.get("dy", 0) for x in seg)
        a, b = R[i - 1], R[j]; da = b["area"] - a["area"]
        bgch = float(np.abs(np.array(a["bg"]) - np.array(b["bg"])).sum())
        cen = lambda x: ((x["box"][0] + x["box"][2]) / 2, (x["box"][1] + x["box"][3]) / 2) if x["box"] else None
        ca, cb = cen(a), cen(b); mv = (abs(cb[0] - ca[0]) + abs(cb[1] - ca[1])) if ca and cb else 0
        sharp_min = min(x["sharp"] for x in seg); sharp_ref = max(a["sharp"], b["sharp"], 1)
        if L <= 2 and pk > 12: kind = "cut"
        elif bgch > 40 and L <= 4: kind = "cut+bg"
        elif abs(sx) + abs(sy) > 60 and pk > 8: kind = "whip/pan"
        elif sharp_min < 0.35 * sharp_ref and L >= 3: kind = "blur-transition"
        elif bgch > 40: kind = "bg-change"
        elif mv > 25 and L >= 4: kind = "slide/move"
        elif abs(da) > 0.06 and L >= 4: kind = "scale/zoom" if abs(sx) + abs(sy) < 20 else "zoom+move"
        elif L >= 6 and pk < 12: kind = "dissolve/fade"
        elif L <= 4: kind = "pop/swap"
        else: kind = "other"
        # easing: share of total movement done in the first third of the event
        tr = [cen(x) for x in R[i - 1:j + 1] if x["box"]]
        ease = None
        if len(tr) >= 6 and mv > 25:
            d = [abs(tr[k][0] - tr[0][0]) + abs(tr[k][1] - tr[0][1]) for k in range(len(tr))]
            ease = round(d[len(d) // 3] / max(d[-1], 1), 2); over = round(max(d) / max(d[-1], 1), 2)
        else: over = None
        add(kind, i, j, peak=round(pk, 1), area_change=round(da, 3), move_px=round(mv, 1), shift=(round(sx), round(sy)), bg_change=round(bgch), ease_first_third=ease, overshoot=over)
        i = j + 1
    else: i += 1
br = np.array([x["bright"] for x in R]); base = np.median(br)
for k, (lo) in enumerate([br < base - 18]):
    s = None
    for t, v in enumerate(list(lo) + [False]):
        if v and s is None: s = t
        if not v and s is not None:
            if t - s >= 8: add("dim", s, t - 1, depth=round(float(base - br[s:t].mean()), 1))
            s = None
s = None
for t in range(1, N):
    if br[t] - br[t - 1] > 25: add("flash", t, t, jump=round(float(br[t] - br[t - 1]), 1))
for key in ("red", "green", "glow"):
    v = np.array([x[key] for x in R]); on = v > 0.004; s = None
    for t, x in enumerate(list(on) + [False]):
        if x and s is None: s = t
        if not x and s is not None:
            if t - s >= 3: add(f"{key}-on", s, t - 1, share=round(float(v[s:t].mean()), 4))
            s = None
json.dump(dict(src=src, n=N, frames=[{k: x[k] for k in ("diff", "bright", "sharp", "area", "red", "green", "glow")} | {"bg": x["bg"]} for x in R[::3]], events=ev), open(out, "w"))
from collections import Counter
c = Counter(e["kind"] for e in ev); print(src, N, dict(c.most_common()))
