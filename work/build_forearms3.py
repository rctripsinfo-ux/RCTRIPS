# Day 1 re-made with NO exercise clips (owner, 29 Oct): every move is H pose images swapped in a loop.
# Based on build_forearms.py (Day 1 V1).
# Day 1 of TOPICS-30-DAYS: "Weak Forearms? Do These 2 Moves" (owner, 28 Oct). Approved template (posture2) +
# voice 1.3x with all silences cut (fast_render.py) + one gag image on the joke line.
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


plan = {
    "title": "Weak Forearms? Do These 2 Moves",
    "canvas": {"background": BG},
    "style": {"accent": YEL},
    "captions": {"mode": "phrase", "look": "clean", "size": 58, "y": 0.82, "maxWords": 3,
                 "keywords": ["small", "forearms", "spaghetti", "fix", "three", "heaviest", "mercy", "ARMS"],
                 "hide": [["Here's the fix-0.05", "Two moves"]]},
    "scenes": [
        sc("hook", "start", [
            img("hero_this_small", "start", "not your biceps", enter="cut", **BODY),
            {**title("SMALL ARMS?", "start", "It's your forearms"), "animation": "none"},
            img("hero_double_biceps", "not your biceps", enter="cut", id="h", **BODY),
            title("IT'S YOUR FOREARMS", "It's your forearms", size=125),
            pain(0.2, 0.36, "It's your forearms", None, 0.24),
            pain(0.8, 0.36, "It's your forearms", None, 0.24),
        ], camera=punch("It's your forearms", (0.5, 0.42), 1.12)),
        sc("curl", "You curl every-0.05", [
            poses(loop("hero_curl_down", "hero_curl_up", "You curl every", 8)),
            title("CURLS EVERY DAY", "You curl every"),
        ]),
        sc("gag", "cooked spaghetti-0.05", [
            img("gag_spaghetti_arms", "cooked spaghetti", enter="pop", width=0.62, x=0.5, y=0.6, autoPlace=False),
            title("SPAGHETTI FOREARMS", "cooked spaghetti", size=120),
        ]),
        sc("fix", "Here's the fix-0.05", [
            text("HERE'S THE FIX", "Here's the fix-0.05", None, 0.47, 170, "#FFFFFF", "cut"),
        ], camera=[{"at": "Here's the fix-0.05", "zoom": 1}, {"at": "fix.+0.05", "zoom": 1}, {"at": "fix.+0.2", "zoom": 1.18}]),
        sc("two", "the fix+0.45", [  # starts right after the bumper so no empty frame in the tiny gap
            img("hero_count_2", "the fix+0.45", enter="cut", **BODY),
            title("2 MOVES", "Two moves"),
        ], camera=[{"at": "Two moves", "zoom": 1}, {"at": "Two moves+2", "zoom": 1.07}]),
        sc("m1", "One: dead hangs-0.05", [
            poses([("hero_look_up_bar", "One: dead hangs"), ("hero_pullup_hang", "Hang from")], autoAlign=False, width=0.66, y=0.64),  # smaller + lower: bar stays under the sub
            title("#1 DEAD HANG", "One: dead hangs"), sub("MAX TIME x3", "as long as"),
            bubble("anat_muscle_forearm_grip", "as long as", None, None, x=0.78, y=0.62, size=0.32)  # beside the legs, never near the face,
        ]),
        sc("m2", "Two: farmer's-0.05", [
            poses([("hero_curl_down", "Two: farmer's"), ("hero_pick_dumbbell", "Grab the"), ("hero_curl_down", "hold until")]),
            title("#2 FARMER'S HOLD", "Two: farmer's"), sub("HEAVIEST WEIGHTS", "heaviest weights", "begs for mercy"),
            sub("TILL YOUR GRIP GIVES UP", "begs for mercy"),
        ]),
        sc("after", "Do this three-0.05", [
            img("hero_double_biceps", "Do this three", "look complete", enter="cut", **BODY),
            title("3x A WEEK", "Do this three", "look complete"),
            img("gag_sunglasses_thumbs", "look complete", enter="cut", width=0.62, x=0.5, y=0.6, autoPlace=False),
            title("ARMS: COMPLETE", "look complete"),
        ]),
        sc("cta", "Comment ARMS-0.05", [
            img("hero_point_viewer", "Comment ARMS", enter="cut", id="h", **BODY),
            title('COMMENT "ARMS"', "Comment ARMS"),
            {"type": "comment", "text": "ARMS \U0001F4AA", "user": "you", "ago": "now", "likes": "2.4K",
             "x": 0.5, "y": 0.3, "width": 0.7, "size": 50, "at": "Comment ARMS+0.3", "enter": "pop"},
        ], camera=[{"at": "Comment ARMS", "zoom": 1}, {"at": "need help", "zoom": 1.3, "focus": "face"}]),
    ],
    "sfx": [dict(zip(("at", "src", "volume"), e)) for e in [
        ("start", "sfx_whoosh_soft"), ("not your biceps", "sfx_pop_soft"), ("It's your forearms", "sfx_ding"),
        ("You curl every", "sfx_whoosh_soft"), ("cooked spaghetti", "sfx_boing"),
        ("Here's the fix-0.05", "sfx_typing_loud", 1.0), ("fix.+0.15", "sfx_whoosh_big"), ("Two moves", "sfx_pop_soft"),
        ("One: dead hangs", "sfx_whoosh_soft"), ("as long as", "sfx_pop_soft"),
        ("Two: farmer's", "sfx_whoosh_soft"), ("begs for mercy", "sfx_pop_soft"),
        ("Do this three", "sfx_whoosh_soft"), ("look complete", "sfx_ding"),
        ("Comment ARMS", "sfx_whoosh_soft"), ("Comment ARMS+0.3", "sfx_notification")]],
}
json.dump(plan, open("forearms3.json", "w"), indent=1, ensure_ascii=False)
