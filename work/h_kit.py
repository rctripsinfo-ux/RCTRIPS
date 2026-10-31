# Reusable kit for Effortless Exercise Shorts (from REFERENCE-ANALYSIS.md, 31 Oct 2026).
# Import it in a build file: `from h_kit import *`. Older build files keep their own copies and still work.
# Contents: style presets, layer helpers (same as build_day2b.py), hook entrances, attitude poses, form guides,
# SFX cue categories, a static plan validator and a QA frame sheet.
import json, os, re, subprocess

INK = "#16191D"; SUB = "#5A4A36"; RED = "#EF4444"; YEL = "#FACC15"; WHITE = "#FFFFFF"
LIB = os.path.expanduser("~/reel-engine-tool/public/library")

# ---------- 1. style presets (keep them separate; pick one per video) ----------
PRESETS = {
    # approved template (Day 1/2): sand beige + spotlight, headings y 0.15, small captions y 0.82
    "beige": {"bg": "#E2D3B9", "spot": True, "title_y": 0.15, "sub_y": 0.215, "cap_y": 0.82,
              "safe": {"top": 0.08, "bottom": 0.90, "side": 0.05}},
    # test preset (owner brief, 31 Oct): pure white, top 18 % and bottom 12 % empty, 5 % sides, 1080x1920
    "white_safe": {"bg": "#FFFFFF", "spot": False, "title_y": 0.215, "sub_y": 0.27, "cap_y": 0.845,
                   "safe": {"top": 0.18, "bottom": 0.88, "side": 0.05}},
}
P = PRESETS["beige"]


def use_preset(name):
    global P
    P = PRESETS[name]
    return P


BODY = {"width": 0.8, "y": 0.62}
LEFT = {"width": 0.7, "y": 0.6, "x": 0.36}       # H moves left when a bubble opens on the right
HANG = {"autoAlign": False, "width": 0.66, "y": 0.64}  # bar / hang images: bar stays under the heading
GAG = {"width": 0.62, "x": 0.5, "y": 0.6, "autoPlace": False}

# ---------- 2. layer helpers ----------
def img(a, at, until=None, enter="pop", **kw):
    d = {"type": "image", "asset": a, "shadow": a.startswith("hero_"), "enter": enter, "at": at, **kw}
    if until: d["until"] = until
    return d


def text(t, at, until, y, size, color, enter="fade"):
    d = {"type": "text", "text": t, "x": 0.5, "y": y, "size": size, "align": "center", "color": color, "font": "pop",
         "maxWidth": 0.9, "animation": "typewriter", "untype": False, "enter": enter, "exit": "cut",
         "stroke": {"color": WHITE, "width": 0}, "at": at}
    if until: d["until"] = until
    return d


def title(t, at, until=None, size=140, color=INK, typed=True):
    d = text(t, at, until, P["title_y"], size, color, "pop")
    if not typed: d["animation"] = "none"  # hook heading: shown in full from frame 1
    return d


def sub(t, at, until=None): return text(t, at, until, P["sub_y"], 62, SUB)


def sc(id, start, layers, camera=None, drift=True):
    """Scene. drift=True keeps the approved slow push-in (1.0 -> 1.07); give camera=[...] to override."""
    d = {"id": id, "start": start, "backdrop": "none", "layers": layers}
    base = start[:-5] if start.endswith("-0.05") else start
    if camera: d["camera"] = camera
    elif drift: d["camera"] = [{"at": base, "zoom": 1}, {"at": f"{base}+3", "zoom": 1.07}]
    if id == "fix": d["background"] = "#1E2228"
    elif P["spot"]: d.update(backdrop="spotlight", backdropColor="#FFF6E8", backdropOpacity=1)
    return d


def bubble(asset, at, until=None, x=0.77, y=0.62, size=0.34):
    # anatomy circle: lower half beside the legs, never near the face (owner rule)
    d = {"type": "zoomBubble", "asset": asset, "zoom": 1, "x": x, "y": y, "size": size, "at": at, "enter": "pop",
         "borderColor": WHITE}
    if until: d["until"] = until
    return d


