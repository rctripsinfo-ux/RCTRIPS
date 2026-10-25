# "I Did Dead Hangs Every Day for 30 Days" (owner, 25 Oct): remake of the old channel's best video (15.8K views,
# 101 subs) in the new-channel rules: ~30 s, H hanging with the hook text from frame 1, one idea, simple and smooth
# (white background, cuts between scenes, fades inside), big grey day number behind H, red = struggle, green = progress.
import json
RED = "#FF4D3D"; GREEN = "#3DDC84"; BLACK = "#111111"; NUM = "#D5DAE0"
HANG = {"width": 0.78, "y": 0.5}
STAND = {"width": 0.8, "y": 0.5}


def img(a, at, until=None, enter="fade", **kw):
    d = {"type": "image", "asset": a, "shadow": True, "enter": enter, "at": at, **kw}
    if until: d["until"] = until
    return d


def clip(a, at, until=None):
    d = {"type": "video", "asset": a, "at": at, "enter": "fade", "width": 1.0, "y": 0.5}
    if until: d["until"] = until
    return d


def box(t, at, until, color=BLACK, y=0.67, size=96):
    d = {"type": "text", "text": t, "look": "box", "boxColor": color, "x": 0.5, "y": y, "size": size, "align": "center",
         "at": at, "animation": "words"}
    if until: d["until"] = until
    return d


def glow(anchor, at, until, color, target="h"):
    d = {"type": "glow", "anchor": anchor, "color": color, "at": at, "target": target}
    if until: d["until"] = until
    return d


def day(n, at):
    # giant grey "DAY n" behind H
    return {"type": "text", "text": f"DAY {n}", "look": "giant", "behind": True, "x": 0.5, "y": 0.3, "size": 260,
            "color": NUM, "align": "center", "maxWidth": 1, "animation": "none", "untype": False, "tilt": 0,
            "at": at, "enter": "fade"}


def sc(id, start, layers, camera=None):
    d = {"id": id, "start": start, "backdrop": "none", "layers": layers}
    if camera: d["camera"] = camera
    return d


INK = "#16191D"; SUB = "#5B6670"
HANG_CLIP = {"width": 0.78, "y": 0.58}
BODY = {"width": 0.7, "y": 0.6}


def title(t, at, until=None):
    # section heading at the top: big, clean, no box
    d = {"type": "text", "text": t, "x": 0.5, "y": 0.1, "size": 150, "align": "center", "color": INK, "font": "pop",
         "maxWidth": 0.9, "animation": "none", "untype": False, "enter": "fade", "exit": "cut",
         "stroke": {"color": "#FFFFFF", "width": 0}, "at": at}
    if until: d["until"] = until
    return d


def sub(t, at, until=None):
    # one short line under the heading, swaps with the voice
    d = {"type": "text", "text": t, "x": 0.5, "y": 0.165, "size": 64, "align": "center", "color": SUB, "font": "pop",
         "maxWidth": 0.9, "animation": "none", "untype": False, "enter": "fade", "exit": "cut",
         "stroke": {"color": "#FFFFFF", "width": 0}, "at": at}
    if until: d["until"] = until
    return d


plan = {
    "title": "I Did Dead Hangs Every Day for 30 Days",
    "captions": {"mode": "phrase", "look": "clean", "size": 56, "y": 0.8, "maxWords": 3,
                 "keywords": ["thirty", "fire", "grip", "minute", "shoulders", "forearms", "pull-ups", "five"]},
    "scenes": [
        # one continuous hang clip from the first frame to Day 30 (no clip restarts = no blank frames)
        sc("hang", "start", [
            {"type": "video", "asset": "clip_dead_hang", "at": "start", "enter": "cut", **HANG_CLIP},
            title("30 DAYS", "start", "Day one"), sub("OF DEAD HANGS", "start", "Day one"),
            title("DAY 1", "Day one", "Day seven"), sub("20 SECONDS", "twenty seconds", "on fire"),
            sub("HANDS ON FIRE", "on fire", "Day seven"),
            title("DAY 7", "Day seven", "Day fourteen"), sub("40 SECONDS", "forty seconds", "stopped slipping"),
            sub("GRIP LOCKED IN", "stopped slipping", "Day fourteen"),
            title("DAY 14", "Day fourteen"), sub("1 MINUTE", "one full minute", "shoulders"),
            sub("SHOULDERS LOOSER", "shoulders"),
        ]),
        sc("d30", "Day thirty-0.05", [
            img("hero_double_biceps", "Day thirty", id="h", enter="cut", **BODY),
            title("DAY 30", "Day thirty"), sub("2 MINUTES", "two minutes", "thicker forearms"),
            glow("forearms", "thicker forearms", None, "#FF4D3D"),
            sub("THICKER FOREARMS", "thicker forearms", "pull-ups felt"),
            sub("PULL-UPS FEEL EASY", "pull-ups felt"),
        ]),
        sc("try", "Try it-0.05", [
            img("hero_look_up_bar", "Try it", enter="cut", **BODY),
            title("TRY IT", "Try it"), sub("HANG EVERY DAY", "Try it", "add five"),
            sub("+5 SECONDS EACH TIME", "add five"),
        ]),
        sc("cta", "Send this to-0.05", [
            img("hero_point_viewer", "Send this to", enter="cut", **BODY),
            title("SEND THIS", "Send this to"), sub("TO YOUR WEAKEST-GRIP FRIEND", "Send this to"),
        ]),
    ],
    "sfx": [{"at": a, "src": s} for a, s in [
        ("start", "sfx_whoosh_soft"),
        ("Day one", "sfx_pop_soft"), ("on fire", "sfx_pop_soft"),
        ("Day seven", "sfx_pop_soft"), ("stopped slipping", "sfx_ding"),
        ("Day fourteen", "sfx_pop_soft"), ("shoulders", "sfx_ding"),
        ("Day thirty", "sfx_whoosh_soft"), ("thicker forearms", "sfx_ding"), ("pull-ups felt", "sfx_pop_soft"),
        ("Try it", "sfx_whoosh_soft"), ("add five", "sfx_pop_soft"),
        ("Send this to", "sfx_whoosh_soft")]],
}
json.dump(plan, open("deadhang30.json", "w"), indent=1, ensure_ascii=False)
