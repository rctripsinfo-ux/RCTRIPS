#!/usr/bin/env python3
"""posture02 — v2 of the posture reel, built from GAP_REPORT.md (posture01).

Key changes vs v1: big medium/close framing, side views, grow+rise entrances with clean (non-overlapping)
swaps, drawn spine / arrows / wall / mat, bad-vs-good colour grade, constant micro-animation (wisps,
sparkles), full-screen stat card, minimal text, one continuous English TTS take, louder ducked music bed
with EQ + compression.

Usage: python3 build.py [--preview 1.0,5.2,...]
"""
import argparse, json, math, os, subprocess, wave
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)
BG_GOOD = np.array([76, 92, 44], np.float32)      # BGR #2C5C4C
BG_BAD = np.array([66, 78, 100], np.float32)      # BGR warm brown "problem" grade
RED, GREEN, WHITE, CYAN = (40, 50, 235), (90, 220, 120), (255, 255, 255), (235, 225, 120)   # BGR
rng = np.random.default_rng(7)

def ease_out(x):
    x = min(max(x, 0.0), 1.0); return 1 - (1 - x) ** 3
def ease_io(x):
    x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def back_out(x, k=1.6):
    x = min(max(x, 0.0), 1.0); return 1 + (k + 1) * (x - 1) ** 3 + k * (x - 1) ** 2

# ---------------- assets ----------------
def _load(name):
    im = cv2.imread(P("assets/poses", name + ".webp"), cv2.IMREAD_UNCHANGED)
    ys, xs = np.nonzero(im[:, :, 3] > 8)
    return im[ys.min():ys.max() + 1, xs.min():xs.max() + 1].copy()

def _with_bench(im):
    """Bench drawn into the pose layer (behind the body) so it moves with the character."""
    h, w = im.shape[:2]
    a = im[:, :, 3] > 8
    seat = int(np.nonzero(a[: int(0.75 * h), : int(0.35 * w)].any(1))[0].max()) - 8
    pad = 0
    canvas = np.zeros((h, w, 4), np.uint8)
    x0, x1 = int(0.0 * w), int(0.64 * w)
    col, top, dark = (38, 52, 46, 255), (70, 92, 82, 255), (22, 30, 26, 255)
    cv2.rectangle(canvas, (x0, seat), (x1, seat + 54), col, -1)
    cv2.rectangle(canvas, (x0, seat), (x1, seat + 14), top, -1)
    cv2.rectangle(canvas, (x0, seat), (x1, seat + 54), dark, 4)
    for lx in (x0 + 24, x1 - 60):
        cv2.rectangle(canvas, (lx, seat + 54), (lx + 34, h - 4), col, -1)
        cv2.rectangle(canvas, (lx, seat + 54), (lx + 34, h - 4), dark, 4)
    al = im[:, :, 3:4].astype(np.float32) / 255
    out = canvas.astype(np.float32)
    out[:, :, :3] = im[:, :, :3] * al + out[:, :, :3] * (1 - al)
    out[:, :, 3] = np.maximum(canvas[:, :, 3], im[:, :, 3])
    return out.astype(np.uint8)

