# Reference animation style (work/ANIMATION-STYLE-SPEC.md), done with the current tool only:
# zoom-slam hook, stacked grey keywords, empty-screen lines typed word by word with a cursor, corner peeks,
# slow push-in on every still, punch zooms on key words, ghost positions, quiet music bed, cartoon sounds.
import json
G = "#2FD94E"; R = "#E3262E"; GREY = "#9AA4AD"; LIGHT = "#C9D0D6"
SLAM = {"type": "zoom", "duration": 0.2}
RISE = {"type": "up", "duration": 0.3}
PUSH = {"type": "zoomIn"}


def img(a, at, until=None, enter="cut", motion=PUSH, **kw):
    d = {"type": "image", "asset": a, "shadow": True, "enter": enter, "at": at, **kw}
    if motion: d["motion"] = motion
    if until: d["until"] = until
    return d


def peek(a, at, until=None, side="left"):
    # corner peek: a small H rising from the bottom corner, his lower half below the frame
    return img(a, at, until, enter=RISE, motion=None, x=0.22 if side == "left" else 0.78, y=0.97, width=0.62, opacity=0.95)


def clip(a, at, until=None, rate=1.0, enter="cut", floor=True):
    d = {"type": "video", "asset": a, "at": at, "rate": rate, "enter": enter,
         **({"width": 1.0, "y": 0.62} if floor else {"width": 0.72, "y": 0.62})}
    if until: d["until"] = until
    return d


def word(t, at, until, y):
    # stacked grey keyword behind H, appears on the spoken word
    return {"type": "text", "text": t, "look": "giant", "behind": True, "x": 0.5, "y": y, "size": 150, "color": LIGHT,
            "align": "center", "maxWidth": 1, "animation": "none", "untype": False, "tilt": 0, "at": at, "until": until,
            "enter": "pop"}


def typed(words, until):
    # empty-screen line typed WORD BY WORD in sync with the voice, thin cursor at the end
    L = []
    for i, (w, at) in enumerate(words):
        txt = " ".join(x for x, _ in words[:i + 1]) + "\u00a0|"
        L.append({"type": "text", "text": txt, "x": 0.5, "y": 0.4, "size": 140, "align": "center", "color": GREY,
                  "maxWidth": 1, "animation": "none", "untype": False, "enter": "cut", "exit": "cut",
                  "stroke": {"color": "#FFFFFF", "width": 0}, "at": at,
                  "until": words[i + 1][1] if i + 1 < len(words) else until})
    return L


def sc(id, start, layers, camera=None, bd="none"):
    s = {"id": id, "start": start, "backdrop": bd, "layers": layers}
    if id == "hook": s["shakes"] = [{"at": "new chiropractor"}]
    if camera: s["camera"] = camera
    return s


