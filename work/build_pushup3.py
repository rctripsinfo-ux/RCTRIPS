# "Stop These 3 Push-Up Mistakes" (owner, 29 Oct): old-viral look on WHITE (owner-approved suggestions): dashed guide
# lines (red = wrong, green = right), muscle label with a dashed arrow, faded H behind, side-by-side result, 2-pose rep
# flip-book; style-D cards and viral captions unchanged; 1.3x voice, short holds; calm, one idea at a time, simple words.
import json
INK = "#16191D"; SUB = "#5A4A36"; RED = "#EF4444"; GREEN = "#22C55E"; YEL = "#FACC15"; BG = "#FFFFFF"  # sand beige (owner pick 3, 26 Oct), lighter spotlight in the middle
BODY = {"width": 0.66, "y": 0.69}  # head stays below the caption line (0.32)
LEFT = {"width": 0.7, "y": 0.6, "x": 0.36}  # H moves left when an anatomy circle opens on the right
CLIP = {"width": 0.95, "y": 0.58}


def img(a, at, until=None, enter="pop", **kw):
    d = {"type": "image", "asset": a, "shadow": a.startswith("hero_"), "enter": enter, "at": at, **kw}
    if until: d["until"] = until
    return d


def text(t, at, until, y, size, color, enter="fade"):
    d = {"type": "text", "text": t, "x": 0.5, "y": y, "size": size, "align": "center", "color": color, "font": "pop",
         "maxWidth": 0.9, "animation": "typewriter", "untype": False, "enter": enter, "exit": "cut",
         "stroke": {"color": "#FFFFFF", "width": 0}, "at": at}
    if until: d["until"] = until
    return d


def title(t, at, until=None, size=140): return text(t, at, until, 0.15, size, INK, "pop")
def sub(t, at, until=None): return text(t, at, until, 0.215, 62, SUB)


def glow(anchor, at, color, target, until=None):
    d = {"type": "glow", "anchor": anchor, "color": color, "at": at, "target": target}
    if until: d["until"] = until
    return d


def icon(name, at, until=None, label=None, x=0.86, y=0.5, color=None, size=0.14):
    d = {"type": "icon", "name": name, "at": at, "x": x, "y": y, "size": size, "enter": "pop"}
    if label: d["label"] = label
    if color: d["color"] = color
    if until: d["until"] = until
    return d


def chip(t, at, until=None, icon_name=None, x=0.5, y=0.33, color=RED):
    d = {"type": "chip", "text": t, "at": at, "x": x, "y": y, "color": color, "enter": "pop"}
    if icon_name: d["icon"] = icon_name
    if until: d["until"] = until
    return d


def ring(x, y, at, until=None, w=0.2):
    # Captain-style red ring on the problem area
    d = {"type": "highlight", "shape": "circle", "x": x, "y": y, "w": w, "h": w * 0.5625, "color": RED, "at": at}
    if until: d["until"] = until
    return d


def punch(at, focus=(0.5, 0.55), zoom=1.12):
    return [{"at": at, "zoom": 1}, {"at": f"{at}+0.3", "zoom": zoom, "focus": list(focus) if isinstance(focus, tuple) else focus}]


def sc(id, start, layers, camera=None):
    d = {"id": id, "start": start, "backdrop": "none", "layers": layers}
    base = start[:-5] if start.endswith("-0.05") else start
    if camera: d["camera"] = camera
    elif not id.startswith("c_"): d["camera"] = [{"at": base, "zoom": 1}, {"at": f"{base}+3", "zoom": 1.07}]  # clips stay unzoomed (titles)
    if id == "fix": d["background"] = "#1E2228"
    else: d["background"] = "#FFFFFF"  # old viral look: plain white everywhere
    return d


def bubble(asset, at, until=None, frm=None, x=0.75, y=0.4, size=0.4):
    d = {"type": "zoomBubble", "asset": asset, "zoom": 1, "x": x, "y": y, "size": size, "at": at, "enter": "pop",
         "borderColor": "#FFFFFF"}
    if frm: d["from"] = list(frm)
    if until: d["until"] = until
    return d


def pain(x, y, at, until=None, w=0.34, color=RED):
    d = {"type": "highlight", "shape": "pain", "x": x, "y": y, "w": w, "color": color, "at": at, "enter": "cut"}
    if until: d["until"] = until
    return d


CLIPW = {"width": 1.0, "y": 0.62}  # lower so heads stay clear of the headings


def clip(a, at, rate=1.4):
    return {"type": "video", "asset": a, "at": at, "enter": "cut", "rate": rate, **CLIPW}


def card(t, at, until, color=INK, size=150, y=0.45):
    # full-screen statement / move card, typed word by word like the old viral videos
    d = text(t, at, until, y, size, color, "cut"); d["animation"] = "words"; d["maxWidth"] = 0.86
    return d


