# Videos 1 and 2 of the 30-topic list, option-2 style (see build_abspain2.py): the old approved look
# + reference extras (typed line, grey step numbers, ghost, cartoon sounds). Each video opens on its own
# thumbnail art (project asset "thumb_open"), so the 0.1 s cover flows straight into the first shot.
import json
RED = "#FF4D3D"; GREEN = "#3DDC84"; BLUE = "#3DA5FF"; BLACK = "#111111"; YEL = "#FFD23F"
GREY = "#6E7881"; NUM = "#D5DAE0"
LYING = {"width": 0.82, "y": 0.56}


def img(a, at, until=None, enter="punch", **kw):
    d = {"type": "image", "asset": a, "shadow": True, "enter": enter, "at": at, **kw}
    if until: d["until"] = until
    return d


def ghost(a, at, until=None, **kw):
    return img(a, at, until, enter="fade", opacity=0.3, shadow=False, **kw)


def opener(at, until):
    # the thumbnail itself, full frame, slow push-in: the cover comes alive
    return img("thumb_open", at, until, enter="cut", shadow=False, width=1.0, x=0.5, y=0.5, motion={"type": "zoomIn"})


def poses(frames, at, until=None, **kw):
    d = {"type": "poses", "shadow": True, "crossfade": 0, "enter": "punch", "at": at,
         "frames": [{"asset": a, "at": t} for a, t in frames], **kw}
    if until: d["until"] = until
    return d


def clip(a, at, until=None, rate=1.0, floor=True, frm=0.0):
    d = {"type": "video", "asset": a, "at": at, "rate": rate, "enter": "punch",
         **({"width": 1.0, "y": 0.6} if floor else {"width": 0.72, "y": 0.62})}
    if frm: d["from"] = frm
    if until: d["until"] = until
    return d


def box(t, at, until, color=BLACK, y=0.7, size=104):
    d = {"type": "text", "text": t, "look": "box", "boxColor": color, "x": 0.5, "y": y, "size": size, "align": "center",
         "at": at, "animation": "words"}
    if until: d["until"] = until
    return d


def chip(t, at, until, icon, color=RED, x=0.24, y=0.32):
    d = {"type": "chip", "text": t, "icon": icon, "color": color, "x": x, "y": y, "at": at}
    if until: d["until"] = until
    return d


def glow(anchor, at, until, color, target=None):
    d = {"type": "glow", "anchor": anchor, "color": color, "at": at}
    if until: d["until"] = until
    if target: d["target"] = target
    return d


def number(n, at, until, y=0.3):
    return {"type": "text", "text": n, "look": "giant", "behind": True, "x": 0.5, "y": y, "size": 400, "color": NUM,
            "align": "center", "maxWidth": 1, "animation": "none", "untype": False, "tilt": 0, "at": at, "enter": "pop",
            **({"until": until} if until else {})}


def typed(words, until):
    L = []
    for i, (w, at) in enumerate(words):
        txt = (" ".join(x for x, _ in words[:i + 1]) + " |").replace("\n ", "\n")
        L.append({"type": "text", "text": txt, "x": 0.5, "y": 0.42, "size": 180, "align": "center", "color": GREY,
                  "font": "pop", "maxWidth": 1, "animation": "none", "untype": False, "enter": "cut", "exit": "cut",
                  "stroke": {"color": "#FFFFFF", "width": 0}, "at": at,
                  "until": words[i + 1][1] if i + 1 < len(words) else until})
    return L


def sc(id, start, layers, bd="none", color=None, tr="circle", camera=None, shakes=None):
    s = {"id": id, "start": start, "backdrop": bd, "layers": layers}
    if color: s["backdropColor"] = color
    if bd == "grid": s["backdropOpacity"] = 0.6
    if tr == "circle": s["transition"] = {"type": "circle", "duration": 0.6}
    if tr == "zoom": s["transition"] = {"type": "zoomBlur", "duration": 0.45}
    if camera: s["camera"] = camera
    if shakes: s["shakes"] = [{"at": a} for a in shakes]
    return s


def typing_sfx(phrases):
    return [(p, "sfx_click_soft") for p in phrases]


def save(name, title, keywords, bottom, hide, scenes, sfx):
    plan = {"title": title, "captions": {"mode": "word", "keywords": keywords, "bottom": [bottom], "hide": hide},
            "scenes": scenes, "sfx": [{"at": a, "src": s} for a, s in sfx]}
    json.dump(plan, open(name + ".json", "w"), indent=1, ensure_ascii=False)


