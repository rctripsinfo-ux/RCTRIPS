# Option 2 style (owner, 23 Oct): the old approved look (examples/plans/08: big H in every frame, word captions,
# box labels, chips, red/green glows, mood backgrounds, circle transitions, "Send this to" ending)
# + from the reference shorts: empty-screen line typed word by word with a cursor, a big grey number behind each
# step, a faded ghost of the other position, fire behind H, cartoon whistles, music ~13 dB under the voice.
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


def poses(frames, at, until=None, **kw):
    d = {"type": "poses", "shadow": True, "crossfade": 0, "enter": "punch", "at": at,
         "frames": [{"asset": a, "at": t} for a, t in frames], **kw}
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


def number(n, at, until):
    return {"type": "text", "text": n, "look": "giant", "behind": True, "x": 0.5, "y": 0.3, "size": 400, "color": NUM,
            "align": "center", "maxWidth": 1, "animation": "none", "untype": False, "tilt": 0, "at": at, "until": until,
            "enter": "pop"}


def typed(words, until):
    # reference: empty screen, the line typed WORD BY WORD in sync with the voice, thin cursor at the end
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
    if tr == "circle": s["transition"] = {"type": "circle", "duration": 0.6}
    if tr == "zoom": s["transition"] = {"type": "zoomBlur", "duration": 0.45}
    if camera: s["camera"] = camera
    if shakes: s["shakes"] = [{"at": a} for a in shakes]
    return s


scenes = [
    sc("hook", "start", [
        {"type": "speed", "at": "start"},
        poses([("hero_leg_raise_down", "start"), ("hero_leg_raise_up", "start+0.35"), ("hero_leg_raise_down", "start+0.7"),
               ("hero_leg_raise_up", "start+1.05"), ("hero_leg_raise_down", "like that"), ("hero_leg_raise_up", "like that+0.35")],
              "start", "zero abs", enter="cut", **LYING),
        box("LEG RAISES *LIKE THIS?*", "start", "zero abs", BLACK, y=0.36),
        img("hero_this_small", "zero abs", "back pain"),
        box("*0* ABS", "zero abs", "back pain", RED),
        img("hero_sore_back", "back pain", "maybe a new"),
        glow("back", "back pain+0.1", "maybe a new", RED),
        box("BACK *PAIN*", "back pain", "maybe a new", RED),
        {"type": "pulse", "kind": "edge", "color": RED, "at": "back pain"},
        img("hero_facepalm", "maybe a new", "Here's what's"),
        box("NEW *CHIROPRACTOR*", "new chiropractor", "Here's what's", RED, size=92),
    ], bd="spotlight", color="#FF8A80", tr=None, shakes=["new chiropractor"]),
    sc("line1", "Here's what's-0.05", typed([("HERE'S", "Here's what's"), ("WHAT'S\n", "what's actually"),
                                             ("ACTUALLY", "actually happening"), ("HAPPENING", "happening")],
                                            "You swing your legs"), tr="cut"),
    sc("burn", "You swing your legs-0.05", [
        poses([("hero_leg_raise_down", "You swing your legs"), ("hero_leg_raise_up", "You swing your legs+0.25"),
               ("hero_leg_raise_down", "You swing your legs+0.5"), ("hero_leg_raise_up", "up fast")],
              "You swing your legs", "and feel a burn", **LYING),
        box("*SWINGING* FAST", "You swing your legs", "and feel a burn", BLACK, y=0.36),
        img("prop_fire", "and feel a burn", "That burn is not", enter="pop", motion={"type": "pulse"}, x=0.5, y=0.5,
            width=0.62, behind=True, shadow=False),
        img("hero_leg_raise_up", "and feel a burn", "pulling on your", motion={"type": "shake", "amount": 0.4}, id="up", **LYING),
        ghost("hero_leg_raise_down", "That burn is not", "pulling on your", **LYING),
        box("BURN?", "and feel a burn", "That burn is not", RED, y=0.2),
        box("NOT YOUR *ABS*", "That burn is not", "hip flexors", RED, y=0.2),
        glow("hips", "hip flexors", "pulling on your", RED, target="up"),
        box("*HIP* FLEXORS", "hip flexors", "pulling on your", RED, y=0.2),
        img("hero_sore_back", "pulling on your"),
        glow("back", "your lower back#1", None, RED),
        box("PULLS YOUR *BACK*", "pulling on your", None, RED),
        {"type": "pulse", "kind": "edge", "color": RED, "at": "your lower back#1"},
    ], bd="spotlight", color="#7FB2FF"),
    sc("line2", "Want to fix-0.05", typed([("WANT", "Want to fix"), ("TO", "to fix it"), ("FIX", "fix it"),
                                           ("IT?", "fix it+0.2")], "Press your lower back"), tr="cut"),
    sc("fix", "Press your lower back-0.05", [
        number("1", "Press your lower back", "Bend your knees"),
        img("hero_glute_bridge_down", "Press your lower back", "Lower your legs slowly", id="flat", **LYING),
        glow("hips", "into the floor", "Bend your knees", GREEN, target="flat"),
        box("BACK *FLAT*", "Press your lower back", "Bend your knees", GREEN, y=0.74),
        number("2", "Bend your knees", "Lower your legs slowly"),
        glow("knees", "Bend your knees+0.1", "Lower your legs slowly", GREEN, target="flat"),
        box("KNEES *BENT*", "Bend your knees", "Lower your legs slowly", GREEN, y=0.74),
        number("3", "Lower your legs slowly", "Three sets of ten"),
        poses([("hero_leg_raise_up", "Lower your legs slowly"), ("hero_leg_raise_down", "and stop before")],
              "Lower your legs slowly", "Three sets of ten", **LYING),
        ghost("hero_leg_raise_down", "Lower your legs slowly", "and stop before", **LYING),
        box("*SLOWLY* DOWN", "Lower your legs slowly", "and stop before", GREEN, y=0.42),
        chip("STOP HERE", "and stop before", "Three sets of ten", "warning", RED, x=0.24, y=0.3),
        box("BACK STAYS *DOWN*", "and stop before", "Three sets of ten", GREEN, y=0.42, size=96),
    ], bd="rays", color=GREEN, camera=[{"at": "Press your lower back", "zoom": 1}, {"at": "into the floor", "zoom": 1.12, "focus": "hips"},
                                       {"at": "Bend your knees", "zoom": 1.12, "focus": "knees"},
                                       {"at": "Lower your legs slowly", "zoom": 1}]),
    sc("plan", "Three sets of ten-0.1", [
        {"type": "text", "text": "THE PLAN", "until": "slow and controlled"},
        img("hero_count_3", "Three sets of ten", "slow and controlled"),
        box("*3* X 10", "Three sets of ten", "slow and controlled", BLUE, y=0.58, size=120),
        img("hero_clipboard", "slow and controlled"),
        chip("SLOW", "slow and controlled", None, "timer", GREEN, x=0.24, y=0.34),
        box("*CONTROLLED*", "slow and controlled", None, GREEN, y=0.58),
    ], bd="grid", color="#B0B6BE", tr="zoom"),
    sc("cta", "Send this to-0.1", [
        img("hero_point_viewer", "Send this to", "swings his legs"),
        img("prop_phone", "Send this to", "swings his legs", x=0.8, y=0.4, width=0.18, motion={"type": "pulse"}, enter="pop"),
        box("*SEND* THIS", "Send this to", "swings his legs", BLACK),
        poses([("hero_leg_raise_down", "swings his legs"), ("hero_leg_raise_up", "swings his legs+0.3"),
               ("hero_leg_raise_down", "swings his legs+0.6"), ("hero_leg_raise_up", "swings his legs+0.9")],
              "swings his legs", **LYING),
        box("SWINGS HIS *LEGS*", "swings his legs", None, RED, y=0.36),
    ], bd="rays", color=YEL),
]
scenes[2]["layers"] = [l for l in scenes[2]["layers"]]
for s in scenes:
    if s["id"] == "plan": s["backdropOpacity"] = 0.6
