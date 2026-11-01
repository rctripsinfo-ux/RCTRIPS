# DIRECTOR: renders a Short straight from a per-scene plan (owner's master workflow, 1 Nov 2026).
# Full-frame 9:16 scene images, real overlapping transitions (push, zoom-through, smash, swing, flash, fade; zero empty
# frames), per-scene camera keyframes (push-ins, motion-matched pans), white intro cards, one-word bold italic captions
# (black, red keywords, white outline) placed per scene, hook heading, SFX on word anchors, music, -13 LUFS master.
# usage: from director import render; render(PLAN)   (see d04_plan.py)
import json, math, os, glob, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
SFX_DIR = os.path.expanduser("~/reel-engine-tool/public/library/sfx")
F_CAP = f"{HERE}/fonts/rubik-800-italic.woff2"; F_BIG = f"{HERE}/fonts/anton.woff2"
INK, RED = (17, 17, 17), (225, 29, 46)

def ease(p): p = min(1, max(0, p)); return 1 - (1 - p) ** 3
def smooth(p): p = min(1, max(0, p)); return p * p * (3 - 2 * p)
def back(p, s=1.6): p = min(1, max(0, p)) - 1; return 1 + p * p * ((s + 1) * p + s)
def norm(t): return "".join(c for c in t.lower() if c.isalnum() or c == "'")

class Timeline:
    def __init__(self, plan):
        self.P = plan; self.words = json.load(open(plan["words"]))["words"]
        k = 0; self.sc = []
        for s in plan["scenes"]:
            n = len(s["text"].split()); ws = self.words[k:k + n]
            assert [norm(w["text"]) for w in ws] == [norm(x) for x in s["text"].split()], (s["text"], [w["text"] for w in ws])
            self.sc.append({**s, "w0": k, "ws": ws}); k += n
        assert k == len(self.words), f"script has {len(self.words)} words, plan covers {k}"
        self.end = self.words[-1]["end"] + plan.get("tail", 0.6)
        for i, s in enumerate(self.sc):
            s["T"] = 0.0 if i == 0 else s["ws"][0]["start"] - plan.get("lead", 0.06)
        for i, s in enumerate(self.sc): s["E"] = self.sc[i + 1]["T"] if i + 1 < len(self.sc) else self.end
    def at(self, anchor, s=None):
        """'word' / 'word#2' (inside scene s, else whole script), '+0.3' offsets, numbers = seconds from scene start"""
        if isinstance(anchor, (int, float)): return (s["T"] if s else 0) + anchor
        off = 0.0
        if "+" in anchor[1:]: anchor, o = anchor.rsplit("+", 1); off = float(o)
        name, _, nth = anchor.partition("#"); nth = int(nth or 1)
        pool = s["ws"] if s else self.words; hits = [w for w in pool if norm(w["text"]) == norm(name)]
        assert len(hits) >= nth, f"anchor not found: {anchor}"
        return hits[nth - 1]["start"] + off

