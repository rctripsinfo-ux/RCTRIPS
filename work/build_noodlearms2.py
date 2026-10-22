# Reference style (Captain-Workout-type explainer, owner 22 Oct): H, white background, hook insult ->
# "LET ME FIX THAT" typed -> the truth -> 3 numbered moves (big grey number behind) -> short close.
# Small phrase captions at the bottom, no music, quiet sounds, a new picture every 1-2 s.
import json
B = "#111111"; R = "#E3262E"; G = "#2FD94E"; GREY = "#9AA4AD"; LIGHT = "#E3E7EB"
STAND = {"width": 0.8, "y": 0.6}


def img(a, at, until=None, enter="punch", **kw):
    d = {"type": "image", "asset": a, "shadow": True, "enter": enter, "at": at, **kw}
    if until: d["until"] = until
    return d


def ghost(a, at, until=None, **kw):
    # faded copy of the other position of the movement (reference "ghost" look)
    return img(a, at, until, enter="fade", opacity=0.28, shadow=False, **kw)


def clip(a, at, until=None, rate=1.0, floor=True, frm=0.0, enter="punch"):
    d = {"type": "video", "asset": a, "at": at, "rate": rate, "enter": enter,
         **({"width": 1.0, "y": 0.6} if floor else {"width": 0.72, "y": 0.6})}
    if frm: d["from"] = frm
    if until: d["until"] = until
    return d


def number(n, at, until):
    # huge faded number behind the exercise
    return {"type": "text", "text": n, "look": "giant", "behind": True, "x": 0.5, "y": 0.36, "size": 400, "color": LIGHT,
            "align": "center", "maxWidth": 1, "animation": "none", "untype": False, "tilt": 0, "at": at, "until": until,
            "enter": "pop"}


def typed(t, at, until):
    return {"type": "text", "text": t, "x": 0.5, "y": 0.45, "size": 150, "align": "center", "color": GREY,
            "animation": "typewriter", "cps": 18, "untype": False, "stroke": {"color": "#FFFFFF", "width": 0},
            "at": at, "until": until}


def sc(id, start, layers, tr="cut", bd="none", camera=None):
    s = {"id": id, "start": start, "backdrop": bd, "layers": layers}
    if tr == "whip": s["transition"] = {"type": "whip", "duration": 0.28}
    if camera: s["camera"] = camera
    return s