scenes = [
    sc("hook", "start", [
        word("0 ABS", "zero abs", "Here's what's", 0.22),
        word("BACK PAIN", "back pain", "Here's what's", 0.31),
        word("CHIROPRACTOR", "new chiropractor", "Here's what's", 0.40),
        clip("clip_leg_raise", "start", rate=1.7, enter=SLAM),
        peek("hero_facepalm", "maybe a new", "Here's what's"),
    ], camera=[{"at": "start", "zoom": 1}, {"at": "zero abs", "zoom": 1.05}, {"at": "back pain", "zoom": 1.1},
               {"at": "new chiropractor", "zoom": 1.15}]),
    sc("line1", "Here's what's-0.05", typed([("HERE'S", "Here's what's"), ("WHAT'S", "what's actually"),
                                             ("ACTUALLY", "actually happening"), ("HAPPENING", "happening")],
                                            "You swing your legs") + [peek("hero_thinking", "Here's what's+0.2", "You swing your legs")]),
    sc("swing", "You swing your legs-0.05", [
        img("prop_fire", "and feel a burn", "That burn is not", enter="pop", motion={"type": "pulse"}, x=0.6, y=0.6, width=0.75),
        clip("clip_leg_raise", "You swing your legs", "That burn is not", rate=1.9, enter=RISE),
    ], camera=[{"at": "You swing your legs", "zoom": 1}, {"at": "and feel a burn", "zoom": 1.2}]),
    sc("truth", "That burn is not-0.05", [
        img("hero_leg_raise_up", "That burn is not", "pulling on your", enter=RISE, width=0.82, y=0.58),
        img("hero_leg_raise_down", "That burn is not+0.3", "pulling on your", enter="fade", motion=None, width=0.82, y=0.58,
            opacity=0.3, shadow=False),
        {"type": "glow", "anchor": "hips", "color": R, "at": "hip flexors", "until": "pulling on your"},
        {"type": "callout", "text": "hip flexors", "anchor": "left_hip", "x": 0.3, "y": 0.3, "at": "hip flexors",
         "until": "pulling on your", "color": "#FFFFFF"},
        img("hero_sore_back", "pulling on your", enter="cut"),
        {"type": "glow", "anchor": "back", "color": R, "at": "your lower back#1"},
        {"type": "pulse", "kind": "impact", "at": "your lower back#1", "duration": 0.2},
    ], camera=[{"at": "That burn is not", "zoom": 1}, {"at": "hip flexors", "zoom": 1.12, "focus": "hips"},
               {"at": "pulling on your", "zoom": 1}, {"at": "your lower back#1", "zoom": 1.15, "focus": "back"}]),
    sc("line2", "Want to fix-0.05", typed([("WANT", "Want to fix"), ("TO", "to fix it"), ("FIX", "fix it"),
                                           ("IT?", "fix it+0.2")], "Press your lower back")),
    sc("fix", "Press your lower back-0.05", [
        img("hero_leg_raise_down", "Press your lower back", "Bend your knees", enter=RISE, width=0.82, y=0.58),
        {"type": "glow", "anchor": "back", "color": G, "at": "into the floor", "until": "Bend your knees"},
        img("hero_reverse_crunch", "Bend your knees", "Lower your legs slowly", width=0.82, y=0.58),
        {"type": "glow", "anchor": "knees", "color": G, "at": "Bend your knees+0.2", "until": "Lower your legs slowly"},
        clip("clip_leg_raise", "Lower your legs slowly", rate=0.55),
        peek("hero_stop_palm", "stop before your back", "Slow and controlled", side="right"),
        img("prop_stopwatch", "Slow and controlled", "Master this first", enter=RISE, motion={"type": "pulse"},
            x=0.8, y=0.3, width=0.2, rotation=-8),
    ], camera=[{"at": "Press your lower back", "zoom": 1}, {"at": "into the floor", "zoom": 1.2, "focus": "back"},
               {"at": "Bend your knees", "zoom": 1}, {"at": "stop before your back", "zoom": 1.25},
               {"at": "Slow and controlled", "zoom": 1}]),
    sc("end", "Master this first-0.05", [
        img("hero_double_biceps", "Master this first", enter=RISE, width=0.8, y=0.6),
    ], bd="rays"),
]
scenes[-1]["backdropColor"] = "#B0B6BE"
sfx = [("start", "sfx_whoosh_big"), ("zero abs", "sfx_pop_soft"), ("back pain", "sfx_pop_soft"),
       ("new chiropractor", "sfx_boing"),
       ("Here's what's", "sfx_click_soft"), ("what's actually", "sfx_click_soft"), ("actually happening", "sfx_click_soft"),
       ("happening", "sfx_click_soft"),
       ("You swing your legs", "sfx_swoosh_up"), ("and feel a burn", "sfx_whoosh_fire"), ("That burn is not", "sfx_whistle_down"),
       ("hip flexors", "sfx_pop_soft"), ("your lower back#1", "sfx_bone_crack"),
       ("Want to fix", "sfx_click_soft"), ("to fix it", "sfx_click_soft"), ("fix it", "sfx_click_soft"),
       ("Press your lower back", "sfx_whoosh_short"), ("into the floor", "sfx_ding"), ("Bend your knees", "sfx_swoosh_up"),
       ("Lower your legs slowly", "sfx_whoosh_soft"), ("stop before your back", "sfx_whistle_tweet"),
       ("Slow and controlled", "sfx_pop_soft"), ("Master this first", "sfx_whistle_up"), ("then level up", "sfx_level_start")]
plan = {"title": "Leg raises hurt your back", "progressBar": False,
        "captions": {"mode": "phrase", "bottom": [["start", "end"]],
                     "hide": [["Here's what's", "You swing your legs"], ["Want to fix", "Press your lower back"]]},
        "scenes": scenes, "sfx": [{"at": a, "src": s} for a, s in sfx]}
json.dump(plan, open("abspain.json", "w"), indent=1, ensure_ascii=False)