def label(t, at, frm, x, y, until=None):
    # red muscle name + arrow to the muscle
    d = [{"type": "callout", "text": t, "to": list(frm), "x": x, "y": y, "size": 100, "color": RED, "look": "tag", "at": at}]
    if until: d[0]["until"] = until
    return d


import re


def ref(start, delta):
    # "phrase+0.25" + 3 -> "phrase+3.25" (the tool takes one offset per anchor)
    m = re.match(r"^(.*?)([+-]\d+(?:\.\d+)?)?$", start)
    off = float(m.group(2) or 0) + delta
    return f"{m.group(1)}{off:+.2f}" if off else m.group(1)


def dline(t, sync, until, color, size, y, at=None):
    # style D card line: big Bebas, typed while `sync` is spoken (fast_render sets the exact time)
    d = text(t, at or sync, until, y, min(size, 400), color, "cut"); d.update(sync=sync, maxWidth=0.98, font="pop")
    return d


CARDS = {c["id"]: c for c in json.load(open("pushup3.cards.json"))}


def dcard(cid, syncs, until, at):
    # exact style-D card (transparent PNG frames over the scene colour), timed by fast_render.py
    steps = [len(l["text"]) for l in CARDS[cid]["lines"]]
    d = {"type": "poses", "frames": [{"asset": f"card_{cid}_01", "at": at}], "sync": syncs, "steps": steps, "card": cid,
         "x": 0.5, "y": 0.5, "width": 1.0, "autoAlign": False, "life": False, "shadow": False, "autoPlace": False,
         "enter": "cut", "at": at}
    if until: d["until"] = until
    return d


def drift(start, z=1.1, f0=(0.48, 0.48), f1=(0.53, 0.56), dur=4):
    # the camera keeps moving through the whole scene (no frozen frame)
    return [{"at": start, "zoom": 1, "focus": list(f0)}, {"at": ref(start, dur), "zoom": z, "focus": list(f1)}]


def flip(assets, start, n=8, step=0.45, **kw):
    # flip-book: swap gesture drawings so H keeps moving
    fr = [{"asset": assets[i % len(assets)], "at": ref(start, round(i * step, 2)) if i else start} for i in range(n)]
    return {"type": "poses", "frames": fr, "at": start, "enter": "pop", "shadow": True, **kw}


def scene(id, start, layers, camera=None, transition=None, shakes=None):
    d = sc(id, start, layers, camera)
    if transition: d["transition"] = {"type": transition, "duration": 0.3}
    if shakes: d["shakes"] = [{"at": a, "duration": 0.3, "intensity": 9} for a in shakes]
    return d


GREEN = "#16A34A"
POSE = {"width": 0.95, "x": 0.5, "y": 0.55, "autoPlace": False, "life": False}  # side push-up drawings (coordinates measured)


def dash(a, b, at, until=None, color=RED, bend=0, arrow=False, th=10):
    d = {"type": "dash", "from": list(a), "to": list(b), "at": at, "color": color, "bend": bend, "arrow": arrow, "thickness": th}
    if until: d["until"] = until
    return d


def label(t, at, x, y, color=RED, size=78, until=None):
    d = text(t, at, until, y, size, color, "fade"); d.update(x=x, animation="none")
    return d


