# Reference demo (owner, 31 Oct): an original remake of ref V06 "How Many Push-Ups Do You Really Need?" with H on
# our beige background. Same structure: cover -> close-up zoom-out hook -> "looks tough" flex with speed lines ->
# frustration beat -> bumper -> "only 3" -> #1 hand placement / #2 range of motion / #3 core control, each with
# guides on the body (ref V06 technique) -> recap -> sunglasses ending. Own words, own voice, no ref audio.
import json, os
from PIL import Image, ImageDraw, ImageFont
from h_kit import *

use_preset("beige")
S = open("pushdemo.txt").read()
PUSH = {"autoAlign": False, "width": 0.92, "y": 0.55}  # side-view floor poses: body sits at y 0.41-0.69
SMALL = {"width": 0.66, "y": 0.66}                     # hook: H smaller so the push-up bubble fits above
pt = lambda a, part, L: body_xy(a, part, L["width"], L["y"], L.get("x", 0.5))
chest = pt("hero_facepalm", "chest", BODY)
sh, wr = pt("hero_pushup_top_v3", "shoulder_l", PUSH), pt("hero_pushup_top_v3", "wrist_l", PUSH)
sh_low = pt("hero_pushup_mid", "shoulder_l", PUSH)
hip, ank, shp = pt("hero_plank", "hip_l", PUSH), pt("hero_plank", "ankle_l", PUSH), pt("hero_plank", "shoulder_l", PUSH)
floor = round(wr[1] + 0.01, 3)


def ring(xy, at, until=None, w=0.07):
    d = {"type": "highlight", "shape": "circle", "x": xy[0], "y": xy[1], "w": w, "color": RED, "at": at}
    if until: d["until"] = until
    return d