def _with_mat(im):
    """Exercise mat under floor poses (pads the layer downwards)."""
    h, w = im.shape[:2]
    pad = int(0.06 * h) + 20
    canvas = np.zeros((h + pad, w + 80, 4), np.uint8)
    y0 = h - int(0.05 * h)
    pts = np.array([[20, y0 + pad // 2], [w + 60, y0 + pad // 2], [w + 30, h + pad - 4], [50, h + pad - 4]], np.int32)
    cv2.fillPoly(canvas, [pts], (52, 56, 60, 255))
    cv2.polylines(canvas, [pts], True, (28, 30, 32, 255), 5, cv2.LINE_AA)
    sub = canvas[0:h, 40:40 + w]
    al = im[:, :, 3:4].astype(np.float32) / 255
    sub[:, :, :3] = (im[:, :, :3] * al + sub[:, :, :3] * (1 - al)).astype(np.uint8)
    sub[:, :, 3] = np.maximum(sub[:, :, 3], im[:, :, 3])
    return canvas

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
        l, t, r, b = f.getbbox(s)
        pad = 28
        im = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.text((pad - l + 5, pad - t + 7), s, font=f, fill=(0, 0, 0, 120))
        d.text((pad - l, pad - t), s, font=f, fill=color + (255,))
        TEXTS[key] = cv2.cvtColor(np.array(im), cv2.COLOR_RGBA2BGRA)
    return TEXTS[key]

# ---------------- compositing ----------------
def blit_affine(frame, rgba, s, tx, ty, alpha=1.0, tint=None):
    """Place rgba scaled by s with its top-left at (tx, ty)."""
    if alpha <= 0.01:
        return
    M = np.float32([[s, 0, tx], [0, s, ty]])
    lay = cv2.warpAffine(rgba, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    a = lay[:, :, 3:4].astype(np.float32) * (alpha / 255)
    ys, xs = np.nonzero(a[:, :, 0] > 0.004)
    if not len(ys):
        return
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    src = lay[y0:y1, x0:x1, :3].astype(np.float32)
    if tint is not None:
        src = np.clip(src * tint, 0, 255)
    aa = a[y0:y1, x0:x1]
    roi = frame[y0:y1, x0:x1].astype(np.float32)
    frame[y0:y1, x0:x1] = (roi * (1 - aa) + src * aa).astype(np.uint8)

def blit_center(frame, rgba, cx, cy, s=1.0, alpha=1.0):
    h, w = rgba.shape[:2]
    blit_affine(frame, rgba, s, cx - w * s / 2, cy - h * s / 2, alpha)

# ---------------- beats (scenes) ----------------
# Each beat: line index, start fraction within the line, pose, shot, plus overlays.
# shot = (height_px, anchor_fx, anchor_fy, screen_x, screen_y, zoom_end)  -> pose height in px, pose point placed on screen.
FULL = lambda: (1450, 0.5, 1.0, 540, 1800, 1.015)
BEATS = [
    # hook: the problem on the body, warm "bad" grade
    dict(line=0, at=0.0, pose="bad_posture_desk", shot=(2300, 0.55, 0.0, 540, 360, 1.06), grade="bad",
         wisps=[(0.60, 0.13, RED)], sfx=[(0, "swoosh_up", .35), (0.05, "sad_sting", .35)]),
    dict(line=0, at=0.52, pose="bad_posture_desk", shot=(2900, 0.55, 0.08, 560, 700, 1.08), grade="bad",
         wisps=[(0.60, 0.13, RED)], texts=[(0.55, "NOT MUSCLE", 120, (255, 255, 255), 300)],
         sfx=[(0, "swoosh_up", .3)]),
    # mechanism: red spine + forward-head arrow
    dict(line=1, at=0.0, pose="bad_posture_desk", shot=(1750, 0.45, 0.0, 560, 420, 1.015),
         spine=([(0.66, 0.10), (0.55, 0.14), (0.40, 0.15), (0.25, 0.20), (0.14, 0.30), (0.10, 0.40), (0.12, 0.48)], RED, 0.15),
         arrows=[((0.62, 0.06), (0.86, 0.10), RED, 0.45, False)],
         sfx=[(0, "swoosh_up", .3), (0.45, "pop_soft", .5)]),
    # consequences
    dict(line=2, at=0.0, pose="slumped", shot=(2200, 0.5, 0.0, 540, 380, 1.015),
         sfx=[(0, "swoosh_up", .3)]),
    dict(line=2, at=0.6, pose="sore_back", shot=(2600, 0.45, 0.05, 520, 520, 1.015), grade="bad",
         wisps=[(0.62, 0.10, RED), (0.30, 0.30, RED)], flash=0.0, sfx=[(0, "sad_sting", .4)]),
    # self-test: wall
    dict(line=3, at=0.0, pose="side_view", shot=FULL(), wall=0.03, sfx=[(0, "swoosh_up", .35)]),
    dict(line=4, at=0.0, pose="side_view", shot=(2600, 0.3, 0.0, 330, 360, 1.015), wall=0.03,
         arrows=[((0.03, 0.06), (0.30, 0.06), RED, 0.12, True)], wisps=[(0.40, 0.06, RED)],
         sfx=[(0.12, "pop_soft", .5)]),
    dict(line=4, at=0.55, pose="phone_scroll", shot=(2200, 0.5, 0.0, 540, 380, 1.015),
         wisps=[(0.5, 0.135, RED)], sfx=[(0, "swoosh_up", .3)]),
    # stat card
    dict(line=5, at=0.0, card=dict(num=12, unit="KG", sub="EVERY 15° FORWARD"), sfx=[(0, "whistle_up", .35), (0.45, "boing", .35)]),
    # the fix: good grade, sparkles
    dict(line=6, at=0.0, pose="point_viewer", shot=(2300, 0.5, 0.0, 540, 400, 1.015), sparkles=True,
         texts=[(0.45, "15 DAYS", 130, (255, 255, 255), 300), (0.62, "5 MIN / DAY", 90, (255, 255, 255), 430)],
         sfx=[(0, "swoosh_up", .35), (0.45, "pop_soft", .5), (0.62, "pop_soft", .5)]),
    # exercises
    dict(line=7, at=0.0, pose="side_view", shot=(3300, 0.55, 0.0, 600, 520, 1.015), label="CHIN TUCKS",
         arrows=[((0.98, 0.085), (0.70, 0.085), GREEN, 0.25, True)], sfx=[(0, "swoosh_up", .35)]),
    dict(line=8, at=0.0, pose="cobra_stretch", shot=(1150, 0.5, 1.0, 540, 1550, 1.015), label="COBRA STRETCH",
         arrows=[((0.80, 0.55), (0.80, 0.12), GREEN, 0.25, True)], sfx=[(0, "swoosh_up", .35)]),
    dict(line=9, at=0.0, pose="hip_flexor_stretch", shot=(1500, 0.5, 1.0, 540, 1780, 1.015), label="HIP FLEXOR STRETCH",
         arrows=[((0.30, 0.56), (0.66, 0.56), GREEN, 0.25, True)], sfx=[(0, "swoosh_up", .35)]),
    dict(line=10, at=0.0, pose="glute_bridge_down", alt="glute_bridge_up", shot=(850, 0.5, 1.0, 540, 1450, 1.015),
         label="GLUTE BRIDGE", arrows=[((0.40, 0.60), (0.40, 0.08), GREEN, 0.2, True)], sfx=[(0, "swoosh_up", .35)]),
    # after state
    dict(line=11, at=0.0, pose="good_posture_desk", shot=(1750, 0.45, 0.0, 560, 420, 1.015), sparkles=True,
         spine=([(0.45, 0.10), (0.40, 0.17), (0.33, 0.27), (0.29, 0.37), (0.29, 0.46), (0.32, 0.54)], GREEN, 0.1),
         sfx=[(0, "swoosh_up", .35), (0.1, "pop_soft", .4)]),
    # CTA
    dict(line=12, at=0.0, pose="point_viewer", shot=(3000, 0.5, 0.0, 540, 560, 1.05), sparkles=True,
         typewriter=[("SAVE THIS", 120, (255, 255, 255), 250), ("FOLLOW", 150, (235, 64, 52), 400)],
         sfx=[(0, "swoosh_up", .35)]),
]

def beat_times(timing):
    """Absolute start/end for every beat (a beat starts slightly before its words)."""
    out = []
    for k, b in enumerate(BEATS):
        ln = timing[b["line"]]
        dur = ln["end"] - ln["start"]
        st = ln["start"] + b["at"] * dur - (0.10 if b["at"] == 0 else 0)
        out.append(max(0.0, st))
    ends = out[1:] + [timing[-1]["end"] + 0.8]
    return list(zip(out, ends))

def pose_xform(b, name, t, t0, t1):
    """Scale and offset of the pose for beat b at time t (camera push-in inside the beat)."""
    hpx, ax, ay, sx, sy, zend = b["shot"]
    im = pose(name)
    ph, pw = im.shape[:2]
    if name in ("cobra_stretch", "glute_bridge_up", "glute_bridge_down", "hip_flexor_stretch"):
        s0 = min(hpx / ph, 980 / pw)              # wide floor poses are width-limited
    else:
        s0 = hpx / ph
    z = 1 + (zend - 1) * ease_io((t - t0) / max(0.1, t1 - t0))
    s = s0 * z
    tx = sx - ax * pw * s
    ty = sy - ay * ph * s
    return s, tx, ty, pw, ph

def to_screen(fx, fy, xf):
    s, tx, ty, pw, ph = xf
    return int(tx + fx * pw * s), int(ty + fy * ph * s)

def draw_arrow(frame, p0, p1, color, prog, thick=16):
    if prog <= 0:
        return
    x = p0[0] + (p1[0] - p0[0]) * prog; y = p0[1] + (p1[1] - p0[1]) * prog
    cv2.line(frame, p0, (int(x), int(y)), (20, 20, 20), thick + 8, cv2.LINE_AA)
    cv2.line(frame, p0, (int(x), int(y)), color, thick, cv2.LINE_AA)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0]); L = 48
    for d in (2.6, -2.6):
        q = (int(x + L * math.cos(ang + d)), int(y + L * math.sin(ang + d)))
        cv2.line(frame, (int(x), int(y)), q, (20, 20, 20), thick + 8, cv2.LINE_AA)
        cv2.line(frame, (int(x), int(y)), q, color, thick, cv2.LINE_AA)

def draw_spine(frame, pts, color, prog):
    pts = np.array(pts, np.float32)
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    n = 26
    for k in range(int(n * prog)):
        d = seg[-1] * k / (n - 1)
        i = min(np.searchsorted(seg, d, side="right") - 1, len(pts) - 2)
        f = (d - seg[i]) / max(1e-6, seg[i + 1] - seg[i])
        x, y = pts[i] + (pts[i + 1] - pts[i]) * f
        cv2.circle(frame, (int(x), int(y)), 15, (25, 25, 25), -1, cv2.LINE_AA)
        cv2.circle(frame, (int(x), int(y)), 11, color, -1, cv2.LINE_AA)

def draw_wisps(frame, c, t, color, r=110):
    over = frame.copy()
    for k in range(3):
        ph = t * 3.2 + k * 2.1
        a0 = ph % (2 * math.pi)
        pts = []
        for j in range(18):
            ang = a0 + j * 0.16
            rr = r * (0.75 + 0.25 * math.sin(ph * 1.7 + j * 0.5))
            pts.append((int(c[0] + rr * math.cos(ang)), int(c[1] + rr * 0.8 * math.sin(ang))))
        cv2.polylines(over, [np.array(pts, np.int32)], False, color, 7, cv2.LINE_AA)
    cv2.addWeighted(over, 0.75, frame, 0.25, 0, frame)

SPARKS = rng.uniform(0, 1, (14, 3))
def draw_sparkles(frame, t, box):
    x0, y0, x1, y1 = box
    for i, (u, v, ph) in enumerate(SPARKS):
        a = 0.5 + 0.5 * math.sin(t * 5 + ph * 6.28)
        if a < 0.35:
            continue
        x = int(x0 + u * (x1 - x0)); y = int(y0 + v * (y1 - y0)); L = int(10 + 22 * a)
        cv2.line(frame, (x - L, y), (x + L, y), (220, 255, 255), 4, cv2.LINE_AA)
        cv2.line(frame, (x, y - L), (x, y + L), (220, 255, 255), 4, cv2.LINE_AA)

def render_frame(t, timing, bts, frame):
    k = max(i for i, (a, b) in enumerate(bts) if a <= t or i == 0)
    b = BEATS[k]; t0, t1 = bts[k]
    ln = timing[b["line"]]; ldur = ln["end"] - ln["start"]
    lt = lambda frac: ln["start"] + frac * ldur          # time of a fraction of this beat's line
    since = t - t0
    # background grade: 3-frame blend into the beat's grade
    bad = b.get("grade") == "bad"
    prev_bad = k > 0 and BEATS[k - 1].get("grade") == "bad"
    g = min(1, since * FPS / 3)
    mix = (1 if bad else 0) * g + (1 if prev_bad else 0) * (1 - g)
    frame[:] = (BG_GOOD * (1 - mix) + BG_BAD * mix).astype(np.uint8)
    tint = np.array([0.80, 0.86, 1.08]) if mix > 0.5 else None
    # wall (self-test)
    if "card" in b:
        render_card(frame, b, t, t0)
    else:
        name = b["pose"]
        if "alt" in b and since > 0.6:                   # rep loop: down/up every 0.45 s
            name = b["alt"] if int((since - 0.6) / 0.45) % 2 == 0 else b["pose"]
        xf = pose_xform(b, name, t, t0, t1)
        if "wall" in b:
            wx = to_screen(b["wall"], 0, xf)[0]
            cv2.rectangle(frame, (0, 0), (wx, H), (98, 124, 70), -1)
            cv2.line(frame, (wx, 0), (wx, H), (130, 160, 105), 10)
        # entrance: grow + rise over 9 frames; previous beat's pose is NOT drawn (clean swap)
        e = ease_out(since * FPS / 9) if "alt" not in b or since < 0.6 else 1
        s, tx, ty, pw, ph = xf
        grow = 0.6 + 0.4 * e
        cx, by = tx + pw * s / 2, ty + ph * s
        s2 = s * grow
        tx2, ty2 = cx - pw * s2 / 2, by - ph * s2 + (1 - e) * 650
        blit_affine(frame, pose(name), s2, tx2, ty2, min(1.0, 0.25 + e), tint)
        # overlays only after the entrance settles
        if e > 0.97:
            if "spine" in b:
                pts, col, at = b["spine"]
                prog = ease_out((t - lt(at)) * FPS / 14)
                draw_spine(frame, [to_screen(x, y, xf) for x, y in pts], col, prog)
            for p0, p1, col, at, loop in b.get("arrows", []):
                kk = (t - lt(at)) * FPS
                if kk > 0:
                    prog = ease_out(kk / 10)
                    if loop and kk > 10:
                        prog = 0.55 + 0.45 * (0.5 + 0.5 * math.cos((kk - 10) / FPS * 2 * math.pi / 0.9))
                    draw_arrow(frame, to_screen(*p0, xf), to_screen(*p1, xf), col, prog)
            for fx, fy, col in b.get("wisps", []):
                draw_wisps(frame, to_screen(fx, fy, xf), t, col)
            if b.get("sparkles"):
                draw_sparkles(frame, t, (60, 580, 1020, 1500))
    # small exercise label (one line, top)
    if "label" in b:
        kk = since * FPS
        blit_center(frame, text_img(b["label"], 92), 540 - (1 - ease_out(kk / 8)) * 700, 230, 1, min(1, kk / 3))
    for at, s_, size, col, y in b.get("texts", []):
        kk = (t - lt(at)) * FPS
        if kk >= 0:
            blit_center(frame, text_img(s_, size, col), 540, y + 6 * math.sin(t * 3), back_out(kk / 8), min(1, kk / 3))
    for j, (s_, size, col, y) in enumerate(b.get("typewriter", [])):
        t_start = t0 + 0.25 + j * 0.7
        n = int(max(0, t - t_start) * 18)
        if n > 0:
            full = text_img(s_, size, col); part = text_img(s_[:n], size, col)
            blit_center(frame, part, 540 - (full.shape[1] - part.shape[1]) / 2, y)
    if "flash" in b and since * FPS < 9:
        amt = math.sin(math.pi * since * FPS / 9) * 0.7
        red = np.zeros_like(frame); red[:] = (25, 15, 140)
        cv2.addWeighted(red, amt, frame, 1 - amt, 0, frame)
    return k

def render_card(frame, b, t, t0):
    c = b["card"]; since = t - t0
    kk = since * FPS
    n = min(c["num"], int(c["num"] * ease_out(since / 0.8)))
    shake = 8 * math.sin(kk * 1.9) * max(0, 1 - since / 0.4)
    big = text_img(f"{n} {c['unit']}", 250)
    blit_center(frame, big, 540 + shake, 860, back_out(kk / 8), min(1, kk / 3))
    if kk > 14:
        blit_center(frame, text_img(c["sub"], 80), 540, 1130, back_out((kk - 14) / 8), min(1, (kk - 14) / 3))
    # pulsing red ring for micro-motion
    r = int(450 + 22 * math.sin(t * 6))
    cv2.circle(frame, (540, 900), r, RED, 10, cv2.LINE_AA)

# ---------------- audio ----------------
def load_audio(path, sr=48000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

def build_audio(timing, bts, total, out_wav):
    sr = 48000; n = int(total * sr)
    mix = np.zeros((n, 2), np.float32)
    v = load_audio(P("voice/voice_full.wav"))[:n]
    mix[:len(v)] += v
    # music: crossfaded loop (no seams), ducked under the voice
    m = load_audio(P("assets/music/hyper_lillian_thorn.mp3"))
    xf = int(1.5 * sr); body = m[:-xf]; tail = m[-xf:]
    ramp = np.linspace(0, 1, xf)[:, None]
    loop = np.concatenate([body[xf:], np.zeros((0, 2), np.float32)])
    seg = np.concatenate([m[:xf] * ramp + tail * (1 - ramp), body[xf:]])  # one seamless cycle
    mus = np.tile(seg, (int(np.ceil(n / len(seg))) + 1, 1))[:n]
    env = np.abs(v[:, 0]) if len(v) else np.zeros(n)
    env = np.convolve(np.pad(env, (0, n - len(env))), np.ones(int(0.12 * sr)) / int(0.12 * sr), "same")
    duck = 1 - 0.35 * np.clip(env / (env.max() * 0.25 + 1e-9), 0, 1)
    vr = np.sqrt((v ** 2).mean()); mr = np.sqrt((mus ** 2).mean()) + 1e-9
    gain = vr / mr * 10 ** (0 / 20)                   # bed level with the voice RMS, then ducked under speech
    fade = np.ones(n); fl = int(1.2 * sr); fade[-fl:] = np.linspace(1, 0, fl)
    mix += mus * gain * (duck * fade)[:, None]
    cache = {}
    def sfx(name, at, vol):
        if name not in cache:
            ext = ".mp3" if name.startswith("typing") else ".wav"
            cache[name] = load_audio(P("assets/sfx", name + ext))
        s = cache[name]; i0 = int(at * sr)
        if 0 <= i0 < n:
            seg = s[:n - i0]; mix[i0:i0 + len(seg)] += seg * vol * vr / 0.1
    for k, b in enumerate(BEATS):
        t0, t1 = bts[k]
        ln = timing[b["line"]]; ldur = ln["end"] - ln["start"]
        for at, name, vol in b.get("sfx", []):
            sfx(name, t0 + at * max(0.1, t1 - t0) if at else t0, vol)
        for j, _ in enumerate(b.get("typewriter", [])):
            sfx("typing_loud", t0 + 0.25 + j * 0.7, 0.25)
    mix /= np.abs(mix).max() / 0.9
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview")
    a = ap.parse_args()
    timing = json.load(open(P("voice/timing.json")))
    bts = beat_times(timing)
    total = timing[-1]["end"] + 0.8
    os.makedirs(P("out"), exist_ok=True)
    frame = np.zeros((H, W, 3), np.uint8)
    if a.preview:
        os.makedirs(P("out/stills"), exist_ok=True)
        for s in a.preview.split(","):
            render_frame(float(s), timing, bts, frame)
            cv2.imwrite(P("out/stills", f"t{float(s):05.2f}.jpg"), frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        return
    build_audio(timing, bts, total, P("out/mix.wav"))
    af = ("deesser=i=0.5,equalizer=f=110:t=q:w=1:g=4,equalizer=f=6500:t=q:w=1.2:g=-4,"
          "acompressor=threshold=-18dB:ratio=2.5:attack=8:release=150:makeup=1.5,loudnorm=I=-14:TP=-1.0:LRA=7")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", P("out/mix.wav"), "-af", af, "-ar", "48000",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                            P("out/posture02.mp4")], stdin=subprocess.PIPE)
    nframes = int(total * FPS)
    for i in range(nframes):
        render_frame(i / FPS, timing, bts, frame)
        enc.stdin.write(frame.tobytes())
    enc.stdin.close(); enc.wait()
    print(f"{nframes} frames -> out/posture02.mp4")

if __name__ == "__main__":
    main()