sfx = [("start", "sfx_whoosh_big"), ("zero abs", "sfx_whistle_down"), ("back pain", "sfx_bone_crack"),
       ("new chiropractor", "sfx_boing"),
       ("Here's what's", "sfx_click_soft"), ("what's actually", "sfx_click_soft"), ("actually happening", "sfx_click_soft"),
       ("happening", "sfx_click_soft"),
       ("You swing your legs", "sfx_swoosh_up"), ("and feel a burn", "sfx_whoosh_fire"), ("That burn is not", "sfx_shocked_2"),
       ("hip flexors", "sfx_pop"), ("your lower back#1", "sfx_hammer"),
       ("Want to fix", "sfx_click_soft"), ("to fix it", "sfx_click_soft"), ("fix it", "sfx_click_soft"),
       ("Press your lower back", "sfx_whistle_up"), ("into the floor", "sfx_ding"), ("Bend your knees", "sfx_pop_soft"),
       ("Lower your legs slowly", "sfx_whoosh_soft"), ("and stop before", "sfx_whistle_tweet"),
       ("Three sets of ten", "sfx_whoosh_swipe"), ("slow and controlled", "sfx_chime"),
       ("Send this to", "sfx_whoosh_big"), ("swings his legs", "sfx_crying_laugh")]
plan = {"title": "Leg raises hurt your back (option 2)",
        "captions": {"mode": "word", "keywords": ["leg", "abs", "pain", "chiropractor", "burn", "hip", "flexors", "back",
                                                  "fix", "floor", "knees", "slowly", "controlled"],
                     "bottom": [["You swing your legs", "Send this to"]],
                     "hide": [["Here's what's", "You swing your legs"], ["Want to fix", "Press your lower back"]]},
        "scenes": scenes, "sfx": [{"at": a, "src": s} for a, s in sfx]}
json.dump(plan, open("abspain2.json", "w"), indent=1, ensure_ascii=False)
