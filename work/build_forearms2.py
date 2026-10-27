# Forearms V2 (owner, 28 Oct): approved template + everything from the old viral videos (OLD-VIRAL-ANALYSIS.md):
# 2 bumpers (black "what's really going on" + dark "fix"), move cards centred first then on top, one big word
# caption at a time, a test with a timer, muscle label + arrow, small->big progress, a picture on most lines,
# a value fact, 2 jokes. Voice 1.3x without silences, thumbnail as the first 0.1 s.
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


plan = {
    "title": "Weak Forearms? Do These 2 Moves",
    "canvas": {"background": BG},
    "style": {"accent": YEL},
    "captions": {"mode": "phrase", "look": "clean", "size": 58, "y": 0.82, "maxWords": 3,  # word mode turns small/unreadable while a heading is on screen
                 "keywords": ["biceps", "half", "spaghetti", "thirty", "weak", "heaviest", "mercy", "month", "ARMS"],
                 "hide": [["Here's what's-0.05", "Your forearms are"], ["Here's the fix-0.05", "One: dead+0.6"],
                          ["Two: farmer's-0.05", "Grab the heaviest"]]},
    "scenes": [
        sc("hook", "start", [
            img("hero_this_small", "start", "not your biceps", enter="cut", **BODY),
            {**title("SMALL ARMS?", "start", "not your biceps"), "animation": "none"},
            img("hero_double_biceps", "not your biceps", enter="cut", id="h", **BODY),
            title("IT'S NOT YOUR BICEPS", "not your biceps", size=115),
            pain(0.2, 0.36, "not your biceps", None, 0.24), pain(0.8, 0.36, "not your biceps", None, 0.24),
        ], camera=punch("not your biceps", (0.5, 0.42), 1.12)),
        sc("c_real", "Here's what's-0.05", [
            card("HERE'S WHAT'S REALLY GOING ON", "Here's what's-0.05", None, INK, 200, 0.42),
        ]),
        sc("why", "Your forearms are-0.05", [
            img("hero_double_biceps", "Your forearms are", "cooked spaghetti", enter="cut", id="h", **BODY),
            title("FOREARMS = HALF YOUR ARM", "Your forearms are", "cooked spaghetti", size=105),
            bubble("anat_muscle_forearms", "half your arm", "cooked spaghetti", (0.8, 0.36), x=0.74, y=0.62, size=0.36),
            img("gag_spaghetti_arms", "cooked spaghetti", enter="pop", width=0.62, x=0.5, y=0.6, autoPlace=False),
            title("SPAGHETTI FOREARMS", "cooked spaghetti", size=120),
        ]),
        sc("c_test", "Quick test-0.05", [
            clip("clip_dead_hang", "Quick test", 1.0),
            title("30 SEC TEST", "Quick test"),
            {"type": "counter", "from": 0, "to": 30, "suffix": " SEC", "duration": 1.6, "x": 0.5, "y": 0.27,
             "size": 120, "color": RED, "at": "thirty seconds", "until": "If not"},
            img("gag_facepalm", "If not", enter="pop", width=0.36, x=0.8, y=0.72, autoPlace=False),
            {**title("CAN'T? GRIP = WEAK", "If not", None, 110), "y": 0.27, "color": RED},
        ]),
        sc("fix", "Here's the fix-0.05", [
            text("HERE'S THE FIX", "Here's the fix-0.05", None, 0.47, 170, "#FFFFFF", "cut"),
        ], camera=[{"at": "Here's the fix-0.05", "zoom": 1}, {"at": "the fix+0.25", "zoom": 1.18}]),
        sc("c_m1", "the fix+0.45", [
            card("#1", "the fix+0.45", "One: dead+0.6", RED, 220, 0.4),
            card("DEAD HANG", "One: dead", "One: dead+0.6", RED, 150, 0.52),
            clip("clip_dead_hang", "One: dead+0.6", 1.3),
            title("#1 DEAD HANG", "One: dead+0.6"), sub("3 ROUNDS · MAX TIME", "Three rounds"),
            *label("GRIP", "Three rounds", (0.36, 0.2), 0.2, 0.36),
        ]),
        sc("c_m2", "Two: farmer's-0.05", [
            card("#2", "Two: farmer's-0.05", "Grab the heaviest", RED, 220, 0.4),
            card("FARMER'S HOLD", "Two: farmer's", "Grab the heaviest", RED, 140, 0.52),
            clip("clip_farmer_walk", "Grab the heaviest", 1.4),
            title("#2 FARMER'S HOLD", "Grab the heaviest"), sub("HEAVIEST WEIGHTS", "Grab the heaviest", "begs for mercy"),
            sub("HOLD TILL GRIP GIVES UP", "begs for mercy"),
            *label("FOREARMS", "hold until", (0.33, 0.55), 0.18, 0.4),
        ]),
        sc("after", "Three times a-0.05", [
            title("3x A WEEK", "Three times a", "in a month"),
            img("hero_this_small", "Three times a", None, enter="pop", width=0.5, x=0.26, y=0.62, autoPlace=False),
            {"type": "arrow", "from": [0.45, 0.55], "to": [0.57, 0.55], "color": RED, "thickness": 22, "at": "in a month"},
            img("hero_double_biceps", "in a month", None, enter="pop", width=0.5, x=0.75, y=0.62, autoPlace=False),
            title("1 MONTH LATER", "in a month"), sub("SLEEVES GET TIGHT", "sleeves get"),
        ]),
        sc("cta", "Comment ARMS-0.05", [
            img("hero_point_viewer", "Comment ARMS", enter="cut", id="h", **BODY),
            title('COMMENT "ARMS"', "Comment ARMS"),
            {"type": "comment", "text": "ARMS \U0001F4AA", "user": "you", "ago": "now", "likes": "2.4K",
             "x": 0.5, "y": 0.3, "width": 0.7, "size": 50, "at": "Comment ARMS+0.3", "enter": "pop"},
        ], camera=[{"at": "Comment ARMS", "zoom": 1}, {"at": "still empty", "zoom": 1.2, "focus": "face"}]),
    ],
    "sfx": [dict(zip(("at", "src", "volume"), e)) for e in [
        ("start", "sfx_whoosh_soft"), ("not your biceps", "sfx_ding"),
        ("Here's what's-0.05", "sfx_typing_loud", 1.0), ("half your arm", "sfx_pop_soft"), ("cooked spaghetti", "sfx_boing"),
        ("Quick test", "sfx_whoosh_soft"), ("thirty seconds", "sfx_counter"), ("If not", "sfx_pop_soft"),
        ("Here's the fix-0.05", "sfx_typing_loud", 1.0), ("the fix+0.25", "sfx_whoosh_big"),
        ("the fix+0.45", "sfx_pop_soft"), ("One: dead+0.6", "sfx_whoosh_soft"), ("Three rounds", "sfx_click_soft"),
        ("Two: farmer's-0.05", "sfx_pop_soft"), ("Grab the heaviest", "sfx_whoosh_soft"), ("begs for mercy", "sfx_pop_soft"),
        ("Three times a", "sfx_whoosh_soft"), ("in a month", "sfx_ding"),
        ("Comment ARMS", "sfx_whoosh_soft"), ("Comment ARMS+0.3", "sfx_notification")]],
}
json.dump(plan, open("forearms2.json", "w"), indent=1, ensure_ascii=False)
