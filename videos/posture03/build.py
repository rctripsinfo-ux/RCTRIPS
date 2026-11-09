#!/usr/bin/env python3
"""posture03 — v3: every fix from posture02/REVIEW_v2.md.

Visual events are synced to spoken WORDS (voice/words.json, Whisper-aligned to the final voice track).
Usage: python3 build.py [--preview 1.0,5.2,...]
"""
import argparse, json, math, os, subprocess, wave
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)
BG_GOOD = np.array([76, 92, 44], np.float32)       # BGR #2C5C4C
BG_BAD = np.array([46, 52, 70], np.float32)        # dark cool-brown "problem" grade (contrast with skin, fix 19)
BG_FLASH = np.array([40, 40, 120], np.float32)
RED, GREEN = (40, 50, 235), (80, 215, 110)       # BGR
WORDS = json.load(open(P("voice/words.json")))
TIMING = json.load(open(P("voice/timing.json")))
END_HOLD = 1.0                                     # fix 23

def ease_out(x):
    x = min(max(x, 0.0), 1.0); return 1 - (1 - x) ** 3
def back_out(x, k=1.6):
    x = min(max(x, 0.0), 1.0); return 1 + (k + 1) * (x - 1) ** 3 + k * (x - 1) ** 2
def smooth(x):
    x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)

def wt(line, word, occ=0, edge="s"):
    """Time a word is spoken (start or end) in a given line."""
    ws = [w for w in WORDS if w["line"] == line and w["w"] == word]
    return ws[min(occ, len(ws) - 1)][edge]

# ---------------- assets ----------------
def _load(name):
    im = cv2.imread(P("assets/poses", name + ".webp"), cv2.IMREAD_UNCHANGED)
    ys, xs = np.nonzero(im[:, :, 3] > 8)
    return im[ys.min():ys.max() + 1, xs.min():xs.max() + 1].copy()

def _over(dst, src):
    a = src[:, :, 3:4].astype(np.float32) / 255
    dst[:, :, :3] = (src[:, :, :3] * a + dst[:, :, :3] * (1 - a)).astype(np.uint8)
    dst[:, :, 3] = np.maximum(dst[:, :, 3], src[:, :, 3])

def _with_bench(im):
    """Shaded bench drawn behind the body (fix 24)."""
    h, w = im.shape[:2]
    a = im[:, :, 3] > 8
    seat = int(np.nonzero(a[: int(0.75 * h), : int(0.35 * w)].any(1))[0].max()) - 8
    c = np.zeros((h, w, 4), np.uint8)
    x0, x1 = 0, int(0.64 * w)
    for y in range(seat, seat + 56):                     # vertical gradient seat
        k = (y - seat) / 56
        col = (int(78 - 40 * k), int(98 - 46 * k), int(86 - 40 * k), 255)
        cv2.line(c, (x0, y), (x1, y), col, 1)
    cv2.rectangle(c, (x0, seat), (x1, seat + 56), (20, 26, 22, 255), 4)
    for lx in (x0 + 24, x1 - 60):
        cv2.rectangle(c, (lx, seat + 56), (lx + 34, h - 4), (36, 46, 40, 255), -1)
        cv2.line(c, (lx + 6, seat + 60), (lx + 6, h - 8), (70, 88, 78, 255), 4)
        cv2.rectangle(c, (lx, seat + 56), (lx + 34, h - 4), (20, 26, 22, 255), 4)
    _over(c, im)
    return c

def _with_mat(im):
    """Shaded exercise mat (fix 24)."""
    h, w = im.shape[:2]
    pad = int(0.07 * h) + 24
    c = np.zeros((h + pad, w + 80, 4), np.uint8)
    y0 = h - int(0.05 * h) + pad // 3
    pts = np.array([[24, y0], [w + 56, y0], [w + 34, h + pad - 6], [46, h + pad - 6]], np.int32)
    cv2.fillPoly(c, [pts], (60, 66, 72, 255))
    cv2.fillPoly(c, [np.array([[24, y0], [w + 56, y0], [w + 52, y0 + 10], [28, y0 + 10]], np.int32)], (96, 104, 112, 255))
    cv2.polylines(c, [pts], True, (26, 28, 30, 255), 5, cv2.LINE_AA)
    sub = c[0:h, 40:40 + w].copy(); _over(sub, im); c[0:h, 40:40 + w] = sub
    return c

