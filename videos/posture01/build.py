#!/usr/bin/env python3
"""Render the posture reel: mascot poses on a flat brand background, green.faction-style motion.

Inputs: assets/poses/*.webp, voice/voice_full.wav + voice/timing.json, assets/music, assets/sfx
Output: out/posture01.mp4 (1080x1920, 30 fps, -13 LUFS)
Usage: python3 build.py [--preview SECONDS_LIST]   e.g. --preview 1,8,26  -> stills in out/stills/
"""
import argparse, json, math, os, subprocess, wave
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
BG = np.array([76, 92, 44], np.uint8)            # BGR of #2C5C4C (measured green.faction background)
WHITE, YELLOW, RED = (255, 255, 255), (255, 211, 77), (229, 57, 53)   # RGB for PIL text
RED_BGR = (53, 57, 229)
FONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)

# ---------- easing ----------
def ease_out(x):  # fast start, slow settle (measured: ~3-frame ease-in, ~7-frame settle)
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3

def back_out(x, k=1.7):  # pop with slight overshoot
    x = min(max(x, 0.0), 1.0)
    return 1 + (k + 1) * (x - 1) ** 3 + k * (x - 1) ** 2

# ---------- assets ----------
POSES = {}
def pose(name):
    if name not in POSES:
        im = cv2.imread(P("assets/poses", name + ".webp"), cv2.IMREAD_UNCHANGED)
        ys, xs = np.nonzero(im[:, :, 3] > 8)
        im = im[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        bw, bh = 900, 1060                         # pose box (keeps head below the text zone)
        s = min(bw / im.shape[1], bh / im.shape[0])
        POSES[name] = cv2.resize(im, (int(im.shape[1] * s), int(im.shape[0] * s)), interpolation=cv2.INTER_AREA)
    return POSES[name]

TEXTS = {}
def text_img(s, size, color=WHITE, stroke=0):
    key = (s, size, color, stroke)
    if key not in TEXTS:
        f = ImageFont.truetype(FONT, size)
        l, t, r, b = f.getbbox(s, stroke_width=stroke)
        pad = 24
        im = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.text((pad - l + 6, pad - t + 8), s, font=f, fill=(0, 0, 0, 110), stroke_width=stroke)  # soft drop shadow
        d.text((pad - l, pad - t), s, font=f, fill=color + (255,), stroke_width=stroke, stroke_fill=(20, 30, 25, 255))
        a = np.array(im)
        TEXTS[key] = cv2.cvtColor(a, cv2.COLOR_RGBA2BGRA)
    return TEXTS[key]

def blit(frame, rgba, cx, cy, scale=1.0, alpha=1.0):
    """Alpha-blend rgba (BGRA) centred at (cx, cy)."""
    if scale <= 0.01 or alpha <= 0.01:
        return
    img = rgba if abs(scale - 1) < 1e-3 else cv2.resize(rgba, (max(1, int(rgba.shape[1] * scale)), max(1, int(rgba.shape[0] * scale))))
    h, w = img.shape[:2]
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    fx0, fy0, fx1, fy1 = max(x0, 0), max(y0, 0), min(x0 + w, W), min(y0 + h, H)
    if fx0 >= fx1 or fy0 >= fy1:
        return
    sub = img[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0]
    a = sub[:, :, 3:4].astype(np.float32) / 255 * alpha
    roi = frame[fy0:fy1, fx0:fx1]
    roi[:] = (roi * (1 - a) + sub[:, :, :3] * a).astype(np.uint8)

def blit_bottom(frame, rgba, cx, bottom, scale=1.0, alpha=1.0):
    h = rgba.shape[0] * scale
    blit(frame, rgba, cx, bottom - h / 2, scale, alpha)

# ---------- scene plan ----------
# Each scene i follows voice line i. Times inside a scene are fractions of the line (0..1).
# poses: [(at, name)]  texts: [(at, string, size, color, y)]  fx: [(at, kind, args)]  sfx: [(at, file, vol)]
PLAN = [
    dict(poses=[(0, "bad_posture_desk")],
         texts=[(0.15, "9 GHANTE", 150, YELLOW, 330), (0.15, "JHUKE HUE?", 96, WHITE, 475)],
         props=[(0.45, "prop_stopwatch", 930, 760, 210)],
         sfx=[(0, "swoosh_up", .5), (0.15, "pop_soft", .7)]),
    dict(poses=[(0, "sore_back")],
         texts=[(0.05, "GARDAN + KAMAR", 104, WHITE, 330), (0.45, "TOOT RAHI HAI", 112, RED, 470)],
         props=[(0.6, "prop_red_x", 900, 1050, 210)],
         fx=[(0.45, "flash", {}), (0.5, "circle", dict(fx=0.30, fy=0.30, rx=0.30, ry=0.12))],
         sfx=[(0, "swoosh_up", .5), (0.45, "sad_sting", .6)]),
    dict(poses=[(0, "shocked")],
         texts=[(0.05, "15° JHUKAV", 120, WHITE, 310), (0.55, "= 12 KG", 170, YELLOW, 480)],
         fx=[(0.55, "circle", dict(fx=0.50, fy=0.11, rx=0.22, ry=0.09))],
         sfx=[(0, "swoosh_up", .5), (0.55, "boing", .5)]),
    dict(poses=[(0, "slumped"), (0.55, "confused_scratch")],
         texts=[(0.0, "CHOTI BODY", 104, WHITE, 280), (0.38, "PET BAHAR", 104, WHITE, 410), (0.7, "CONFIDENCE GAYAB", 86, RED, 535)],
         props=[(0.72, "prop_red_x", 905, 1020, 200)],
         sfx=[(0, "swoosh_up", .5), (0.38, "pop_soft", .6), (0.7, "pop_soft", .6)]),
    dict(poses=[(0, "arms_crossed")],
         texts=[(0.25, "SCROLL", 140, WHITE, 320), (0.55, "ya FIX?", 140, YELLOW, 480)],
         props=[(0.25, "prop_phone", 170, 1000, 260), (0.55, "prop_green_check", 905, 1000, 200)],
         sfx=[(0, "swoosh_up", .5), (0.25, "pop_soft", .6), (0.55, "whistle_up", .45)]),
    dict(poses=[(0, "explain")],
         texts=[(0.0, "4 STRETCH", 130, YELLOW, 280), (0.3, "5 MIN / DIN", 100, WHITE, 410), (0.62, "NO GYM", 100, WHITE, 535)],
         props=[(0.3, "prop_stopwatch", 905, 1000, 220)],
         sfx=[(0, "swoosh_up", .5), (0.3, "pop_soft", .6), (0.62, "pop_soft", .6)]),
    dict(poses=[(0, "count_1"), (0.33, "neck_stretch")], label=("1", "NECK STRETCH", "20 sec hold"),
         props=[(0.5, "prop_stopwatch", 910, 1060, 190)],
         fx=[(0.4, "circle", dict(fx=0.50, fy=0.17, rx=0.22, ry=0.08))],
         sfx=[(0, "swoosh_up", .5), (0.33, "swoosh_up", .4)]),
    dict(poses=[(0, "count_2"), (0.35, "cobra_stretch")], label=("2", "COBRA STRETCH", "chest upar"),
         props=[(0.55, "prop_green_check", 905, 1030, 180)],
         sfx=[(0, "swoosh_up", .5), (0.35, "swoosh_up", .4)]),
    dict(poses=[(0, "count_3"), (0.35, "hip_flexor_stretch")], label=("3", "HIP FLEXOR", "30 sec / side"),
         props=[(0.55, "prop_stopwatch", 910, 1000, 190)],
         fx=[(0.45, "circle", dict(fx=0.57, fy=0.53, rx=0.20, ry=0.10))],
         sfx=[(0, "swoosh_up", .5), (0.35, "swoosh_up", .4)]),
    dict(poses=[(0, "count_4"), (0.33, "glute_bridge_down"), (0.48, "glute_bridge_up"), (0.63, "glute_bridge_down"),
                (0.78, "glute_bridge_up"), (0.93, "glute_bridge_down")], label=("4", "GLUTE BRIDGE", "15 reps"), quick=True,
         props=[(0.6, "prop_fire", 905, 1000, 220)],
         sfx=[(0, "swoosh_up", .5), (0.33, "swoosh_up", .4)]),
    dict(poses=[(0, "good_posture_desk"), (0.55, "victory")],
         texts=[(0.0, "15 DIN", 160, YELLOW, 320), (0.5, "FARAK DIKHEGA", 104, WHITE, 480)],
         props=[(0.08, "prop_calendar", 175, 1000, 230), (0.55, "prop_green_check", 905, 1000, 200)],
         sfx=[(0, "swoosh_up", .5), (0.5, "whistle_up", .45)]),
    dict(poses=[(0, "thumbs_up")], typewriter=[("SAVE KARO", 130, WHITE, 320), ("+ FOLLOW", 130, YELLOW, 470)],
         sfx=[(0, "swoosh_up", .5)]),
]

def draw_stool(frame, alpha, name):
    # flat bench under the seated desk poses (they are drawn sitting on nothing)
    img = pose(name)
    h, w = img.shape[:2]
    left, top = 540 - w / 2, 1720 - h
    a = img[:, :, 3] > 8
    # seat height = lowest row of the buttocks: lowest opaque pixel in the left 35% of the figure above 75% height
    cols = a[: int(0.75 * h), : int(0.35 * w)]
    seat_y = int(top + np.nonzero(cols.any(1))[0].max()) - 6
    x0, x1 = int(left + 0.02 * w), int(left + 0.62 * w)
    dark, edge = (36, 46, 31), (64, 80, 56)
    cv2.rectangle(frame, (x0, seat_y), (x1, seat_y + 46), dark, -1)
    cv2.rectangle(frame, (x0, seat_y), (x1, seat_y + 12), edge, -1)
    for lx in (x0 + 26, x1 - 56):
        cv2.rectangle(frame, (lx, seat_y + 46), (lx + 30, 1716), dark, -1)
    cv2.rectangle(frame, (x0 + 26, seat_y + 150), (x1 - 26, seat_y + 170), dark, -1)

def render_frame(t, timing, frame):
    frame[:] = BG
    # which scene
    i = max(k for k, s in enumerate(timing) if s["start"] - 0.12 <= t or k == 0)
    sc, tm = PLAN[i], timing[i]
    dur = tm["end"] - tm["start"] + 0.12
    st = tm["start"] - 0.12                       # scene starts a beat before the words
    f = (t - st) / dur
    # --- pose: current + fading previous ---
    cur = [p for p in sc["poses"] if f >= p[0]] or sc["poses"][:1]
    at, name = cur[-1]
    since = t - (st + at * dur)
    if len(cur) > 1:
        prev_name = cur[-2][1]
    elif i > 0:
        prev_name = PLAN[i - 1]["poses"][-1][1]
    else:
        prev_name = None
    quick = sc.get("quick") and len(cur) > 2           # rep loop: hard swap, no slide
    fade = 5 / FPS
    SEATED = ("bad_posture_desk", "good_posture_desk")
    if prev_name and since < fade and not quick:
        if prev_name in SEATED:
            draw_stool(frame, 1.0, prev_name)
        blit_bottom(frame, pose(prev_name), 540, 1720, 1.0, 1 - since / fade)
    if name in SEATED:
        draw_stool(frame, 1.0, name)
    e = 1.0 if quick else ease_out(since / (10 / FPS))
    rise = (1 - e) * 700
    breathe = 1 + 0.006 * math.sin(2 * math.pi * t / 2.4)   # tiny idle motion so the frame is never static
    breathe *= 1 + 0.045 * ease_out(min(1, max(0, f)))       # slow push-in through every scene
    blit_bottom(frame, pose(name), 540, 1720 + rise, breathe, min(1.0, 0.3 + e))
    # --- texts (pop in with overshoot) ---
    for at, s, size, color, y in sc.get("texts", []):
        k = (t - (st + at * dur)) * FPS
        if k >= 0:
            blit(frame, text_img(s, size, color), 540, y, back_out(k / 8), min(1, k / 3))
    # --- props (pop in with overshoot, gentle bob) ---
    for at, pname, px, py, ph in sc.get("props", []):
        k = (t - (st + at * dur)) * FPS
        if k >= 0:
            im = pose(pname)
            sc_ = ph / im.shape[0] * back_out(k / 8)
            blit(frame, im, px, py + 10 * math.sin(2 * math.pi * t / 1.6), sc_, min(1, k / 3))
    # --- exercise label ---
    if "label" in sc:
        n, title, sub = sc["label"]
        k = (t - st) * FPS
        blit(frame, text_img(n, 200, YELLOW), 540, 270, back_out(k / 8), min(1, k / 3))
        k2 = k - 6
        if k2 >= 0:
            blit(frame, text_img(title, 104, WHITE), 540 - (1 - ease_out(k2 / 9)) * 600, 445, 1, min(1, k2 / 4))
        k3 = k - 14
        if k3 >= 0:
            blit(frame, text_img(sub, 66, YELLOW), 540, 545, back_out(k3 / 8), min(1, k3 / 3))
    # --- typewriter end card ---
    for j, (s, size, color, y) in enumerate(sc.get("typewriter", [])):
        t0 = st + 0.15 * dur + j * 0.9
        nchar = int(max(0, t - t0) * 16)
        if nchar > 0:
            shown = s[:nchar]
            img = text_img(s, size, color)
            part = text_img(shown, size, color)
            blit(frame, part, 540 - (img.shape[1] - part.shape[1]) / 2, y)
    # --- effects ---
    for at, kind, a in sc.get("fx", []):
        k = (t - (st + at * dur)) * FPS
        if k < 0:
            continue
        if kind == "circle":
            prog = ease_out(k / 10)
            ph, pw = pose(name).shape[:2]
            x0, y0 = 540 - pw / 2, 1720 - ph
            c = (int(x0 + a["fx"] * pw), int(y0 + a["fy"] * ph))
            ax = (int(a["rx"] * pw), int(a["ry"] * ph))
            cv2.ellipse(frame, c, ax, -90, 0, 360 * prog, RED_BGR, 12, cv2.LINE_AA)
        if kind == "flash" and k < 9:
            amt = math.sin(math.pi * k / 9) * 0.75
            red = np.zeros_like(frame); red[:] = (20, 10, 120)
            gray = cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
            tinted = cv2.addWeighted(gray, 0.55, red, 0.9, 0)
            cv2.addWeighted(tinted, amt, frame, 1 - amt, 0, frame)
    return i

# ---------- audio ----------
def load_audio(path, sr=48000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

def build_audio(timing, total, out_wav, music_vol=0.06):
    sr = 48000
    n = int(total * sr)
    mix = np.zeros((n, 2), np.float32)
    v = load_audio(P("voice/voice_full.wav"))[:n]
    mix[:len(v)] += v
    m = load_audio(P("assets/music/hyper_lillian_thorn.mp3"))
    reps = int(np.ceil(n / len(m)))
    mm = np.tile(m, (reps, 1))[:n]
    fade = np.ones(n, np.float32); fl = int(1.0 * sr); fade[-fl:] = np.linspace(1, 0, fl)
    mix += mm * music_vol / max(1e-6, np.abs(m).max()) * fade[:, None]
    cache = {}
    def sfx(name, at, vol):
        if name not in cache:
            ext = ".mp3" if name.startswith("typing") else ".wav"
            cache[name] = load_audio(P("assets/sfx", name + ext))
        s = cache[name]; i0 = int(at * sr)
        if i0 >= n: return
        seg = s[:n - i0]
        mix[i0:i0 + len(seg)] += seg * vol
    for i, sc in enumerate(PLAN):
        st = timing[i]["start"] - 0.12
        dur = timing[i]["end"] - timing[i]["start"] + 0.12
        for at, name, vol in sc.get("sfx", []):
            sfx(name, st + at * dur, vol)
        for j, _ in enumerate(sc.get("typewriter", [])):
            sfx("typing_loud", st + 0.15 * dur + j * 0.9, 0.35)
    peak = np.abs(mix).max()
    mix = mix / peak * 0.9
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", help="comma-separated seconds; write stills only")
    a = ap.parse_args()
    timing = json.load(open(P("voice/timing.json")))
    total = timing[-1]["end"] + 0.7
    os.makedirs(P("out"), exist_ok=True)
    frame = np.zeros((H, W, 3), np.uint8)
    if a.preview:
        os.makedirs(P("out/stills"), exist_ok=True)
        for s in a.preview.split(","):
            render_frame(float(s), timing, frame)
            cv2.imwrite(P("out/stills", f"t{float(s):05.2f}.jpg"), frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        print("stills ->", P("out/stills"))
        return
    build_audio(timing, total, P("out/mix.wav"))
    nframes = int(total * FPS)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", P("out/mix.wav"),
                            "-af", "loudnorm=I=-13:TP=-1.0:LRA=7", "-ar", "48000",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                            P("out/posture01.mp4")], stdin=subprocess.PIPE)
    for k in range(nframes):
        render_frame(k / FPS, timing, frame)
        enc.stdin.write(frame.tobytes())
    enc.stdin.close(); enc.wait()
    print(f"{nframes} frames -> {P('out/posture01.mp4')}")

if __name__ == "__main__":
    main()
