# V2 with the 12-point review applied (bigger H, pose swaps, slow zoom per scene, instant hook title, more sfx,
# comment-bubble CTA, bumper punch). "Rounded shoulders? It's your phone." (owner, 27 Oct): first video on the new clip library. ~30 s, fast:
# clips sped up (rate 1.4) on WHITE scenes (clips are white), image scenes on sand beige, anatomy circles only twice.
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


plan = {
    "title": "Rounded Shoulders? It's Your Phone",
    "canvas": {"background": BG},
    "style": {"accent": YEL},
    "captions": {"mode": "phrase", "look": "clean", "size": 58, "y": 0.82, "maxWords": 3,
                 "keywords": ["phone", "tight", "asleep", "fix", "thirty", "fifteen", "three", "POSTURE"],
                 "hide": [["Here's the fix-0.05", "Three moves-0.05"]]},
    "scenes": [
        sc("hook", "start", [
            img("hero_bad_posture_desk", "start", "It's not bad", enter="cut", id="h", **BODY),
            {**title("ROUNDED SHOULDERS?", "start", "It's your phone", size=125), "animation": "none"},  # readable in frame 1
            pain(0.41, 0.415, "start", "It's not bad", 0.32),
            img("hero_shrug", "It's not bad", "It's your phone", enter="cut", **BODY),
            img("hero_phone_scroll", "It's your phone", enter="cut", id="h", **BODY),
            title("IT'S YOUR PHONE", "It's your phone"),
        ], camera=punch("It's your phone", (0.5, 0.45), 1.2)),
        sc("c_why", "Eight hours-0.05", [
            clip("clip_wrong_posture_desk", "Eight hours", 1.0),
            title("8 HOURS HUNCHED", "Eight hours"),
            sub("CHEST: TIGHT", "chest gets tight", "upper back falls"),
            bubble("anat_muscle_chest", "chest gets tight", "upper back falls", None, x=0.78, y=0.36, size=0.34),
            sub("UPPER BACK: ASLEEP", "upper back falls"),
            bubble("anat_weak_upper_back", "upper back falls", None, None, x=0.78, y=0.36, size=0.34),
        ]),
        sc("fix", "Here's the fix-0.05", [
            text("HERE'S THE FIX", "Here's the fix-0.05", None, 0.47, 170, "#FFFFFF", "cut"),
        ], camera=[{"at": "Here's the fix-0.05", "zoom": 1}, {"at": "fix.+0.05", "zoom": 1}, {"at": "fix.+0.2", "zoom": 1.18}]),
        sc("three", "Three moves-0.05", [
            img("hero_count_3", "Three moves", enter="cut", **BODY),
            title("3 MOVES", "Three moves"),
        ]),
        sc("c_m1", "One: doorway-0.05", [
            clip("clip_doorway_chest_stretch", "One: doorway", 1.3),
            title("#1 CHEST STRETCH", "One: doorway", size=125), sub("30 SECONDS", "thirty seconds"),
        ]),
        sc("c_m2", "Two: band-0.05", [
            clip("clip_band_pull_apart", "Two: band", 1.5),
            title("#2 BAND PULL-APARTS", "Two: band", size=115),
            {"type": "counter", "from": 0, "to": 15, "suffix": " REPS", "duration": 1.0, "x": 0.5, "y": 0.27,
             "size": 120, "color": RED, "at": "fifteen reps"},
        ]),
        sc("c_m3", "Three: supermans-0.05", [
            {**clip("clip_superman", "Three: supermans", 1.4), "width": 1.12, "y": 0.5},  # lying move: bigger, lifted above captions
            title("#3 SUPERMANS", "Three: supermans"), sub("HOLD 3 SEC AT THE TOP", "hold for three"),
        ]),
        sc("after", "Do this daily-0.05", [
            img("hero_good_posture_desk", "Do this daily", "roll back", enter="cut", **BODY),
            title("EVERY DAY", "Do this daily", "roll back"),
            img("hero_lean_confident", "roll back", enter="cut", **BODY),
            title("SHOULDERS BACK", "roll back"),
        ]),
        sc("cta", "Comment POSTURE-0.05", [
            img("hero_point_viewer", "Comment POSTURE", enter="cut", id="h", **BODY),
            title('COMMENT "POSTURE"', "Comment POSTURE", size=120),
            {"type": "comment", "text": "POSTURE \U0001F622", "user": "you", "ago": "now", "likes": "1.2K",
             "x": 0.5, "y": 0.3, "width": 0.7, "size": 50, "at": "Comment POSTURE+0.3", "enter": "pop"},
        ], camera=[{"at": "Comment POSTURE", "zoom": 1}, {"at": "hunched over#2", "zoom": 1.3, "focus": "face"}]),
    ],
    "sfx": [dict(zip(("at", "src", "volume"), e)) for e in [
        ("start", "sfx_whoosh_soft"), ("It's not bad", "sfx_pop_soft"), ("It's your phone", "sfx_ding"),
        ("Eight hours", "sfx_whoosh_soft"), ("chest gets tight", "sfx_pop_soft"), ("upper back falls", "sfx_pop_soft"),
        ("Here's the fix-0.05", "sfx_typing_loud", 1.0), ("fix.+0.15", "sfx_whoosh_big"), ("Three moves", "sfx_pop_soft"),
        ("One: doorway", "sfx_whoosh_soft"), ("Two: band", "sfx_whoosh_soft"), ("fifteen reps", "sfx_counter"),
        ("Three: supermans", "sfx_whoosh_soft"), ("Do this daily", "sfx_whoosh_soft"), ("roll back", "sfx_ding"),
        ("Comment POSTURE", "sfx_whoosh_soft"), ("Comment POSTURE+0.3", "sfx_notification"), ("thirty seconds", "sfx_click_soft"), ("hold for three", "sfx_click_soft")]],
}
json.dump(plan, open("posture2.json", "w"), indent=1, ensure_ascii=False)