# ------------------------------------------------------------------ 1. Why your arms still look small
save("armsmall", "Why Your Arms Still Look Small",
     ["curls", "sleeves", "biceps", "third", "triceps", "train", "diamond", "chair", "pike", "ninety", "curls"],
     ["Your biceps are only", "Send this to"],
     [["start", "every day"], ["Here's what nobody", "Your biceps are only"]],
     [
    sc("hook", "start", [
        opener("start", "every day"),
        poses([("hero_curl_down", "every day"), ("hero_curl_up", "every day+0.3"), ("hero_curl_down", "for a year"),
               ("hero_curl_up", "for a year+0.3")], "every day", "and your sleeves", width=0.8, y=0.62),
        box("CURLS *EVERY DAY*", "every day", "and your sleeves", BLACK),
        chip("365 DAYS", "for a year", "and your sleeves", "calendar", BLUE),
        img("hero_this_small", "and your sleeves"),
        box("SAME *SLEEVES*", "and your sleeves", "Here's what nobody", RED),
        {"type": "pulse", "kind": "edge", "color": RED, "at": "fit the same"},
    ], bd="spotlight", color="#FF8A80", tr=None, shakes=["fit the same"]),
    sc("line", "Here's what nobody-0.05", typed([("HERE'S", "Here's what nobody"), ("WHAT", "what nobody tells"),
                                                 ("NOBODY\n", "nobody tells you"), ("TELLS", "tells you"),
                                                 ("YOU", "tells you+0.25")], "Your biceps are only"), tr="cut"),
    sc("truth", "Your biceps are only-0.05", [
        img("hero_double_biceps", "Your biceps are only", "The other two thirds", id="front"),
        glow("arms", "Your biceps are only+0.2", "The other two thirds", RED, target="front"),
        box("BICEPS = *1/3*", "one third", "The other two thirds", RED),
        img("hero_back_double_biceps", "The other two thirds", "So train them", id="back"),
        ghost("hero_double_biceps", "The other two thirds", "are triceps"),
        glow("arms", "are triceps", "So train them", GREEN, target="back"),
        box("TRICEPS = *2/3*", "are triceps", "So train them", GREEN),
        img("hero_crack_knuckles", "So train them"),
        box("TRAIN *THEM*", "So train them", None, GREEN),
    ], bd="spotlight", color="#7FB2FF"),
    sc("one", "Number one-0.05", [
        number("1", "Number one", None),
        clip("clip_diamond_pushup", "Number one", rate=1.0, frm=1.2),
        box("*DIAMOND* PUSH-UPS", "diamond push-ups", "Hands close", BLACK, y=0.76),
        box("HANDS *CLOSE*", "Hands close", "elbows tight", GREEN, y=0.76),
        box("ELBOWS *TIGHT*", "elbows tight", None, GREEN, y=0.76),
    ], camera=[{"at": "Number one", "zoom": 1}, {"at": "elbows tight", "zoom": 1.15}, {"at": "to your ribs|end", "zoom": 1}]),
    sc("two", "Number two-0.05", [
        number("2", "Number two", None, y=0.2),
        clip("clip_chair_dip", "Number two", rate=1.0, floor=False),
        box("CHAIR *DIPS*", "chair dips", "Elbows straight back", BLACK, y=0.2),
        box("ELBOWS *BACK*", "Elbows straight back", "lower to ninety", GREEN, y=0.2),
        box("DOWN TO *90°*", "lower to ninety", None, GREEN, y=0.2),
    ], camera=[{"at": "Number two", "zoom": 1}, {"at": "lower to ninety", "zoom": 1.15}, {"at": "ninety degrees|end", "zoom": 1}]),
    sc("three", "Number three-0.05", [
        number("3", "Number three", None),
        clip("clip_pike_pushup", "Number three", rate=1.0),
        box("*PIKE* PUSH-UPS", "pike push-ups", "Hips high", BLACK, y=0.76),
        box("HIPS *HIGH*", "Hips high", "head between", GREEN, y=0.76),
        box("HEAD *BETWEEN HANDS*", "head between", None, GREEN, y=0.76, size=92),
    ], camera=[{"at": "Number three", "zoom": 1}, {"at": "head between", "zoom": 1.15}, {"at": "your hands|end", "zoom": 1}]),
    sc("plan", "Three sets of ten-0.1", [
        {"type": "text", "text": "THE PLAN", "until": "three times a week"},
        img("hero_count_3", "Three sets of ten", "three times a week"),
        box("*3* X 10", "Three sets of ten", "three times a week", BLUE, y=0.58, size=120),
        img("hero_clipboard", "three times a week"),
        chip("MON WED FRI", "three times a week", None, "calendar", GREEN, x=0.24, y=0.34),
        box("*3X* A WEEK", "three times a week", None, GREEN, y=0.58, size=120),
    ], bd="grid", color="#B0B6BE", tr="zoom"),
    sc("cta", "Send this to-0.1", [
        img("hero_point_viewer", "Send this to", "only does curls"),
        img("prop_phone", "Send this to", "only does curls", x=0.8, y=0.4, width=0.18, motion={"type": "pulse"}, enter="pop"),
        box("*SEND* THIS", "Send this to", "only does curls", BLACK),
        poses([("hero_curl_down", "only does curls"), ("hero_curl_up", "only does curls+0.3"),
               ("hero_curl_down", "only does curls+0.6"), ("hero_curl_up", "only does curls+0.9")], "only does curls",
              width=0.8, y=0.62),
        box("ONLY *CURLS*", "only does curls", None, RED),
    ], bd="rays", color=YEL),
], [("start", "sfx_whoosh_big"), ("every day", "sfx_whoosh_short"), ("for a year", "sfx_counter"),
    ("and your sleeves", "sfx_whistle_down"), ("fit the same", "sfx_pop_soft")]
   + typing_sfx(["Here's what nobody", "what nobody tells", "nobody tells you", "tells you", "tells you+0.25"])
   + [("Your biceps are only", "sfx_swoosh_up"), ("one third", "sfx_pop_soft"), ("The other two thirds", "sfx_whoosh_short"),
      ("are triceps", "sfx_whistle_up"), ("So train them", "sfx_level_start"),
      ("Number one", "sfx_whistle_tweet"), ("Hands close", "sfx_pop"), ("elbows tight", "sfx_pop_soft"),
      ("Number two", "sfx_whistle_tweet"), ("Elbows straight back", "sfx_pop"), ("lower to ninety", "sfx_pop_soft"),
      ("Number three", "sfx_whistle_tweet"), ("Hips high", "sfx_pop"), ("head between", "sfx_pop_soft"),
      ("Three sets of ten", "sfx_whoosh_swipe"), ("three times a week", "sfx_chime"),
      ("Send this to", "sfx_whoosh_big"), ("only does curls", "sfx_whoosh_soft")])

