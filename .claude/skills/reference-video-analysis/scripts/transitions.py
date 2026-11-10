#!/usr/bin/env python3
"""Detect and classify transitions in flat-background motion-graphics videos.

Tracks the foreground (everything that differs from the background colour) frame by frame and classifies each
change of scene by how the foreground's bounding box behaves:
  drop   - enters from the top edge and falls into place
  pop    - grows from a small blob around a fixed centre
  flip   - width collapses to a sliver while height stays (3D card turn)
  rise   - foreground enters from the bottom edge (top edge travels upward)
  slide  - centre travels horizontally
  scale  - width and height grow/shrink together around the same centre (zoom in/out, pop)
  fade   - foreground disappears/appears in place (opacity)
  cut    - instant change of content with no in-between frames
Also reports how often the same type repeats back-to-back and the tilt (rotation) events.

Usage: transitions.py VIDEO [VIDEO ...] [--fps 15] [--json out.json]
"""
import argparse, json, subprocess
import numpy as np

def frames(path, fps, w=90, h=160):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={w}:{h}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(np.int16)

def fg_stats(f):
    border = np.concatenate([f[:4].reshape(-1, 3), f[-4:].reshape(-1, 3), f[:, :3].reshape(-1, 3), f[:, -3:].reshape(-1, 3)])
    bg = np.median(border, 0)
    m = np.abs(f - bg).sum(2) > 60
    area = m.mean()
    if area < 0.004:
        return dict(area=area, w=0, h=0, cx=0.5, cy=0.5, top=1.0, sig=None)
    ys, xs = np.nonzero(m)
    x0, x1 = np.percentile(xs, [2, 98]); y0, y1 = np.percentile(ys, [2, 98])
    W, H = f.shape[1], f.shape[0]
    sig = np.histogram(xs, 12, (0, W))[0] / len(xs)
    return dict(area=area, w=(x1 - x0) / W, h=(y1 - y0) / H, cx=(x0 + x1) / 2 / W, cy=(y0 + y1) / 2 / H, top=y0 / H, sig=sig)

def classify(seq):
    """seq: stats over the transition window (dip in the middle)."""
    pre, post = seq[0], seq[-1]
    mid = min(seq, key=lambda s: s["area"])
    ws = [s["w"] for s in seq if s["area"] > 0.004]; hs = [s["h"] for s in seq if s["area"] > 0.004]
    if ws and hs:
        wn = max(pre["w"], post["w"], 1e-3); hn = max(pre["h"], post["h"], 1e-3)
        if min(ws) < 0.35 * wn and min(hs) > 0.6 * hn:
            return "flip"
    tops = [s["top"] for s in seq if s["area"] > 0.004]
    vis = [s for s in seq if s["area"] > 0.004]
    if len(vis) >= 3:
        # drop: enters from the top edge (centre travels downward into place)
        if vis[0]["cy"] < post["cy"] - 0.12 and vis[0]["top"] < 0.05 and post["top"] > vis[0]["top"] + 0.05:
            return "drop"
        # pop: grows from a small blob around a fixed centre
        if (min(s["w"] * s["h"] for s in vis) < 0.25 * post["w"] * post["h"]
                and abs(vis[0]["cx"] - post["cx"]) < 0.1 and abs(vis[0]["cy"] - post["cy"]) < 0.12):
            return "pop"
    if mid["area"] < 0.35 * max(pre["area"], post["area"]):
        if len(tops) >= 3 and tops[-1] < tops[len(tops) // 2] - 0.08 and seq[len(seq) // 2]["cy"] > post["cy"] + 0.05:
            return "rise"
        if ws and hs and min(ws) < 0.6 * max(pre["w"], post["w"]) and min(hs) < 0.6 * max(pre["h"], post["h"]):
            return "scale"
        return "fade"
    if abs(pre["cx"] - post["cx"]) > 0.18:
        return "slide"
    if abs(pre["h"] - post["h"]) > 0.2 or abs(pre["w"] - post["w"]) > 0.25:
        return "scale"
    return "cut"

def analyze(path, fps):
    F = frames(path, fps)
    st = [fg_stats(f) for f in F]
    area = np.array([s["area"] for s in st])
    n = len(st)
    diff = np.r_[0, np.abs(np.diff(F.reshape(n, -1).astype(np.float32), axis=0)).mean(1)] / 255
    events = []
    i = 1
    base = np.maximum.accumulate(np.r_[area[:1], area[:-1]])
    while i < n - 1:
        roll = np.median(area[max(0, i - int(fps)):i + 1]) if i > 2 else area[i]
        dip = area[i] < 0.6 * roll and area[i] <= area[i - 1]
        cut = diff[i] > 0.12
        if dip or cut:
            j = i
            while j < n - 1 and area[j + 1] < 0.85 * max(roll, 1e-4) and j - i < fps:
                j += 1
            a, b = max(0, i - 2), min(n - 1, j + 3)
            typ = "cut" if cut and not dip else classify(st[a:b + 1])
            events.append(dict(t=round(i / fps, 2), type=typ, frames=int(j - i + 1)))
            i = j + 3
        else:
            i += 1
    types = [e["type"] for e in events]
    repeats = sum(1 for a, b in zip(types, types[1:]) if a == b)
    dur = n / fps
    counts = {k: types.count(k) for k in sorted(set(types))}
    return dict(video=path, duration=round(dur, 1), events=len(events), per_min=round(len(events) / dur * 60, 1),
                distinct_types=len(counts), counts=counts,
                same_type_back_to_back_pct=round(100 * repeats / max(1, len(types) - 1), 1),
                top_type_share_pct=round(100 * max(counts.values()) / max(1, len(types)), 1) if counts else 0,
                timeline=events)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("videos", nargs="+"); ap.add_argument("--fps", type=float, default=15)
    ap.add_argument("--json"); a = ap.parse_args()
    res = [analyze(v, a.fps) for v in a.videos]
    for r in res:
        print(f"{r['video'].split('/')[-1]:28} {r['events']:3d} events ({r['per_min']}/min) types={r['distinct_types']} "
              f"top_share={r['top_type_share_pct']}% repeats={r['same_type_back_to_back_pct']}% {r['counts']}")
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1)

if __name__ == "__main__":
    main()