plan = {
    "title": "How Many Push-Ups Do You Really Need?",
    "canvas": {"background": P["bg"]},
    "style": {"accent": YEL},
    "captions": {"mode": "phrase", "look": "clean", "size": 58, "y": P["cap_y"], "maxWords": 3,
                 "keywords": ["chest", "three", "hands", "shoulders", "half", "floor", "elbows", "hips", "straight", "plank"],
                 "hide": [["Here's the fix-0.05", "You only need"]]},
    "scenes": [
        # 0-3 s: zoom-out from the flat chest (ref 0.03-0.5 s), arms crossed, push-up bubble drops in (ref real clip inset)
        sc("hook", "start", [
            img("hero_arms_crossed", "start", "look tough", enter="cut", **SMALL),
            title("NO CHEST?", "start", "look tough", size=150, color=RED, typed=False),
            {**bubble("hero_pushup_top_v3", "hundreds", "look tough", x=0.78, y=0.33, size=0.3), "zoom": 1.6},
        ], camera=zoom_out("start", list(pt("hero_arms_crossed", "chest", SMALL)), z=2.8, dur=0.4)),
        # "look tough": flex with anime speed lines (ref 1.6-2.9 s)
        sc("tough", "look tough-0.05", [
            {"type": "speed", "at": "look tough", "until": "but your chest", "color": "#FFFFFF", "duration": 0.6},
            img("hero_double_biceps", "look tough", "but your chest", enter="punch", **BODY),
            title("LOOKS TOUGH", "look tough", "but your chest"),
        ], camera=punch("look tough", (0.5, 0.5), 1.1)),
        # frustration beat (ref 2.9-3.6 s black spin): facepalm + pain on the flat chest, then crying
        sc("flat", "but your chest-0.05", [
            img("hero_facepalm", "but your chest", "looks flat", enter="cut", **BODY),
            pain("but your chest+0.2", None, x=chest[0], y=chest[1], w=0.2),
            title("STILL FLAT", "but your chest", color=RED),
            img("hero_sad_crying", "looks flat", enter="cut", **BODY),
        ]),
        sc("fix", "Here's the fix-0.05", [
            text("HERE'S THE FIX", "Here's the fix-0.05", None, 0.47, 170, WHITE, "cut"),
        ], camera=[{"at": "Here's the fix-0.05", "zoom": 1}, {"at": "fix.+0.05", "zoom": 1}, {"at": "fix.+0.2", "zoom": 1.18}]),
        # "only 3" (ref 4.5-8.9 s: three fingers, then sunglasses)
        sc("three", "You only need-0.05", [
            img(count(3), "You only need", "finally starts", enter="cut", **BODY),
            title("ONLY 3 FIXES", "three small form", "finally starts"),
            img("gag_sunglasses_thumbs", "finally starts", enter="cut", **GAG),
            title("CHEST: GROWING", "finally starts"),
        ]),
        # #1 hand placement (ref 8.9-21 s): side view, hands under the shoulders, white dashed line shoulder -> wrist
        sc("m1", "Number one-0.05", [
            title("#1 HAND PLACEMENT", "Number one", size=110),
            img("hero_pushup_top_v3", "Number one", enter="cut", **PUSH),
            sub("NOT TOO WIDE, NOT TOO CLOSE", "too wide", "just outside"),
            guide(sh, (wr[0], floor), "just outside", "all work", arrow=True),
            ring(wr, "just outside", "all work"),
            sub("HANDS UNDER SHOULDERS", "just outside", "all work"),
            sub("CHEST + SHOULDERS + TRICEPS", "all work"),
        ], drift=False),
        # #2 range of motion (ref 21-29 s): slow down/up loop (same side view), red depth arrow to the floor
        sc("m2", "Number two-0.05", [
            title("#2 RANGE OF MOTION", "Number two", "keep your elbows", size=110),
            {**poses(loop("hero_pushup_top_v3", "hero_pushup_mid", "Number two", 14, 0.6), **PUSH), "until": "keep your elbows"},
            sub("HALF REPS = HALF RESULTS", "Half reps", "Go down"),
            sub("CHEST NEAR THE FLOOR", "Go down", "keep your elbows"),
            guide((sh_low[0], sh_low[1] - 0.06), (sh_low[0], floor), "Go down", "keep your elbows", color=RED, arrow=True),
            img(ATT["no"], "keep your elbows", enter="cut", **BODY),
            title("ELBOWS IN", "keep your elbows"),
        ], drift=False),
        # #3 core control (ref 30.7-43 s): plank side view, red ring on the hips, white straight line heels -> shoulders
        sc("m3", "Number three-0.05", [
            title("#3 CORE CONTROL", "Number three", size=110),
            img("hero_plank", "Number three", "bad yoga", enter="cut", **PUSH),
            ring(hip, "hips sag", "bad yoga", w=0.09),
            sub("HIPS DON'T SAG", "hips sag", "bad yoga"),
            img(count(1), "bad yoga", "Keep one straight", enter="cut", **BODY),
            sub("NOT YOGA", "bad yoga", "Keep one straight"),
            img("hero_plank", "Keep one straight", enter="cut", **PUSH),
            guide(ank, shp, "Keep one straight", None, arrow=False),
            sub("ONE STRAIGHT LINE", "Keep one straight", "like a plank"),
            sub("LIKE A MOVING PLANK", "like a plank"),
        ], drift=False),
        # recap + ending (ref 43-50 s: thumbs up, finger, sunglasses)
        sc("recap", "That's it-0.05", [
            img(ATT["ok"], "That's it", "No gym", enter="cut", **BODY),
            title("3 FIXES = BIG DIFFERENCE", "That's it", "No gym", size=105),
            img(ATT["rule"], "No gym", "Just clean", enter="cut", **BODY),
            title("NO GYM. NO GEAR.", "No gym", "Just clean"),
            img("gag_sunglasses_thumbs", "Just clean", enter="cut", **GAG),
            title("CLEAN REPS = REAL CHEST", "Just clean", size=105),
        ]),
    ],
    "sfx": cues([
        ("start", "big"), ("hundreds", "info"), ("look tough", "drop"), ("but your chest", "enter"), ("looks flat", "info"),
        ("Here's the fix-0.05", "bumper"), ("fix.+0.15", "big"),
        ("You only need", "enter"), ("finally starts", "reveal"),
        ("Number one", "enter"), ("just outside", "info"), ("all work", "tick"),
        ("Number two", "enter"), ("Go down", "info"), ("keep your elbows", "enter"),
        ("Number three", "enter"), ("hips sag", "info"), ("bad yoga", "enter"), ("Keep one straight", "info"),
        ("That's it", "enter"), ("No gym", "tick"), ("Just clean", "reveal")]),
}
validate(plan, S)
json.dump(plan, open("pushdemo.json", "w"), indent=1, ensure_ascii=False)

# cover (first 0.1 s, like the ref): beige, "NO CHEST?", crying H with a red ring on the chest
W, H = 1080, 1920
im = Image.new("RGB", (W, H), P["bg"]); d = ImageDraw.Draw(im)
f = next((x for x in ["/usr/share/fonts/opentype/inter/Inter-Black.otf", "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
                      "/usr/share/fonts/opentype/inter/Inter-Bold.otf"] if os.path.exists(x)), None)
font = ImageFont.truetype(f, 150) if f else ImageFont.load_default()
d.text((W / 2, 300), "NO CHEST?", font=font, fill=INK, anchor="mm")
h = Image.open(next(f"{LIB}/hero/{x}" for x in os.listdir(f"{LIB}/hero") if x.startswith("hero_sad_crying."))).convert("RGBA")
hw = int(W * 0.8); hh = int(h.height * hw / h.width); h = h.resize((hw, hh))
top = int(H * 0.62 - hh / 2); im.paste(h, ((W - hw) // 2, top), h)
cx, cy = body_xy("hero_sad_crying", "chest", 0.8, 0.62); r = 0.11 * W
d.ellipse([cx * W - r, cy * H - r, cx * W + r, cy * H + r], outline=RED, width=14)
im.save("thumbnails/pushdemo.jpg", quality=92)
print("cover ok")
