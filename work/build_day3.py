# Day 3: dead hang 60 s test, no-clip format (H poses only), copied from build_day2b.py.
import json
INK = "#16191D"; SUB = "#5A4A36"; RED = "#EF4444"; GREEN = "#22C55E"; YEL = "#FACC15"; BG = "#E2D3B9"  # sand beige (owner pick 3, 26 Oct), lighter spotlight in the middle
BODY = {"width": 0.8, "y": 0.62}
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
    elif id.startswith("c_"): d["background"] = "#FFFFFF"  # exercise clips keep their own white
    else: d.update(backdrop="spotlight", backdropColor="#FFF6E8", backdropOpacity=1)
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


CLIPW = {"width": 1.0, "y": 0.58}


def poses(frames, enter="cut", **kw):
    # frames = [(asset, anchor)]; clean cuts between drawings make the move
    return {"type": "poses", "frames": [{"asset": a, "at": t} for a, t in frames], "at": frames[0][1], "enter": enter,
            "shadow": True, **{**BODY, **kw}}


def loop(a, b, at, n, step=0.4):
    # a/b swap every `step` s starting at `at` (one rep = down + up)
    return [((a, b)[k % 2], at if k == 0 else f"{at}+{round(k * step, 2)}") for k in range(n)]


def card(t, at, until, color=INK, size=150, y=0.45):
    # full-screen statement / move card, typed word by word like the old viral videos
    d = text(t, at, until, y, size, color, "cut"); d["animation"] = "words"; d["maxWidth"] = 0.86
    return d


def label(t, at, frm, x, y, until=None):
    # red muscle name + arrow to the muscle
    d = [{"type": "callout", "text": t, "to": list(frm), "x": x, "y": y, "size": 100, "color": RED, "look": "tag", "at": at}]
    if until: d[0]["until"] = until
    return d


HANG = {"autoAlign": False, "width": 0.66, "y": 0.64}  # Day-1 hang size: bar stays under the heading/sub

plan = {
    "title": "Can You Hold a Dead Hang for 60 Seconds?",
    "canvas": {"background": BG},
    "style": {"accent": YEL},
    "captions": {"mode": "phrase", "look": "clean", "size": 58, "y": 0.82, "maxWords": 3,
                 "keywords": ["sixty", "thirty", "grip", "forearms", "slip", "five", "strong", "time"],
                 "hide": [["Here's the fix-0.05", "One: dead"]]},
    "scenes": [
        sc("hook", "start", [
            img("hero_look_up_bar", "start", "drop before", enter="cut", **HANG),
            {**title("60 SEC DEAD HANG?", "start", "drop before", size=125), "animation": "none"},
            pain(0.26, 0.6, "start", "drop before", 0.22),
            img("hero_drop_from_bar", "drop before", enter="cut", **HANG),
            {**title("MOST DROP AT 30", "drop before", size=125), "color": RED},
        ], camera=punch("drop before", (0.5, 0.5), 1.12)),
        sc("why", "not your arms-0.05", [
            img("hero_stand", "not your arms", enter="cut", id="h", **LEFT),
            title("NOT YOUR ARMS", "not your arms", "your grip"),
            title("IT'S YOUR GRIP", "your grip", "forearms get tired"),
            bubble("anat_muscle_forearm_grip", "your grip", "forearms get tired", None, x=0.77, y=0.62, size=0.34),
        ]),
        sc("gag", "Your forearms get-0.05", [
            img("gag_dead_on_floor", "Your forearms get", enter="cut", width=0.66, x=0.5, y=0.6, autoPlace=False),
            title("TIRED FOREARMS", "Your forearms get", "slip off"),
            title("= HANDS SLIP OFF", "slip off"),
        ]),
        sc("fix", "Here's the fix-0.05", [
            text("HERE'S THE FIX", "Here's the fix-0.05", None, 0.47, 170, "#FFFFFF", "cut"),
        ], camera=[{"at": "Here's the fix-0.05", "zoom": 1}, {"at": "fix.+0.05", "zoom": 1}, {"at": "fix.+0.2", "zoom": 1.18}]),
        sc("m1", "One: dead-0.05", [
            poses([("hero_look_up_bar", "One: dead"), ("hero_pullup_hang_v2", "Hang as")], **HANG),
            title("#1 DEAD HANG", "One: dead"), sub("MAX TIME x3", "as long as"),
        ]),
        sc("m2", "Two: add-0.05", [
            poses([("hero_pullup_hang", "Two: add")], **HANG),
            title("#2 +5 SEC EVERY DAY", "Two: add", size=120),
            {"type": "counter", "from": 30, "to": 60, "suffix": " SEC", "duration": 1.2, "x": 0.5, "y": 0.215,
             "size": 90, "color": RED, "at": "Thirty becomes"},
        ]),
        sc("after", "Do this and-0.05", [
            img("hero_stand", "Do this and", "crazy strong", enter="cut", **BODY),
            title("DO IT DAILY", "Do this and", "crazy strong"),
            img("gag_sunglasses_thumbs", "crazy strong", enter="cut", width=0.62, x=0.5, y=0.6, autoPlace=False),
            title("GRIP: LOCKED", "crazy strong"),
        ]),
        sc("cta", "Comment your-0.05", [
            img("hero_point_viewer", "Comment your", enter="cut", id="h", **BODY),
            title("COMMENT YOUR TIME", "Comment your", size=125),
            {"type": "comment", "text": "42 sec \U0001F605", "user": "you", "ago": "now", "likes": "2.1K",
             "x": 0.5, "y": 0.3, "width": 0.7, "size": 50, "at": "Comment your+0.3", "enter": "pop"},
        ], camera=[{"at": "Comment your", "zoom": 1}, {"at": "time below", "zoom": 1.2, "focus": "face"}]),
    ],
    "sfx": [dict(zip(("at", "src", "volume"), e)) for e in [
        ("start", "sfx_whoosh_soft"), ("drop before", "sfx_pop_soft"),
        ("not your arms", "sfx_whoosh_soft"), ("your grip", "sfx_ding"),
        ("Your forearms get", "sfx_whoosh_soft"), ("slip off", "sfx_pop_soft"),
        ("Here's the fix-0.05", "sfx_typing_loud", 1.0), ("fix.+0.15", "sfx_whoosh_big"),
        ("One: dead", "sfx_whoosh_soft"), ("as long as", "sfx_click_soft"),
        ("Two: add", "sfx_whoosh_soft"), ("Thirty becomes", "sfx_counter"),
        ("Do this and", "sfx_whoosh_soft"), ("crazy strong", "sfx_ding"),
        ("Comment your", "sfx_whoosh_soft"), ("Comment your+0.3", "sfx_notification")]],
}
json.dump(plan, open("day3.json", "w"), indent=1, ensure_ascii=False)