scenes = [
    sc("hook", "start", [
        {"type": "speed", "at": "start"},
        img("hero_curl_up", "start", "but your arms", enter="zoom", motion={"type": "shake", "amount": 0.6}, **STAND),
        ghost("hero_curl_down", "start+0.5", "but your arms", **STAND),
        img("hero_beginner", "but your arms", motion={"type": "zoomIn"}, **STAND),
        img("prop_red_x", "two dry noodles", x=0.78, y=0.42, width=0.2, enter="pop"),
    ], camera=[{"at": "start", "zoom": 1}, {"at": "two dry noodles", "zoom": 1.3}, {"at": "two dry noodles+0.7", "zoom": 1}]),
    sc("secret", "Here's what nobody-0.05", [
        img("hero_whisper", "Here's what nobody", width=0.78, y=0.64, enter="punch"),
        {"type": "text", "text": "NOBODY TELLS YOU", "x": 0.5, "y": 0.2, "size": 120, "align": "center", "color": GREY,
         "animation": "words", "untype": False, "behind": True, "stroke": {"color": "#FFFFFF", "width": 0},
         "at": "what nobody", "until": "end"},
    ]),
    sc("truth", "Biceps don't make-0.1", [
        img("hero_double_biceps", "Biceps don't make", "Triceps do", **STAND),
        {"type": "glow", "anchor": "arms", "color": R, "at": "Biceps don't make", "until": "Triceps do"},
        img("hero_back_double_biceps", "Triceps do", "Here are three moves", **STAND),
        {"type": "glow", "anchor": "arms", "color": G, "at": "Triceps do+0.15", "until": "Here are three moves"},
        {"type": "callout", "text": "2/3", "anchor": "left_arm", "x": 0.2, "y": 0.3, "at": "two thirds",
         "until": "Here are three moves", "color": G},
        img("hero_count_3", "Here are three moves", **STAND),
    ], tr="whip"),
    sc("one", "First, diamond push-ups-0.1", [
        number("1", "First, diamond push-ups", "end"),
        clip("clip_diamond_pushup", "First, diamond push-ups", rate=0.85, frm=1.2),
    ], tr="whip", camera=[{"at": "First, diamond push-ups", "zoom": 1}, {"at": "elbows tight to your ribs", "zoom": 1.25},
                          {"at": "chest down to your thumbs", "zoom": 1.1}, {"at": "chest down to your thumbs+1.0", "zoom": 1}]),
    sc("two", "Second, chair dips-0.1", [
        number("2", "Second, chair dips", "end"),
        clip("clip_chair_dip", "Second, chair dips", rate=0.85, floor=False),
    ], tr="whip", camera=[{"at": "Second, chair dips", "zoom": 1}, {"at": "Hands behind you", "zoom": 1.2},
                          {"at": "elbows point straight back", "zoom": 1}, {"at": "ninety degrees", "zoom": 1.3},
                          {"at": "ninety degrees+0.9", "zoom": 1}]),
    sc("three", "Third, pike push-ups-0.1", [
        number("3", "Third, pike push-ups", "end"),
        clip("clip_pike_pushup", "Third, pike push-ups", rate=0.85),
    ], tr="whip", camera=[{"at": "Third, pike push-ups", "zoom": 1}, {"at": "Hips high", "zoom": 1.2},
                          {"at": "head down between", "zoom": 1}, {"at": "then press back up", "zoom": 1.15},
                          {"at": "then press back up+0.8", "zoom": 1}]),
    sc("plan", "Three sets of ten-0.1", [
        img("hero_clipboard", "Three sets of ten", "three times a week", **STAND),
        img("hero_count_3", "three times a week", **STAND),
    ], tr="whip"),
    sc("close", "No more noodles-0.1", [
        img("hero_beginner", "No more noodles", "Just arms", **STAND),
        img("prop_red_x", "No more noodles+0.2", "Just arms", x=0.78, y=0.42, width=0.2, enter="pop"),
        img("hero_double_biceps", "Just arms", enter="zoom", **STAND),
    ], tr="whip", bd="rays"),
]
scenes[-1]["backdropColor"] = "#B0B6BE"
sfx = [("start", "sfx_swoosh_up"), ("but your arms", "sfx_whistle_down"), ("two dry noodles", "sfx_boing"),
       ("Here's what nobody", "sfx_sparkle"), ("Biceps don't make", "sfx_pop_soft"), ("Triceps do", "sfx_whistle_up"),
       ("two thirds", "sfx_pop_soft"), ("Here are three moves", "sfx_whoosh_short"),
       ("First, diamond push-ups", "sfx_whistle_tweet"), ("elbows tight to your ribs", "sfx_swoosh_up"),
       ("Second, chair dips", "sfx_whistle_tweet"), ("Hands behind you", "sfx_swoosh_up"), ("ninety degrees", "sfx_pop_soft"),
       ("Third, pike push-ups", "sfx_whistle_tweet"), ("Hips high", "sfx_swoosh_up"), ("Three sets of ten", "sfx_whoosh_soft"),
       ("No more noodles", "sfx_whistle_down"), ("Just arms", "sfx_whistle_up"), ("Just arms+0.6", "sfx_chime")]
plan = {"title": "Noodle arms fix", "progressBar": False,
        "captions": {"mode": "phrase", "bottom": [["start", "end"]], "hide": [["Here's what nobody", "Biceps don't make"]]},
        "scenes": scenes, "sfx": [{"at": a, "src": s} for a, s in sfx]}
json.dump(plan, open("noodlearms2.json", "w"), indent=1, ensure_ascii=False)
