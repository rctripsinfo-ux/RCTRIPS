# DIRECTOR: renders a Short straight from a per-scene plan (owner's master workflow, 1 Nov 2026).
# Full-frame 9:16 scene images, real overlapping transitions (push, zoom-through, smash, swing, flash, fade; zero empty
# frames), per-scene camera keyframes (push-ins, motion-matched pans), white intro cards, one-word bold italic captions
# (black, red keywords, white outline) placed per scene, hook heading, SFX on word anchors, music, -13 LUFS master.
# usage: from director import render; render(PLAN)   (see d04_plan.py)
import json, math, os, glob, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = (1920, 1080, 30) if os.environ.get("LANDSCAPE") else (1080, 1920, 30)  # LANDSCAPE=1: 16:9 long videos
HERE = os.path.dirname(os.path.abspath(__file__))
SFX_DIR = os.path.expanduser("~/reel-engine-tool/public/library/sfx")
F_CAP = f"{HERE}/fonts/rubik-800-italic.woff2"; F_BIG = f"{HERE}/fonts/anton.woff2"
F_MARK = f"{HERE}/fonts/permanentmarker.ttf"; F_HAND = f"{HERE}/fonts/caveatbrush.ttf"
ORANGE, NAVY, MINT, TOMATO, STICKY = (255, 107, 26), (31, 42, 68), (43, 196, 138), (229, 72, 77), (255, 216, 77)
# brand themes (owner 15 Nov: no cream, no orange). Keys: bg grid set, text = writing on the set, accent = live marker / caption swipe,
# accent2 = second highlight, sticky + sticky_text, mini = Mini-H caption colour, good / warn / bad = meter + right / wrong,
# frame = mirror + lens rim, plate = meter face, kw_text = caption word on the accent swipe
THEMES = {
    "board": dict(bg=(23, 63, 63), text=(238, 243, 234), accent=(200, 242, 60), accent2=(52, 209, 224), sticky=(92, 225, 230), sticky_text=(14, 38, 38),
                  mini=(92, 225, 230), good=(200, 242, 60), warn=(246, 224, 94), bad=(255, 79, 139), frame=(11, 33, 33), plate=(238, 243, 234), kw_text=(14, 38, 38)),
    "midnight": dict(bg=(16, 27, 51), text=(243, 246, 255), accent=(25, 211, 255), accent2=(242, 245, 66), sticky=(242, 245, 66), sticky_text=(10, 18, 34),
                     mini=(242, 245, 66), good=(61, 245, 160), warn=(242, 245, 66), bad=(255, 79, 139), frame=(8, 14, 28), plate=(243, 246, 255), kw_text=(10, 18, 34)),
    "ice": dict(bg=(230, 242, 243), text=(15, 59, 68), accent=(123, 92, 255), accent2=(29, 185, 122), sticky=(212, 245, 91), sticky_text=(15, 59, 68),
                mini=(123, 92, 255), good=(29, 185, 122), warn=(245, 200, 60), bad=(240, 62, 110), frame=(15, 59, 68), plate=(255, 255, 255), kw_text=(255, 255, 255)),
}
TH = dict(THEMES["ice"])  # brand theme locked by the owner (15 Nov): ice
def C(x): return TH[x] if isinstance(x, str) else x
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

_hero_cache = {}
HERO_DIR = os.path.expanduser("~/reel-engine-tool/public/library/hero")
def defringe(im):
    """cut-outs from white backgrounds keep a light halo: shrink the alpha 2 px and pull edge pixels away from white (owner 18 Nov)"""
    a = im.getchannel("A")
    if a.getextrema()[0] == 255: return im  # opaque backdrop: nothing to do
    a2 = a.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(0.7))
    arr = np.asarray(im).astype(np.float32); edge = (np.asarray(a2) < 250) & (np.asarray(a2) > 0)
    rgb = arr[..., :3]; light = rgb.min(-1) > 200
    rgb[edge & light] *= 0.82  # white fringe -> soft shade of the outline
    out = Image.fromarray(np.dstack([rgb, np.asarray(a2)]).clip(0, 255).astype(np.uint8), "RGBA"); return out
def hero(asset):
    if asset not in _hero_cache:
        im = Image.open(asset if "/" in asset else glob.glob(f"{HERO_DIR}/{asset}.*")[0]).convert("RGBA")
        _hero_cache[asset] = defringe(im) if os.environ.get("DEFRINGE", "1") == "1" else im
    return _hero_cache[asset]
_hero_lib = None
def part_xy(asset, part, place):
    """canvas (0..1) point of a body landmark ('knee_l', 'elbow_r', or a segment mid 'upper_arm_l', 'shin_r') of a pose"""
    global _hero_lib
    if _hero_lib is None: _hero_lib = {a["id"]: a for a in json.load(open(f"{HERO_DIR}/library.json"))["assets"]}
    A = _hero_lib[asset]; p = A["points"]; seg = {"forearm": ("elbow", "wrist"), "upper_arm": ("shoulder", "elbow"), "thigh": ("hip", "knee"), "shin": ("knee", "ankle")}
    k, sd = part[:-2], part[-1]
    px, py = (((p[f"{seg[k][0]}_{sd}"][0] + p[f"{seg[k][1]}_{sd}"][0]) / 2, (p[f"{seg[k][0]}_{sd}"][1] + p[f"{seg[k][1]}_{sd}"][1]) / 2) if k in seg else p[part])
    iw, ih = A["size"]; w = place.get("width", 0.8); h = w * W * ih / iw / H
    return place.get("x", 0.5) - w / 2 + px * w, place.get("y", 0.6) - h / 2 + py * h

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

def norm_cap(w): return w.lower().replace(".", "").replace(",", "").replace("?", "").replace("!", "")

def paste_center(canvas, im, x, y, scale=1.0, alpha=1.0):
    if scale != 1.0: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if alpha < 1: a = im.getchannel("A").point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    canvas.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))

def rounded(im, r=36):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=255)
    o = im.convert("RGBA"); o.putalpha(m); return o