# ------------------------------------------------------------------ 2. Why your abs workout hurts your back
save("situpback", "Why your abs workout hurts your back",
     ["sit-up", "back", "abs", "hip", "flexors", "arches", "fix", "flatten", "floor", "planks", "glutes", "reverse", "slowly"],
     ["When you sit all", "Send this to"],
     [["start", "is pulling"], ["Here's what's", "When you sit all"], ["Want to fix", "First, flatten"]],
     [
    sc("hook", "start", [
        opener("start", "is pulling"),
        img("hero_sore_back", "is pulling", "not building"),
        glow("back", "your lower back#1", "not building", RED),
        box("LOWER *BACK*", "your lower back#1", "not building", RED),
        {"type": "pulse", "kind": "edge", "color": RED, "at": "your lower back#1"},
        img("hero_what", "not building"),
        box("NOT YOUR *ABS*", "not building", "Here's what's", RED),
    ], bd="spotlight", color="#FF8A80", tr=None, shakes=["your lower back#1"]),
    sc("line1", "Here's what's-0.05", typed([("HERE'S", "Here's what's"), ("WHAT'S\n", "what's actually"),
                                             ("ACTUALLY", "actually happening"), ("HAPPENING", "happening")],
                                            "When you sit all"), tr="cut"),
    sc("why", "When you sit all-0.05", [
        img("hero_sit_floor_explain", "When you sit all", "and your lower back", id="sit"),
        box("SIT ALL THE WAY *UP*", "When you sit all", "your hip flexors", BLACK, y=0.3, size=96),
        glow("hips", "your hip flexors", "and your lower back", RED, target="sit"),
        box("*HIP FLEXORS* LIFT", "your hip flexors", "and your lower back", RED, y=0.3),
        img("hero_sore_back", "and your lower back"),
        glow("back", "arches off", None, RED),
        box("BACK *ARCHES*", "arches off", None, RED),
        {"type": "pulse", "kind": "impact", "at": "arches off", "duration": 0.2},
    ], bd="spotlight", color="#7FB2FF"),
    sc("line2", "Want to fix-0.05", typed([("WANT", "Want to fix"), ("TO", "to fix it"), ("FIX", "fix it"),
                                           ("IT?", "fix it+0.2")], "First, flatten"), tr="cut"),
    sc("one", "First, flatten-0.05", [
        number("1", "First, flatten", None),
        img("hero_glute_bridge_down", "First, flatten", id="flat", **LYING),
        box("BACK *FLAT*", "First, flatten", "Lie down", GREEN, y=0.74),
        box("KNEES *BENT*", "Lie down", "and press your back", GREEN, y=0.74),
        glow("hips", "and press your back", None, GREEN, target="flat"),
        box("PRESS INTO *FLOOR*", "and press your back", "Hold that every rep", GREEN, y=0.74, size=96),
        chip("EVERY REP", "Hold that every rep", None, "check", GREEN, x=0.24, y=0.3),
        box("*HOLD* IT", "Hold that every rep", None, GREEN, y=0.74),
    ], bd="rays", color=GREEN, camera=[{"at": "First, flatten", "zoom": 1}, {"at": "and press your back", "zoom": 1.15, "focus": "hips"},
                                       {"at": "Hold that every rep", "zoom": 1}]),
    sc("two", "Second, swap-0.05", [
        number("2", "Second, swap", None),
        clip("clip_plank", "Second, swap", rate=1.0),
        box("SWAP FOR *PLANKS*", "Second, swap", "Squeeze your glutes", BLACK, y=0.76),
        box("SQUEEZE *GLUTES*", "Squeeze your glutes", "keep one straight line", GREEN, y=0.76),
        box("ONE *STRAIGHT* LINE", "keep one straight line", None, GREEN, y=0.76),
    ], camera=[{"at": "Second, swap", "zoom": 1}, {"at": "Squeeze your glutes", "zoom": 1.12}, {"at": "keep one straight line", "zoom": 1}]),
    sc("three", "Third, reverse crunches-0.05", [
        number("3", "Third, reverse crunches", None),
        poses([("hero_glute_bridge_down", "Third, reverse crunches"), ("hero_reverse_crunch", "Curl your hips up"),
               ("hero_glute_bridge_down", "slowly"), ("hero_reverse_crunch", "don't swing")],
              "Third, reverse crunches", **LYING),
        box("*REVERSE* CRUNCH", "Third, reverse crunches", "Curl your hips up", BLACK, y=0.74),
        box("HIPS UP *SLOWLY*", "Curl your hips up", "don't swing", GREEN, y=0.74),
        box("*NO* SWINGING", "don't swing", None, RED, y=0.74),
    ], bd="rays", color=GREEN),
    sc("plan", "Three sets-0.1", [
        {"type": "text", "text": "THE PLAN", "until": "three times a week"},
        img("hero_count_3", "Three sets", "three times a week"),
        box("*3* SETS", "Three sets", "three times a week", BLUE, y=0.58, size=120),
        img("hero_clipboard", "three times a week"),
        chip("MON WED FRI", "three times a week", None, "calendar", GREEN, x=0.24, y=0.34),
        box("*3X* A WEEK", "three times a week", None, GREEN, y=0.58, size=120),
    ], bd="grid", color="#B0B6BE", tr="zoom"),
    sc("cta", "Send this to-0.1", [
        img("hero_point_viewer", "Send this to", "a hundred sit-ups"),
        img("prop_phone", "Send this to", "a hundred sit-ups", x=0.8, y=0.4, width=0.18, motion={"type": "pulse"}, enter="pop"),
        box("*SEND* THIS", "Send this to", "a hundred sit-ups", BLACK),
        img("hero_tired_sweating", "a hundred sit-ups"),
        box("100 *SIT-UPS* A DAY", "a hundred sit-ups", None, RED, size=96),
    ], bd="rays", color=YEL),
], [("start", "sfx_whoosh_big"), ("is pulling", "sfx_whoosh_short"), ("your lower back#1", "sfx_bone_crack"),
    ("not building", "sfx_whistle_down")]
   + typing_sfx(["Here's what's", "what's actually", "actually happening", "happening"])
   + [("When you sit all", "sfx_swoosh_up"), ("your hip flexors", "sfx_pop"), ("arches off", "sfx_hammer")]
   + typing_sfx(["Want to fix", "to fix it", "fix it"])
   + [("First, flatten", "sfx_whistle_tweet"), ("Lie down", "sfx_pop_soft"), ("and press your back", "sfx_ding"),
      ("Hold that every rep", "sfx_pop"),
      ("Second, swap", "sfx_whistle_tweet"), ("Squeeze your glutes", "sfx_pop_soft"), ("keep one straight line", "sfx_chime"),
      ("Third, reverse crunches", "sfx_whistle_tweet"), ("Curl your hips up", "sfx_swoosh_up"), ("don't swing", "sfx_pop"),
      ("Three sets", "sfx_whoosh_swipe"), ("three times a week", "sfx_chime"),
      ("Send this to", "sfx_whoosh_big"), ("a hundred sit-ups", "sfx_whoosh_soft")])
print("ok")
