# V3 (owner, 26 Oct): pain = big red disc with spinning white dashes (no X), no small icons, no green, every text
# typed letter by letter, Captain-style typed bumper. Based on V2 with every Captain Workout lesson (26 Oct): funny analogy, a new thing on screen every
# ~0.5-1 s (icons, chips, counter, pose swaps), red dashed ring on the problem, same bumper, yellow keywords,
# slower voice (speed 1.0), face punch at the end and a last line that loops into the first.
import json
INK = "#16191D"; SUB = "#3F4A55"; RED = "#EF4444"; GREEN = "#22C55E"; YEL = "#FACC15"; BG = "#C3CCD5"
BODY = {"width": 0.7, "y": 0.6}
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
    if camera: d["camera"] = camera
    if id == "fix": d["background"] = "#1E2228"
    return d


def pain(x, y, at, until=None, w=0.34):
    d = {"type": "highlight", "shape": "pain", "x": x, "y": y, "w": w, "color": RED, "at": at, "enter": "cut"}
    if until: d["until"] = until
    return d


plan = {
    "title": "Lower Back Pain? It's Your Glutes",
    "canvas": {"background": BG},
    "style": {"accent": YEL},
    "captions": {"mode": "phrase", "look": "clean", "size": 58, "y": 0.8, "maxWords": 3,
                 "keywords": ["glutes", "vacation", "double", "fix", "fifteen", "thirty", "yanking", "off", "BACK"]},
    "scenes": [
        sc("hook", "start", [
            img("hero_sore_back", "start", enter="cut", id="h", **BODY),
            title("LOWER BACK PAIN?", "start", "It's your glutes"),
            pain(0.45, 0.5, "start", "It's your glutes"),
            title("IT'S YOUR GLUTES", "It's your glutes"),
            pain(0.46, 0.585, "It's your glutes"),
        ], camera=punch("It's your glutes", "glutes", 1.15)),
        sc("why", "You sit all day#1-0.05", [
            img("hero_bad_posture_desk", "You sit all day#1", "double shift", enter="cut", id="h", **BODY),
            title("YOU SIT ALL DAY", "You sit all day#1"),
            sub("GLUTES: ON VACATION", "vacation", "double shift"),
            glow("glutes", "vacation", "#7A8796", "h", "double shift"),
            img("hero_tired_sweating", "double shift", enter="cut", id="h2", **BODY),
            sub("BACK: DOUBLE SHIFT", "double shift"),
            chip("2X WORK", "double shift+0.3", icon_name="warning", x=0.82, y=0.56),
        ]),
        sc("fix", "Here's the fix-0.05", [  # dark title card like Captain
            text("HERE'S THE FIX", "Here's the fix-0.05", None, 0.47, 170, "#FFFFFF", "cut"),
        ]),
        sc("two", "Two moves-0.05", [
            img("hero_count_2", "Two moves", enter="cut", **BODY),
            title("2 MOVES", "Two moves"), sub("NO GYM", "no gym"),
        ]),
        sc("m1", "First, glute bridges-0.05", [
            {"type": "video", "asset": "clip_glute_bridge", "at": "First, glute bridges", "enter": "cut", **CLIP},
            title("#1 GLUTE BRIDGE", "First, glute bridges", size=120),
            sub("SQUEEZE 2 SEC AT THE TOP", "Squeeze", "fifteen reps"),
            {"type": "counter", "from": 0, "to": 15, "suffix": " REPS", "duration": 1.2, "x": 0.5, "y": 0.34,
             "size": 130, "color": RED, "at": "fifteen reps"},
        ]),
        sc("m2", "Second, the hip-0.05", [
            img("hero_hip_flexor_stretch", "Second, the hip", enter="cut", id="h", **BODY),
            title("#2 HIP FLEXOR STRETCH", "Second, the hip", size=110),
            sub("30 SEC EACH SIDE", "Thirty seconds"),
            pain(0.46, 0.6, "so your hips", None, 0.28),
        ], camera=punch("so your hips", (0.46, 0.6))),
        sc("daily", "Do both every-0.05", [
            img("hero_thumbs_up", "Do both every", "day off", enter="cut", **BODY),
            title("EVERY DAY", "Do both every", "day off"), sub("FOR 2 WEEKS", "two weeks", "day off"),
            img("hero_victory", "day off", enter="cut", width=0.62, y=0.64),
            title("BACK: DAY OFF", "day off"),
        ]),
        sc("cta", "Comment BACK-0.05", [
            img("hero_point_viewer", "Comment BACK", enter="cut", id="h", **BODY),
            title('COMMENT "BACK"', "Comment BACK"),
        ], camera=[{"at": "Comment BACK", "zoom": 1}, {"at": "if your lower", "zoom": 1.35, "focus": "face"}]),
    ],
    "sfx": [{"at": a, "src": s} for a, s in [
        ("start", "sfx_whoosh_soft"), ("It's your glutes", "sfx_ding"),
        ("You sit all day#1", "sfx_whoosh_soft"), ("vacation", "sfx_pop_soft"), ("double shift", "sfx_pop_soft"),
        ("Here's the fix-0.05", "sfx_typing"), ("Two moves", "sfx_pop_soft"),
        ("First, glute bridges", "sfx_whoosh_soft"), ("fifteen reps", "sfx_counter"),
        ("Second, the hip", "sfx_whoosh_soft"), ("so your hips", "sfx_pop_soft"),
        ("Do both every", "sfx_whoosh_soft"), ("day off", "sfx_ding"),
        ("Comment BACK", "sfx_whoosh_soft")]],
}
json.dump(plan, open("backglutes3.json", "w"), indent=1, ensure_ascii=False)