class Renderer:
    def __init__(self, plan):
        TH.clear(); TH.update(THEMES[plan.get("theme", "ice")]); TH.update(plan.get("theme_over", {}))
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
        z_prev = keyval(s["_keys"], u - 1 / FPS, dur)[0]
        if abs(z - z_prev) > 0.04:  # fast camera zoom: motion blur like the reference hook
            img = view(self.pose_canvas(s, t), z, fx, fy, dx, dy) if s.get("poses") is not None else view(load(f"{self.P['dir']}/{s['img']}", s.get("pad", False)), z, fx, fy, dx, dy)
            return self.overlay(s, t, img.filter(ImageFilter.GaussianBlur(min(14, abs(z - z_prev) * 60))))
        if s.get("poses") is not None:  # white set + H library poses (swapped at word anchors = pose animation) + extras
            return self.overlay(s, t, view(self.pose_canvas(s, t), z, fx, fy, dx, dy))
        if s.get("clip"):  # owner's animated version of the scene image (muted): frame at the scene's local time, held at the end
            fr = clip_frames(f"{self.P['dir']}/{s['clip']}"); src = fr[min(len(fr) - 1, int(u * FPS))]
        else: src = load(f"{self.P['dir']}/{s['img']}", s.get("pad", False))
        return view(src, z, fx, fy, dx, dy)

    def paper(self):
        """H's Playbook page: warm paper, faint grid, grain, soft vignette (generated once)"""
        if not hasattr(self, "_paper"):
            base = np.full((H, W, 3), TH["bg"], np.float32); gk = 1.1 if sum(TH["bg"]) < 300 else 0.965
            for k in range(0, W, 54): base[:, k:k + 2] *= gk
            for k in range(0, H, 54): base[k:k + 2, :] *= gk
            base *= (1 + np.random.default_rng(5).normal(0, 0.012, (H, W, 1)))
            yy, xx = np.mgrid[0:H, 0:W]; v = ((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2; base *= (1 - 0.18 * v)[..., None]
            self._paper = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
        return self._paper

    def stage_words(self, s, t, c):
        """big low-contrast words typed BEHIND the characters (set dressing, not captions)"""
        for bw in s.get("bgwords", []):
            a = self.tl.at(bw["at"], s)
            if t < a or (bw.get("until") and t >= self.tl.at(bw["until"], s)): continue
            n = min(len(bw["text"]), int((t - a) / bw.get("cps", 0.045)) + 1)
            im = text_img(bw["text"][:n], bw.get("font", F_BIG), bw.get("size", 230), C(bw.get("color", (205, 210, 216))), shadow=False)
            px = int(W * bw.get("x", 0.5) - im.width / 2) if bw.get("center", True) else int(W * bw.get("x", 0.08)); py = int(H * bw["y"] - im.height / 2)
            c.alpha_composite(im, (px, py))
            if bw.get("cursor") and (n < len(bw["text"]) or int((t - a) / 0.45) % 2 == 0):  # blinking bar cursor (reference typewriter bumper)
                sz = bw.get("size", 230); ImageDraw.Draw(c).rectangle([px + im.width + 8, py + im.height * 0.12, px + im.width + 8 + max(6, sz // 22), py + im.height * 0.88], fill=(*bw.get("color", (205, 210, 216)), 255))

    def stage_layer(self, s, L, t, c):
        """one character / prop layer on the stage: own enter / exit, pose swaps in place, shiver, ghost copy"""
        a = self.tl.at(L.get("at", 0), s); b = self.tl.at(L["until"], s) if L.get("until") else s["E"] + 1
        en, ex = L.get("enter", ("cut", 0)), L.get("exit", ("cut", 0))
        if t < a or t >= b + ex[1]: return
        cur = L.get("asset"); prev = None; ts = -1.0
        for asset, k in L.get("poses", []):
            tk = self.tl.at(k, s)
            if tk <= t:
                if cur is not None and asset != cur: prev, ts = cur, tk
                cur = asset
        if cur is None and L.get("poses"): cur = L["poses"][0][0]  # first pose anchored later than the layer start: show it from the start
        im = hero(cur)
        xf = L.get("xf", self.P.get("pose_xf", 0))  # long-form: 2-3 frame in-between dissolve instead of a hard swap
        if xf and prev and 0 <= t - ts < xf and hero(prev).size == im.size: im = Image.blend(hero(prev), im, ease((t - ts) / xf))
        hl = L.get("highlight")  # same picture with the muscle drawn red: blink on 3 f / off 3 f, then stays (owner 15 Nov)
        if hl and cur == hl["base"] and self.tl.at(hl["at"], s) <= t < (self.tl.at(hl["until"], s) if hl.get("until") else 1e9):
            u_ = t - self.tl.at(hl["at"], s)
            if u_ >= hl.get("blink", 2) * 0.2 or int(u_ / 0.1) % 2 == 0: im = hero(hl["asset"])
        if L.get("flip"): im = im.transpose(Image.FLIP_LEFT_RIGHT)
        w = int(W * L.get("w", 0.8)); h = int(w * im.height / im.width); x, y, sc, al, rot = W * L.get("x", 0.5), H * L.get("y", 0.6), 1.0, 1.0, 0
        def move(kind, p):  # p: 0 = off, 1 = in place
            nonlocal x, y, sc, al, rot
            q = 1 - p
            if kind == "slide_l": x -= q * (W * 0.5 + w)
            elif kind == "slide_r": x += q * (W * 0.5 + w)
            elif kind == "rise": y += q * (H * 0.5 + h * 0.6)
            elif kind == "drop": y -= q * (H * 0.5 + h * 0.6)
            elif kind == "fade": al = p
            elif kind == "pop": sc = 0.3 + 0.7 * p
            elif kind.startswith("corner"):  # grows out of a corner (commentator cameo)
                cx = W * (1.02 if kind.endswith("r") else -0.02); x = cx + (x - cx) * p; y = H * 1.02 + (y - H * 1.02) * p; sc = 0.15 + 0.85 * p
            elif kind == "fall": y += q * H * 0.7; rot = -25 * q
        entering = t < a + en[1]
        if entering: move(en[0], back((t - a) / en[1], 1.2) if en[0] in ("pop", "slide_l", "slide_r", "rise", "drop") or en[0].startswith("corner") else ease((t - a) / en[1]))
        elif t >= b: move(ex[0], 1 - ease((t - b) / ex[1]))
        for sa, su in L.get("shiver", []):  # effort / panic: fast tiny shake + side marks
            if self.tl.at(sa, s) <= t < self.tl.at(su, s):
                r_ = random.Random(int(t * FPS) * 7 + int(x)); x += (r_.random() - .5) * 10; y += (r_.random() - .5) * 6
                d = ImageDraw.Draw(c)
                for side in (-1, 1):
                    for k_ in range(3):
                        sx = x + side * (w * 0.42 + 18 * k_); sy = y - h * 0.15 + 40 * k_ - 40
                        d.arc([sx - 18, sy - 18, sx + 18, sy + 18], 100 if side < 0 else 280, 260 if side < 0 else 80, fill=(150, 150, 150, 255), width=5)
        g = L.get("ghost")
        if g and self.tl.at(g["at"], s) <= t < (self.tl.at(g["until"], s) if g.get("until") else b):  # onion-skin of the other end of the move
            ga = g.get("alpha", 0.3) * min(1, (t - self.tl.at(g["at"], s)) / 0.4)
            gi = hero(g["asset"]).resize((w, h), Image.LANCZOS); gi.putalpha(gi.getchannel("A").point(lambda v: int(v * ga)))
            c.alpha_composite(gi, (int(x - w / 2), int(y - h / 2)))
        if L.get("breathe", self.P.get("breathe")): sc *= 1 + 0.008 * math.sin(2 * math.pi * t / 3.6)  # style v2: never a frozen still
        pp = L.get("pop", self.P.get("pose_pop", 0))
        if pp and prev and 0 <= t - ts < 0.14:  # long-form v2: pose change = small squash-pop + hop (4 frames), never two poses on screen
            k_ = 1 - ease((t - ts) / 0.14); sc *= 1 + pp * k_; y -= 12 * k_
        if L.get("puppet", self.P.get("puppet")):  # long-form: slow +-1.2 deg sway on held drawings (measured "puppet" motion)
            rot += 1.2 * math.sin(2 * math.pi * t / 3.3 + (hash(str(L.get("asset"))) % 7))
        im = im.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.LANCZOS)
        if entering and en[0] in ("slide_l", "slide_r") and (t - a) / en[1] < 0.45:  # fast part of a slide: smear + streaks
            k = max(2, int(im.width / 7)); im = im.resize((k, im.height), Image.BILINEAR).resize((im.width, im.height), Image.BILINEAR)
            d = ImageDraw.Draw(c); side = 1 if en[0] == "slide_r" else -1
            for k_ in range(4):
                yy = y - h * 0.3 + k_ * h * 0.18; xx = x + side * (w * 0.45 + 30)
                d.line([(xx, yy), (xx + side * (160 + 40 * k_), yy)], fill=(170, 176, 184, 255), width=6)
        if rot: im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
        al *= L.get("alpha", 1.0)
        if al < 1: im.putalpha(im.getchannel("A").point(lambda v: int(v * al)))
        c.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))

    def pose_canvas(self, s, t):
        c = self.paper().copy() if self.P.get("paper") and not s.get("set") else Image.new("RGBA", (W, H), (*s.get("set", self.P.get("set", (255, 255, 255))), 255))  # one flat set colour (reference: #BAC8D0); section cards override
        self.stage_words(s, t, c)
        for e in s.get("mirrors", []): self.mirror(e, s, t, c)
        top = [L for L in s.get("layers", []) if L.get("z", 0) >= 3]
        for L in sorted([L for L in s.get("layers", []) if L.get("z", 0) < 3], key=lambda L: L.get("z", 0)) + ["W"] + top:
            if L == "W": self.widgets(s, t, c); continue
            if L.get("focus") and self.tl.at(L.get("at", 0), s) <= t < (self.tl.at(L["until"], s) if L.get("until") else 1e9):  # everything behind goes soft + a bit darker
                k = min(1, (t - self.tl.at(L.get("at", 0), s)) / 0.3); c = c.filter(ImageFilter.GaussianBlur(12 * k))
                c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(40 * k))))
            self.stage_layer(s, L, t, c)
        if s.get("poses"):
            fr = [(a, self.tl.at(k, s)) for a, k in s["poses"]]; cur = fr[0][0]
            for a, k in fr:
                if k <= t: cur = a
            pl = s.get("place", {}); im = hero(cur)
            w = int(W * pl.get("width", 0.8)); im = im.resize((w, int(w * im.height / im.width)), Image.LANCZOS)
            c.alpha_composite(im, (int(W * pl.get("x", 0.5) - w / 2), int(H * pl.get("y", 0.6) - im.height / 2)))
        for e in s.get("extras", []):  # anatomy bubbles / props that pop in
            a = self.tl.at(e["at"], s)
            if t < a or (e.get("until") and t >= self.tl.at(e["until"], s)): continue
            im = hero(e["asset"]); w = int(W * e.get("w", 0.3)); im = im.resize((w, int(w * im.height / im.width)), Image.LANCZOS)
            sc_ = 0.5 + 0.5 * back((t - a) / 0.25, 1.8); paste_center(c, im, W * e["x"], H * e["y"], sc_)
        for tx in s.get("texts", []):  # kinetic headline words (black / red), slam in
            a = self.tl.at(tx["at"], s)
            if t < a or (tx.get("until") and t >= self.tl.at(tx["until"], s)): continue
            if "_im" not in tx: tx["_im"] = text_img(tx["text"], F_BIG, tx.get("size", 170), tx.get("color", INK), stroke=8, maxw=W * 0.9)
            p = (t - a) / 0.2; paste_center(c, tx["_im"], W / 2, H * tx.get("y", 0.15), 1.6 - 0.6 * back(p, 1.4) if p < 1 else 1.0, min(1, p * 2))
        self.fx(s, t, c)
        return c.convert("RGB")

    # ---------- long-form widgets (research/LONGFORM-24-ANALYSIS-AND-PLAN.md, D6) ----------
    def overlay(self, s, t, img):
        """text widgets drawn AFTER the camera: never zoomed out of the frame (owner 19 Nov: cut text)"""
        if not self.P.get("text_overlay") or not any(s.get(k) for k in ("kinetic", "counters", "rings")): return img
        c = img.convert("RGBA"); self.widgets(s, t, c, only=("kinetic", "counters", "rings")); return c.convert("RGB")

    def widgets(self, s, t, c, only=None):
        d = ImageDraw.Draw(c); FI = f"{HERE}/fonts/rubik-800-italic.woff2"
        ov = self.P.get("text_overlay")
        def on(k): return (k in only) if only else not (ov and k in ("kinetic", "counters", "rings"))
        for e in (s.get("kinetic", []) if on("kinetic") else []):  # big italic words, no box: slide 90 px + fade in over 5 frames (ease-out), fade out 6 frames
            lv = self._live(e, s, t, 0.0 if e.get("until") else 0.2)  # replaced words vanish at once: never two words on one spot
            if not lv: continue
            u, f = lv; key = "_k"
            if key not in e: e[key] = text_img(e["text"], FI, e.get("size", 110), tuple(e.get("color", (34, 40, 48))), stroke=e.get("stroke", 0), stroke_fill=tuple(e.get("stroke_fill", (255, 255, 255))), shadow=False, maxw=W * e.get("maxw", 0.6))
            q = ease(u / 0.17); off = {"l": (-90, 0), "r": (90, 0), "b": (0, 60), "t": (0, -60)}[e.get("from", "l")]
            iw, ih = e[key].size; mx, my = 0.025 * W, 0.02 * H  # safe area: the whole word stays inside the frame
            cx = min(max(W * e["x"], mx + iw / 2), W - mx - iw / 2); cy = min(max(H * e["y"], my + ih / 2), H - my - ih / 2)
            paste_center(c, e[key], cx + off[0] * (1 - q), cy + off[1] * (1 - q), 1.0, min(1, u / 0.17) * f)
        for e in (s.get("counters", []) if on("counters") else []):  # number counts up (ease-out) then a small 1.08 punch
            lv = self._live(e, s, t, 0.2)
            if not lv: continue
            u, f = lv; dur = e.get("dur", 1.5); q = ease(min(1, u / dur)); val = round(e.get("a", 0) + (e["b"] - e.get("a", 0)) * q)
            im = text_img(f"{val}{e.get('suffix', '')}", FI, e.get("size", 220), tuple(e.get("color", (34, 40, 48))), stroke=e.get("stroke", 0), stroke_fill=tuple(e.get("stroke_fill", (34, 40, 48))), shadow=False)
            pk = 1 + 0.08 * math.sin(min(1, max(0, (u - dur) / 0.2)) * math.pi)
            paste_center(c, im, W * e["x"], H * e["y"], pk, f)
            if e.get("label"):
                if "_l" not in e: e["_l"] = text_img(e["label"], FI, e.get("lsize", 54), tuple(e.get("color", (34, 40, 48))), stroke=e.get("stroke", 0), stroke_fill=tuple(e.get("stroke_fill", (34, 40, 48))), shadow=False)
                paste_center(c, e["_l"], W * e["x"], H * e["y"] + im.height * 0.55, 1.0, f)
        for e in (s.get("rings", []) if on("rings") else []):  # stopwatch ring: arc grows over dur, seconds inside
            lv = self._live(e, s, t, 0.2)
            if not lv: continue
            u, f = lv; R = int(H * e.get("r", 0.16)); x, y = W * e["x"], H * e["y"]; q = min(1, u / e.get("dur", 3)); a_ = int(255 * f)
            sc_ = ease(min(1, u / 0.17)); R = max(4, int(R * sc_))
            d.ellipse([x - R, y - R, x + R, y + R], fill=(255, 255, 255, a_), outline=(34, 40, 48, a_), width=max(2, R // 14))
            d.arc([x - R * 0.82, y - R * 0.82, x + R * 0.82, y + R * 0.82], -90, -90 + 360 * q, fill=(*e.get("color", (15, 139, 133)), a_), width=max(3, R // 7))
            num = text_img(f"{int(e.get('max', 60) * q)}", FI, max(10, int(R * 0.7)), (34, 40, 48), shadow=False); paste_center(c, num, x, y - R * 0.08, 1.0, f)
            if e.get("unit"): paste_center(c, text_img(e["unit"], FI, max(8, int(R * 0.25)), (34, 40, 48), shadow=False), x, y + R * 0.42, 1.0, f)
        for e in (s.get("calendars", []) if on("calendars") else []):  # month grid, cells tick one by one (4 f each, 2 f stagger) at the given anchors
            lv = self._live(e, s, t, 0.2)
            if not lv: continue
            u, f = lv; cols, n = e.get("cols", 10), e.get("n", 30); rows = (n + cols - 1) // cols
            cw = W * e.get("w", 0.42) / cols; x0, y0 = W * e["x"] - cw * cols / 2, H * e["y"] - cw * rows / 2; a_ = int(255 * f)
            filled = 0.0; base_ = 0
            for an, cnt in e.get("ticks", []):  # [(anchor, total ticked after it)], in order
                ta = self.tl.at(an, s)
                if t >= ta: filled = min(cnt, base_ + (t - ta) / 0.067)
                base_ = cnt
            for k in range(n):
                cx, cy = x0 + (k % cols) * cw, y0 + (k // cols) * cw; p_ = min(1, max(0, filled - k))
                d.rounded_rectangle([cx + 4, cy + 4, cx + cw - 4, cy + cw - 4], int(cw * 0.15), fill=(255, 255, 255, a_), outline=(34, 40, 48, a_), width=3)
                if p_ > 0:
                    r_ = (cw - 16) / 2 * ease(p_); mx, my = cx + cw / 2, cy + cw / 2
                    d.rounded_rectangle([mx - r_, my - r_, mx + r_, my + r_], int(r_ * 0.3), fill=(*e.get("color", (15, 139, 133)), a_))
                    if p_ >= 1: d.line([(mx - r_ * 0.45, my), (mx - r_ * 0.1, my + r_ * 0.35), (mx + r_ * 0.5, my - r_ * 0.35)], fill=(255, 255, 255, a_), width=max(3, int(cw * 0.08)))
                if e.get("numbers", True):
                    tn = text_img(str(k + 1), FI, int(cw * 0.26), (120, 128, 138), shadow=False); c.alpha_composite(tn, (int(cx + 8), int(cy + 4))) if p_ == 0 else None
        for e in (s.get("bars", []) if on("bars") else []):  # bar chart, bars grow one after another (stagger, 6 f each), value on top
            lv = self._live(e, s, t, 0.2)
            if not lv: continue
            u, f = lv; vals = e["values"]; n = len(vals); bw = W * e.get("w", 0.4) / n; x0 = W * e["x"] - bw * n / 2; yb = H * e["y"]; hm = H * e.get("h", 0.4); a_ = int(255 * f)
            d.line([(x0 - 10, yb), (x0 + bw * n + 10, yb)], fill=(34, 40, 48, a_), width=4)
            for k, v in enumerate(vals):
                q = ease(min(1, max(0, (u - k * e.get("stagger", 0.12)) / 0.2)))
                if q <= 0: continue
                hh = hm * v / max(vals) * q; col = e.get("hi_color", (122, 26, 26)) if k == n - 1 and e.get("hi_last") else e.get("color", (15, 139, 133))
                d.rounded_rectangle([x0 + k * bw + bw * 0.15, yb - hh, x0 + (k + 1) * bw - bw * 0.15, yb], 8, fill=(*col, a_))
                if q >= 1 and e.get("show_values", True): paste_center(c, text_img(str(v), FI, int(bw * 0.38), (34, 40, 48), shadow=False), x0 + k * bw + bw / 2, yb - hh - bw * 0.3, 1.0, f)
                if e.get("labels"): paste_center(c, text_img(e["labels"][k], FI, int(bw * 0.26), (90, 98, 108), shadow=False), x0 + k * bw + bw / 2, yb + bw * 0.28, 1.0, f)

    # ---------- effects library (research/EFFECTS-LIBRARY-36-VIDEOS.md) ----------
    def _live(self, e, s, t, fade=0.15):
        a = self.tl.at(e.get("at", 0), s); b = self.tl.at(e["until"], s) if e.get("until") else 1e9
        if t < a or t >= b + fade: return None
        return t - a, (1 - (t - b) / fade) if t >= b else 1.0

    def fx(self, s, t, c):
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for e in s.get("arcs", []):  # dashed motion arc drawn on along the move, arrowhead at the end
            lv = self._live(e, s, t)
            if not lv: continue
            u, f = lv; X, Y, R = W * e["x"], H * e["y"], W * e.get("r", 0.15); a0, a1 = e.get("a0", 200), e.get("a1", 340)
            end = a0 + (a1 - a0) * ease(u / 0.35); col = (*e.get("color", (255, 255, 255)), int(235 * f)); st_ = 9 if a1 > a0 else -9
            for k in range(int((end - a0) / st_)):
                g0 = a0 + k * st_; g1 = g0 + st_ * 0.55
                d.arc([X - R, Y - R, X + R, Y + R], min(g0, g1), max(g0, g1), fill=col, width=e.get("wd", 9))
            if e.get("arrow", True) and u > 0.3:
                ang = math.radians(a1); tx_, ty_ = X + R * math.cos(ang), Y + R * math.sin(ang); dv = 1 if a1 > a0 else -1
                vx, vy = -math.sin(ang) * dv, math.cos(ang) * dv; px, py = -vy, vx
                d.polygon([(tx_ + vx * 34, ty_ + vy * 34), (tx_ + px * 22, ty_ + py * 22), (tx_ - px * 22, ty_ - py * 22)], fill=col)
        for e in s.get("particles", []):  # green plus signs floating up (growth)
            lv = self._live(e, s, t)
            if not lv: continue
            u, f = lv; rnd = random.Random(e.get("seed", 3)); col = e.get("color", (60, 200, 90))
            for k in range(e.get("n", 12)):
                ox, oy, ph, sz = (rnd.random() - .5) * W * e.get("spread", 0.4), (rnd.random() - .5) * H * 0.15, rnd.random(), 18 + rnd.random() * 20
                q = (u * 0.8 + ph) % 1; X, Y = W * e["x"] + ox, H * e["y"] + oy - q * 260; al = int(255 * f * min(1, q * 5) * (1 - q))
                d.rectangle([X - sz, Y - sz * 0.28, X + sz, Y + sz * 0.28], fill=(*col, al)); d.rectangle([X - sz * 0.28, Y - sz, X + sz * 0.28, Y + sz], fill=(*col, al))
        c.alpha_composite(ov)
        for e in s.get("insets", []): self.inset(e, s, t, c)
        for e in s.get("meters", []): self.meter(e, s, t, c)
        for e in s.get("scribbles", []): self.scribble(e, s, t, c)
        live = [e for e in s.get("labels", []) if self._live(e, s, t)]
        self._pre = c.copy()  # label placement looks at the picture BEFORE any text-mode blur (faces stay detectable)
        if len(live) >= 3 and not s.get("no_textmode"):  # a lot of text: soften the picture behind it (owner 15 Nov)
            k = min(1, (t - min(self.tl.at(e.get("at", 0), s) for e in live[2:3])) / 0.25)
            soft = c.filter(ImageFilter.GaussianBlur(10)); soft.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, 90)))
            c.paste(Image.blend(c, soft, k)); s["_textmode"] = True
        self._lab_boxes = []
        for e in s.get("labels", []): self.label(e, s, t, c)
        for e in s.get("dim", []):  # whole frame darkens (marks are drawn later, so they stay bright)
            lv = self._live(e, s, t, 0.25)
            if not lv: continue
            u, f = lv; c.alpha_composite(Image.new("RGBA", (W, H), (10, 14, 20, int(255 * e.get("amount", 0.44) * ease(u / e.get("ramp", 0.6)) * f))))

    def scribble(self, e, s, t, c):
        """orange marker drawn live (write-on 0.35 s), lines 'boil' (re-jittered 8x/s): circle, arrow, underline, v, check, x, curve"""
        lv = self._live(e, s, t)
        if not lv: return
        u, f = lv; k = e.get("kind", "circle"); pr = ease(u / e.get("dur", 0.35)); jr = random.Random(int(t * 8) * 13 + int(e["x"] * 100))
        X, Y = W * e["x"], H * e["y"]; pts = []
        if k == "circle":
            rx, ry = W * e.get("rx", 0.12), W * e.get("ry", e.get("rx", 0.12))
            pts = [(X + rx * (1 + 0.06 * math.sin(a * 3)) * math.cos(a), Y + ry * (1 + 0.05 * math.cos(a * 2)) * math.sin(a)) for a in [-2.2 + j * 0.08 for j in range(int(7.4 / 0.08))]]
        elif k in ("arrow", "underline", "curve"):
            x1, y1 = W * e["x1"], H * e["y1"]; bend = e.get("bend", 0.0 if k != "curve" else 0.25); n = 30
            mx, my = (X + x1) / 2 - (y1 - Y) * bend, (Y + y1) / 2 + (x1 - X) * bend
            pts = [((1 - q) ** 2 * X + 2 * (1 - q) * q * mx + q * q * x1, (1 - q) ** 2 * Y + 2 * (1 - q) * q * my + q * q * y1) for q in [j / n for j in range(n + 1)]]
        elif k == "v":
            sz = W * e.get("size", 0.15); pts = [(X - sz, Y - sz * 1.1), (X, Y + sz * 0.9), (X + sz, Y - sz * 1.1)]
            pts = [(a[0] + (b[0] - a[0]) * q / 12, a[1] + (b[1] - a[1]) * q / 12) for a, b in zip(pts, pts[1:]) for q in range(13)]
        elif k == "check":
            sz = W * e.get("size", 0.06); pts = [(X - sz, Y), (X - sz * 0.3, Y + sz * 0.7), (X + sz, Y - sz * 0.9)]
            pts = [(a[0] + (b[0] - a[0]) * q / 8, a[1] + (b[1] - a[1]) * q / 8) for a, b in zip(pts, pts[1:]) for q in range(9)]
        m = max(2, int(len(pts) * pr)); pts = [(x + jr.uniform(-2.5, 2.5), y + jr.uniform(-2.5, 2.5)) for x, y in pts[:m]]
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); col = (*C(e.get("color", "accent")), int(245 * f)); wd = e.get("wd", 13)
        d.line(pts, fill=col, width=wd, joint="curve")
        for x, y in (pts[0], pts[-1]): d.ellipse([x - wd / 2, y - wd / 2, x + wd / 2, y + wd / 2], fill=col)
        if k == "arrow" and pr > 0.95:
            (ax, ay), (bx, by) = pts[-4], pts[-1]; ang = math.atan2(by - ay, bx - ax)
            for da in (2.5, -2.5): d.line([(bx, by), (bx + 46 * math.cos(ang + da), by + 46 * math.sin(ang + da))], fill=col, width=wd)
        c.alpha_composite(ov)

    def meter(self, e, s, t, c):
        """Effort-o-meter: half dial mint -> sticky yellow -> tomato, needle swings to the value with overshoot, handwritten title + verdict"""
        lv = self._live(e, s, t)
        if not lv: return
        u, f = lv; X, Y, R = W * e["x"], H * e["y"], W * e.get("r", 0.16)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); a_ = int(255 * f)
        sc = 0.6 + 0.4 * back(u / 0.25, 1.5); R *= sc
        d.pieslice([X - R - 14, Y - R - 14, X + R + 14, Y + R + 14], 180, 360, fill=(*TH["plate"], a_), outline=(*TH["frame"], a_), width=8)
        for k_, col in enumerate((TH["good"], TH["warn"], TH["accent2"], TH["bad"])):
            d.arc([X - R + 10, Y - R + 10, X + R - 10, Y + R - 10], 180 + k_ * 45 + 1, 180 + (k_ + 1) * 45 - 1, fill=(*col, a_), width=int(R * 0.22))
        v = e.get("value", 0.15) * back(min(1, max(0, (u - 0.2) / 0.45)), 2.2); ang = math.radians(180 + 180 * v)
        d.line([(X, Y), (X + R * 0.82 * math.cos(ang), Y + R * 0.82 * math.sin(ang))], fill=(*TH["frame"], a_), width=12); d.ellipse([X - 20, Y - 20, X + 20, Y + 20], fill=(*TH["frame"], a_))
        c.alpha_composite(ov)
        for txt, yy, sz, col in ((e.get("title", "EFFORT"), Y + 50, int(64 * sc), TH["text"]), (e.get("verdict", ""), Y + 120, int(78 * sc), C(e.get("vcolor", "accent")))):
            if txt and (yy == Y + 50 or u > 0.6):
                im = text_img(txt, F_MARK, sz, col, shadow=False); c.alpha_composite(im, (int(X - im.width / 2), int(yy - im.height / 2)))

    def mirror(self, e, s, t, c):
        """oval wall mirror: navy frame, pale glass with glare; shows a reflection asset that swaps (crossfade) on word anchors"""
        lv = self._live(e, s, t)
        if not lv: return
        u, f = lv; X, Y, w, h = W * e["x"], H * e["y"], W * e.get("w", 0.5), H * e.get("h", 0.42)
        drop = (1 - back(u / 0.45, 1.3)) * H * 0.6; Y -= drop
        glass = Image.new("RGBA", (int(w), int(h)), (226, 236, 240, 255)); gd = ImageDraw.Draw(glass)
        for k_ in range(int(h)): gd.line([(0, k_), (w, k_)], fill=(int(214 + 22 * k_ / h), int(228 + 14 * k_ / h), int(234 + 10 * k_ / h), 255))
        items = [(a_, self.tl.at(k, s), sc_) for a_, k, sc_ in e["show"]]; cur = [it for it in items if it[1] <= t]
        def put(asset, sc_, al):
            im = hero(asset); hh = int(h * sc_); ww = int(hh * im.width / im.height)
            if ww > w * 0.9: ww = int(w * 0.9); hh = int(ww * im.height / im.width)
            im = im.resize((ww, hh), Image.LANCZOS)
            if al < 1: im.putalpha(im.getchannel("A").point(lambda v: int(v * al)))
            glass.alpha_composite(im, (int((w - ww) / 2), int(h * 0.97 - hh)))
        if cur:
            last = cur[-1]; pf = min(1, (t - last[1]) / 0.3)
            if len(cur) > 1 and pf < 1: put(cur[-2][0], cur[-2][2], 1 - pf)
            put(last[0], last[2], pf if len(cur) > 1 or t - last[1] < 0.3 else 1)
        for k_ in (0.18, 0.3):  # glare streaks
            gl = Image.new("RGBA", glass.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).line([(w * k_, h * 0.05), (w * (k_ + 0.3), h * 0.5)], fill=(255, 255, 255, 90), width=int(w * 0.04)); glass.alpha_composite(gl)
        m = Image.new("L", glass.size, 0); ImageDraw.Draw(m).ellipse([0, 0, w - 1, h - 1], fill=255)
        out = Image.new("RGBA", (int(w) + 40, int(h) + 40), (0, 0, 0, 0)); sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([24, 30, w + 24, h + 30], fill=(0, 0, 0, 60)); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
        out.paste(glass, (20, 20), m); ImageDraw.Draw(out).ellipse([14, 14, w + 26, h + 26], outline=(*TH["frame"], 255), width=16)
        ImageDraw.Draw(out).ellipse([30, 30, w + 10, h + 10], outline=(*TH["accent"], 255), width=4)
        if f < 1: out.putalpha(out.getchannel("A").point(lambda v: int(v * f)))
        c.alpha_composite(out, (int(X - out.width / 2), int(Y - out.height / 2)))

    def inset(self, e, s, t, c):
        """circle badge with a zoomed crop of a pose (muscle close-up): pops from 125 % with blur, optional big-centre start, red X / green tick"""
        lv = self._live(e, s, t)
        if not lv: return
        u, f = lv; R = int(W * e.get("r", 0.13))
        if "_im" not in e:
            src = hero(e["asset"]); cx, cy, fr = e.get("crop", (0.5, 0.4, 0.5)); cw = src.width * fr
            cr = src.crop((int(cx * src.width - cw / 2), int(cy * src.height - cw / 2), int(cx * src.width + cw / 2), int(cy * src.height + cw / 2))).resize((2 * R, 2 * R), Image.LANCZOS)
            im = Image.new("RGBA", (2 * R + 16, 2 * R + 16), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse([8, 8, 2 * R + 8, 2 * R + 8], fill=(*e.get("bg", (150, 164, 176)), 255))
            if e.get("paint"):  # colour on the muscle inside the badge
                px, py, rx, ry, col = e["paint"]; col = C(col); g = Image.new("RGBA", cr.size, (0, 0, 0, 0))
                ImageDraw.Draw(g).ellipse([(px - rx) * 2 * R, (py - ry) * 2 * R, (px + rx) * 2 * R, (py + ry) * 2 * R], fill=(*col, 170)); g = g.filter(ImageFilter.GaussianBlur(R * 0.05))
                cr = cr.copy(); cr.alpha_composite(Image.composite(g, Image.new("RGBA", cr.size, (0, 0, 0, 0)), cr.getchannel("A")))
            m = Image.new("L", (2 * R, 2 * R), 0); ImageDraw.Draw(m).ellipse([0, 0, 2 * R, 2 * R], fill=255)
            body = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0)); body.paste(cr, (0, 0), Image.composite(cr.getchannel("A"), Image.new("L", cr.size, 0), m))
            im.alpha_composite(body, (8, 8)); ImageDraw.Draw(im).ellipse([8, 8, 2 * R + 8, 2 * R + 8], outline=(*TH["frame"], 255) if e.get("lens") else (40, 46, 54, 255), width=14 if e.get("lens") else 7)
            if e.get("lens"):
                gl = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).arc([R * 0.35, R * 0.35, R * 1.2, R * 1.2], 190, 250, fill=(255, 255, 255, 170), width=int(R * 0.08)); im.alpha_composite(gl)
            e["_im"] = im
        x, y = W * e["x"], H * e["y"]
        if e.get("from"):  # lens glides in from its start point
            q = ease(u / 0.45); x, y = W * e["from"][0] + (x - W * e["from"][0]) * q, H * e["from"][1] + (y - H * e["from"][1]) * q
        if e.get("lens"):  # X-Ray lens: navy handle behind the glass
            d_ = ImageDraw.Draw(c); r_ = R * 1.0; hx, hy = x + r_ * 0.75, y + r_ * 0.75
            d_.line([(hx, hy), (hx + r_ * 0.75, hy + r_ * 0.75)], fill=(*TH["frame"], int(255 * f)), width=int(r_ * 0.26))
            d_.line([(hx, hy), (hx + r_ * 0.25, hy + r_ * 0.25)], fill=(*TH["accent"], int(255 * f)), width=int(r_ * 0.3))
        if e.get("big_at") is not None:  # starts big in the centre, then shrinks to its corner spot
            mv = ease((t - self.tl.at(e["big_at"], s)) / 0.4) if t >= self.tl.at(e["big_at"], s) else 0
            x, y = W * 0.5 + (x - W * 0.5) * mv, H * 0.42 + (y - H * 0.42) * mv; scale = 2.1 - 1.1 * mv
        else: scale = 1.0
        if e.get("grow"):  # long-form: grows from the body part it explains, 0 -> 100 % in 5 frames, ease-out, no bounce
            q = ease(u / 0.17); gx, gy = W * e["grow"][0], H * e["grow"][1]; x, y = gx + (x - gx) * q, gy + (y - gy) * q; scale *= max(0.05, q)
        elif u < 0.14: scale *= 1.25 - 0.25 * ease(u / 0.14)
        im = e["_im"].resize((int(e["_im"].width * scale), int(e["_im"].height * scale)), Image.LANCZOS)
        if u < 0.07 and not e.get("grow"): im = im.filter(ImageFilter.GaussianBlur(6))
        al = (1.0 if e.get("grow") else min(1, u / 0.07)) * f
        if al < 1: im.putalpha(im.getchannel("A").point(lambda v: int(v * al)))
        c.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
        mk = e.get("mark")
        if mk and u > e.get("mark_delay", 0.3):  # red X or green tick at the badge's top-right, drawn on
            k = ease((u - e.get("mark_delay", 0.3)) / 0.2); r = R * scale; mx, my = x + r * 0.72, y - r * 0.72; d = ImageDraw.Draw(c); a_ = int(255 * f)
            if mk == "x":
                s_ = r * 0.32
                for (x0, y0, x1, y1) in ((-1, -1, 1, 1), (1, -1, -1, 1)):
                    d.line([(mx + x0 * s_, my + y0 * s_), (mx + x0 * s_ + (x1 - x0) * s_ * k, my + y0 * s_ + (y1 - y0) * s_ * k)], fill=(225, 29, 46, a_), width=int(r * 0.13))
            else:
                pts = [(mx - r * 0.3, my), (mx - r * 0.08, my + r * 0.24), (mx + r * 0.36, my - r * 0.3)]
                d.line(pts[:2] if k < 0.4 else pts, fill=(40, 190, 80, a_), width=int(r * 0.13), joint="curve")

    def occupancy(self, c, s):
        """where things are drawn (not the plain set), at 1/8 size, plus the figure's face zone (top 30 % of the biggest blob)"""
        a = np.asarray(c.convert("RGB").resize((W // 8, H // 8))).astype(int); bg = np.array(s.get("set", self.P.get("set", (255, 255, 255))))
        occ = np.abs(a - bg).sum(-1) > 45
        from scipy import ndimage  # (face zone grown by a few px below so labels keep a gap)
        lab_, n = ndimage.label(ndimage.binary_closing(occ, iterations=2)); face = np.zeros_like(occ)
        for i in range(1, n + 1):
            ys, xs = np.nonzero(lab_ == i)
            if len(ys) < occ.size * 0.02: continue
            y0, y1 = ys.min(), ys.max(); m = (lab_ == i); m[int(y0 + (y1 - y0) * 0.3):] = False; face |= m
        return occ, face

    def place(self, e, s, c):
        """best spot for a label: inside the frame, off the caption band, off other labels, off the picture (faces cost the most)"""
        if e.get("fixed"): return W * e["x"], H * e["y"]
        tm = bool(s.get("_textmode"))  # text mode: the picture is blurred, labels may cross the body but never a face
        occ, face = self.occupancy(getattr(self, "_pre", c), s); bw, bh = e["_im"].width / 8, e["_im"].height / 8; best = None
        cy = self.P.get("cap_y", 0.8)
        for yy in np.arange(0.06, 0.93, 0.02):
            for xx in (e["x"], 0.5, 0.3, 0.7, 0.22, 0.78):
                x0, y0 = xx * W / 8 - bw / 2, yy * H / 8 - bh / 2
                if x0 < W / 8 * 0.03 or x0 + bw > W / 8 * 0.97 or y0 < 0 or y0 + bh > H / 8 * 0.95: continue
                if abs(yy - cy) < 0.06: continue
                sl = (slice(int(y0), int(y0 + bh) + 1), slice(int(x0), int(x0 + bw) + 1))
                o, fo = occ[sl].mean(), face[sl].mean()
                lo = sum(max(0, min(x0 + bw, bx1) - max(x0, bx0)) * max(0, min(y0 + bh, by1) - max(y0, by0)) for bx0, by0, bx1, by1 in self._lab_boxes) / (bw * bh)
                cost = (0 if tm else o * 100) + fo * 2000 + lo * 500 + abs(yy - e["y"]) * 25 + abs(xx - e["x"]) * 10
                if best is None or cost < best[0]: best = (cost, xx, yy, x0, y0, o, fo)
        _, xx, yy, x0, y0, o, fo = best; self._lab_boxes.append((x0, y0, x0 + bw, y0 + bh))
        self.qa = getattr(self, "qa", []); self.qa.append(dict(text=e["text"], scene=s["text"][:40], over=round(float(o), 3), face=round(float(fo), 3)))
        return W * xx, H * yy

    def label(self, e, s, t, c):
        """small white box with a dark border (reference labels): drops in from above with motion blur, optional leader line"""
        lv = self._live(e, s, t)
        if not lv: return
        u, f = lv
        if e.get("style") == "sticky":  # sticky note slapped on: rotated, shadow, overshoot scale in 4 frames
            if "_im" not in e:
                tx = text_img(e["text"], F_MARK, e.get("size", 54), TH["sticky_text"], shadow=False, maxw=W * 0.4); pad = 34
                im = Image.new("RGBA", (tx.width + 2 * pad + 20, tx.height + 2 * pad + 20), (0, 0, 0, 0)); sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
                ImageDraw.Draw(sh).rectangle([14, 18, im.width - 4, im.height - 2], fill=(0, 0, 0, 70)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
                ImageDraw.Draw(im).rectangle([6, 6, im.width - 14, im.height - 14], fill=(*C(e.get("color", "sticky")), 255))
                ImageDraw.Draw(im).rectangle([6, 6, im.width - 14, 22], fill=tuple(int(v * 0.92) for v in C(e.get("color", "sticky"))) + (255,))
                im.alpha_composite(tx, (6 + pad, 6 + pad)); e["_im"] = im.rotate(e.get("rot", random.Random(len(e["text"])).uniform(-5, 5)), expand=True, resample=Image.BICUBIC)
            sc = 1.18 - 0.18 * ease(u / 0.13) if u < 0.13 else 1.0; im = e["_im"].resize((int(e["_im"].width * sc), int(e["_im"].height * sc)), Image.LANCZOS)
            if f < 1: im.putalpha(im.getchannel("A").point(lambda v: int(v * f)))
            c.alpha_composite(im, (int(W * e["x"] - im.width / 2), int(H * e["y"] - im.height / 2))); return  # sticky notes keep their hand-set spot
        if "_im" not in e:
            tx = text_img(e["text"], f"{HERE}/fonts/rubik-800.woff2", e.get("size", 50), (25, 28, 32), shadow=False)
            im = Image.new("RGBA", (tx.width + 56, tx.height + 26), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle([2, 2, im.width - 3, im.height - 3], 14, fill=(255, 255, 255, 255), outline=(30, 34, 40, 255), width=5)
            im.alpha_composite(tx, (28, 13)); e["_im"] = im
        if "_xy" not in e: e["_xy"] = self.place(e, s, c)  # free spot, decided once when the label appears
        else:
            bw, bh = e["_im"].width / 8, e["_im"].height / 8; self._lab_boxes.append((e["_xy"][0] / 8 - bw / 2, e["_xy"][1] / 8 - bh / 2, e["_xy"][0] / 8 + bw / 2, e["_xy"][1] / 8 + bh / 2))
        x, y = e["_xy"]; p = ease(u / 0.27); y -= (1 - p) * H * 0.1
        im = e["_im"]
        if u < 0.18: im = im.filter(ImageFilter.GaussianBlur(5 * (1 - u / 0.18)))
        al = min(1, u / 0.08) * f
        if al < 1: im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * al)))
        if e.get("leader") and p > 0.8:
            lx, ly = e["leader"]; ImageDraw.Draw(c).line([(x, y), (W * lx, H * ly)], fill=(30, 34, 40, int(255 * f)), width=5)
        c.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))

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
        if kind == "squash":  # old squeezes to a vertical line (ease-in), 1 empty frame, new expands from the line (ease-out)
            bg = old.getpixel((4, 4)); c = Image.new("RGB", (W, H), bg)
            if p < 0.45: sx = 1 - (p / 0.45) ** 2; im = old
            elif p < 0.55: return c
            else: sx = ease((p - 0.55) / 0.45); im = new; c = Image.new("RGB", (W, H), new.getpixel((4, 4)))
            im = im.resize((max(2, int(W * sx)), H), Image.BILINEAR); c.paste(im, ((W - im.width) // 2, 0)); return c
        if kind == "brush":  # rough paint strokes sweep across, band by band from the top, revealing the new scene
            m = Image.new("L", (W, H), 0); dm = ImageDraw.Draw(m); rnd = random.Random(11); nb = 7; bh = H / nb
            for k in range(nb):
                pk = ease((p - k * 0.06) / 0.55); xe = pk * W * 1.35 - 0.2 * W; y0, y1 = k * bh - 25, (k + 1) * bh + 25
                pts = [(-10, y0)] + [(xe + rnd.uniform(-90, 90), y0 + (y1 - y0) * j / 10) for j in range(11)] + [(-10, y1)]
                if xe > -0.2 * W: dm.polygon(pts, fill=255)
                for j in range(5):  # dry-brush streaks ahead of the stroke
                    yy = y0 + rnd.uniform(0, y1 - y0); ln = rnd.uniform(40, 220)
                    if 0 < pk < 1: dm.line([(xe, yy), (xe + ln * pk, yy)], fill=255, width=rnd.randint(3, 9))
            c.paste(old); c.paste(new, (0, 0), m); return c
        if kind == "page":  # notebook page turn: old page folds to the left edge, curl highlight + shadow on the new page
            c.paste(new); xe = int(W * (1 - e)); sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dsh = ImageDraw.Draw(sh)
            for k in range(60): dsh.line([(xe + k, 0), (xe + k, H)], fill=(0, 0, 0, int(90 * (1 - k / 60))))
            c = Image.alpha_composite(c.convert("RGBA"), sh).convert("RGB")
            if xe > 2:
                o = old.resize((xe, H), Image.BILINEAR); c.paste(o, (0, 0))
                cw = max(2, int(80 * math.sin(math.pi * e))); g = Image.new("RGBA", (cw, H), (255, 255, 255, 0)); dg = ImageDraw.Draw(g)
                for k in range(cw): dg.line([(k, 0), (k, H)], fill=(*tuple(min(255, v + 25) for v in TH["bg"]), int(255 * (k / cw))))
                c.paste(g, (max(0, xe - cw), 0), g)
            return c
        if kind.startswith("iris"):  # plain circle grows from a point (no outline)
            cx, cy = (float(v) for v in (kind.split(":")[1].split(",") if ":" in kind else (0.5, 0.5)))
            r = e * 1.25 * H; m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).ellipse([cx * W - r, cy * H - r, cx * W + r, cy * H + r], fill=255)
            c.paste(old); c.paste(new, (0, 0), m); return c
        if kind == "dip":  # long-form: old fades into the set tint, then the new scene fades up (measured 8-12 f out, 6-8 f in)
            bg = Image.new("RGB", (W, H), tuple(self.P.get("set", (255, 255, 255))))
            return Image.blend(old, bg, ease(p / 0.6)) if p < 0.6 else Image.blend(bg, new, ease((p - 0.6) / 0.4))
        if kind == "greyout":  # old greys out (~35 %) and softens, then the new scene comes up
            if p < 0.6:
                k = ease(p / 0.6); return Image.blend(old.filter(ImageFilter.GaussianBlur(6 * k)), Image.new("RGB", (W, H), (70, 74, 80)), 0.35 * k)
            return Image.blend(Image.blend(old, Image.new("RGB", (W, H), (70, 74, 80)), 0.35), new, ease((p - 0.6) / 0.4))
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
            p = t / en[1]; e = back(p, 1.4); off = (1 - e) * (en[2] if len(en) > 2 else 0.6)
            img = self.scene(0, t); c = Image.new("RGB", (W, H), (255, 255, 255))
            if p < 0.4: img = img.resize((max(2, int(W / (4 + 30 * p))), H)).resize((W, H)) if en[0] in ("left", "right") else img
            dx = {"left": -1, "right": 1}.get(en[0], 0) * off * W; dy = {"bottom": 1, "top": -1}.get(en[0], 0) * off * H
            c.paste(img, (int(dx), int(dy))); return c, 0
        return self.scene(i, t), i

    # ---------- overlays ----------
    def caption_build(self, t, j):
        """reference style: bottom, lowercase, 2-3 words per phrase, built word by word, white with a dark stroke"""
        ws = self.tl.words
        if not hasattr(self, "_chunks"):
            self._chunks, cur = [], []
            for k, w in enumerate(ws):
                cur.append(k)
                if len(cur) >= self.P.get("cap_words", 3) or w["text"][-1:] in ".,?!:;": self._chunks.append(cur); cur = []
            if cur: self._chunks.append(cur)
        ch = next((c_ for c_ in self._chunks if ws[c_[0]]["start"] - 0.02 <= t < (ws[c_[-1]]["end"] + 0.35)), None)
        if not ch: return None
        shown = [ws[k]["text"] for k in ch if ws[k]["start"] - 0.02 <= t]
        if self.P.get("cap_swipe"):  # house style: key word gets an orange marker swipe; Mini-H lines in sticky yellow
            ks = [k for k in ch if ws[k]["start"] - 0.02 <= t]
            if not ks: return None
            col = TH["mini"] if ws[ks[0]].get("spk") == "M" else (255, 255, 255); fnt = f"{HERE}/fonts/rubik-800.woff2"; sz = self.P.get("cap_size", 62)
            ims = [text_img(norm_cap(ws[k]["text"]), fnt, sz, col, stroke=7, stroke_fill=(25, 28, 32), shadow=False) for k in ks]
            gap = 14; tw = sum(i.width for i in ims) + gap * (len(ims) - 1); th = max(i.height for i in ims)
            out = Image.new("RGBA", (tw + 30, th + 20), (0, 0, 0, 0)); x = 15
            for k, im in zip(ks, ims):
                if norm(ws[k]["text"]) in self.kw:
                    q = ease((t - ws[k]["start"]) / 0.13); ImageDraw.Draw(out).rounded_rectangle([x - 8, 18, x - 8 + (im.width + 16) * q, th + 4], 10, fill=(*TH["accent"], 255))
                    if q > 0.5: im = text_img(norm_cap(ws[k]["text"]), fnt, sz, TH["kw_text"], stroke=0, shadow=False)
                out.alpha_composite(im, (x, 10)); x += im.width + gap
            return out, self.P.get("cap_y", 0.78), 1.0
        txt = " ".join(shown).lower().replace(".", "").replace(",", "").replace("?", "").replace("!", "")
        if not txt: return None
        key = ("B", txt, ws[ch[0]].get("spk"))
        if key not in self.cap_cache:
            col = tuple(self.P["cap_mini"]) if self.P.get("cap_mini") and ws[ch[0]].get("spk") == "M" else (255, 255, 255)
            self.cap_cache[key] = text_img(txt, f"{HERE}/fonts/rubik-800.woff2", self.P.get("cap_size", 62), col, stroke=self.P.get("cap_stroke", 7), stroke_fill=(25, 28, 32), shadow=False, maxw=W * 0.8)
        return self.cap_cache[key], self.P.get("cap_y", 0.78), 1.0

    def caption(self, t, j):
        if self.P.get("cap_mode") == "none": return None  # long-form: no burned captions (upload SRT instead)
        if any(a <= t < b for a, b in self.hide): return None
        if self.P.get("cap_mode") == "build": return self.caption_build(t, j)
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
                y = next((cy for cy in (0.84, 0.2) if not any(abs(cy * H - my) < r + 110 for my, r in self.mark_y)), 0.84)
            paste_center(c, cap[0], W / 2, H * y, cap[2])
        for ft in self.flashes:
            if 0 <= t - ft < 0.15: c = Image.blend(c, Image.new("RGBA", (W, H), (255, 255, 255, 255)), 0.75 * (1 - (t - ft) / 0.15))
        return c.convert("RGB")

    # ---------- highlight marks: rolling white dashed ring (+ soft green glow) and a pointing arrow ----------
    def draw_mark(self, c, s, j, m, t):
        a = self.tl.at(m["at"], s); b = self.tl.at(m["until"], s) if m.get("until") else s["E"] - 0.05
        if not (a <= t < b) or j not in self.cam: return
        if s.get("poses") is not None:  # pose scene: the canvas is the source; points may come from the pose's landmarks
            size = (W, H); mx, my = (part_xy(m["pose"], m["part"], s.get("place", {})) if m.get("part") else (m["x"], m["y"]))
        else:
            size = load(f"{self.P['dir']}/{s['img']}", s.get("pad", False)).size; mx, my = m["x"], m["y"]
        x0, y0, cw, ch = view_box(size, *self.cam[j])
        X = (mx * size[0] - x0) / cw * W; Y = (my * size[1] - y0) / ch * H; R = m.get("r", 0.12) * size[0] / cw * W
        u = t - a; p = back(u / 0.25, 1.6); fade = min(1, (b - t) / 0.15)
        R *= 0.6 + 0.4 * p; o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
        st = m.get("style", "ring")
        if st == "paint":  # reference style: colour painted ON the muscle (soft ellipse), small label beside it
            k = min(1, u / 0.25) * fade; col = m.get("color", (225, 29, 46))
            if m.get("blink") and u < m["blink"] * 0.2: k = fade if int(u / 0.1) % 2 == 0 else 0  # on 3 f / off 3 f, then stays
            if m.get("pulse"): k *= 0.78 + 0.22 * math.sin(u * 7)
            rx, ry = m.get("rx", 0.08) * size[0] / cw * W, m.get("ry", 0.05) * size[0] / cw * W
            g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([X - rx, Y - ry, X + rx, Y + ry], fill=(*col, int(150 * k)))
            c.alpha_composite(g.filter(ImageFilter.GaussianBlur(max(4, ry * 0.35))))
            if m.get("text") and k > 0.5:
                lab = text_img(m["text"], F_BIG, 78, (255, 255, 255), stroke=6, stroke_fill=(20, 22, 26), shadow=False)
                lx = X + (rx + 40 + lab.width / 2) * (1 if X < W * 0.55 else -1); lx = min(max(lx, lab.width / 2 + 20), W - lab.width / 2 - 20)
                c.alpha_composite(lab, (int(lx - lab.width / 2), int(Y - lab.height / 2)))
            self.mark_y = (self.mark_y or []) + [(Y, ry)]; return
        if st == "disc":  # translucent disc with a lighter dashed rim that rolls (reference forearm circles)
            col = m.get("color", (225, 29, 46)); Rd = R * (1 + 0.04 * math.sin(u * 6)); rot = u * 60
            d.ellipse([X - Rd, Y - Rd, X + Rd, Y + Rd], fill=(*col, int(140 * fade)))
            lc = tuple(min(255, v + 70) for v in col)
            for k_ in range(18):
                a0 = rot + k_ * 20; d.arc([X - Rd, Y - Rd, X + Rd, Y + Rd], a0, a0 + 11, fill=(*lc, int(230 * fade)), width=6)
            c.alpha_composite(o); self.mark_y = (self.mark_y or []) + [(Y, R)]; return
        if st == "spot":  # spotlight: everything else dims
            k = min(1, u / 0.25) * fade; mk = Image.new("L", (W, H), int(150 * k)); ImageDraw.Draw(mk).ellipse([X - R, Y - R, X + R, Y + R], fill=0)
            c.alpha_composite(Image.merge("RGBA", (*[Image.new("L", (W, H), 0)] * 3, mk.filter(ImageFilter.GaussianBlur(18)))))
            d.ellipse([X - R, Y - R, X + R, Y + R], outline=(255, 255, 255, int(230 * fade)), width=6)
            c.alpha_composite(o); self.mark_y = (self.mark_y or []) + [(Y, R)]; return
        if st == "tag":  # label pill with a leader line to the point
            lab = text_img(m["text"], F_BIG, 70, (255, 255, 255), shadow=False); tw_, th_ = lab.width + 30, lab.height
            side = 1 if X < W * 0.55 else -1; bx = X + side * (R + 170); bx = min(max(bx, tw_ / 2 + 30), W - tw_ / 2 - 30); by = Y - R - 60
            e = ease(u / 0.25); al = int(255 * fade)
            d.line([(X, Y), (bx, by)], fill=(225, 29, 46, al), width=8); d.ellipse([X - 14, Y - 14, X + 14, Y + 14], fill=(225, 29, 46, al))
            d.rounded_rectangle([bx - tw_ / 2 * e, by - th_ / 2, bx + tw_ / 2 * e, by + th_ / 2], 18, fill=(225, 29, 46, al))
            if e > 0.9: o.alpha_composite(lab, (int(bx - lab.width / 2), int(by - lab.height / 2)))
            c.alpha_composite(o); self.mark_y = (self.mark_y or []) + [(by, th_)]; return
        if st == "pain":  # red spinning dashed circle with a heartbeat pulse
            Rp = R * (1 + 0.06 * math.sin(u * 12)); rot = u * 200
            for k_ in range(14):
                a0 = rot + k_ * 360 / 14; d.arc([X - Rp, Y - Rp, X + Rp, Y + Rp], a0, a0 + 15, fill=(225, 29, 46, int(255 * fade)), width=14)
            c.alpha_composite(o); self.mark_y = (self.mark_y or []) + [(Y, R)]; return
        if m.get("glow", False):
            g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([X - R, Y - R, X + R, Y + R], fill=(34, 197, 94, int(70 * fade)))
            o.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.25)))
        rot = u * 120; n = 16 if st == "ring" else 0
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
            fg = (225, 29, 46, al) if st == "arrow" else (255, 255, 255, al)
            for col, wd, grow in (((0, 0, 0, int(al * 0.6)), 30, 6), (fg, 18, 0)):
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
        fl.append(f"[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={dur},asplit=2[v][vsc]")
        fl.append(f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},volume={music_gain:.4f},afade=t=in:d=0.3,afade=t=out:st={dur - 1.2}:d=1.2[mr]")
        duck = P.get("duck", True)  # music dips ~4-6 dB while H speaks and swells back in the pauses (competitor-style bed)
        fl.append("[mr][vsc]sidechaincompress=threshold=0.04:ratio=4:attack=30:release=350[m]" if duck else "[mr]anull[m]")
        if not duck: fl.append("[vsc]anullsink")
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
        if getattr(self, "qa", None): json.dump(self.qa, open(out + ".labels.json", "w"), indent=0)  # where every label went (QA)

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
