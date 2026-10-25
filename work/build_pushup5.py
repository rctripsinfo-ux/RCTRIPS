# "STOP These 5 Push Up Mistakes!" (owner, 25 Oct): simple and smooth. White background the whole video,
# hard cuts between scenes, fades inside them, one label at a time, red = the mistake, green = the fix,
# small clean captions at the bottom, few soft sounds. Opens on the thumbnail (project asset "thumb_open").
import json
RED = "#FF4D3D"; GREEN = "#3DDC84"; BLACK = "#111111"; NUM = "#D5DAE0"
FLOOR = {"width": 0.95, "y": 0.55}


def img(a, at, until=None, enter="fade", **kw):
    d = {"type": "image", "asset": a, "shadow": True, "enter": enter, "at": at, **kw}
    if until: d["until"] = until
    return d


def opener(at, until):
    return img("thumb_open", at, until, enter="cut", shadow=False, width=1.0, x=0.5, y=0.5, motion={"type": "zoomIn"})


def poses(frames, at, until=None, **kw):
    d = {"type": "poses", "shadow": True, "crossfade": 0, "enter": "fade", "at": at,
         "frames": [{"asset": a, "at": t} for a, t in frames], **kw}
    if until: d["until"] = until
    return d


def clip(a, at, rate=1.0):
    return {"type": "video", "asset": a, "at": at, "rate": rate, "enter": "fade", "width": 1.0, "y": 0.55}


def box(t, at, until, color=BLACK, y=0.75, size=100):
    d = {"type": "text", "text": t, "look": "box", "boxColor": color, "x": 0.5, "y": y, "size": size, "align": "center",
         "at": at, "animation": "words"}
    if until: d["until"] = until
    return d


def glow(anchor, at, until, color, target="p"):
    d = {"type": "glow", "anchor": anchor, "color": color, "at": at, "target": target}
    if until: d["until"] = until
    return d


def number(n, at):
    return {"type": "text", "text": n, "look": "giant", "behind": True, "x": 0.5, "y": 0.27, "size": 400, "color": NUM,
            "align": "center", "maxWidth": 1, "animation": "none", "untype": False, "tilt": 0, "at": at, "enter": "fade"}


def sc(id, start, layers):
    return {"id": id, "start": start, "backdrop": "none", "layers": layers}


def mistake(n, word, bad, fix):
    """bad: (pose, [(anchor, label, at, until)]); fix: [(label, at, until)] shown over the push-up clip."""
    pose, marks = bad
    L = [number(n, f"Mistake {word}")]
    L.append(img(pose, f"Mistake {word}", fix[0][1], id="p", **FLOOR))
    for anchor, label, at, until in marks:
        if anchor: L.append(glow(anchor, at, until, RED))
        L.append(box(label, at, until, RED))
    L.append(clip("clip_pushup", fix[0][1]))
    for label, at, until in fix:
        L.append(box(label, at, until, GREEN))
    return sc(f"m{n}", f"Mistake {word}-0.05", L)


plan = {
    "title": "STOP These 5 Push Up Mistakes!",
    "captions": {"mode": "phrase", "look": "clean", "size": 58, "y": 0.88, "maxWords": 3,
                 "keywords": ["mistakes", "neck", "shoulders", "forty-five", "hips", "glutes", "chest", "forward"],
                 "hide": [["start", "but only if"]]},
    "scenes": [
        sc("hook", "start", [
            opener("start", "but only if"),
            img("hero_pushup_top", "but only if", "Odds are", **FLOOR),
            box("DO THEM *RIGHT*", "do them right", "Odds are", GREEN),
            img("hero_point_viewer", "Odds are", width=0.8, y=0.5),
            box("*5* MISTAKES", "five mistakes", None, RED),
        ]),
        mistake("1", "one", ("hero_pushup_top", [("neck", "LOOKING *UP*", "looking up", "Look at the floor")]),
                [("LOOK *DOWN*", "Look at the floor", None)]),
        mistake("2", "two", ("hero_pushup_mid", [("elbows", "ELBOWS *FLARED*", "elbows flared", "That puts your"),
                                                 ("shoulders", "SHOULDERS *AT RISK*", "That puts your", "Tuck them")]),
                [("TUCK TO *45°*", "Tuck them", None)]),
        mistake("3", "three", ("hero_pushup_top", [("hips", "HIPS *SAG*", "sagging hips", "That crushes"),
                                                   ("back", "LOWER BACK *PAIN*", "That crushes", "Squeeze your")]),
                [("SQUEEZE *GLUTES*", "Squeeze your", "one straight line"), ("ONE *STRAIGHT* LINE", "one straight line", None)]),
        mistake("4", "four", ("hero_pushup_top", [("shoulders", "SHOULDERS *ROLLED*", "shoulders rolled", "Your chest"),
                                                  ("chest", "CHEST *OFF*", "Your chest", "Pull them back")]),
                [("SHOULDERS *BACK*", "Pull them back", None)]),
        sc("m5", "Mistake five-0.05", [
            number("5", "Mistake five"),
            poses([("hero_pushup_top", "Mistake five"), ("hero_pushup_mid", "straight up"), ("hero_pushup_top", "and down"),
                   ("hero_pushup_mid", "and down+0.4")], "Mistake five", "Push the floor", **FLOOR),
            box("STRAIGHT *UP & DOWN*", "going straight", "Push the floor", RED, size=92),
            clip("clip_pushup", "Push the floor", rate=0.9),
            box("PUSH *FORWARD* + UP", "Push the floor", None, GREEN, size=92),
        ]),
        sc("cta", "Send this to-0.05", [
            img("hero_point_viewer", "Send this to", "whose push-ups", width=0.8, y=0.5),
            img("prop_phone", "Send this to", "whose push-ups", x=0.8, y=0.38, width=0.18, enter="fade"),
            box("*SEND* THIS", "Send this to", "whose push-ups", BLACK),
            img("hero_thumbs_up", "whose push-ups", width=0.8, y=0.5),
            box("FIX YOUR *PUSH-UPS*", "whose push-ups", None, GREEN),
        ]),
    ],
    "sfx": [{"at": a, "src": s} for a, s in [
        ("but only if", "sfx_whoosh_soft"), ("five mistakes", "sfx_pop_soft"),
        ("Mistake one", "sfx_whoosh_soft"), ("Look at the floor", "sfx_ding"),
        ("Mistake two", "sfx_whoosh_soft"), ("Tuck them", "sfx_ding"),
        ("Mistake three", "sfx_whoosh_soft"), ("Squeeze your", "sfx_ding"),
        ("Mistake four", "sfx_whoosh_soft"), ("Pull them back", "sfx_ding"),
        ("Mistake five", "sfx_whoosh_soft"), ("Push the floor", "sfx_ding"),
        ("Send this to", "sfx_whoosh_soft"), ("whose push-ups", "sfx_pop_soft")]],
}
json.dump(plan, open("pushup5.json", "w"), indent=1, ensure_ascii=False)
