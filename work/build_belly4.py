# Day 2 V4 (owner, 28 Oct): V3 flow + constant motion like the old viral videos: the camera never stops (slow zoom
# and pan in every scene, punches/shakes on key words), H gestures (pose flip-books), clips instead of stills where
# possible, pictures slide/pop in, and whip / zoom-blur transitions between sections. Fewer new pictures, more motion.
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
    else: d.update(backdrop="rays", backdropColor="#C9B48F", backdropOpacity=0.55)  # slow turning rays: texture makes camera moves visible
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


import re


def ref(start, delta):
    # "phrase+0.25" + 3 -> "phrase+3.25" (the tool takes one offset per anchor)
    m = re.match(r"^(.*?)([+-]\d+(?:\.\d+)?)?$", start)
    off = float(m.group(2) or 0) + delta
    return f"{m.group(1)}{off:+.2f}" if off else m.group(1)


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


plan = {
    "title": "Lower Belly Pooch? It's Your Hips",
    "canvas": {"background": BG},
    "style": {"accent": YEL},
    "captions": {"mode": "phrase", "look": "clean", "size": 58, "y": 0.82, "maxWords": 3,
                 "keywords": ["fat", "pelvis", "gap", "tilt", "thirty", "fifteen", "ten", "taller", "HIPS"],
                 "hide": [["Here's what's-0.05", "Sitting all day-0.05"], ["Here's the fix-0.05", "thirty seconds-0.05"],
                          ["Two: glute-0.05", "fifteen reps-0.05"], ["Three: dead-0.05", "ten slow-0.05"]]},
    "scenes": [
        scene("hook", "start", [
            img("hero_measuring_waist", "start", "not always fat", enter="cut", **BODY),
            {**title("LOWER BELLY POOCH?", "start", "not always fat", size=120), "animation": "none"},
            pain(0.5, 0.55, "start", "not always fat", 0.3),
            img("gag_scale_shock", "not always fat", enter="slam", width=0.62, x=0.5, y=0.6, autoPlace=False),
            title("IT'S NOT ALWAYS FAT", "not always fat", size=115),
        ], camera=drift("start", 1.16, (0.5, 0.5), (0.5, 0.56), 6) + [{"at": "not always fat", "zoom": 1.25, "focus": [0.5, 0.5]}, {"at": "not always fat+0.35", "zoom": 1.05, "focus": [0.5, 0.52]}],
           shakes=["not always fat"]),
        scene("c_real", "Here's what's-0.05", [card("HERE'S WHAT'S REALLY GOING ON", "Here's what's-0.05", None, INK, 200, 0.42)],
              camera=drift("Here's what's-0.05", 1.16, (0.5, 0.45), (0.5, 0.45), 6), transition="zoomBlur"),
        scene("why", "Sitting all day-0.05", [
            img("gag_couch_potato", "Sitting all day", None, enter="up", width=0.66, x=0.5, y=0.6, autoPlace=False),
            title("SITTING ALL DAY", "Sitting all day"),
            sub("= TIGHT HIP FLEXORS", "your hip flexors"),
        ], camera=drift("Sitting all day", 1.16, (0.45, 0.5), (0.55, 0.55), 6), transition="whip"),
        scene("c_pelvis", "tip your pelvis-0.05", [
            clip("clip_wrong_posture_desk", "tip your pelvis-0.05", 1.0),
            title("PELVIS TIPS FORWARD", "tip your pelvis-0.05", None, 120),
            bubble("anat_bone_pelvis_tilt", "tip your pelvis", None, None, x=0.77, y=0.64, size=0.36),
            {**sub("= BELLY PUSHED OUT", "pushed out"), "color": RED},
        ], camera=[{"at": "tip your pelvis-0.05", "zoom": 1}, {"at": "tip your pelvis+4", "zoom": 1.07, "focus": [0.5, 0.6]}]),
        scene("test", "Quick test-0.05", [
            img("hero_lean_wall", "Quick test", "Big gap", enter="left", **BODY),
            title("WALL TEST", "Quick test", "Big gap"),
            img("hero_side_view", "Big gap", enter="pop", **BODY),
            title("BIG GAP = TILT", "Big gap"),
            pain(0.44, 0.5, "Big gap", None, 0.26),
        ], camera=drift("Quick test", 1.16, (0.5, 0.5), (0.47, 0.52), 6), transition="zoomBlur", shakes=["Big gap"]),
        scene("fix", "Here's the fix-0.05", [text("HERE'S THE FIX", "Here's the fix-0.05", None, 0.47, 170, "#FFFFFF", "cut")],
              camera=[{"at": "Here's the fix-0.05", "zoom": 1}, {"at": "fix.+0.1", "zoom": 1.2}], transition="whip"),
        scene("c_m1", "One: hip-0.05", [
            {**card("#1 HIP FLEXOR STRETCH", "One: hip-0.05", "thirty seconds-0.05", RED, 140, 0.45), "enter": "pop"},
            clip("clip_hip_flexor_stretch", "thirty seconds-0.05", 1.0),
            title("#1 HIP FLEXOR STRETCH", "thirty seconds-0.05", size=110), sub("30 SEC EACH SIDE", "thirty seconds-0.05"),
        ], camera=[{"at": "One: hip-0.05", "zoom": 1.15}, {"at": "thirty seconds-0.05", "zoom": 1}, {"at": "thirty seconds+4", "zoom": 1.07, "focus": [0.5, 0.6]}],
           transition="zoomBlur"),
        scene("c_m2", "Two: glute-0.05", [
            {**card("#2 GLUTE BRIDGE", "Two: glute-0.05", "fifteen reps-0.05", RED, 150, 0.45), "enter": "pop"},
            clip("clip_glute_bridge", "fifteen reps-0.05", 1.3),
            title("#2 GLUTE BRIDGE", "fifteen reps-0.05"),
            {"type": "counter", "from": 0, "to": 15, "suffix": " REPS", "duration": 1.2, "x": 0.5, "y": 0.3,
             "size": 120, "color": RED, "at": "fifteen reps"},
        ], camera=[{"at": "Two: glute-0.05", "zoom": 1.15}, {"at": "fifteen reps-0.05", "zoom": 1}, {"at": "fifteen reps+3", "zoom": 1.06, "focus": [0.5, 0.6]}],
           transition="whip"),
        scene("c_m3", "Three: dead-0.05", [
            {**card("#3 DEAD BUG", "Three: dead-0.05", "ten slow-0.05", RED, 150, 0.45), "enter": "pop"},
            {**clip("clip_dead_bug", "ten slow-0.05", 1.2), "width": 0.95, "y": 0.52},
            title("#3 DEAD BUG", "ten slow-0.05"), sub("10 SLOW REPS", "ten slow-0.05"),
        ], camera=[{"at": "Three: dead-0.05", "zoom": 1.15}, {"at": "ten slow-0.05", "zoom": 1}, {"at": "ten slow+3", "zoom": 1.06, "focus": [0.5, 0.6]}],
           transition="whip"),
        scene("after", "Do it daily-0.05", [
            title("EVERY DAY", "Do it daily", "two weeks"),
            img("hero_bad_posture_desk", "Do it daily", None, enter="left", width=0.5, x=0.26, y=0.62, autoPlace=False),
            {"type": "arrow", "from": [0.45, 0.55], "to": [0.57, 0.55], "color": RED, "thickness": 22, "at": "two weeks"},
            img("hero_victory", "two weeks", None, enter="right", width=0.5, x=0.75, y=0.62, autoPlace=False),
            title("2 WEEKS LATER", "two weeks"), sub("STAND TALLER", "stand taller"),
        ], camera=drift("Do it daily", 1.16, (0.4, 0.55), (0.6, 0.55), 6), transition="zoomBlur"),
        scene("cta", "taller.+0.25", [
            flip(["hero_point_viewer", "hero_come_on", "hero_point_viewer", "hero_come_on_v2"], "taller.+0.25", 10, 0.45, **BODY),
            title('COMMENT "HIPS"', "Comment HIPS"),
            {"type": "comment", "text": "HIPS \U0001F633", "user": "you", "ago": "now", "likes": "1.8K",
             "x": 0.5, "y": 0.3, "width": 0.7, "size": 50, "at": "Comment HIPS+0.3", "enter": "pop"},
        ], camera=drift("taller.+0.25", 1.16, (0.5, 0.5), (0.5, 0.42), 6), transition="whip"),
    ],
    "sfx": [dict(zip(("at", "src", "volume"), e)) for e in [
        ("start", "sfx_whoosh_soft"), ("not always fat", "sfx_ding"),
        ("Here's what's-0.05", "sfx_typing_loud", 1.0), ("Sitting all day-0.05", "sfx_whoosh_fast"), ("Sitting all day", "sfx_boing"),
        ("tip your pelvis", "sfx_pop_soft"), ("Quick test-0.05", "sfx_whoosh_fast"), ("Big gap", "sfx_pop_soft"),
        ("Here's the fix-0.05", "sfx_typing_loud", 1.0),
        ("One: hip-0.05", "sfx_whoosh_fast"), ("Two: glute-0.05", "sfx_whoosh_fast"), ("fifteen reps", "sfx_counter"),
        ("Three: dead-0.05", "sfx_whoosh_fast"), ("Do it daily-0.05", "sfx_whoosh_fast"), ("two weeks", "sfx_ding"),
        ("taller.+0.25", "sfx_whoosh_soft"), ("Comment HIPS+0.3", "sfx_notification")]],
}
json.dump(plan, open("belly4.json", "w"), indent=1, ensure_ascii=False)
