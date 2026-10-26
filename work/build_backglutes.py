# Demo in the Captain Workout pace (26 Oct): "Lower back hurts? It's your glutes."
# Hook + problem in frame 1, own bumper "HERE'S THE FIX", 2 moves, comment CTA. Grey-blue canvas, cuts only,
# something new every ~1-2 s (pop-in props, glows, small camera punches), headings top, captions bottom.
import json
INK = "#16191D"; SUB = "#3F4A55"; RED = "#EF4444"; GREEN = "#22C55E"; BG = "#C3CCD5"
BODY = {"width": 0.7, "y": 0.6}
CLIP = {"width": 0.95, "y": 0.58}


def img(a, at, until=None, enter="pop", **kw):
    d = {"type": "image", "asset": a, "shadow": True, "enter": enter, "at": at, **kw}
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


def glow(anchor, at, color, until=None):
    d = {"type": "glow", "anchor": anchor, "color": color, "at": at, "target": "h"}
    if until: d["until"] = until
    return d


def punch(at, focus=(0.5, 0.55), zoom=1.12):
    # small reframe on a key word: hold, then ease in
    return [{"at": at, "zoom": 1}, {"at": f"{at}+0.3", "zoom": zoom, "focus": list(focus) if isinstance(focus, tuple) else focus}]


def sc(id, start, layers, camera=None):
    d = {"id": id, "start": start, "backdrop": "none", "layers": layers}
    if camera: d["camera"] = camera
    return d


plan = {
    "title": "Lower Back Pain? It's Your Glutes",
    "canvas": {"background": BG},
    "captions": {"mode": "phrase", "look": "clean", "size": 56, "y": 0.8, "maxWords": 3,
                 "keywords": ["glutes", "back", "fix", "two", "fifteen", "thirty", "every"]},
    "scenes": [
        sc("hook", "start", [
            img("hero_sore_back", "start", enter="cut", id="h", **BODY),
            title("LOWER BACK PAIN?", "start", "It's your glutes"),
            img("prop_red_x", "not your back", "It's your glutes", x=0.78, y=0.52, width=0.22),
            title("IT'S YOUR GLUTES", "It's your glutes"),
            glow("glutes", "It's your glutes", RED),
        ], camera=punch("It's your glutes", "glutes", 1.15)),
        sc("why", "You sit all day#1-0.05", [
            img("hero_bad_posture_desk", "You sit all day#1", enter="cut", id="h", **BODY),
            title("YOU SIT ALL DAY", "You sit all day#1"),
            sub("GLUTES SWITCH OFF", "fall asleep", "lower back does"),
            glow("glutes", "fall asleep", "#7A8796", "lower back does"),
            sub("BACK DOES THEIR JOB", "lower back does"),
        ], camera=punch("lower back does", "back")),
        sc("fix", "Here's the fix-0.05", [
            text("HERE'S", "Here's the fix", None, 0.42, 190, INK, "slam"),
            text("THE FIX", "Here's the fix+0.15", None, 0.53, 190, RED, "slam"),
        ]),
        sc("two", "Two moves-0.05", [
            img("hero_count_2", "Two moves", enter="cut", **BODY),
            title("2 MOVES", "Two moves"), sub("NO GYM NEEDED", "Two moves"),
        ]),
        sc("m1", "First, glute bridges-0.05", [
            {"type": "video", "asset": "clip_glute_bridge", "at": "First, glute bridges", "enter": "cut", **CLIP},
            title("#1 GLUTE BRIDGE", "First, glute bridges", size=120),
            sub("SQUEEZE 2 SEC", "Squeeze", "fifteen reps"),
            sub("15 REPS", "fifteen reps"),
            img("prop_stopwatch", "two seconds", "fifteen reps", x=0.82, y=0.34, width=0.16),
        ]),
        sc("m2", "Second, the hip-0.05", [
            img("hero_hip_flexor_stretch", "Second, the hip", enter="cut", id="h", **BODY),
            title("#2 HIP FLEXOR STRETCH", "Second, the hip", size=110),
            sub("30 SEC EACH SIDE", "Thirty seconds", "hips stop"),
            sub("BACK PAIN EASES", "hips stop"),
            glow("hips", "hips stop", GREEN),
        ], camera=punch("hips stop", "hips")),
        sc("daily", "Do both every-0.05", [
            img("hero_thumbs_up", "Do both every", enter="cut", **BODY),
            title("EVERY DAY", "Do both every"), sub("FOR 2 WEEKS", "two weeks"),
            img("prop_green_check", "two weeks", None, x=0.8, y=0.4, width=0.2),
        ]),
        sc("cta", "Comment BACK-0.05", [
            img("hero_point_viewer", "Comment BACK", enter="cut", **BODY),
            title('COMMENT "BACK"', "Comment BACK"), sub("IF YOU SIT ALL DAY", "if you sit"),
        ]),
    ],
    "sfx": [{"at": a, "src": s} for a, s in [
        ("start", "sfx_whoosh_soft"), ("not your back", "sfx_pop_soft"), ("It's your glutes", "sfx_ding"),
        ("You sit all day#1", "sfx_whoosh_soft"), ("lower back does", "sfx_pop_soft"),
        ("Here's the fix", "sfx_whoosh_big"), ("Two moves", "sfx_pop_soft"),
        ("First, glute bridges", "sfx_whoosh_soft"), ("two seconds", "sfx_click_soft"), ("fifteen reps", "sfx_pop_soft"),
        ("Second, the hip", "sfx_whoosh_soft"), ("hips stop", "sfx_ding"),
        ("Do both every", "sfx_whoosh_soft"), ("two weeks", "sfx_ding"), ("Comment BACK", "sfx_pop_soft")]],
}
json.dump(plan, open("backglutes.json", "w"), indent=1, ensure_ascii=False)