def pain(at, until=None, anchor=None, x=0.5, y=0.55, w=0.3, target=None):
    """Spinning dashed red pain circle. Prefer anchor="forearms"/"knees"/... (library landmarks) over x/y."""
    d = {"type": "highlight", "shape": "pain", "w": w, "color": RED, "at": at, "enter": "cut"}
    d.update({"anchor": anchor} if anchor else {"x": x, "y": y})
    if target: d["target"] = target
    if until: d["until"] = until
    return d


def poses(frames, enter="cut", **kw):
    return {"type": "poses", "frames": [{"asset": a, "at": t} for a, t in frames], "at": frames[0][1], "enter": enter,
            "shadow": True, **{**BODY, **kw}}


def loop(a, b, at, n, step=0.4):
    """Rep loop: a/b swap every `step` s (0.4 normal, 0.6 slow). a and b must be the SAME camera view."""
    return [((a, b)[k % 2], at if k == 0 else f"{at}+{round(k * step, 2)}") for k in range(n)]


def counter(frm, to, at, suffix="", y=None, size=90, dur=1.0):
    return {"type": "counter", "from": frm, "to": to, "suffix": suffix, "duration": dur, "x": 0.5,
            "y": y if y is not None else P["sub_y"], "size": size, "color": RED, "at": at}


def comment(t, at, likes="2.1K"):
    return {"type": "comment", "text": t, "user": "you", "ago": "now", "likes": likes,
            "x": 0.5, "y": 0.3, "width": 0.7, "size": 50, "at": at, "enter": "pop"}


def punch(at, focus=(0.5, 0.55), zoom=1.12):
    return [{"at": at, "zoom": 1}, {"at": f"{at}+0.3", "zoom": zoom, "focus": list(focus) if isinstance(focus, tuple) else focus}]


# ---------- 3. hook entrances (first meaningful motion at 0.0-0.2 s; the heading itself never moves) ----------
ENTER = {
    "rise": {"type": "flyUp", "duration": 0.35},    # H rises in from the bottom edge (refs V07, V10)
    "jump": {"type": "up", "duration": 0.25},       # short hop up: grabbing a bar, jumping
    "fall": {"type": "flyDown", "duration": 0.3},   # drops in from above: falling off, landing
    "slide": {"type": "flyLeft", "duration": 0.3},  # slides in from the side (ref V09)
    "whip": {"type": "whip", "duration": 0.35},     # fast slide with ghost copies
}


def zoom_out(at="start", focus="face", z=1.6, dur=0.35):
    """Close-up -> wide reveal (refs V02-V06, V09). Zooms the whole scene, so use it only when the frame-1
    heading may scale too (white_safe preset, or a scene without a heading). Focus a body part, never 'face' for pain."""
    return [{"at": at, "zoom": z, "focus": focus}, {"at": f"{at}+{dur}", "zoom": 1}]


# ---------- 4. attitude poses: one per narration beat, chosen by meaning (all exist in the hero library) ----------
ATT = {
    "stop": "hero_stop_palm",        # "It's not...", "Stop...", "No..."
    "no": "hero_arms_crossed",       # myth / wrong / refusal
    "rule": "hero_count_1",          # one finger up = a rule / tip
    "think": "hero_thinking",        # "Most people think..."
    "point_r": "hero_point_right",   # points to the viewer's right: pair with a bubble at x 0.77
    "point_l": "hero_point_left",
    "you": "hero_point_viewer",      # "you", questions, CTA
    "sad": "hero_sad_crying",        # the pain point
    "shock": "hero_shocked",
    "win": "hero_double_biceps",     # result
    "ok": "hero_thumbs_up",
    "teach": "hero_teacher_pointer",
}


def count(n): return f"hero_count_{n}"  # 1-5: "One:", "Two:", "only 3 moves"


# same-view groups: never loop frames from different groups (owner rule 31 Oct)
VIEW = {"hero_pullup_hang": "side", "hero_pullup_top": "side", "hero_pullup_hang_v2": "front", "hero_look_up_bar": "front"}