POSES = {}
def pose(name):
    if name not in POSES:
        im = _load(name)
        if name in ("bad_posture_desk", "good_posture_desk"):
            im = _with_bench(im)
        if name in ("cobra_stretch", "glute_bridge_up", "glute_bridge_down"):
            im = _with_mat(im)
        POSES[name] = im
    return POSES[name]

FONT = P("assets/fonts/Nunito.ttf")
TEXTS = {}
def text_img(s, size, color=(255, 255, 255)):
    key = (s, size, color)
    if key not in TEXTS:
        f = ImageFont.truetype(FONT, size); f.set_variation_by_name("Black")
        l, t, r, b = f.getbbox(s); pad = 30
        im = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.text((pad - l + 5, pad - t + 7), s, font=f, fill=(0, 0, 0, 120))
        d.text((pad - l, pad - t), s, font=f, fill=color + (255,))
        TEXTS[key] = cv2.cvtColor(np.array(im), cv2.COLOR_RGBA2BGRA)
    return TEXTS[key]

# ---------------- compositing ----------------
MASK = np.zeros((H, W), np.float32)          # silhouette of the last drawn pose (for sparkles, fix 13)
def blit_affine(frame, rgba, s, tx, ty, alpha=1.0, tint=None, keep_mask=True):
    if alpha <= 0.01:
        return
    M = np.float32([[s, 0, tx], [0, s, ty]])
    lay = cv2.warpAffine(rgba, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    a = lay[:, :, 3].astype(np.float32) * (alpha / 255)
    if keep_mask:
        MASK[:] = a
    ys, xs = np.nonzero(a > 0.004)
    if not len(ys):
        return
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    src = lay[y0:y1, x0:x1, :3].astype(np.float32)
    if tint is not None:
        src = np.clip(src * tint, 0, 255)
    aa = a[y0:y1, x0:x1, None]
    roi = frame[y0:y1, x0:x1].astype(np.float32)
    frame[y0:y1, x0:x1] = (roi * (1 - aa) + src * aa).astype(np.uint8)

def blit_center(frame, rgba, cx, cy, s=1.0, alpha=1.0):
    h, w = rgba.shape[:2]
    blit_affine(frame, rgba, s, cx - w * s / 2, cy - h * s / 2, alpha, keep_mask=False)

GLOW = None
def draw_glow(frame, c, t, r=150):
    """Soft pulsing red glow on a pain point (replaces the scribble wisps, fix 3)."""
    global GLOW
    if GLOW is None:
        g = cv2.getGaussianKernel(301, 60); GLOW = (g @ g.T); GLOW /= GLOW.max()
    s = r / 150
    k = cv2.resize(GLOW, (int(301 * s), int(301 * s)))
    amt = 0.45 + 0.25 * math.sin(t * 7)
    x0, y0 = int(c[0] - k.shape[1] / 2), int(c[1] - k.shape[0] / 2)
    fx0, fy0, fx1, fy1 = max(0, x0), max(0, y0), min(W, x0 + k.shape[1]), min(H, y0 + k.shape[0])
    if fx0 >= fx1 or fy0 >= fy1:
        return
    kk = k[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0, None] * amt
    roi = frame[fy0:fy1, fx0:fx1].astype(np.float32)
    frame[fy0:fy1, fx0:fx1] = (roi * (1 - kk) + np.array([30, 40, 255], np.float32) * kk).astype(np.uint8)

def draw_arrow(frame, p0, p1, color, prog, thick=18, curve=0.0):
    """Thick arrow, optionally curved (fix: style gap 4). prog 0..1 draws it on."""
    if prog <= 0:
        return
    p0 = np.array(p0, np.float32); p1 = np.array(p1, np.float32)
    mid = (p0 + p1) / 2 + curve * np.array([-(p1 - p0)[1], (p1 - p0)[0]], np.float32)
    ts = np.linspace(0, prog, 24)
    pts = [((1 - u) ** 2) * p0 + 2 * (1 - u) * u * mid + (u ** 2) * p1 for u in ts]
    pts = np.array(pts, np.int32)
    cv2.polylines(frame, [pts], False, (18, 18, 18), thick + 10, cv2.LINE_AA)
    cv2.polylines(frame, [pts], False, color, thick, cv2.LINE_AA)
    tip, prev = pts[-1].astype(np.float32), pts[-3].astype(np.float32)
    ang = math.atan2(tip[1] - prev[1], tip[0] - prev[0]); L = 52
    head = np.array([tip, tip + L * np.array([math.cos(ang + 2.5), math.sin(ang + 2.5)]),
                     tip + L * np.array([math.cos(ang - 2.5), math.sin(ang - 2.5)])], np.int32)
    cv2.fillPoly(frame, [head], color, cv2.LINE_AA)
    cv2.polylines(frame, [head], True, (18, 18, 18), 5, cv2.LINE_AA)

def draw_dashed(frame, p0, p1, color, thick=8, dash=22):
    d = np.hypot(p1[0] - p0[0], p1[1] - p0[1]); n = max(1, int(d / dash))
    for i in range(0, n, 2):
        a = np.array(p0) + (np.array(p1) - np.array(p0)) * i / n
        b = np.array(p0) + (np.array(p1) - np.array(p0)) * min(1, (i + 1) / n)
        cv2.line(frame, tuple(a.astype(int)), tuple(b.astype(int)), color, thick, cv2.LINE_AA)

def draw_spine(frame, pts, color, prog):
    pts = np.array(pts, np.float32)
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    n = 24
    for k in range(int(n * prog)):
        d = seg[-1] * k / (n - 1)
        i = min(np.searchsorted(seg, d, side="right") - 1, len(pts) - 2)
        f = (d - seg[i]) / max(1e-6, seg[i + 1] - seg[i])
        x, y = pts[i] + (pts[i + 1] - pts[i]) * f
        cv2.ellipse(frame, (int(x), int(y)), (17, 12), 0, 0, 360, (25, 25, 25), -1, cv2.LINE_AA)
        cv2.ellipse(frame, (int(x), int(y)), (13, 9), 0, 0, 360, color, -1, cv2.LINE_AA)

SPARKS = np.random.default_rng(3).uniform(0, 1, (22, 3))
def draw_sparkles(frame, t):
    """Soft 4-point glints, only OUTSIDE the character silhouette (fix 13)."""
    for u, v, ph in SPARKS:
        x, y = int(60 + u * 960), int(500 + v * 1250)
        if MASK[min(H - 1, y), min(W - 1, x)] > 0.05:
            continue
        a = 0.5 + 0.5 * math.sin(t * 4 + ph * 6.28)
        if a < 0.3:
            continue
        L = int(8 + 20 * a)
        for dx, dy in ((L, 0), (0, L)):
            cv2.line(frame, (x - dx, y - dy), (x + dx, y + dy), (200, 245, 255), 3, cv2.LINE_AA)
        cv2.circle(frame, (x, y), 4, (230, 255, 255), -1, cv2.LINE_AA)

def contact_shadow(frame, cx, by, width):
    over = frame.copy()
    cv2.ellipse(over, (int(cx), int(by) - 6), (int(width / 2), 26), 0, 0, 360, (20, 26, 22), -1, cv2.LINE_AA)
    cv2.addWeighted(over, 0.35, frame, 0.65, 0, frame)

# ---------------- beats ----------------
# shot = (size_px, anchor_fx, anchor_fy, screen_x, screen_y); size = height (or width if "wide")
SPINE_BAD = [(0.57, 0.125), (0.46, 0.14), (0.32, 0.18), (0.19, 0.27), (0.12, 0.37), (0.12, 0.47)]   # fix 4: starts at skull base
SPINE_GOOD = [(0.40, 0.125), (0.35, 0.19), (0.31, 0.28), (0.29, 0.37), (0.30, 0.46), (0.33, 0.54)]
BEATS = [
    dict(start=0.0, pose="bad_posture_desk", shot=(1900, 0.5, 0.0, 560, 330), grade="bad",       # fix 1, 20
         glow=[(0.58, 0.13, "w", 0, "body")], sfx=[("t", 0.0, "sad_sting", .3)]),
    dict(start=("w", 0, "because"), pose="bad_posture_desk", shot=(2700, 0.6, 0.08, 560, 760), grade="bad",
         glow=[(0.58, 0.13, "w", 0, "because")], texts=[(("w", 0, "lack"), "NOT MUSCLE", 130, 330)]),
    dict(start=("line", 1), pose="bad_posture_desk", shot=(1750, 0.45, 0.0, 560, 430),
         spine=(SPINE_BAD, RED, ("w", 1, "posture")),
         arrows=[((0.84, 0.10), (1.02, 0.11), RED, ("w", 1, "drifted"), False, 0.0)],                 # fix 5
         sfx=[(("w", 1, "drifted"), "pop_soft", .5)]),
    dict(start=("line", 2), pose="slumped", shot=(2100, 0.5, 0.0, 540, 400)),
    dict(start=("w", 2, "starts"), pose="sore_back", shot=(2000, 0.62, 0.0, 560, 380), flash=True,        # fix 6, 7
         glow=[(0.74, 0.12, "w", 2, "neck"), (0.32, 0.33, "w", 2, "pain")], sfx=[("t", 0.0, "sad_sting", .35)]),
    dict(start=("line", 3), pose="side_view", shot=(1650, 0.02, 1.0, 300, 1800), wall=300),            # fix 8
    dict(start=("line", 4), pose="side_view", shot=(2700, 0.02, 0.0, 300, 420), wall=300,
         gap=(("w", 4, "touch")), sfx=[(("w", 4, "touch"), "pop_soft", .5)]),
    dict(start=("w", 4, "millions"), pose="phone_scroll", shot=(2100, 0.5, 0.0, 540, 400),
         glow=[(0.5, 0.135, "w", 4, "millions")]),
    dict(start=("line", 5), card="deg", sfx=[("t", 0.0, "whistle_up", .3)]),                            # fix 10
    dict(start=("w", 5, "adds"), card="kg", sfx=[(("w", 5, "twelve"), "boing", .35)]),                  # fix 11
    dict(start=("line", 6), pose="point_viewer", shot=(2000, 0.5, 0.0, 540, 600),                       # fix 12
         texts=[(("w", 6, "fifteen"), "15 DAYS", 140, 260), (("w", 6, "five"), "5 MIN / DAY", 96, 410)],
         sfx=[(("w", 6, "fifteen"), "pop_soft", .5), (("w", 6, "five"), "pop_soft", .5)]),
    dict(start=("line", 7), pose="side_view", shot=(3000, 0.55, 0.0, 560, 600), label=("1", "CHIN TUCKS"),  # fix 14
         ghost=("w", 7, "pull"), arrows=[((1.06, 0.118), (0.84, 0.118), GREEN, ("w", 7, "pull"), True, 0.0)]),
    dict(start=("line", 8), pose="cobra_stretch", wide=True, shot=(980, 0.5, 0.5, 540, 1180), label=("2", "COBRA STRETCH"),  # fix 15
         arrows=[((0.86, 0.62), (0.80, 0.10), GREEN, ("w", 8, "chest"), True, 0.12)]),
    dict(start=("line", 9), pose="hip_flexor_stretch", shot=(1280, 0.5, 1.0, 540, 1830), label=("3", "HIP FLEXOR"),
         arrows=[((0.30, 0.56), (0.68, 0.56), GREEN, ("w", 9, "push"), True, 0.0)]),
    dict(start=("line", 10), pose="glute_bridge_down", alt="glute_bridge_up", wide=True, shot=(980, 0.5, 0.5, 540, 1180),
         label=("4", "GLUTE BRIDGE"), arrows=[((0.40, 0.62), (0.40, 0.06), GREEN, ("w", 10, "drive"), True, 0.0)]),   # fix 16
    dict(start=("line", 11), pose="good_posture_desk", shot=(1750, 0.45, 0.0, 560, 430), sparkles=True,
         spine=(SPINE_GOOD, GREEN, ("w", 11, "plan"))),
    dict(start=("line", 12), pose="point_viewer", shot=(2700, 0.5, 0.0, 540, 640), sparkles=True,
         typewriter=[(("w", 12, "save"), "SAVE THIS", 120, (255, 255, 255), 250),
                     (("w", 12, "follow"), "FOLLOW", 150, (235, 64, 52), 400)]),
]

def T(cue):
    if isinstance(cue, (int, float)):
        return float(cue)
    if cue[0] == "line":
        return TIMING[cue[1]]["start"] - 0.08
    if cue[0] == "w":
        return wt(cue[1], cue[2]) - 0.04
    raise ValueError(cue)

STARTS = [T(b["start"]) for b in BEATS]
TOTAL = TIMING[-1]["end"] + END_HOLD
ENDS = STARTS[1:] + [TOTAL]

def xform(b, name, t, t0):
    size, ax, ay, sx, sy = b["shot"]
    im = pose(name); ph, pw = im.shape[:2]
    s = size / pw if b.get("wide") else size / ph
    k = BEATS.index(b)
    if k % 2 == 0:                                                     # push-in on alternate beats (ref: ~46% of frames move)
        s *= 1 + 0.03 * smooth((t - t0) / max(0.5, ENDS[k] - t0))
    return s, sx - ax * pw * s, sy - ay * ph * s, pw, ph

def scr(fx, fy, xf):
    s, tx, ty, pw, ph = xf
    return int(tx + fx * pw * s), int(ty + fy * ph * s)

def render_card(frame, b, t, t0):
    since = t - t0; kk = since * FPS
    if b["card"] == "deg":
        blit_center(frame, text_img("EVERY 15°", 190), 540, 820, back_out(kk / 8), min(1, kk / 3))
        tf = wt(5, "forward") - 0.04
        if t > tf:
            k2 = (t - tf) * FPS
            blit_center(frame, text_img("FORWARD", 120, (235, 64, 52)), 540, 1010, back_out(k2 / 8), min(1, k2 / 3))
        # tilting head line: a little animated angle marker
        ang = math.radians(15 * smooth(since / 0.6))
        c = (540, 1420); L = 280
        cv2.line(frame, c, (c[0], c[1] - L), (200, 220, 210), 14, cv2.LINE_AA)
        cv2.line(frame, c, (int(c[0] + L * math.sin(ang)), int(c[1] - L * math.cos(ang))), RED, 20, cv2.LINE_AA)
        cv2.ellipse(frame, c, (170, 170), -90, 0, math.degrees(ang), RED, 10, cv2.LINE_AA)
    else:
        t12 = wt(5, "twelve") - 0.25
        if t >= t12:
            k = (t - t12) * FPS
            n = min(12, int(12 * ease_out((t - t12) / 0.35)))
            shake = 10 * math.sin(k * 1.9) * max(0, 1 - (t - t12) / 0.4)
            blit_center(frame, text_img(f"{n} KG", 290), 540 + shake, 860, back_out(k / 7), min(1, k / 2))
            r = int(470 + 18 * math.sin(t * 6))
            cv2.circle(frame, (540, 900), r, RED, 12, cv2.LINE_AA)
        tn = wt(5, "neck") - 0.04
        if t > tn:
            k2 = (t - tn) * FPS
            blit_center(frame, text_img("ON YOUR NECK", 92), 540, 1150, back_out(k2 / 8), min(1, k2 / 3))

def render_frame(t, frame):
    k = max(i for i, s in enumerate(STARTS) if s <= t or i == 0)
    b = BEATS[k]; t0 = STARTS[k]; since = t - t0
    prev = BEATS[k - 1] if k > 0 else None
    bad = b.get("grade") == "bad"; pbad = prev is not None and prev.get("grade") == "bad"
    g = min(1, since * FPS / 3)
    mix = (1 if bad else 0) * g + (1 if pbad else 0) * (1 - g) if k > 0 else (1 if bad else 0)
    bg = BG_GOOD * (1 - mix) + BG_BAD * mix
    if b.get("flash") and since * FPS < 4:                 # light, background-only flash (fix 6)
        bg = bg * 0.65 + BG_FLASH * 0.35
    frame[:] = bg.astype(np.uint8)
    MASK[:] = 0
    if "card" in b:
        render_card(frame, b, t, t0)
    else:
        name = b["pose"]
        xf = xform(b, name, t, t0)
        if "wall" in b:                                    # real wall with baseboard (fix 8)
            wx = b["wall"]
            cv2.rectangle(frame, (0, 0), (wx, H), (104, 132, 92), -1)
            for yy in range(80, H, 160):
                cv2.line(frame, (0, yy), (wx, yy), (96, 122, 85), 3)
            cv2.rectangle(frame, (0, 1760), (wx, H), (64, 82, 58), -1)
            cv2.line(frame, (wx, 0), (wx, H), (140, 170, 125), 10)
        same = prev is not None and prev.get("pose") == name
        first = k == 0
        s, tx, ty, pw, ph = xf
        if first:
            e = 1.0; sc = s; tx2, ty2 = tx, ty
        elif same:                                         # hard cut + small punch (fix 2)
            e = 1.0; p = 1 + 0.05 * (1 - ease_out(since * FPS / 5)); sc = s * p
            cx, cy = tx + pw * s / 2, ty + ph * s / 2
            tx2, ty2 = cx - pw * sc / 2, cy - ph * sc / 2
        else:                                              # new pose: grow + rise
            e = ease_out(since * FPS / 9); grow = 0.78 + 0.22 * e; sc = s * grow
            cx, by = tx + pw * s / 2, ty + ph * s
            tx2, ty2 = cx - pw * sc / 2, by - ph * sc + (1 - e) * 520
        tint = np.array([0.86, 0.90, 1.06]) if mix > 0.5 else None
        bottom = ty2 + ph * sc
        if bottom < H - 40 and not b.get("wide"):
            contact_shadow(frame, tx2 + pw * sc * 0.5, bottom, pw * sc * 0.75)
        # glute bridge: smooth crossfade rep loop (fix 16)
        if "alt" in b and since > 0.5:
            cyc = ((since - 0.5) % 1.2) / 1.2
            wup = smooth(min(1, max(0, (cyc - 0.05) / 0.08))) * (1 - smooth(min(1, max(0, (cyc - 0.55) / 0.08))))
            xf_up = xform(b, b["alt"], t, t0)
            blit_affine(frame, pose(name), xf[0], xf[1], xf[2], 1 - wup, tint)
            blit_affine(frame, pose(b["alt"]), xf_up[0], xf_up[1], xf_up[2], wup, tint)
        else:
            if b.get("ghost") and t > T(b["ghost"]):        # chin tuck: red ghost of the forward head (fix 14)
                osc = 0.5 + 0.5 * math.sin((t - T(b["ghost"])) * 2 * math.pi / 1.1)
                blit_affine(frame, pose(name), sc, tx2 + 70 * osc, ty2, 0.30 * osc, np.array([0.5, 0.55, 1.4]), keep_mask=False)
            blit_affine(frame, pose(name), sc, tx2, ty2, min(1.0, 0.4 + e), tint)
        if e > 0.97:
            if "spine" in b:
                pts, col, cue = b["spine"]
                draw_spine(frame, [scr(x, y, xf) for x, y in pts], col, ease_out((t - T(cue)) * FPS / 14))
            for p0, p1, col, cue, loop, curve in b.get("arrows", []):
                kk = (t - T(cue)) * FPS
                if kk > 0:
                    prog = ease_out(kk / 10)
                    if loop and kk > 10:
                        prog = 0.6 + 0.4 * (0.5 + 0.5 * math.cos((kk - 10) / FPS * 2 * math.pi / 1.1))
                    draw_arrow(frame, scr(*p0, xf), scr(*p1, xf), col, prog, curve=curve)
            for fx, fy, *cue in b.get("glow", []):
                tc = T(tuple(cue)) if cue[0] == "w" else 0
                if t >= tc:
                    draw_glow(frame, scr(fx, fy, xf), t)
            if "gap" in b and t > T(b["gap"]):
                hx, hy = scr(0.32, 0.06, xf)
                kk = (t - T(b["gap"])) * FPS
                pe = ease_out(kk / 8)
                draw_dashed(frame, (b["wall"], hy), (int(b["wall"] + (hx - b["wall"]) * pe), hy), RED, 10)
                cv2.line(frame, (b["wall"], hy - 40), (b["wall"], hy + 40), RED, 8, cv2.LINE_AA)
                cv2.line(frame, (hx, hy - 40), (hx, hy + 40), RED, 8, cv2.LINE_AA)
                if kk > 6:
                    blit_center(frame, text_img("GAP", 96, (235, 64, 52)), (b["wall"] + hx) / 2, hy - 110, back_out((kk - 6) / 8))
            if b.get("sparkles"):
                draw_sparkles(frame, t)
    if "label" in b:                                       # bigger, centred pop-in (fix 17, 18)
        n_, name_ = b["label"]; kk = since * FPS
        blit_center(frame, text_img(n_, 170, (90, 225, 120)), 540, 210, back_out(kk / 8), min(1, kk / 3))
        if kk > 4:
            blit_center(frame, text_img(name_, 112), 540, 360, back_out((kk - 4) / 8), min(1, (kk - 4) / 3))
    for cue, s_, size, y in b.get("texts", []):
        kk = (t - T(cue)) * FPS
        if kk >= 0:
            blit_center(frame, text_img(s_, size), 540, y + 5 * math.sin(t * 3), back_out(kk / 8), min(1, kk / 3))
    for cue, s_, size, col, y in b.get("typewriter", []):
        n = int(max(0, t - T(cue)) * 20)
        if n > 0:
            full = text_img(s_, size, col); part = text_img(s_[:n], size, col)
            blit_center(frame, part, 540 - (full.shape[1] - part.shape[1]) / 2, y)
    return k

# ---------------- audio ----------------
def load_audio(path, sr=48000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

def build_audio(out_wav):
    sr = 48000; n = int(TOTAL * sr)
    mix = np.zeros((n, 2), np.float32)
    v = load_audio(P("voice/voice_full.wav"))[:n]; mix[:len(v)] += v
    m = load_audio(P("assets/music/hyper_lillian_thorn.mp3"))
    xf = int(1.5 * sr); ramp = np.linspace(0, 1, xf)[:, None]
    cyc = np.concatenate([m[:xf] * ramp + m[-xf:] * (1 - ramp), m[xf:-xf]])     # seamless loop
    mus = np.tile(cyc, (int(np.ceil(n / len(cyc))) + 1, 1))[:n]
    env = np.zeros(n); env[:len(v)] = np.abs(v[:, 0])
    win = int(0.12 * sr); env = np.convolve(env, np.ones(win) / win, "same")
    duck = 1 - 0.5 * np.clip(env / (env.max() * 0.25 + 1e-9), 0, 1)          # deeper ducking (fix 27)
    vr = np.sqrt((v ** 2).mean()); mr = np.sqrt((mus ** 2).mean()) + 1e-9
    fade = np.ones(n); fl = int(1.2 * sr); fade[-fl:] = np.linspace(1, 0, fl)
    mix += mus * (vr / mr) * 10 ** (-2 / 20) * (duck * fade)[:, None]
    cache = {}
    def sfx(name, at, vol):
        if name not in cache:
            cache[name] = load_audio(P("assets/sfx", name + (".mp3" if name.startswith("typing") else ".wav")))
        s = cache[name]; i0 = int(at * sr)
        if 0 <= i0 < n:
            seg = s[:n - i0]; mix[i0:i0 + len(seg)] += seg * vol * vr / 0.1
    for k, b in enumerate(BEATS):
        t0 = STARTS[k]; prev = BEATS[k - 1] if k else None
        if k and b.get("pose") and (not prev or prev.get("pose") != b.get("pose")):
            sfx("swoosh_up", t0, .28)                   # whoosh only on real entrances
        for e in b.get("sfx", []):
            if e[0] == "t":                          # ("t", offset, name, vol): relative to beat start
                sfx(e[2], t0 + e[1], e[3])
            else:                                    # (word_cue, name, vol)
                sfx(e[1], T(e[0]), e[2])
        if "label" in b:
            sfx("pop_soft", t0 + 0.13, .45)
        for cue, *_ in b.get("typewriter", []):
            sfx("typing_loud", T(cue), 0.22)
    mix /= np.abs(mix).max() / 0.9
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--preview"); a = ap.parse_args()
    os.makedirs(P("out"), exist_ok=True)
    frame = np.zeros((H, W, 3), np.uint8)
    if a.preview:
        os.makedirs(P("out/stills"), exist_ok=True)
        for s in a.preview.split(","):
            render_frame(float(s), frame)
            cv2.imwrite(P("out/stills", f"t{float(s):05.2f}.jpg"), frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        return
    build_audio(P("out/mix.wav"))
    af = ("deesser=i=0.4,equalizer=f=110:t=q:w=1:g=3.5,equalizer=f=6500:t=q:w=1.2:g=-3.5,"
          "acompressor=threshold=-20dB:ratio=1.8:attack=10:release=180:makeup=1,loudnorm=I=-14:TP=-1.0:LRA=9")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", P("out/mix.wav"), "-af", af, "-ar", "48000",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                            P("out/posture03.mp4")], stdin=subprocess.PIPE)
    nf = int(TOTAL * FPS)
    for i in range(nf):
        render_frame(i / FPS, frame); enc.stdin.write(frame.tobytes())
    enc.stdin.close(); enc.wait()
    print(f"{nf} frames -> out/posture03.mp4")

if __name__ == "__main__":
    main()
