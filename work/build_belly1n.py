# Same as build_belly1.py, voice back to normal speed 1.0 (owner, 28 Oct: 1.3x was too fast to follow).
# Day 2, V1 variation (owner, 28 Oct): same topic in the simpler forearms V1 format for an A/B test: one bumper,
# no "what's really going on" card, no wall test, no #-cards; headings + clips + pain circle + anatomy + 2 jokes.
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
    "title": "Lower Belly Pooch? It's Your Hips",
    "canvas": {"background": BG},
    "style": {"accent": YEL},
    "captions": {"mode": "phrase", "look": "clean", "size": 58, "y": 0.82, "maxWords": 3,
                 "keywords": ["fat", "hip", "pelvis", "gap", "tilt", "thirty", "fifteen", "ten", "taller", "HIPS"],
                 "hide": [["Here's the fix-0.05", "One: hip"]]},
    "scenes": [
        sc("hook", "start", [
            img("hero_measuring_waist", "start", "not always fat", enter="cut", **BODY),
            {**title("LOWER BELLY POOCH?", "start", "not always fat", size=120), "animation": "none"},
            pain(0.5, 0.55, "start", "not always fat", 0.3),
            img("gag_scale_shock", "not always fat", enter="cut", width=0.62, x=0.5, y=0.6, autoPlace=False),
            title("IT'S NOT ALWAYS FAT", "not always fat", size=115),
        ], camera=punch("not always fat", (0.5, 0.45), 1.12)),
        sc("why", "Sitting all day-0.05", [
            img("gag_couch_potato", "Sitting all day", "your hip flexors", enter="cut", width=0.66, x=0.5, y=0.6, autoPlace=False),
            title("SITTING ALL DAY", "Sitting all day", "your hip flexors"),
            img("hero_bad_posture_desk", "your hip flexors", enter="cut", id="h", **LEFT),
            title("TIGHT HIP FLEXORS", "your hip flexors", "tip your pelvis", size=125),
            bubble("anat_pain_tight_hip_flexor", "your hip flexors", "tip your pelvis", None, x=0.74, y=0.42, size=0.38),
            title("PELVIS TIPS FORWARD", "tip your pelvis", "pushed out", size=120),
            bubble("anat_bone_pelvis_tilt", "tip your pelvis", None, None, x=0.74, y=0.42, size=0.38),
            {**title("= BELLY POOCH", "pushed out"), "color": RED},
        ]),
        sc("fix", "Here's the fix-0.05", [
            text("HERE'S THE FIX", "Here's the fix-0.05", None, 0.47, 170, "#FFFFFF", "cut"),
        ], camera=[{"at": "Here's the fix-0.05", "zoom": 1}, {"at": "the fix+0.25", "zoom": 1.18}]),
        sc("c_m1", "One: hip-0.05", [
            clip("clip_hip_flexor_stretch", "One: hip", 1.0),
            title("#1 HIP FLEXOR STRETCH", "One: hip", size=110), sub("30 SEC EACH SIDE", "thirty seconds"),
        ]),
        sc("c_m2", "Two: glute-0.05", [
            clip("clip_glute_bridge", "Two: glute", 1.4),
            title("#2 GLUTE BRIDGE", "Two: glute"),
            {"type": "counter", "from": 0, "to": 15, "suffix": " REPS", "duration": 1.0, "x": 0.5, "y": 0.3,
             "size": 120, "color": RED, "at": "fifteen reps"},
        ]),
        sc("c_m3", "Three: dead-0.05", [
            {**clip("clip_dead_bug", "Three: dead", 1.3), "width": 0.95, "y": 0.52},  # floor move: bigger, above captions
            title("#3 DEAD BUG", "Three: dead"), sub("10 SLOW REPS", "ten slow"),
            *label("DEEP CORE", "ten slow", (0.5, 0.6), 0.2, 0.36),
        ]),
        sc("after", "Do it daily-0.05", [
            img("hero_stand", "Do it daily", "flattens out", enter="cut", **BODY),
            title("EVERY DAY", "Do it daily", "flattens out"),
            img("gag_sunglasses_thumbs", "flattens out", enter="cut", width=0.62, x=0.5, y=0.6, autoPlace=False),
            title("BELLY: FLAT", "flattens out"),
        ]),
        sc("cta", "flattens out+0.55", [  # no empty frame in the tiny gap before "Comment"
            img("hero_point_viewer", "flattens out+0.55", enter="cut", id="h", **BODY),
            title('COMMENT "HIPS"', "Comment HIPS"),
            {"type": "comment", "text": "HIPS \U0001F633", "user": "you", "ago": "now", "likes": "1.8K",
             "x": 0.5, "y": 0.3, "width": 0.7, "size": 50, "at": "Comment HIPS+0.3", "enter": "pop"},
        ], camera=[{"at": "Comment HIPS", "zoom": 1}, {"at": "got exposed", "zoom": 1.2, "focus": "face"}]),
    ],
    "sfx": [dict(zip(("at", "src", "volume"), e)) for e in [
        ("start", "sfx_whoosh_soft"), ("not always fat", "sfx_ding"),
        ("Sitting all day", "sfx_boing"),
        ("your hip flexors", "sfx_pop_soft"), ("tip your pelvis", "sfx_pop_soft"), ("pushed out", "sfx_pop_soft"),
        ("Here's the fix-0.05", "sfx_typing_loud", 1.0), ("the fix+0.25", "sfx_whoosh_big"),
        ("One: hip", "sfx_whoosh_soft"), ("thirty seconds", "sfx_click_soft"),
        ("Two: glute", "sfx_whoosh_soft"), ("fifteen reps", "sfx_counter"),
        ("Three: dead", "sfx_whoosh_soft"), ("ten slow", "sfx_click_soft"),
        ("Do it daily", "sfx_whoosh_soft"), ("flattens out", "sfx_ding"),
        ("Comment HIPS", "sfx_whoosh_soft"), ("Comment HIPS+0.3", "sfx_notification")]],
}
json.dump(plan, open("belly1n.json", "w"), indent=1, ensure_ascii=False)