plan = {
    "title": "Stop These 3 Push-Up Mistakes",
    "font": "sport",
    "canvas": {"background": BG},
    "style": {"accent": YEL},
    "captions": {"mode": "word", "look": "viral", "size": 104, "y": 0.75,  # like the old videos: one word low on the body (legs), never near the face or headings
                 "keywords": ["three", "straight", "wide", "shoulders", "half", "floor", "ten", "fifty", "PUSH"],
                 "hide": [["Here's the fix-0.05", "One: your-0.05"], ["One: your-0.05", "Keep your body-0.05"],
                          ["Two: your-0.05", "Put them right-0.05"], ["Three: you-0.05", "Bring your chest-0.05"],
                          ["Comment PUSH+0.3", "mistake.+1"],
                          ["Ten good-0.05", "Comment PUSH-0.05"]]},  # result: the two labels speak for themselves  # the comment bubble takes that spot
    "scenes": [
        # problem
        sc("hook", "start", [
            {"type": "image", "asset": "hero_facepalm", "at": "start", "until": "these three", "width": 1.25, "x": 0.5, "y": 0.6,
             "opacity": 0.12, "behind": True, "autoPlace": False, "life": False, "enter": "cut"},          # faded H behind
            img("hero_tired_sweating", "start", "these three", enter="cut", **BODY),
            {**title("PUSH-UPS NOT WORKING?", "start", "these three", size=115), "animation": "none"},
            img("hero_count_3", "these three", enter="up", **BODY),
            title("3 MISTAKES", "these three"),
        ], camera=drift("start", 1.06, (0.5, 0.5), (0.5, 0.52), 5)),
        sc("fix", "Here's the fix-0.05", [dcard("fix", ["Here's the", "fix"], None, "Here's the fix")]),
        # 1: hips
        sc("m1", "One: your-0.05", [
            dcard("pm1", ["One: your", "hips drop"], "Keep your body-0.05", "One: your"),
            img("hero_pushup_top", "Keep your body-0.05", enter="fade", **POSE),
            title("BODY STRAIGHT", "Keep your body-0.05"),
            {**title("LIKE A PLANK OF WOOD", "plank of wood", None, 90), "y": 0.23, "color": GREEN},
            dash((0.05, 0.585), (0.72, 0.452), "Keep your body", color=GREEN, th=12),
            label("CORE TIGHT", "plank of wood", 0.24, 0.79, RED, 100),
            dash((0.3, 0.745), (0.47, 0.56), "plank of wood", color=RED, bend=-0.4, arrow=True, th=8),
        ]),
        # 2: hands
        sc("m2", "Two: your-0.05", [
            dcard("pm2", ["Two: your", "hands are too wide"], "Put them right-0.05", "Two: your"),
            {**clip("clip_archer_pushup", "Put them right-0.05", 0.3), "y": 0.62},
            title("HANDS UNDER SHOULDERS", "Put them right-0.05", None, 105),
            dash((0.31, 0.6), (0.31, 0.9), "under your shoulders", color=GREEN, th=12),
            dash((0.69, 0.6), (0.69, 0.9), "under your shoulders", color=GREEN, th=12),
        ]),
        # 3: depth (2-pose rep flip-book)
        sc("m3", "Three: you-0.05", [
            dcard("pm3", ["Three: you", "only go half way"], "Bring your chest-0.05", "Three: you"),
            flip(["hero_pushup_top", "hero_pushup_mid"], "Bring your chest-0.05", 8, 0.55, **POSE),
            title("CHEST TO THE FLOOR", "Bring your chest-0.05", None, 115),
            dash((0.86, 0.47), (0.86, 0.66), "close to the", color=GREEN, arrow=True, th=12),
            label("ALL THE WAY", "close to the", 0.62, 0.74, GREEN, 70),
        ]),
        # plan
        sc("c_plan", "Do three sets-0.05", [
            {**clip("clip_wide_pushup", "Do three sets-0.05", 1.2), "y": 0.5},  # higher so the word sits on the body, not the head
            title("3 SETS x 10 REPS", "Do three sets-0.05"),
            {**title("EVERY OTHER DAY", "every other day", None, 90), "y": 0.23, "color": RED},
        ]),
        # result: side by side
        sc("after", "Ten good-0.05", [
            title("10 GOOD > 50 BAD", "Ten good-0.05"),
            img("hero_pushup_top", "Ten good-0.05", None, enter="left", width=0.5, x=0.27, y=0.55, autoPlace=False, life=False),
            label("10 GOOD", "Ten good", 0.27, 0.66, GREEN, 80),
            img("hero_tired_sweating", "fifty bad", None, enter="right", width=0.36, x=0.76, y=0.55, autoPlace=False),
            label("50 BAD", "fifty bad", 0.76, 0.85, RED, 80),
        ]),
        sc("cta", "Comment PUSH-0.05", [
            flip(["hero_point_viewer", "hero_come_on", "hero_point_viewer", "hero_come_on_v2"], "Comment PUSH-0.05", 8, 0.45, **BODY),
            title('COMMENT "PUSH"', "Comment PUSH"),
            {"type": "comment", "text": "PUSH \U0001F4AA", "user": "you", "ago": "now", "likes": "2.1K",
             "x": 0.5, "y": 0.3, "width": 0.7, "size": 50, "at": "Comment PUSH+0.3", "enter": "pop"},
        ]),
    ],
    "sfx": [dict(zip(("at", "src", "volume"), e)) for e in [
        ("start", "sfx_whoosh_soft"), ("these three", "sfx_whoosh_soft"),
        ("Keep your body", "sfx_pop_soft"), ("plank of wood", "sfx_pop_soft"),
        ("Put them right", "sfx_pop_soft"), ("under your shoulders", "sfx_pop_soft"),
        ("Bring your chest", "sfx_whoosh_soft"), ("close to the", "sfx_pop_soft"),
        ("Do three sets", "sfx_whoosh_soft"), ("Ten good", "sfx_whoosh_soft"), ("fifty bad", "sfx_whoosh_soft"),
        ("Comment PUSH-0.05", "sfx_whoosh_soft"), ("Comment PUSH+0.3", "sfx_notification")]],
}
json.dump(plan, open("pushup3.json", "w"), indent=1, ensure_ascii=False)
