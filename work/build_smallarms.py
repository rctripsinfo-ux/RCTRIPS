# Storytelling style (owner, 22 Oct): the story is told by pictures and the voice; almost no on-screen text,
# no word captions, quiet sound effects under a clear voice.
import json
B = "#111111"; R = "#E3262E"; G = "#2FD94E"; Y = "#FFD23F"


def img(a, at, until=None, enter="whip", **kw):
    d = {"type": "image", "asset": a, "shadow": True, "enter": enter, "at": at, **kw}
    if until: d["until"] = until
    return d


def clip(a, at, until=None, rate=1.0, standing=True, enter="whip"):
    geo = {"width": 0.7, "y": 0.6} if standing else {"width": 1.0, "y": 0.56}
    d = {"type": "video", "asset": a, "at": at, **geo, "rate": rate, "enter": enter}
    if until: d["until"] = until
    return d


def big(t, at, until, c=B, y=0.2, size=260):
    return {"type": "text", "text": t, "look": "giant", "behind": True, "x": 0.5, "y": y, "size": size, "color": c,
            "align": "center", "maxWidth": 1, "animation": "letters", "untype": False, "tilt": 0, "at": at, "until": until}


def sc(id, start, layers, tr="whip", bd="none", bdc=None, camera=None, shakes=None):
    s = {"id": id, "start": start, "backdrop": bd, "layers": layers}
    if shakes: s["shakes"] = [{"at": a} for a in shakes]
    if tr == "whip": s["transition"] = {"type": "whip", "duration": 0.32}
    if tr == "zoom": s["transition"] = {"type": "zoomBlur", "duration": 0.45}
    if bdc: s["backdropColor"] = bdc
    if camera: s["camera"] = camera
    return s


slow = {"type": "zoomIn"}
scenes = [
    sc("meet", "start", [
        {"type": "speed", "at": "start"},
        img("hero_wave_hello", "start", "For one whole year", enter="cut", motion=slow),
        clip("clip_hammer_curl_dumbbells", "For one whole year", "Morning curls", rate=1.0),
        {"type": "counter", "from": 1, "to": 365, "prefix": "DAY ", "duration": 1.6, "at": "For one whole year+0.2",
         "until": "Morning curls", "x": 0.5, "y": 0.17, "size": 150, "color": B},
    ], tr=None, camera=[{"at": "start", "zoom": 1.15, "focus": "body"}, {"at": "he did curls", "zoom": 1.3, "focus": "arms"},
                        {"at": "he did curls+0.6", "zoom": 1, "focus": "body"}]),
    sc("routine", "Morning curls-0.1", [
        img("hero_angry_alarm", "Morning curls", "Night curls"),
        img("hero_sleepy_standing", "Night curls", "Hundreds of curls"),
        clip("clip_hammer_curl", "Hundreds of curls", rate=1.8),
        {"type": "speed", "at": "every single day"},
    ]),
    sc("mirror", "Then one day-0.1", [
        img("hero_selfie", "Then one day", "and froze", motion=slow),
        img("hero_shocked", "and froze", "His arms looked", enter="cut"),
        {"type": "pulse", "kind": "impact", "at": "and froze", "duration": 0.2},
        {"type": "speed", "at": "and froze"},
        img("hero_this_small", "His arms looked", motion=slow),
    ], camera=[{"at": "Then one day", "zoom": 1, "focus": "body"}, {"at": "and froze", "zoom": 1.35, "focus": "face"},
               {"at": "His arms looked", "zoom": 1, "focus": "body"}], bd="spotlight", bdc=Y, shakes=["and froze"]),
    sc("quit", "He almost quit-0.1", [
        img("hero_despair_kneel", "He almost quit", motion=slow),
    ], bd="spotlight", bdc=R),
    sc("coach", "Then an old coach-0.1", [
        img("hero_sit_bench_think", "Then an old coach", "Your biceps are only", motion=slow),
        img("hero_double_biceps", "Your biceps are only", "The other two thirds", width=0.8, y=0.66),
        {"type": "glow", "anchor": "arms", "color": R, "at": "Your biceps are only+0.3", "until": "The other two thirds"},
        big("1/3", "one third", "The other two thirds", c=R),
        img("hero_back_double_biceps", "The other two thirds", width=0.8, y=0.66),
        {"type": "glow", "anchor": "arms", "color": G, "at": "are triceps"},
        big("2/3", "two thirds", "end", c=G),
        {"type": "pulse", "kind": "impact", "at": "are triceps", "duration": 0.2},
    ], bd="spotlight", bdc=G),
    sc("never", "H had never-0.1", [
        img("hero_facepalm", "H had never", "Not once"),
        img("hero_shrug", "Not once"),
    ], bd="spotlight", bdc=Y),
    sc("swap", "So he swapped-0.1", [
        img("hero_idea_bulb", "So he swapped", "chair dips"),
        clip("clip_chair_dip", "chair dips", "diamond push-ups", rate=1.2),
        dict(clip("clip_diamond_pushup", "diamond push-ups", "Three sets", rate=1.2, standing=False), **{"from": 1.2}),
        img("hero_count_3", "Three sets", "Slow on the way down"),
        clip("clip_chair_dip", "Slow on the way down", rate=0.6),
    ]),
    sc("later", "Three months later-0.1", [
        img("hero_walk_toward", "Three months later", "his sleeves got tight", motion=slow),
        img("hero_selfie", "his sleeves got tight", "Same effort"),
        {"type": "glow", "anchor": "arms", "color": G, "at": "his sleeves got tight+0.2", "until": "Same effort"},
        img("hero_smirk", "Same effort", "Smarter plan"),
        img("hero_double_biceps", "Smarter plan", motion=slow),
    ], tr="zoom", bd="spotlight", bdc=G),
    sc("cta", "Send this to-0.1", [
        img("hero_point_viewer", "Send this to", "only does curls"),
        {"type": "image", "asset": "prop_phone", "at": "Send this to", "until": "only does curls", "x": 0.8, "y": 0.4,
         "width": 0.18, "motion": {"type": "pulse"}},
        img("hero_curl_up", "only does curls", motion=slow),
    ], bd="rays", bdc=Y),
]
sfx = [("start", "sfx_pop"), ("For one whole year", "sfx_counter"),
       ("Morning curls", "sfx_whoosh_short"), ("Night curls", "sfx_swish"), ("Hundreds of curls", "sfx_whoosh_fast"),
       ("he flexed in the mirror", "sfx_camera"), ("and froze", "sfx_shocked"), ("He almost quit", "sfx_wind"),
       ("Then an old coach", "sfx_whoosh_soft"), ("Your biceps are only", "sfx_sparkle"), ("are triceps", "sfx_hammer"),
       ("Not once", "sfx_pop_2"), ("So he swapped", "sfx_ding"), ("chair dips", "sfx_whoosh_swipe"),
       ("diamond push-ups", "sfx_whoosh_short"), ("Three sets", "sfx_desk_bell"), ("Three months later", "sfx_whoosh_big"),
       ("his sleeves got tight", "sfx_magic"), ("Smarter plan", "sfx_chime"), ("Send this to", "sfx_whoosh_soft"),
       ("only does curls", "sfx_gold_bell")]
plan = {"title": "Why your arms still look small", "progressBar": True,
        "captions": {"mode": "none"},
        "audio": {"sfxVolume": 0.3},
        "scenes": scenes, "sfx": [{"at": a, "src": s} for a, s in sfx]}
json.dump(plan, open("smallarms.json", "w"), indent=1)
