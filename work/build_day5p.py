# Day 5 in the OLD pose style (owner 1 Nov): H library poses on the beige set, typed headings, red pain circle,
# rep loops from real start/end poses, count_N on the move numbers, anatomy bubble, kinetic HERE'S THE FIX.
# Clamshell / box squat have no library poses: the owner's white-background Day 5 images are used as cutouts
# (sc_d05_v08 / v14 / v07 / v17). Captions: one word, white, middle (owner, 1 Nov).
# usage: python3 build_day5p.py && MUSIC_VOL=0.035 python3 fast_render.py day05p day05.txt day05p.json 1.0
import json
from h_kit import *

use_preset("beige")
S = " ".join(open("day05.txt").read().split())
FLOOR = {"autoAlign": False, "width": 0.98, "y": 0.62}   # lying poses: wide and low
CUT = {"autoAlign": False, "width": 0.95, "y": 0.6}     # owner's full-figure cutouts

plan = {
    "title": "Knees Hurt When You Squat?",
    "canvas": {"background": P["bg"]},
    "style": {"accent": YEL},
    "audio": {"autoSfx": False},
    "captions": {"mode": "word", "look": "viral", "size": 92, "y": 0.5, "keywords": [],
                 "hide": [["Here are three-0.05", "First, glute"]]},
    "scenes": [
        # hook: squat reps from frame 1 -> knee pain on "tenth rep" (red circle, punch-in)
        sc("hook", "start", [
            poses(loop("hero_squat_top", "hero_squat_mid", "start", 6, 0.4), enter="cut", until="but by the"),
            title("SQUATS HURT?", "start", "but by the", size=150, typed=False),
            img("hero_sore_knee", "but by the", enter=ENTER["fall"], **BODY),
            pain("but by the+0.3", anchor="knees", w=0.2),
            title("KNEES ACHE", "but by the", color=RED),
        ], camera=punch("ache", (0.5, 0.62), 1.12)),
        sc("try", "You try going-0.05", [
            img("hero_shrug", "You try going", "and they still", enter=ENTER["slide"], **BODY),
            title("SLOWER? LIGHTER?", "You try going", "and they still", size=125),
            img("hero_sad_crying", "and they still", enter="cut", **BODY),
            title("STILL SORE", "and they still", color=RED),
        ]),
        sc("you", "If that sounds-0.05", [
            img(ATT["you"], "If that sounds", "the problem might", enter=ENTER["rise"], **BODY),
            title("SOUND LIKE YOU?", "If that sounds", "the problem might", size=130),
            img(ATT["stop"], "the problem might", enter="cut", **BODY),
            title("NOT YOUR KNEES", "the problem might"),
        ]),
        sc("why", "Your glutes are-0.05", [
            img("hero_hands_hips_look_back", "Your glutes are", enter=ENTER["slide"], **LEFT),
            title("YOUR GLUTES", "Your glutes are"),
            bubble("anat_muscle_glutes", "Your glutes are+0.3", x=0.8, y=0.66, size=0.3),
        ]),
        sc("job", "Part of their-0.05", [
            img("hero_squat_front", "Part of their", enter=ENTER["slide"], **BODY),
            title("KEEP KNEES STEADY", "Part of their", size=125),
        ]),
        sc("weak", "When they're weak-0.05", [
            img("hero_squat_wrong", "When they're weak", enter="cut", **LEFT),
            title("WEAK = KNEES CAVE IN", "When they're weak", size=115),
            pain("cave in+0.1", anchor="knees", w=0.2),
            bubble("anat_pain_knee", "puts extra+0.1", x=0.8, y=0.66, size=0.28),
        ], camera=punch("cave in", (0.45, 0.65), 1.1)),
        # bumper
        sc("fix", "Here are three-0.05", [
            img(count(3), "Here are three", enter="cut", width=0.7, y=0.72),
            *kinetic([("HERE'S", 0.17, 120, WHITE, 0), ("THE FIX", 0.27, 220, RED, "fix")], "Here are three"),
        ]),
        # #1 glute bridge: one finger, then the real down/up rep loop
        sc("m1", "First, glute-0.05", [
            img(count(1), "First, glute", "Lie on your back", enter="cut", **BODY),
            title("#1 GLUTE BRIDGE", "First, glute", size=130),
            poses(loop("hero_glute_bridge_down", "hero_glute_bridge_up", "Lie on your back", 14, 0.6), **FLOOR),
            sub("SQUEEZE + HIPS UP", "squeeze your", "Do fifteen#1"),
            sub("x15", "Do fifteen#1"),
        ]),
        sc("m2", "Second, clamshells-0.05", [
            img(count(2), "Second, clamshells", "Lie on your side", enter="cut", **BODY),
            title("#2 CLAMSHELL", "Second, clamshells"),
            img("sc_d05_v08", "Lie on your side", enter=ENTER["slide"], **FLOOR),
            sub("OPEN LIKE A BOOK", "open your top", "Do fifteen on"),
            sub("15 EACH SIDE", "Do fifteen on"),
        ]),
        sc("m3", "Third, box squats-0.05", [
            img(count(3), "Third, box squats", "Sit back onto", enter="cut", **BODY),
            title("#3 BOX SQUAT", "Third, box squats"),
            img("sc_d05_v14", "Sit back onto", "push your knees", enter=ENTER["slide"], **CUT),
            sub("SIT BACK", "Sit back onto", "push your knees"),
            img("sc_d05_v07", "push your knees", "and stand up", enter="cut", **CUT),
            sub("KNEES OVER TOES", "push your knees", "and stand up"),
            img("sc_d05_v17", "and stand up", enter=ENTER["jump"], **CUT),
            sub("x10", "Do ten"),
        ]),
        sc("plan", "Do these three-0.05", [
            img(ATT["teach"], "Do these three", "and watch your", enter=ENTER["slide"], **BODY),
            title("3x A WEEK", "Do these three", "and watch your"),
            img("hero_deep_squat_hold", "and watch your", enter="cut", **BODY),
            title("WATCH YOUR KNEES", "and watch your", size=125),
        ]),
        sc("doc", "If the pain-0.05", [
            img("hero_stop_palm_v2", "If the pain", enter="cut", **BODY),
            title("SHARP PAIN?", "If the pain", "see a doctor", color=RED),
            title("SEE A DOCTOR", "see a doctor"),
        ], camera=[{"at": "If the pain", "zoom": 1}, {"at": "see a doctor", "zoom": 1.12, "focus": "face"}]),
    ],
    "sfx": cues([
        ("start", "enter"), ("but by the", "drop"), ("ache", "info"),
        ("You try going", "enter"), ("and they still", "info"),
        ("If that sounds", "enter"), ("the problem might", "info"),
        ("Your glutes are", "enter"), ("Your glutes are+0.3", "info"),
        ("Part of their", "enter"), ("When they're weak", "enter"), ("cave in", "info"),
        ("Here are three", "bumper"), ("fix", "big"),
        ("First, glute", "enter"), ("Lie on your back", "tick"), ("Do fifteen#1", "tick"),
        ("Second, clamshells", "enter"), ("Lie on your side", "tick"), ("Do fifteen on", "tick"),
        ("Third, box squats", "enter"), ("Sit back onto", "tick"), ("and stand up", "drop"), ("Do ten", "tick"),
        ("Do these three", "enter"), ("and watch your", "info"),
        ("If the pain", "enter"), ("see a doctor", "reveal")]),
}
tidy(plan); validate(plan, S)
json.dump(plan, open("day05p.json", "w"), indent=1, ensure_ascii=False)
print("day05p.json ok")