_img_cache = {}
def load(path, pad=False):
    """pad=True: a 16:9 (white-background) image is placed in the middle of a white 9:16 canvas, so the camera keys
    can zoom / pan it without stretching (floor exercises read well wide)"""
    if (path, pad) not in _img_cache:
        im = Image.open(path).convert("RGB")
        if pad:
            c = Image.new("RGB", (im.width, int(im.width * H / W)), (255, 255, 255)); c.paste(im, (0, (c.height - im.height) // 2)); im = c
        _img_cache[(path, pad)] = im
    return _img_cache[(path, pad)]

def view_box(size, z, fx, fy, dx=0.0, dy=0.0):
    iw, ih = size; cw = min(iw, ih * W / H) / z; ch = cw * H / W
    cx = min(max(fx * iw + dx * cw, cw / 2), iw - cw / 2); cy = min(max(fy * ih + dy * ch, ch / 2), ih - ch / 2)
    return cx - cw / 2, cy - ch / 2, cw, ch

def view(img, z, fx, fy, dx=0.0, dy=0.0):
    """cover-fit crop of the source at zoom z, centred on focus (fx, fy) (0..1 of the image), clamped inside it"""
    x0, y0, cw, ch = view_box(img.size, z, fx, fy, dx, dy); cx, cy = x0 + cw / 2, y0 + ch / 2
    return img.transform((W, H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BILINEAR)

_clip_cache = {}
def clip_frames(path):
    """all frames of a video clip at FPS (sound ignored), as PIL images at the clip's own size"""
    if path not in _clip_cache:
        pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", path], capture_output=True, text=True).stdout.split(",")
        w, h = int(pr[0]), int(pr[1])
        raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-an", "-vf", f"fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
        n = len(raw) // (w * h * 3); _clip_cache[path] = [Image.frombuffer("RGB", (w, h), raw[i * w * h * 3:(i + 1) * w * h * 3]) for i in range(n)]
    return _clip_cache[path]

def keyval(keys, u, dur):
    ks = [((dur + float(k[0][1:] or 0)) if isinstance(k[0], str) else k[0], *k[1:]) for k in keys]
    if u <= ks[0][0]: return ks[0][1:]
    for a, b in zip(ks, ks[1:]):
        if u < b[0]:
            p = smooth((u - a[0]) / max(1e-6, b[0] - a[0])); return tuple(x + (y - x) * p for x, y in zip(a[1:], b[1:]))
    return ks[-1][1:]

def font(path, size, _c={}):
    if (path, size) not in _c: _c[(path, size)] = ImageFont.truetype(path, size)
    return _c[(path, size)]

def text_img(txt, path, size, fill, stroke=0, stroke_fill=(255, 255, 255), shadow=True, maxw=None):
    f = font(path, size)
    while maxw and f.getbbox(txt, stroke_width=stroke)[2] > maxw and size > 30: size -= 6; f = font(path, size)
    l, t, r, b = f.getbbox(txt, stroke_width=stroke); pad = 24
    im = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((pad - l + 5, pad - t + 8), txt, font=f, fill=(0, 0, 0, 110), stroke_width=stroke, stroke_fill=(0, 0, 0, 110))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(im)
    d.text((pad - l, pad - t), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return im

def paste_center(canvas, im, x, y, scale=1.0, alpha=1.0):
    if scale != 1.0: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if alpha < 1: a = im.getchannel("A").point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    canvas.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))

def rounded(im, r=36):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=255)
    o = im.convert("RGBA"); o.putalpha(m); return o

class Renderer:
    def __init__(self, plan):
        self.P = plan; self.tl = Timeline(plan); self.cap_cache = {}; self.cam = {}; self.mark_y = None
        self.kw = {norm(k) for k in plan.get("keywords", [])}
        self.shakes = [(self.tl.at(a, s), amp) for s in self.tl.sc for a, amp in s.get("shake", [])]
        self.flashes = [s["T"] for s in self.tl.sc if s.get("tr") == "flash"] + [self.tl.at(a) for a in plan.get("flash", [])]
        self.hide = [(s["T"] - 0.2, s["E"]) for s in self.tl.sc if s.get("card") or s.get("nocap")]  # also while the card slides in

    # ---------- one scene, no transition ----------
    def scene(self, i, t):
        s = self.tl.sc[i]; u = t - s["T"]; dur = s["E"] - s["T"]
        if s.get("card"): return self.card(s, u + 0.2)  # card already half built while it slides in
        if "_keys" not in s:  # word anchors in the keys -> seconds from the scene start
            s["_keys"] = [((self.tl.at(k[0], s) - s["T"]) if isinstance(k[0], str) and not k[0].startswith("E") else k[0], *k[1:])
                          for k in s.get("keys", [(0, 1.0, .5, .5), ("E", 1.06, .5, .5)])]
        z, fx, fy = keyval(s["_keys"], u, dur)
        dx = dy = 0.0
        for ts, amp in self.shakes:
            if 0 <= t - ts < 0.35:
                k = (1 - (t - ts) / 0.35) * amp; rnd = random.Random(int(t * FPS)); dx, dy = (rnd.random() - .5) * k, (rnd.random() - .5) * k
                z = max(z, 1.06)
        self.cam[i] = (z, fx, fy, dx, dy)
        if s.get("clip"):  # owner's animated version of the scene image (muted): frame at the scene's local time, held at the end
            fr = clip_frames(f"{self.P['dir']}/{s['clip']}"); src = fr[min(len(fr) - 1, int(u * FPS))]
        else: src = load(f"{self.P['dir']}/{s['img']}", s.get("pad", False))
        return view(src, z, fx, fy, dx, dy)

    def card(self, s, u):
        num, title = s["card"]; c = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        if not s.get("img"):  # text-only card (owner 1 Nov: no shrunken pictures)
            nb = text_img(num, F_BIG, 420, RED); tt = text_img(title, F_BIG, 170, INK, maxw=W * 0.88)
            e0, e1 = back(u / 0.28, 1.4), ease((u - 0.1) / 0.25)
            paste_center(c, nb, W / 2, H * 0.40, 0.7 + 0.3 * e0, min(1, max(0, u / 0.1)))
            paste_center(c, tt, W / 2 + (1 - e1) * W * 0.6, H * 0.57, alpha=min(1, max(0, (u - 0.1) / 0.1)))
            bar = ease((u - 0.22) / 0.3); d = ImageDraw.Draw(c)
            if bar > 0: d.rectangle([W / 2 - 260 * bar, H * 0.625, W / 2 + 260 * bar, H * 0.625 + 16], fill=RED)
            return c.convert("RGB")
        if s.get("img"):
            src = load(f"{self.P['dir']}/{s['img']}")
            if "_trim" not in s:  # white-background picture: cut the empty white around it so the panel is filled
                g = np.asarray(src.convert("L")) < 235; ys, xs = np.where(g)
                if len(xs):
                    m = 30; s["_trim"] = src.crop((max(0, xs.min() - m), max(0, ys.min() - m), min(src.width, xs.max() + m), min(src.height, ys.max() + m)))
                else: s["_trim"] = src
            src = s["_trim"]; bw = int(W * 0.86); bh = int(bw * src.height / src.width)
            if bh > H * 0.5: bh = int(H * 0.5); bw = int(bh * src.width / src.height)
            panel = rounded(src.resize((bw, bh), Image.BILINEAR)); p = back(u / 0.3, 1.2)
            sh = Image.new("RGBA", (bw + 80, bh + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([40, 50, bw + 40, bh + 40], 36, fill=(0, 0, 0, 70))
            paste_center(c, sh.filter(ImageFilter.GaussianBlur(18)), W / 2, H * 0.33 + 10, 0.85 + 0.15 * p, min(1, u / 0.15))
            paste_center(c, panel, W / 2, H * 0.33 - (1 - ease(u / 0.3)) * 120, 0.85 + 0.15 * p, min(1, u / 0.15))
        n = text_img(num, F_BIG, 250, RED); tt = text_img(title, F_BIG, 150, INK, maxw=W * 0.88)
        e1, e2 = ease((u - 0.06) / 0.25), ease((u - 0.14) / 0.25)
        paste_center(c, n, W / 2 - (1 - e1) * W * 0.6, H * 0.68, alpha=min(1, max(0, (u - 0.06) / 0.1)))
        paste_center(c, tt, W / 2 + (1 - e2) * W * 0.6, H * 0.79, alpha=min(1, max(0, (u - 0.14) / 0.1)))
        bar = ease((u - 0.25) / 0.3); d = ImageDraw.Draw(c)
        if bar > 0: d.rectangle([W / 2 - 230 * bar, H * 0.855, W / 2 + 230 * bar, H * 0.855 + 14], fill=RED)
        return c.convert("RGB")

    # ---------- transitions: both scenes on screen, overlapping (never an empty frame) ----------
    def mix(self, old, new, kind, p):
        e = ease(p); c = Image.new("RGB", (W, H), (255, 255, 255))
        if kind in ("push_l", "push_r"):
            sgn = 1 if kind == "push_l" else -1
            c.paste(old, (int(-sgn * W * e), 0)); c.paste(new, (int(sgn * W * (1 - e)), 0)); return c
        if kind in ("push_u", "push_d"):
            sgn = 1 if kind == "push_u" else -1
            c.paste(old, (0, int(-sgn * H * e))); c.paste(new, (0, int(sgn * H * (1 - e)))); return c
        if kind == "zoom":  # zoom-through: old rushes past the camera, new comes up from behind
            a = old.resize((int(W * (1 + .5 * e)), int(H * (1 + .5 * e))), Image.BILINEAR)
            a = a.crop(((a.width - W) // 2, (a.height - H) // 2, (a.width - W) // 2 + W, (a.height - H) // 2 + H))
            s = 0.82 + 0.18 * e; b = new.resize((int(W * s), int(H * s)), Image.BILINEAR)
            c.paste(a); c.paste(b, ((W - b.width) // 2, (H - b.height) // 2), Image.new("L", b.size, int(255 * min(1, p * 1.6)))); return c
        if kind == "smash":  # new drops from the top with an overshoot, old pushed down
            y = int(-H * (1 - back(p, 1.3))); c.paste(old, (0, y + H)); c.paste(new, (0, y)); return c
        if kind == "swing":  # pendulum: new swings in from the right around a top pivot, old swings out left
            ang = 14 * (1 - e)
            o = old.rotate(-14 * e, center=(W // 2, -H // 3), fillcolor=(255, 255, 255)).transform((W, H), Image.AFFINE, (1, 0, W * e, 0, 1, 0), fillcolor=(255, 255, 255))
            n = new.rotate(ang, center=(W // 2, -H // 3), fillcolor=(255, 255, 255)).transform((W, H), Image.AFFINE, (1, 0, -W * (1 - e), 0, 1, 0), fillcolor=(255, 255, 255))
            m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rectangle([int(W * (1 - e)), 0, W, H], fill=255)
            c.paste(o); c.paste(n, (0, 0), m.rotate(ang, center=(W // 2, -H // 3))); return c
        if kind in ("whip_l", "whip_r"):  # fast push with motion blur in the middle of the move
            sgn = 1 if kind == "whip_l" else -1
            if 0.12 < p < 0.88:
                k = max(2, int(W / (6 + 30 * abs(p - 0.5)))); old = old.resize((k, H)).resize((W, H)); new = new.resize((k, H)).resize((W, H))
            c.paste(old, (int(-sgn * W * e), 0)); c.paste(new, (int(sgn * W * (1 - e)), 0)); return c
        if kind.startswith("circle"):  # iris reveal from a point of the new picture (e.g. the knee)
            cx, cy = (float(v) for v in (kind.split(":")[1].split(",") if ":" in kind else (0.5, 0.5)))
            r = e * 1.25 * H; m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).ellipse([cx * W - r, cy * H - r, cx * W + r, cy * H + r], fill=255)
            c.paste(old); c.paste(new, (0, 0), m); ImageDraw.Draw(c).ellipse([cx * W - r, cy * H - r, cx * W + r, cy * H + r], outline=RED, width=14 if p < 0.95 else 0); return c
        return Image.blend(old, new, e)  # fade / flash

    def base(self, t):
        sc = self.tl.sc; i = max(k for k, s in enumerate(sc) if s["T"] <= t)
        nxt = i + 1 if i + 1 < len(sc) else None
        # transition window around each cut: [T - d/2, T + d/2]
        for j in (i, nxt):
            if j is None or j == 0: continue
            s = sc[j]; d = s.get("d", 0.3); kind = s.get("tr", "push_l")
            if kind == "cut": continue
            if kind == "flash": d = 0.12
            if s["T"] - d / 2 <= t < s["T"] + d / 2:
                return self.mix(self.scene(j - 1, t), self.scene(j, t if s.get("card") else max(t, s["T"])), kind, (t - (s["T"] - d / 2)) / d), j
        en = sc[0].get("enter") if i == 0 else None
        if en and t < en[1]:  # first scene flies in from a side (already ~45% in on frame 1, small overshoot)
            p = t / en[1]; e = back(p, 1.4); off = (1 - e) * 0.6
            img = self.scene(0, t); c = Image.new("RGB", (W, H), (255, 255, 255))
            if p < 0.4: img = img.resize((max(2, int(W / (4 + 30 * p))), H)).resize((W, H)) if en[0] in ("left", "right") else img
            dx = {"left": -1, "right": 1}.get(en[0], 0) * off * W; dy = {"bottom": 1, "top": -1}.get(en[0], 0) * off * H
            c.paste(img, (int(dx), int(dy))); return c, 0
        return self.scene(i, t), i

    # ---------- overlays ----------
    def caption(self, t, j):
        if any(a <= t < b for a, b in self.hide): return None
        ws = self.tl.words; idx = max((k for k, w in enumerate(ws) if w["start"] <= t), default=-1)
        if idx < 0: return None
        if idx < self.tl.sc[j]["w0"]: return None  # never show the last word of the previous scene on the new picture
        w = ws[idx]; nx = ws[idx + 1] if idx + 1 < len(ws) else None
        if t > (max(w["end"] + 0.25, nx["start"]) if nx else w["end"] + 0.5): return None
        txt = w["text"].strip(",.;:!?\"").upper(); kw = norm(w["text"]) in self.kw
        key = (txt, kw)
        if key not in self.cap_cache:
            self.cap_cache[key] = text_img(txt, F_CAP, 132 if kw else 118, RED if kw else (255, 255, 255), stroke=15, stroke_fill=(0, 0, 0), maxw=W * 0.86)  # owner ref: white bold italic, thick black outline
        p = (t - w["start"]) / 0.13; sc = 0.6 + 0.4 * back(p, 2.0) if p < 1 else 1.0
        y = self.tl.sc[j].get("cap_y", self.P.get("cap_y", 0.8))
        return self.cap_cache[key], y, sc

    def frame(self, t):
        img, j = self.base(t); c = img.convert("RGBA")
        hk = self.P.get("hook")
        if hk and t < self.tl.at(hk["until"]):
            if "_im" not in hk:
                ca, cb = hk.get("colors", (INK, RED)); a = text_img(hk["text"][0], F_BIG, 170, ca, shadow=False); b = text_img(hk["text"][1], F_BIG, 170, cb, shadow=False)
                tw, th = a.width + b.width - 30, max(a.height, b.height)  # heading on its own white banner: never on the picture
                im = Image.new("RGBA", (W - 40, th + 30), (0, 0, 0, 0)); sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); bgc = hk.get("bg", (255, 255, 255, 255))
                ImageDraw.Draw(sh).rounded_rectangle([14, 20, im.width - 14, im.height - 4], 34, fill=(0, 0, 0, 90)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
                ImageDraw.Draw(im).rounded_rectangle([10, 8, im.width - 10, im.height - 14], 34, fill=bgc)
                x0 = (im.width - tw) // 2; y0 = (im.height - th) // 2 - 4
                for part, dx in ((a, 0), (b, a.width - 30)): im.alpha_composite(part, (x0 + dx, y0))
                hk["_im"] = im
            pk = 1.0 + 0.06 * math.sin(min(1, max(0, (t - 0.12) / 0.2)) * math.pi)  # punch with the impact at 0.12 s
            paste_center(c, hk["_im"], W / 2, H * hk.get("y", 0.12), pk)
        sb = self.tl.sc[j].get("banner")  # title banner on a scene (e.g. "01 GLUTE BRIDGES" over the number art)
        if sb:
            s_ = self.tl.sc[j]
            if "_bim" not in s_:
                a = text_img(sb[0], F_BIG, 150, RED, shadow=False); b = text_img(sb[1], F_BIG, 150, INK, shadow=False, maxw=W * 0.7)
                th = max(a.height, b.height); tw = a.width + b.width - 30
                im = Image.new("RGBA", (W - 40, th + 30), (0, 0, 0, 0)); sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
                ImageDraw.Draw(sh).rounded_rectangle([14, 20, im.width - 14, im.height - 4], 34, fill=(0, 0, 0, 90)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
                ImageDraw.Draw(im).rounded_rectangle([10, 8, im.width - 10, im.height - 14], 34, fill=(255, 255, 255, 255))
                x0 = (im.width - tw) // 2; y0 = (im.height - th) // 2 - 4
                for part, dx in ((a, 0), (b, a.width - 30)): im.alpha_composite(part, (x0 + dx, y0))
                s_["_bim"] = im
            u = t - s_["T"]; paste_center(c, s_["_bim"], W / 2, H * 0.085 - (1 - back(u / 0.3, 1.3)) * 260, 1.0, min(1, max(0, u / 0.12)))
        self.mark_y = None
        if not (sc_ := self.tl.sc[j]).get("card") and not (sc_.get("enter") and j == 0 and t < sc_["enter"][1]):
            for m in sc_.get("marks", []): self.draw_mark(c, sc_, j, m, t)
        cap = self.caption(t, j)
        if cap:
            y = cap[1]
            if self.mark_y and any(abs(y * H - my) < r + 110 for my, r in self.mark_y):  # never on the highlight
                y = 0.84 if all(my < H * 0.62 for my, _ in self.mark_y) else 0.2
            paste_center(c, cap[0], W / 2, H * y, cap[2])
        for ft in self.flashes:
            if 0 <= t - ft < 0.15: c = Image.blend(c, Image.new("RGBA", (W, H), (255, 255, 255, 255)), 0.75 * (1 - (t - ft) / 0.15))
        return c.convert("RGB")

    # ---------- highlight marks: rolling white dashed ring (+ soft green glow) and a pointing arrow ----------
    def draw_mark(self, c, s, j, m, t):
        a = self.tl.at(m["at"], s); b = self.tl.at(m["until"], s) if m.get("until") else s["E"] - 0.05
        if not (a <= t < b) or j not in self.cam: return
        src = load(f"{self.P['dir']}/{s['img']}", s.get("pad", False)); x0, y0, cw, ch = view_box(src.size, *self.cam[j])
        X = (m["x"] * src.width - x0) / cw * W; Y = (m["y"] * src.height - y0) / ch * H; R = m.get("r", 0.12) * src.width / cw * W
        u = t - a; p = back(u / 0.25, 1.6); fade = min(1, (b - t) / 0.15)
        R *= 0.6 + 0.4 * p; o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
        if m.get("glow", True):
            g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([X - R, Y - R, X + R, Y + R], fill=(34, 197, 94, int(70 * fade)))
            o.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.25)))
        rot = u * 120; n = 16
        for k in range(n):  # dashes, rolling
            a0 = rot + k * 360 / n; a1 = a0 + 360 / n * 0.55
            d.arc([X - R, Y - R, X + R, Y + R], a0, a1, fill=(0, 0, 0, int(150 * fade)), width=20)
            d.arc([X - R, Y - R, X + R, Y + R], a0, a1, fill=(255, 255, 255, int(255 * fade)), width=12)
        ar = m.get("arrow")
        if ar:  # arrow flies in toward the ring and keeps nudging it
            vx, vy = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1), "ul": (-.7, -.7), "ur": (.7, -.7), "dl": (-.7, .7), "dr": (.7, .7)}[ar]
            e = ease((u - 0.1) / 0.3); bob = 14 * math.sin(u * 9)
            gap = R + 25 + bob + (1 - e) * 300; L = 170
            tipx, tipy = X + vx * gap, Y + vy * gap; tx, ty = tipx + vx * L, tipy + vy * L
            px, py = -vy, vx; hw = 34
            head = [(tipx, tipy), (tipx + vx * 60 + px * hw, tipy + vy * 60 + py * hw), (tipx + vx * 60 - px * hw, tipy + vy * 60 - py * hw)]
            al = int(255 * fade * min(1, max(0, (u - 0.1) / 0.1)))
            for col, wd, grow in (((0, 0, 0, int(al * 0.6)), 30, 6), ((255, 255, 255, al), 18, 0)):
                d.line([(tipx + vx * 50, tipy + vy * 50), (tx, ty)], fill=col, width=wd)
                hh = [(x + (x - tipx) * 0 + (vx * -grow if i == 0 else 0), y + (vy * -grow if i == 0 else 0)) for i, (x, y) in enumerate(head)]
                d.polygon(hh, fill=col)
        c.alpha_composite(o)
        if self.mark_y is None: self.mark_y = []
        self.mark_y.append((Y, R))

    # ---------- audio + encode ----------
    # Owner rule (1 Nov): VOICE loudest; SFX clearly lower (peaks SFX_DB under the voice peaks); MUSIC lowest
    # (MUSIC_DB under the voice loudness). Every stem is measured, so a loud sound file can never cover the voice.
    @staticmethod
    def measure(path):
        r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", path, "-af", "ebur128=peak=sample", "-f", "null", "-"], capture_output=True, text=True).stderr
        lufs = float(r[r.rindex("I:"):].split()[1]); pk = float(r[r.rindex("Peak:"):].split()[1])
        return lufs, pk
    def audio(self, out):
        P = self.P; dur = self.tl.end; ins = ["-i", P["voice"], "-stream_loop", "-1", "-i", P["music"]]; fl = []; mixes = ["[v]", "[m]"]
        v_lufs, v_pk = self.measure(P["voice"]); m_lufs, _ = self.measure(P["music"])
        music_gain = 10 ** ((v_lufs - P.get("music_db", 22) - m_lufs) / 20)
        self.sfx_ref = v_pk - P.get("sfx_db", 12)  # target peak of a full-volume sound effect
        print(f"audio: voice {v_lufs:.1f} LUFS / peak {v_pk:.1f} dB, music gain {music_gain:.3f} (-{P.get('music_db', 22)} dB), sfx peaks <= {self.sfx_ref:.1f} dB")
        fl.append(f"[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={dur}[v]")
        fl.append(f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},volume={music_gain:.4f},afade=t=in:d=0.3,afade=t=out:st={dur - 1.2}:d=1.2[m]")
        k = 2
        for s in self.tl.sc:
            for m in s.get("marks", []):
                if m.get("sound", False): s.setdefault("sfx", []).append((m["at"], m.get("sfx", "counter"), 0.3))
            for a, name, vol in s.get("sfx", []):
                f = glob.glob(f"{SFX_DIR}/{name}.*"); assert f, name
                ms = int(max(0, self.tl.at(a, s)) * 1000); ins += ["-i", f[0]]
                _, pk = self.measure(f[0]); g = 10 ** ((self.sfx_ref - pk) / 20) * min(1.0, vol / 0.5)  # vol 0.5 = full level
                fl.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.4f},adelay={ms}|{ms}[s{k}]"); mixes.append(f"[s{k}]"); k += 1
        fl.append("".join(mixes) + f"amix=inputs={len(mixes)}:normalize=0:duration=first,atrim=0:{dur}[out]")
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[out]", "-ar", "48000", out], check=True)

    def render(self, out, t0=0.0, t1=None):
        tmp_a = out + ".mix.wav"; self.audio(tmp_a)
        L = os.environ.get("LUFS", "-13")
        J = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", tmp_a, "-af", f"loudnorm=I={L}:TP=-1.0:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
        j = json.loads(J[J.rindex("{"):J.rindex("}") + 1])
        af = (f"loudnorm=I={L}:TP=-1.0:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
              f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
        t1 = t1 or self.tl.end; n = int(round((t1 - t0) * FPS))
        ff = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                               "-ss", str(t0), "-t", str(t1 - t0), "-i", tmp_a, "-af", af, "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p",
                               "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
        for f in range(n):
            ff.stdin.write(self.frame(t0 + f / FPS).tobytes())
        ff.stdin.close(); ff.wait(); os.remove(tmp_a)
        print("DONE", out, f"{t1 - t0:.2f} s, {n} frames")

def remix(plan, video, out):
    """new audio mix onto an already rendered video (no frame render)"""
    r = Renderer(plan); a = out + ".mix.wav"; r.audio(a); L = os.environ.get("LUFS", "-13")
    J = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", a, "-af", f"loudnorm=I={L}:TP=-1.0:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(J[J.rindex("{"):J.rindex("}") + 1])
    af = (f"loudnorm=I={L}:TP=-1.0:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
          f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", video, "-i", a, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", af,
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True); os.remove(a)

def render(plan, out, **kw): Renderer(plan).render(out, **kw)