# ---------- 5. form guides (exercise readability, ref V06); all kept off the face ----------
def guide(frm, to, at, until=None, color=WHITE, arrow=False, bend=0):
    """Dashed alignment line between canvas points (body line, hand width, depth)."""
    d = {"type": "dash", "from": list(frm), "to": list(to), "at": at, "color": color, "thickness": 8, "dash": 22,
         "arrow": arrow, "bend": bend}
    if until: d["until"] = until
    return d


def joint(anchor, at, until=None, w=0.07, target=None):
    """Small red ring on a joint that moves wrong (sagging hips, caving knees). Not on head/neck anchors."""
    assert anchor not in ("head", "face", "nose", "neck"), "joint marker on the face is not allowed"
    d = {"type": "highlight", "shape": "circle", "anchor": anchor, "w": w, "color": RED, "at": at}
    if target: d["target"] = target
    if until: d["until"] = until
    return d


def move(anchor, pointing, at, until=None, color=WHITE, target=None):
    """Arrow beside a body part showing which way it moves / where it points."""
    d = {"type": "arrow", "anchor": anchor, "pointing": pointing, "color": color, "thickness": 14, "glow": False, "at": at}
    if target: d["target"] = target
    if until: d["until"] = until
    return d


# ---------- 6. SFX cue categories -> licensed assets already in the library ----------
CUE = {
    "enter": ("sfx_whoosh_soft", 0.35),     # H / scene entrance
    "big": ("sfx_whoosh_big", 0.35),        # bumper punch-in
    "bumper": ("sfx_typing_loud", 1.0),     # HERE'S THE FIX (brand stamp, keep identical)
    "info": ("sfx_pop_soft", 0.35),         # heading / bubble / label appears
    "tick": ("sfx_click_soft", 0.35),       # sub line, small info
    "reveal": ("sfx_ding", 0.35),           # good tip / result (max 2 per video)
    "count": ("sfx_counter", 0.35),         # number counting up
    "cta": ("sfx_notification", 0.35),     # comment bubble
    "drop": ("sfx_swoosh_up", 0.3),         # fast vertical move (fall / jump)
}


def cues(pairs):
    """pairs = [(anchor, category)] -> plan sfx list. Rule: max one cue per ~1.5 s, none per rep."""
    return [{"at": a, "src": CUE[k][0], "volume": CUE[k][1]} for a, k in pairs]


# ---------- 7. static validation (cheap, before any render) ----------
def _norm(s): return re.sub(r"[^a-z0-9' ]", " ", s.lower())


def validate(plan, script):
    errs, warn = [], []
    have = {f.rsplit(".", 1)[0] for f in os.listdir(f"{LIB}/hero")} | {"sfx_" + f.rsplit(".", 1)[0] for f in os.listdir(f"{LIB}/sfx")}
    words = " ".join(_norm(script).split())
    S = P["safe"]

    def anchor_ok(a):
        p = re.sub(r"[+-][0-9.]+$", "", a); p = re.sub(r"#\d+", "", p)
        if p in ("start", "end"): return True
        q = " ".join(_norm(p).split())
        n = len(re.findall(rf"(?<![a-z0-9']){re.escape(q)}(?![a-z0-9'])", words))
        if n > 1 and "#" not in a: errs.append(f"anchor spoken {n} times, use a longer phrase or #2: {a!r}")
        return n > 0

    def chk(L, where):
        for a in [L.get("at"), L.get("until")] + [f["at"] for f in L.get("frames", [])]:
            if isinstance(a, str) and not anchor_ok(a): errs.append(f"{where}: anchor not in script: {a!r}")
        for k in ("asset",):
            if k in L and L[k] not in have: errs.append(f"{where}: missing asset {L[k]}")
        for f in L.get("frames", []):
            if f["asset"] not in have: errs.append(f"{where}: missing asset {f['asset']}")
        vs = {VIEW[f["asset"]] for f in L.get("frames", []) if f["asset"] in VIEW}
        if len(vs) > 1 and len(L.get("frames", [])) > 2: warn.append(f"{where}: loop mixes views {vs}")
        if L.get("type") in ("text", "counter"):
            y = L.get("y", 0.5)
            if not (S["top"] <= y <= S["bottom"]): errs.append(f"{where}: text y {y} outside safe area {S}")
        if L.get("type") == "highlight" and L.get("anchor") in ("head", "face", "nose"):
            errs.append(f"{where}: marker on the face")

    for s in plan["scenes"]:
        if not anchor_ok(s["start"]): errs.append(f"scene {s['id']}: start anchor not in script: {s['start']!r}")
        for i, L in enumerate(s["layers"]): chk(L, f"{s['id']}[{i}]")
    for e in plan.get("sfx", []):
        if e["src"] not in have: errs.append(f"sfx missing: {e['src']}")
        if not anchor_ok(e["at"]): errs.append(f"sfx anchor not in script: {e['at']!r}")
    for w in warn: print("WARN", w)
    if errs:
        raise SystemExit("PLAN INVALID:\n" + "\n".join(errs))
    print(f"plan OK: {len(plan['scenes'])} scenes, {sum(len(s['layers']) for s in plan['scenes'])} layers, {len(plan.get('sfx', []))} cues")


