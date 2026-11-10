#!/usr/bin/env python3
"""posture05 — v5 (variation engine, high-energy hook). Based on v4: fixes from posture03/REVIEW_v3.md.

New vs v3: 3D card-flip pose changes, tilt+settle on emphasis words, bounce entrances (full opacity),
muscle-shaped colour highlights clipped to the body, anatomy inset badges (repo anatomy images),
flat block arrows placed only in empty space (auto-checked against the character mask), split bad/good
panels, word-by-word hook captions, exercise key-pose punches, pop-out badges on the CTA.
Usage: python3 build.py [--preview 1.0,5.2,...] [--check]
"""
import argparse, json, math, os, subprocess, wave
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)
BG_GOOD = np.array([76, 92, 44], np.float32)
BG_BAD = np.array([46, 52, 70], np.float32)
BG_FLASH = np.array([40, 40, 120], np.float32)
RED, GREEN, YELLOW, BLUE = (52, 64, 235), (80, 205, 105), (60, 200, 250), (230, 150, 60)   # BGR
WORDS = json.load(open(P("voice/words.json")))
TIMING = json.load(open(P("voice/timing.json")))
END_HOLD = 1.0

def ease_out(x):
    x = min(max(x, 0.0), 1.0); return 1 - (1 - x) ** 3
def back_out(x, k=1.7):
    x = min(max(x, 0.0), 1.0); return 1 + (k + 1) * (x - 1) ** 3 + k * (x - 1) ** 2
def smooth(x):
    x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)

def wt(line, word, occ=0, edge="s"):
    ws = [w for w in WORDS if w["line"] == line and w["w"] == word]
    return ws[min(occ, len(ws) - 1)][edge]

def T(cue):
    if isinstance(cue, (int, float)):
        return float(cue)
    if cue[0] == "line":
        return TIMING[cue[1]]["start"] - 0.08
    return wt(cue[1], cue[2], cue[3] if len(cue) > 3 else 0) - 0.04

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
    h, w = im.shape[:2]
    a = im[:, :, 3] > 8
    seat = int(np.nonzero(a[: int(0.75 * h), : int(0.35 * w)].any(1))[0].max()) - 8
    c = np.zeros((h, w, 4), np.uint8); x0, x1 = 0, int(0.64 * w)
    for y in range(seat, seat + 56):
        k = (y - seat) / 56
        cv2.line(c, (x0, y), (x1, y), (int(78 - 40 * k), int(98 - 46 * k), int(86 - 40 * k), 255), 1)
    cv2.rectangle(c, (x0, seat), (x1, seat + 56), (20, 26, 22, 255), 4)
    for lx in (x0 + 24, x1 - 60):
        cv2.rectangle(c, (lx, seat + 56), (lx + 34, h - 4), (36, 46, 40, 255), -1)
        cv2.line(c, (lx + 6, seat + 60), (lx + 6, h - 8), (70, 88, 78, 255), 4)
        cv2.rectangle(c, (lx, seat + 56), (lx + 34, h - 4), (20, 26, 22, 255), 4)
    _over(c, im); return c

def _with_mat(im):
    h, w = im.shape[:2]; pad = int(0.07 * h) + 24
    c = np.zeros((h + pad, w + 80, 4), np.uint8); y0 = h - int(0.05 * h) + pad // 3
    pts = np.array([[24, y0], [w + 56, y0], [w + 34, h + pad - 6], [46, h + pad - 6]], np.int32)
    cv2.fillPoly(c, [pts], (60, 66, 72, 255))
    cv2.fillPoly(c, [np.array([[24, y0], [w + 56, y0], [w + 52, y0 + 10], [28, y0 + 10]], np.int32)], (96, 104, 112, 255))
    cv2.polylines(c, [pts], True, (26, 28, 30, 255), 5, cv2.LINE_AA)
    sub = c[0:h, 40:40 + w].copy(); _over(sub, im); c[0:h, 40:40 + w] = sub
    return c

# Muscle shapes in % of the *raw* pose crop (traced on a 5% grid). Mats/bench offsets are handled below.
MUSCLES = {
    ("bad_posture_desk", "traps"): [(58, 11), (66, 16), (62, 22), (50, 23), (38, 20), (30, 15), (40, 10), (50, 9)],
    ("sore_back", "lower_back"): [(14, 23), (30, 21), (42, 25), (40, 36), (25, 38), (13, 33)],
    ("sore_back", "neck"): [(66, 8), (77, 6), (84, 11), (78, 16), (66, 15)],
    ("side_view", "neck"): [(36, 9), (62, 9.5), (68, 14), (50, 16.5), (34, 14)],
    ("cobra_stretch", "abs"): [(84, 38), (93, 42), (91, 55), (82, 62), (76, 58), (80, 48)],
    ("hip_flexor_stretch", "hip_flexor"): [(38, 58), (48, 60), (40, 72), (25, 88), (14, 90), (22, 76), (30, 64)],
    ("glute_bridge_up", "glutes"): [(33, 12), (46, 10), (52, 25), (48, 42), (36, 42), (29, 28)],
}
PADS = {}            # name -> (x_off, y_off) of the raw crop inside the composed layer
POSES = {}
def pose(name):
    if name not in POSES:
        im = _load(name)
        PADS[name] = (0, 0, im.shape[1], im.shape[0])
        if name in ("bad_posture_desk", "good_posture_desk"):
            im = _with_bench(im)
        if name in ("cobra_stretch", "glute_bridge_up", "glute_bridge_down"):
            raw = im; im = _with_mat(im); PADS[name] = (40, 0, raw.shape[1], raw.shape[0])
        POSES[name] = im
    return POSES[name]

