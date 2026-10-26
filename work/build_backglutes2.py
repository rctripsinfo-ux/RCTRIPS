# V2 of the glutes demo with every Captain Workout lesson (26 Oct): funny analogy, a new thing on screen every
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
         "maxWidth": 0.9, "animation": "none", "untype": False, "enter": enter, "exit": "cut",
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
            ring(0.45, 0.5, "start", "It's your glutes"),
            img("prop_red_x", "not your back", "It's your glutes", x=0.45, y=0.5, width=0.2),
            title("IT'S YOUR GLUTES", "It's your glutes"),
            glow("glutes", "It's your glutes", RED, "h"),
        ], camera=punch("It's your glutes", "glutes", 1.18)),
        sc("why", "You sit all day-0.05", [
            img("hero_bad_posture_desk", "You sit all day", "double shift", enter="cut", id="h", **BODY),
            title("YOU SIT ALL DAY", "You sit all day"),
            icon("phone", "You sit all day+0.4", "vacation", color=INK),
            sub("GLUTES: ON VACATION", "vacation", "double shift"),
            icon("bed", "vacation", "double shift", label="ZZZ", x=0.16, color="#6B7A8C"),
            glow("glutes", "vacation", "#7A8796", "h", "double shift"),
            img("hero_tired_sweating", "double shift", enter="cut", id="h2", **BODY),
            sub("BACK: DOUBLE SHIFT", "double shift"),
            chip("2X WORK", "double shift+0.3", icon_name="warning", x=0.82, y=0.56),
        ]),
        sc("fix", "Here's the fix-0.05", [
            text("HERE'S", "Here's the fix-0.05", None, 0.42, 190, INK, "slam"),
            text("THE FIX", "Here's the fix+0.15", None, 0.53, 190, RED, "slam"),
            {"type": "pulse", "kind": "edge", "color": RED, "at": "Here's the fix", "duration": 0.5},
        ]),
        sc("two", "Two moves-0.05", [
            img("hero_count_2", "Two moves", enter="cut", **BODY),
            title("2 MOVES", "Two moves"),
            chip("NO GYM", "no gym", icon_name="dumbbell", x=0.78, y=0.36, color=GREEN),
        ]),
        sc("m1", "First, glute bridges-0.05", [
            {"type": "video", "asset": "clip_glute_bridge", "at": "First, glute bridges", "enter": "cut", **CLIP},
            title("#1 GLUTE BRIDGE", "First, glute bridges", size=120),
            sub("SQUEEZE AT THE TOP", "Squeeze", "fifteen reps"),
            icon("timer", "two seconds", "fifteen reps", label="2 SEC", x=0.84, y=0.42, color=RED),
            {"type": "counter", "from": 0, "to": 15, "suffix": " REPS", "duration": 1.2, "x": 0.5, "y": 0.34,
             "size": 130, "color": RED, "at": "fifteen reps"},
        ]),
        sc("m2", "Second, the hip-0.05", [
            img("hero_hip_flexor_stretch", "Second, the hip", enter="cut", id="h", **BODY),
            title("#2 HIP FLEXOR STRETCH", "Second, the hip", size=110),
            icon("timer", "Thirty seconds", "so your hips", label="30 SEC", color=RED),
            sub("EACH SIDE", "each side", "so your hips"),
            glow("hips", "so your hips", RED, "h", "stop yanking+0.6"),
            chip("STOP YANKING", "stop yanking", None, x=0.5, y=0.3),
            glow("hips", "stop yanking+0.6", GREEN, "h"),
        ], camera=punch("so your hips", "hips")),
        sc("daily", "Do both every-0.05", [
            img("hero_thumbs_up", "Do both every", "day off", enter="cut", **BODY),
            title("EVERY DAY", "Do both every", "day off"),
            icon("calendar", "two weeks", "day off", label="14 DAYS", color=INK),
            img("hero_victory", "day off", enter="cut", width=0.62, y=0.64),
            title("BACK: DAY OFF", "day off"),
            img("prop_green_check", "day off+0.2", None, x=0.82, y=0.38, width=0.18),
        ]),
        sc("cta", "Comment BACK-0.05", [
            img("hero_point_viewer", "Comment BACK", enter="cut", id="h", **BODY),
            title('COMMENT "BACK"', "Comment BACK"),
            icon("check", "if your lower", None, label="", color=GREEN),
        ], camera=[{"at": "Comment BACK", "zoom": 1}, {"at": "if your lower", "zoom": 1.35, "focus": "face"}]),
    ],
    "sfx": [{"at": a, "src": s} for a, s in [
        ("start", "sfx_whoosh_soft"), ("not your back", "sfx_pop_soft"), ("It's your glutes", "sfx_ding"),
        ("You sit all day", "sfx_whoosh_soft"), ("vacation", "sfx_pop_soft"), ("double shift", "sfx_pop_soft"),
        ("Here's the fix", "sfx_whoosh_big"), ("Two moves", "sfx_pop_soft"), ("no gym", "sfx_click_soft"),
        ("First, glute bridges", "sfx_whoosh_soft"), ("two seconds", "sfx_click_soft"), ("fifteen reps", "sfx_counter"),
        ("Second, the hip", "sfx_whoosh_soft"), ("stop yanking", "sfx_pop_soft"), ("stop yanking+0.6", "sfx_ding"),
        ("Do both every", "sfx_whoosh_soft"), ("two weeks", "sfx_pop_soft"), ("day off", "sfx_ding"),
        ("Comment BACK", "sfx_whoosh_soft")]],
}
json.dump(plan, open("backglutes2.json", "w"), indent=1, ensure_ascii=False)