# ---------- 8. QA frame sheet of chosen moments (after the render) ----------
def qa_sheet(mp4, times, out):
    """One labelled tile of frames at `times` (seconds) to check overlaps, face, markers, loops, ending."""
    ins, fl = [], []
    for i, t in enumerate(times):
        ins += ["-ss", str(t), "-i", mp4]
        fl.append(f"[{i}:v]trim=end_frame=1,scale=270:-2,drawtext=text='{t}s':x=6:y=6:fontsize=22:fontcolor=red:box=1[v{i}]")
    n = len(times); cols = min(n, 6)
    fl.append("".join(f"[v{i}]" for i in range(n)) + f"xstack=inputs={n}:layout=" +
              "|".join(f"{'+'.join(['w0'] * (i % cols)) or '0'}_{'+'.join(['h0'] * (i // cols)) or '0'}" for i in range(n)) +
              ":fill=black")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-frames:v", "1", out], check=True)
    return out


# ---------- 9. exact body point on the canvas from the library landmarks (anatomy-true markers) ----------
def body_xy(asset, part, width, y, x=0.5):
    """Canvas (x, y) of a body part of an image placed with autoAlign=False at width/x/y (centre).
    part: a landmark ('wrist_l', 'elbow_r', 'hip_l', ...) or a segment mid 'forearm_l'/'forearm_r'/'upper_arm_l'/'shin_r'.
    Two-sided anchors like "forearms" resolve between the arms (on the chest), so use this for one side."""
    A = {a["id"]: a for a in json.load(open(f"{LIB}/hero/library.json"))["assets"]}[asset]
    p = A["points"]; s = part[-1]
    seg = {"forearm": ("elbow", "wrist"), "upper_arm": ("shoulder", "elbow"), "thigh": ("hip", "knee"), "shin": ("knee", "ankle")}
    k = part[:-2]
    if part == "chest":  # a third of the way from the shoulders to the hips
        sx, sy = (p["shoulder_l"][0] + p["shoulder_r"][0]) / 2, (p["shoulder_l"][1] + p["shoulder_r"][1]) / 2
        hx, hy = (p["hip_l"][0] + p["hip_r"][0]) / 2, (p["hip_l"][1] + p["hip_r"][1]) / 2
        px, py = sx + (hx - sx) / 3, sy + (hy - sy) / 3
    elif k in seg:
        a, b = p[f"{seg[k][0]}_{s}"], p[f"{seg[k][1]}_{s}"]; px, py = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    if part != "chest" and k not in seg:
        px, py = p[part]
    iw, ih = A["size"]
    h = width * 1080 * ih / iw / 1920  # image height as a share of the canvas height
    return round(x - width / 2 + px * width, 3), round(y - h / 2 + py * h, 3)