def muscle_mask(name, part):
    """Soft mask (layer coordinates) of a muscle, clipped to the body alpha."""
    key = ("mm", name, part)
    if key not in POSES:
        im = pose(name); ox, oy, rw, rh = PADS[name]
        pts = np.array([(ox + x / 100 * rw, oy + y / 100 * rh) for x, y in MUSCLES[(name, part)]], np.int32)
        m = np.zeros(im.shape[:2], np.float32); cv2.fillPoly(m, [pts], 1.0, cv2.LINE_AA)
        m = cv2.GaussianBlur(m, (0, 0), max(2, 0.008 * im.shape[0]))
        POSES[key] = m * (im[:, :, 3] / 255.0)
    return POSES[key]

ANAT = {}
def anat(name, d=330):
    """Round inset badge from a repo anatomy image: circle crop, white ring, drop shadow."""
    key = (name, d)
    if key not in ANAT:
        im = cv2.imread(P("assets/anatomy", name + ".webp"))
        im = cv2.resize(im, (d, d), interpolation=cv2.INTER_AREA)
        pad = 24; S = d + 2 * pad
        out = np.zeros((S, S, 4), np.uint8)
        sh = np.zeros((S, S), np.float32); cv2.circle(sh, (S // 2 + 6, S // 2 + 10), d // 2 + 8, 1, -1)
        sh = cv2.GaussianBlur(sh, (0, 0), 9); out[:, :, 3] = (sh * 110).astype(np.uint8)
        cm = np.zeros((d, d), np.uint8); cv2.circle(cm, (d // 2, d // 2), d // 2 - 8, 255, -1, cv2.LINE_AA)
        ring = np.zeros((S, S, 4), np.uint8); cv2.circle(ring, (S // 2, S // 2), d // 2 + 2, (255, 255, 255, 255), -1, cv2.LINE_AA)
        _over(out, ring)
        core = np.zeros((S, S, 4), np.uint8); core[pad:pad + d, pad:pad + d, :3] = im; core[pad:pad + d, pad:pad + d, 3] = cm
        _over(out, core)
        ANAT[key] = out
    return ANAT[key]

FONT = P("assets/fonts/Nunito.ttf")
TEXTS = {}
def text_img(s, size, color=(255, 255, 255)):
    key = (s, size, color)
    if key not in TEXTS:
        f = ImageFont.truetype(FONT, size); f.set_variation_by_name("Black")
        l, t, r, b = f.getbbox(s); pad = 30
        im = Image.new("RGBA", (max(1, r - l) + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.text((pad - l + 5, pad - t + 7), s, font=f, fill=(0, 0, 0, 120))
        d.text((pad - l, pad - t), s, font=f, fill=color + (255,))
        TEXTS[key] = cv2.cvtColor(np.array(im), cv2.COLOR_RGBA2BGRA)
    return TEXTS[key]

# ---------------- compositing ----------------
MASK = np.zeros((H, W), np.float32)
def blit_m(frame, rgba, M, alpha=1.0, tint=None, keep_mask=True, extra=None):
    """Blit with a full 2x3 affine. extra: list of (mask_layer, BGR colour, strength) muscle highlights."""
    if alpha <= 0.01:
        return
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
    for mm, col, k in (extra or []):
        mw = cv2.warpAffine(mm, M, (W, H), flags=cv2.INTER_LINEAR)[y0:y1, x0:x1, None] * k
        lum = src.mean(2, keepdims=True) / 255
        painted = np.array(col, np.float32) * (0.45 + 0.75 * lum)          # flat colour that keeps the shading
        src = src * (1 - mw) + np.clip(painted, 0, 255) * mw
    aa = a[y0:y1, x0:x1, None]
    roi = frame[y0:y1, x0:x1].astype(np.float32)
    frame[y0:y1, x0:x1] = (roi * (1 - aa) + src * aa).astype(np.uint8)

def M_of(s, tx, ty, sx_mul=1.0, rot_deg=0.0, pivot=None):
    """Scale s (x scaled by sx_mul), translate, then rotate around pivot (screen)."""
    M = np.float32([[s * sx_mul, 0, tx], [0, s, ty]])
    if rot_deg and pivot is not None:
        R = cv2.getRotationMatrix2D(pivot, rot_deg, 1.0)
        M = (np.vstack([R, [0, 0, 1]]) @ np.vstack([M, [0, 0, 1]]))[:2].astype(np.float32)
    return M

def blit_center(frame, rgba, cx, cy, s=1.0, alpha=1.0):
    h, w = rgba.shape[:2]
    blit_m(frame, rgba, np.float32([[s, 0, cx - w * s / 2], [0, s, cy - h * s / 2]]), alpha, keep_mask=False)

def block_arrow(length, width, color, curve=0.0):
    """Flat block arrow sprite pointing +x (BGRA), with a darker underside and soft shadow."""
    head_l, head_w = width * 1.25, width * 2.2
    L = int(length); Hh = int(head_w + 40)
    c = np.zeros((Hh + 30, L + 40, 4), np.uint8)
    cy = Hh // 2 + 10
    shaft = [(20, cy - width / 2), (20 + L - head_l, cy - width / 2), (20 + L - head_l, cy - head_w / 2),
             (20 + L, cy), (20 + L - head_l, cy + head_w / 2), (20 + L - head_l, cy + width / 2), (20, cy + width / 2)]
    pts = np.array(shaft, np.float32)
    if curve:
        xs = (pts[:, 0] - 20) / L
        pts[:, 1] -= curve * width * 3 * np.sin(np.pi * xs)
    p = pts.astype(np.int32)
    sh = np.zeros(c.shape[:2], np.float32); cv2.fillPoly(sh, [p + np.array([6, 10])], 1.0, cv2.LINE_AA)
    sh = cv2.GaussianBlur(sh, (0, 0), 6); c[:, :, 3] = (sh * 90).astype(np.uint8)
    body = np.zeros_like(c); cv2.fillPoly(body, [p], tuple(int(v) for v in color) + (255,), cv2.LINE_AA)
    dark = tuple(int(v * 0.72) for v in color)
    lower = p.copy(); lower[:, 1] = np.maximum(lower[:, 1], cy + width * 0.12)
    under = np.zeros_like(c); cv2.fillPoly(under, [p], dark + (255,), cv2.LINE_AA)
    under[: int(cy + width * 0.1), :, 3] = 0
    _over(c, body); _over(c, under)
    return c

ARROWS = {}
def draw_block_arrow(frame, x0, y0, x1, y1, color, width, prog, curve=0.0, check=None):
    if prog <= 0.01:
        return
    L = max(40, math.hypot(x1 - x0, y1 - y0))
    key = (int(L), width, color, curve)
    if key not in ARROWS:
        ARROWS[key] = block_arrow(L, width, color, curve)
    spr = ARROWS[key]
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
    slide = (1 - ease_out(prog)) * 70
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    sx0, sy0 = x0 - ux * slide, y0 - uy * slide
    h, w = spr.shape[:2]
    M = cv2.getRotationMatrix2D((20, h / 2), -ang, 1.0); M[0, 2] += sx0 - 20; M[1, 2] += sy0 - h / 2
    if check is not None:                                  # overlap with the character silhouette
        lay = cv2.warpAffine(spr[:, :, 3], M.astype(np.float32), (W, H))
        check.append(float(((lay > 200) & (MASK > 0.5)).sum()))
    blit_m(frame, spr, M.astype(np.float32), min(1, prog * 1.5), keep_mask=False)

# ---------------- variation engine ----------------
SEED = int(os.environ.get("STYLE_SEED", "5"))           # each video gets its own seed -> its own look
RNG = np.random.default_rng(SEED)
ENTERS = ["rise", "slide_l", "slide_r", "drop", "pop", "cut", "fade", "panel", "flip"]

def ease(kind, x):
    x = min(max(x, 0.0), 1.0)
    if kind == "back":
        return back_out(x, 1.5)
    if kind == "expo":
        return 1 - 2 ** (-10 * x) if x < 1 else 1.0
    return ease_out(x)

def style_palette(rng):
    """2 main + 2 accent transition types for this video (flip is only ever an accent)."""
    pool = ["rise", "slide", "drop", "pop", "cut", "fade", "panel"]
    motion = ["rise", "slide", "drop", "pop", "panel"]          # main styles always carry real motion
    main = list(rng.choice(motion, 2, replace=False))
    acc = list(rng.choice([p for p in pool if p not in main], 2, replace=False))
    w = {p: 0.0 for p in pool}
    for p in main: w[p] = 3.0
    for p in acc: w[p] = 1.2
    return w

def assign_transitions(beats, rng):
    """Fill missing 'enter' values: weighted by this video's palette, never the same twice in a row,
    at most 2 flips, random duration 6-13 frames and random easing."""
    pal = style_palette(rng)
    flips = sum(1 for b in beats if b.get("enter") == "flip")
    prev = None
    for b in beats:
        if "card" in b or b.get("split"):
            prev = "card"; continue
        if "enter" not in b:
            opts = {k: v for k, v in pal.items() if v > 0 and k != (prev[:5] if prev else None)}
            if b.get("hint") == "reveal" and flips < 2:
                opts["flip"] = 2.5
            ks = list(opts); p = np.array([opts[k] for k in ks]); p /= p.sum()
            e = str(rng.choice(ks, p=p))
            if e == "slide":
                e = "slide_l" if rng.random() < 0.5 else "slide_r"
            if e == "flip":
                flips += 1
            b["enter"] = e
        b.setdefault("dur", int(rng.integers(9, 17)))
        b.setdefault("easing", str(rng.choice(["out", "back", "expo"])))
        prev = b["enter"]
    return pal

# ---------------- beats ----------------
# shot = (size, ax, ay, sx, sy); wide=True -> size is width.  Hook (0-5 s) is hand-directed for maximum motion.
BEATS = [
    # HOOK: 4 different moves in ~5 s
    dict(start=0.0, pose="bad_posture_desk", shot=(1850, 0.5, 0.0, 560, 430), grade="bad", enter="slide_r", dur=13,
         preroll=3, easing="out", muscles=[("traps", RED, ("w", 0, "body"))], caption=0, zooms=[(("w", 0, "body"), 0.10, (0.6, 0.3))],
         sfx=[("t", 0.0, "sad_sting", .3)]),
    dict(start=("w", 0, "small"), pose="this_small", shot=(1800, 0.5, 0.0, 540, 470), grade="bad", enter="pop", dur=9,
         easing="back", caption=0),
    dict(start=("w", 0, "because"), pose="double_biceps", shot=(1750, 0.5, 0.0, 540, 520), enter="drop", dur=8, zooms=[(("w", 0, "muscle"), 0.12, (0.5, 0.25))],
         easing="back", stamp=(("w", 0, "muscle"), "NOT MUSCLE"), sfx=[(("w", 0, "muscle"), "boing", .3)]),
    dict(start=("line", 1), pose="bad_posture_desk", shot=(1500, 0.45, 0.0, 470, 600), enter="panel", dur=9, easing="out",
         caption=1, zooms=[(("w", 1, "posture"), 0.08, (0.55, 0.35)), (("w", 1, "head"), 0.10, (0.7, 0.3))], insets=[("anat_bone_spine_bad", ("w", 1, "posture"), 180, 920, 1470)],
         arrows=[((0.97, 0.08), (1.19, 0.08), RED, 60, ("w", 1, "drifted"), 0.0)], flash_at=("w", 1, "head"),
         sfx=[(("w", 1, "posture"), "pop_soft", .5), (("w", 1, "drifted"), "swoosh_up", .3)]),
    # body
    dict(start=("line", 2), pose="slumped", shot=(2050, 0.5, 0.0, 540, 420)),
    dict(start=("w", 2, "starts"), pose="sore_back", shot=(1950, 0.62, 0.0, 600, 420), flash=True,
         muscles=[("neck", RED, ("w", 2, "neck")), ("lower_back", RED, ("w", 2, "pain"))],
         insets=[("anat_pain_neck", ("w", 2, "neck"), 180, 195, 1530)], sfx=[("t", 0.0, "sad_sting", .35)]),
    dict(start=("line", 3), pose="side_view", shot=(1700, 0.02, 1.0, 330, 1800), wall=330, gap=("w", 4, "touch"),
         sfx=[(("w", 4, "touch"), "pop_soft", .5)]),
    dict(start=("w", 4, "millions"), pose="phone_scroll", shot=(2050, 0.5, 0.0, 540, 430), hint="reveal"),
    dict(start=("line", 5), card="deg", sfx=[("t", 0.0, "whistle_up", .3)]),
    dict(start=("w", 5, "adds"), card="kg", sfx=[(("w", 5, "twelve"), "boing", .35)]),
    dict(start=("line", 6), pose="point_viewer", shot=(2000, 0.5, 0.0, 540, 620),
         texts=[(("w", 6, "fifteen"), "15 DAYS", 140, 270), (("w", 6, "five"), "5 MIN / DAY", 96, 420)],
         sfx=[(("w", 6, "fifteen"), "pop_soft", .5), (("w", 6, "five"), "pop_soft", .5)]),
    dict(start=("line", 7), pose="side_view", shot=(2900, 0.55, 0.0, 470, 620), label=("1", "CHIN TUCKS"),
         muscles=[("neck", GREEN, ("w", 7, "chin"))], insets=[("anat_muscle_neck", ("w", 7, "chin"), 220, 880, 1350)],
         arrows=[((1.55, 0.118), (1.10, 0.118), GREEN, 56, ("w", 7, "pull"), 0.0)]),
    dict(start=("line", 8), pose="cobra_stretch", wide=True, shot=(1000, 0.5, 0.5, 540, 1250), label=("2", "COBRA STRETCH"),
         muscles=[("abs", GREEN, ("w", 8, "chest"))], insets=[("anat_muscle_abs", ("w", 8, "chest"), 200, 190, 740)],
         arrows=[((0.45, 0.62), (0.45, 0.18), GREEN, 58, ("w", 8, "chest"), 0.0)]),
    dict(start=("line", 9), pose="hip_flexor_stretch", shot=(1250, 0.5, 1.0, 650, 1830), label=("3", "HIP FLEXOR"),
         insets=[("anat_muscle_hip_flexors", ("w", 9, "hips"), 190, 200, 720)],
         arrows=[((-0.34, 0.56), (-0.05, 0.56), GREEN, 58, ("w", 9, "push"), 0.0)]),
    dict(start=("line", 10), pose="glute_bridge_down", alt="glute_bridge_up", wide=True, shot=(1000, 0.5, 0.5, 540, 1250),
         label=("4", "GLUTE BRIDGE"), muscles=[("glutes", GREEN, ("w", 10, "squeeze"))],
         insets=[("anat_muscle_glutes", ("w", 10, "squeeze"), 200, 880, 760)],
         arrows=[((0.40, -0.12), (0.40, -0.62), GREEN, 56, ("w", 10, "drive"), 0.0)]),
    dict(start=("line", 11), split=True, sfx=[("t", 0.0, "swoosh_up", .3), ("t", 0.25, "swoosh_up", .3)]),
    dict(start=("line", 12), pose="point_viewer", shot=(2700, 0.5, 0.0, 540, 640), hint="reveal",
         typewriter=[(("w", 12, "save"), "SAVE THIS", 120, (255, 255, 255), 250),
                     (("w", 12, "follow"), "FOLLOW", 150, (235, 64, 52), 400)]),
]
PALETTE = assign_transitions(BEATS, RNG)
LABEL_STYLES = list(RNG.permutation(4))                   # 4 exercises -> 4 different label layouts
for i, b in enumerate([b for b in BEATS if "label" in b]):
    b["label_style"] = int(LABEL_STYLES[i % 4])
STARTS = [T(b["start"]) for b in BEATS]
TOTAL = TIMING[-1]["end"] + END_HOLD
ENDS = STARTS[1:] + [TOTAL]
for k_, b_ in enumerate(BEATS):                              # one zoom punch on every long beat (seeded amount/focus)
    if "zooms" not in b_ and ENDS[k_] - STARTS[k_] > 3.0 and "card" not in b_:
        zs = []
        for frac in ((0.4, 0.8) if ENDS[k_] - STARTS[k_] > 4.0 else (0.55,)):
            mid = STARTS[k_] + frac * (ENDS[k_] - STARTS[k_])
            w_ = min(WORDS, key=lambda w: abs(w["s"] - mid))
            zs.append((float(w_["s"]), float(RNG.uniform(0.07, 0.13)), (float(RNG.uniform(0.35, 0.65)), float(RNG.uniform(0.25, 0.5)))))
        b_["zooms"] = zs
for a_, b_ in zip(BEATS, BEATS[1:]):                       # rule: never the same pose twice in a row
    assert not (a_.get("pose") and a_.get("pose") == b_.get("pose")), "same pose back-to-back"

def base_xf(b, name):
    size, ax, ay, sx, sy = b["shot"]
    im = pose(name); ph, pw = im.shape[:2]
    s = size / pw if b.get("wide") else size / ph
    return s, sx - ax * pw * s, sy - ay * ph * s, pw, ph

def pose_pt(fx, fy, xf, name):
    s, tx, ty, pw, ph = xf; ox, oy, rw, rh = PADS[name]
    return int(tx + (ox + fx * rw) * s), int(ty + (oy + fy * rh) * s)

def muscles_extra(b, name, t, t0):
    extra = []
    for part, col, cue in b.get("muscles", []):
        if (name, part) not in MUSCLES:
            continue
        tc = T(cue) if not isinstance(cue, float) else t0
        if t >= tc:
            extra.append((muscle_mask(name, part), col, min(0.8, (t - tc) * FPS / 6 * 0.8)))   # fade in once, then hold
    return extra

def draw_pose(frame, b, k, t, name, tint):
    """Entrance animation chosen by the engine; character holds still after it settles (no idle wobble)."""
    t0 = STARTS[k]; f = (t - t0) * FPS + b.get("preroll", 0); dur = b["dur"]
    prev = BEATS[k - 1] if k else None
    s, tx, ty, pw, ph = base_xf(b, name)
    e = ease(b["easing"], f / dur); kind = b["enter"]
    cx, cy, by = tx + pw * s / 2, ty + ph * s / 2, ty + ph * s
    M = None; alpha = 1.0; sxm = 1.0; dx = dy = 0.0; sc = 1.0
    prev_pose = prev.get("pose") if prev and not prev.get("split") and "card" not in prev else None
    if kind == "flip" and prev_pose and f < dur / 2:
        ps, ptx, pty, ppw, pph = base_xf(prev, prev_pose); m = 1 - smooth(f / (dur / 2))
        blit_m(frame, pose(prev_pose), M_of(ps, ptx + ppw * ps * (1 - m) / 2, pty, m), 1.0, np.array([0.8, 0.8, 0.8]))
        return None
    if kind == "flip":
        sxm = back_out(min(1, (f - dur / 2) / (dur / 2)), 1.2) if f < dur else 1.0
    elif kind == "rise":
        dy = (1 - e) * 900; sc = 0.85 + 0.15 * min(1, e)
    elif kind in ("slide_l", "slide_r"):
        sgn = -1 if kind == "slide_l" else 1
        dx = sgn * (1 - e) * 1100
        if prev_pose and f < dur:                             # push the previous pose out the other side
            ps, ptx, pty, ppw, pph = base_xf(prev, prev_pose)
            blit_m(frame, pose(prev_pose), M_of(ps, ptx - sgn * e * 1100, pty), 1.0, keep_mask=False)
    elif kind == "drop":
        dy = -(1 - e) * 1500
    elif kind == "pop":
        sc = max(0.05, e)
    elif kind == "cut":
        sc = 1 + 0.06 * (1 - ease_out(f / 5))
    elif kind == "fade":
        alpha = min(1, f / max(1, dur))
    elif kind == "panel":
        top = int(H - min(1, e) * (H - 200))
        cv2.rectangle(frame, (0, max(0, top)), (W, H), (86, 108, 58), -1)
        cv2.line(frame, (0, max(0, top)), (W, max(0, top)), (110, 140, 80), 10)
        if f < dur:
            tmp = frame.copy()
            s2 = s
            blit_m(tmp, pose(name), M_of(s2, tx, ty + (1 - min(1, e)) * 300), 1.0, tint, extra=muscles_extra(b, name, t, t0))
            frame[max(0, top):] = tmp[max(0, top):]
            return None
    s2 = s * sc
    tx2 = cx - pw * s2 * sxm / 2 + dx
    ty2 = (cy - ph * s2 / 2 if kind == "pop" else by - ph * s2) + dy
    blit_m(frame, pose(name), M_of(s2, tx2, ty2, sxm), alpha, tint, extra=muscles_extra(b, name, t, t0))
    settled = f >= dur
    return (s, tx, ty, pw, ph) if settled else None

def render_card(frame, b, t, t0):
    since = t - t0; kk = since * FPS
    if b["card"] == "deg":
        blit_center(frame, text_img("EVERY 15°", 200), 540, 760, back_out(kk / 8), min(1, kk / 3))
        tf = T(("w", 5, "forward"))
        if t > tf:
            k2 = (t - tf) * FPS
            blit_center(frame, text_img("FORWARD", 130, (235, 64, 52)), 540, 960, back_out(k2 / 8), min(1, k2 / 3))
        ang = math.radians(15 * smooth(since / 0.6)); c = (540, 1450); L = 300
        cv2.line(frame, c, (c[0], c[1] - L), (200, 220, 210), 16, cv2.LINE_AA)
        cv2.line(frame, c, (int(c[0] + L * math.sin(ang)), int(c[1] - L * math.cos(ang))), RED, 22, cv2.LINE_AA)
        cv2.ellipse(frame, c, (180, 180), -90, 0, math.degrees(ang), RED, 12, cv2.LINE_AA)
    else:
        t12 = T(("w", 5, "twelve")) - 0.2
        if t >= t12:
            k = (t - t12) * FPS
            n = min(12, int(12 * ease_out((t - t12) / 0.35)))
            shake = 12 * math.sin(k * 1.9) * max(0, 1 - (t - t12) / 0.4)
            blit_center(frame, text_img(f"{n} KG", 330), 540 + shake, 860, back_out(k / 7), min(1, k / 2))
        tn = T(("w", 5, "neck"))
        if t > tn:
            k2 = (t - tn) * FPS
            blit_center(frame, text_img("ON YOUR NECK", 100, (235, 64, 52)), 540, 1110, back_out(k2 / 8), min(1, k2 / 3))

def render_split(frame, b, t, t0):
    since = t - t0
    for i, (name, col, badge) in enumerate((("bad_posture_desk", (54, 60, 96), "prop_red_x"),
                                            ("good_posture_desk", (88, 118, 62), "prop_green_check"))):
        e = ease_out((since * FPS - i * 4) / 10)
        x0 = i * 540; top = int(300 + (1 - e) * 1700)
        cv2.rectangle(frame, (x0 + 14, top), (x0 + 526, 1800), col, -1)
        if e > 0.05:
            im = pose(name); s = 470 / im.shape[1]
            blit_m(frame, im, np.float32([[s, 0, x0 + 35], [0, s, top + 1440 - im.shape[0] * s]]), 1.0, keep_mask=False)
            kb = since * FPS - 12 - i * 6
            if kb > 0:
                bi = pose(badge); bs = 170 / bi.shape[0] * back_out(kb / 8)
                blit_m(frame, bi, np.float32([[bs, 0, x0 + 270 - bi.shape[1] * bs / 2], [0, bs, top + 60]]), 1.0, keep_mask=False)
    k = since * FPS
    blit_center(frame, text_img("NO PLAN", 120), 540, 200, back_out(k / 8), min(1, k / 3))

CAPS = {0: ["YOUR", "BODY", "ISN'T", "SMALL"], 1: ["IT'S", "YOUR", "POSTURE"]}
CAP_CUES = {0: [("w", 0, "your"), ("w", 0, "body"), ("w", 0, "doesn't"), ("w", 0, "small")],
            1: [("w", 1, "the"), ("w", 1, "real"), ("w", 1, "posture")]}
CAP_RED = {"SMALL", "POSTURE"}
def draw_caption(frame, line, t):
    x, y = 70, 210
    for word, cue in zip(CAPS[line], CAP_CUES[line]):
        kk = (t - T(cue)) * FPS
        if kk < 0:
            break
        im = text_img(word, 84, (235, 64, 52) if word in CAP_RED else (255, 255, 255))
        if x + im.shape[1] - 40 > 1020:
            x, y = 70, y + 110
        s = back_out(kk / 6)
        blit_m(frame, im, np.float32([[s, 0, x], [0, s, y + (1 - s) * 30]]), min(1, kk / 2), keep_mask=False)
        x += im.shape[1] - 40

def draw_label(frame, b, since):
    """4 different exercise-label layouts (assigned per video by the seed)."""
    n_, name_ = b["label"]; kk = since * FPS; st = b["label_style"]
    if st == 0:                                              # top-centre pop
        blit_center(frame, text_img(n_, 170, (90, 225, 120)), 540, 210, back_out(kk / 8), min(1, kk / 3))
        if kk > 4:
            blit_center(frame, text_img(name_, 112), 540, 360, back_out((kk - 4) / 8), min(1, (kk - 4) / 3))
    elif st == 1:                                            # huge number rises bottom-left, title typed top-left
        big = text_img(n_, 520, (90, 225, 120)); e = ease_out(kk / 10)
        blit_m(frame, big, np.float32([[1, 0, 20], [0, 1, 1380 + (1 - e) * 600]]), 0.9, keep_mask=False)
        n = int(max(0, kk - 4) / FPS * 22)
        if n:
            blit_m(frame, text_img(name_[:n], 104), np.float32([[1, 0, 50], [0, 1, 180]]), 1.0, keep_mask=False)
    elif st == 2:                                            # pill sliding in from the left
        e = ease_out(kk / 9); txt = text_img(f"{n_}  {name_}", 92)
        w = txt.shape[1] + 20; x = int(-w + e * (w + 40))
        cv2.rectangle(frame, (x, 205), (x + w, 335), (60, 160, 80), -1)
        cv2.rectangle(frame, (x, 205), (x + w, 335), (30, 90, 40), 5)
        blit_m(frame, txt, np.float32([[1, 0, x + 10], [0, 1, 205 - 10]]), 1.0, keep_mask=False)
    else:                                                    # round number badge + title beside it
        r = int(95 * back_out(kk / 8))
        if r > 2:
            cv2.circle(frame, (150, 270), r, (80, 205, 105), -1, cv2.LINE_AA)
            cv2.circle(frame, (150, 270), r, (255, 255, 255), 8, cv2.LINE_AA)
            blit_center(frame, text_img(n_, 130), 150, 262, min(1, kk / 8))
        if kk > 5:
            e = ease_out((kk - 5) / 9)
            blit_m(frame, text_img(name_, 96), np.float32([[1, 0, 270 + (1 - e) * 300], [0, 1, 200]]), min(1, e * 1.5), keep_mask=False)

def draw_overlays(frame, b, t, since):
    if "stamp" in b and t > T(b["stamp"][0]):                  # stamp slams in (scale 2 -> 1, rotated)
        kk = (t - T(b["stamp"][0])) * FPS
        im = text_img(b["stamp"][1], 150, (235, 64, 52)); s = 1 + 1.0 * (1 - ease_out(kk / 5))
        h_, w_ = im.shape[:2]
        M = cv2.getRotationMatrix2D((w_ / 2, h_ / 2), 8, s); M[0, 2] += 540 - w_ / 2; M[1, 2] += 330 - h_ / 2
        blit_m(frame, im, M.astype(np.float32), min(1, kk / 2), keep_mask=False)
    if "label" in b:
        draw_label(frame, b, since)
    if "caption" in b:
        draw_caption(frame, b["caption"], t)
    for cue, s_, size, y in b.get("texts", []):
        kk = (t - T(cue)) * FPS
        if kk >= 0:
            blit_center(frame, text_img(s_, size), 540, y, back_out(kk / 8), min(1, kk / 3))
    for cue, s_, size, col, y in b.get("typewriter", []):
        n = int(max(0, t - T(cue)) * 20)
        if n > 0:
            full = text_img(s_, size, col); part = text_img(s_[:n], size, col)
            blit_center(frame, part, 540 - (full.shape[1] - part.shape[1]) / 2, y)

def zoom_amount(b, t):
    z = 1.0; focus = (0.5, 0.4)
    for cue, amt, fc in b.get("zooms", []):
        tc = T(cue) if not isinstance(cue, float) else cue
        if t >= tc:
            z *= 1 + amt * back_out((t - tc) * FPS / 10, 1.2)     # punch in, then HOLD (no oscillation)
            focus = fc
    return z, focus

def render_frame(t, frame, check=None):
    k_ = max(i for i, s in enumerate(STARTS) if s <= t or i == 0)
    out = _render_frame(t, frame, check)
    z, (fx, fy) = zoom_amount(BEATS[k_], t)
    if z > 1.001:
        cx, cy = fx * W, fy * H
        M = np.float32([[z, 0, cx - z * cx], [0, z, cy - z * cy]])
        frame[:] = cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    b = BEATS[k_]
    if "card" not in b and not b.get("split"):
        draw_overlays(frame, b, t, t - STARTS[k_])
    return out

def _render_frame(t, frame, check=None):
    k = max(i for i, s in enumerate(STARTS) if s <= t or i == 0)
    b = BEATS[k]; t0 = STARTS[k]; since = t - t0
    prev = BEATS[k - 1] if k else None
    bad = b.get("grade") == "bad"; pbad = prev is not None and prev.get("grade") == "bad"
    g = min(1, since * FPS / 3)
    mix = ((1 if bad else 0) * g + (1 if pbad else 0) * (1 - g)) if k else (1 if bad else 0)
    bg = BG_GOOD * (1 - mix) + BG_BAD * mix
    if (b.get("flash") and since * FPS < 4) or ("flash_at" in b and 0 <= (t - T(b["flash_at"])) * FPS < 4):
        bg = bg * 0.65 + BG_FLASH * 0.35
    frame[:] = bg.astype(np.uint8); MASK[:] = 0
    if "card" in b:
        render_card(frame, b, t, t0); return k
    if b.get("split"):
        render_split(frame, b, t, t0); return k
    name = b["pose"]
    if "alt" in b and since > 0.6:
        name = b["alt"] if int((since - 0.6) / 0.6) % 2 == 0 else b["pose"]
    if "wall" in b:
        wx = b["wall"]
        for x in range(0, wx):
            frame[:, x] = (np.array([96, 112, 104]) * (0.82 + 0.18 * x / wx)).astype(np.uint8)
        frame[1760:, :wx] = (60, 72, 66)
        cv2.rectangle(frame, (wx - 16, 0), (wx, H), (60, 72, 66), -1)
        sh = frame[:, wx:wx + 60].astype(np.float32)
        frame[:, wx:wx + 60] = (sh * np.linspace(0.75, 1, 60)[None, :, None]).astype(np.uint8)
    tint = np.array([0.86, 0.90, 1.06]) if mix > 0.5 else None
    xf = draw_pose(frame, b, k, t, name, tint)
    if xf is not None:
        for p0, p1, col, width, cue, curve in b.get("arrows", []):
            kk = (t - T(cue)) * FPS
            if kk > 0:
                a0 = pose_pt(*p0, xf, name); a1 = pose_pt(*p1, xf, name)
                draw_block_arrow(frame, *a0, *a1, col, width, kk / 8, curve, check)      # slides in once, then holds
        for nm, cue, d, cx, cy in b.get("insets", []):
            kk = (t - T(cue)) * FPS
            if kk > 0:
                blit_center(frame, anat(nm, d * 2), cx, cy, back_out(kk / 9), min(1, kk / 3))
        if "gap" in b and t > T(b["gap"]):
            hx, hy = pose_pt(0.32, 0.06, xf, name); wx = b["wall"]
            kk = (t - T(b["gap"])) * FPS; pe = ease_out(kk / 8)
            for i in range(0, int((hx - wx) * pe), 26):
                cv2.line(frame, (wx + i, hy), (min(hx, wx + i + 14), hy), RED, 12, cv2.LINE_AA)
            cv2.line(frame, (wx, hy - 50), (wx, hy + 50), RED, 10, cv2.LINE_AA)
            if pe > 0.9:
                cv2.line(frame, (hx, hy - 50), (hx, hy + 50), RED, 10, cv2.LINE_AA)
                blit_center(frame, text_img("GAP", 130, (235, 64, 52)), (wx + hx) / 2 + 40, hy - 150, back_out((kk - 6) / 8))
    return k

# ---------------- audio ----------------
def load_audio(path, sr=48000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

ENTER_SFX = {"rise": "swoosh_up", "slide_l": "swoosh_up", "slide_r": "swoosh_up", "drop": "boing", "pop": "pop_soft",
             "cut": None, "fade": None, "panel": "whistle_up", "flip": "swoosh_up"}
def build_audio(out_wav):
    sr = 48000; n = int(TOTAL * sr); arng = np.random.default_rng(SEED + 100)
    mix = np.zeros((n, 2), np.float32)
    v = load_audio(P("voice/voice_full.wav"))[:n]; mix[:len(v)] += v
    m = load_audio(P("assets/music/hyper_lillian_thorn.mp3"))
    xf = int(1.5 * sr); ramp = np.linspace(0, 1, xf)[:, None]
    cyc = np.concatenate([m[:xf] * ramp + m[-xf:] * (1 - ramp), m[xf:-xf]])
    mus = np.tile(cyc, (int(np.ceil(n / len(cyc))) + 1, 1))[:n]
    env = np.zeros(n); env[:len(v)] = np.abs(v[:, 0])
    win = int(0.12 * sr); env = np.convolve(env, np.ones(win) / win, "same")
    duck = 1 - 0.5 * np.clip(env / (env.max() * 0.25 + 1e-9), 0, 1)
    vr = np.sqrt((v ** 2).mean()); mr = np.sqrt((mus ** 2).mean()) + 1e-9
    fade = np.ones(n); fl = int(1.2 * sr); fade[-fl:] = np.linspace(1, 0, fl)
    mix += mus * (vr / mr) * 10 ** (-2 / 20) * (duck * fade)[:, None]
    cache = {}
    def sfx(name, at, vol, vary=True):
        if name not in cache:
            cache[name] = load_audio(P("assets/sfx", name + (".mp3" if name.startswith("typing") else ".wav")))
        s = cache[name]
        if vary:                                             # pitch/volume variation so repeats never sound identical
            r = float(arng.uniform(0.82, 1.22)); idx = np.arange(0, len(s) - 1, r)
            s = np.stack([np.interp(idx, np.arange(len(s)), s[:, c]) for c in (0, 1)], 1).astype(np.float32)
            vol *= float(arng.uniform(0.75, 1.1))
        i0 = int(at * sr)
        if 0 <= i0 < n:
            seg = s[:n - i0]; mix[i0:i0 + len(seg)] += seg * vol * vr / 0.1
    for k, b in enumerate(BEATS):
        t0 = STARTS[k]
        es = ENTER_SFX.get(b.get("enter"))
        if k and es and b.get("pose"):
            sfx(es, t0, .28)
        for e in b.get("sfx", []):
            if e[0] == "t":
                sfx(e[2], t0 + e[1], e[3])
            else:
                sfx(e[1], T(e[0]), e[2])
        if "label" in b:
            sfx("pop_soft", t0 + 0.13, .45)
        if "stamp" in b:
            sfx("pop_soft", T(b["stamp"][0]), .6)
        for nm, cue, *_ in b.get("insets", []):
            sfx("pop_soft", T(cue), .4)
        for cue, *_ in b.get("typewriter", []):
            sfx("typing_loud", T(cue), 0.22, vary=False)
    mix /= np.abs(mix).max() / 0.9
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

def plan_report():
    types = [b.get("enter", "card" if "card" in b else "split") for b in BEATS]
    hook = [(round(s, 2), ty) for s, ty in zip(STARTS, types) if s < 5]
    rep = sum(1 for a, b in zip(types, types[1:]) if a == b)
    print(f"seed {SEED}  palette={ {k: v for k, v in PALETTE.items() if v} }")
    print("transitions:", list(zip([round(s, 1) for s in STARTS], types)))
    print(f"hook (first 5 s): {len(hook)} transitions {hook}")
    print(f"flips={types.count('flip')}  back-to-back repeats={rep}  durations={[b.get('dur') for b in BEATS if 'dur' in b]}")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--preview"); ap.add_argument("--check", action="store_true")
    ap.add_argument("--plan", action="store_true"); a = ap.parse_args()
    os.makedirs(P("out"), exist_ok=True)
    frame = np.zeros((H, W, 3), np.uint8)
    if a.plan:
        plan_report(); return
    if a.check:
        bad = []
        for i in range(int(TOTAL * FPS)):
            c = []; render_frame(i / FPS, frame, c)
            if c and max(c) > 50:
                bad.append((round(i / FPS, 2), int(max(c))))
        print("arrow/character overlaps (time, px):", bad[:40] if bad else "none")
        return
    if a.preview:
        os.makedirs(P("out/stills"), exist_ok=True)
        for s in a.preview.split(","):
            render_frame(float(s), frame)
            cv2.imwrite(P("out/stills", f"t{float(s):05.2f}.jpg"), frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        return
    plan_report()
    build_audio(P("out/mix.wav"))
    af = ("deesser=i=0.4,equalizer=f=110:t=q:w=1:g=3.5,equalizer=f=6500:t=q:w=1.2:g=-3.5,"
          "acompressor=threshold=-20dB:ratio=1.8:attack=10:release=180:makeup=1,loudnorm=I=-14:TP=-1.0:LRA=9")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", P("out/mix.wav"), "-af", af, "-ar", "48000",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                            P("out/posture05.mp4")], stdin=subprocess.PIPE)
    nf = int(TOTAL * FPS)
    for i in range(nf):
        render_frame(i / FPS, frame); enc.stdin.write(frame.tobytes())
    enc.stdin.close(); enc.wait()
    print(f"{nf} frames -> out/posture05.mp4")

if __name__ == "__main__":
    main()
