# Day 3: dead hang 60 s test, no-clip format, upgraded with the reference findings (31 Oct, h_kit.py):
# rise-in hook at 0.0 s, H jumps to the bar on "sixty", falls on "drop", attitude pose per sentence,
# count_N on the move numbers, a form arrow on the hang, SFX by cue category. Script unchanged.
import json
from h_kit import *

use_preset("beige")
S = open("day3.txt").read()

plan = {
    "title": "Can You Hold a Dead Hang for 60 Seconds?",
    "canvas": {"background": P["bg"]},
    "style": {"accent": YEL},
    "captions": {"mode": "phrase", "look": "clean", "size": 58, "y": P["cap_y"], "maxWords": 3,
                 "keywords": ["sixty", "thirty", "grip", "forearms", "slip", "five", "strong", "time"],
                 "hide": [["Here's the fix-0.05", "One: dead"]]},
    "scenes": [
        # hook: H rises in looking at the bar (forearms marked), jumps up to hang on "sixty", falls on "drop"
        sc("hook", "start", [
            img("hero_look_up_bar", "start", "for sixty", enter=ENTER["rise"], **HANG),
            pain("start+0.3", "for sixty", **dict(zip("xy", body_xy("hero_look_up_bar", "forearm_r", HANG["width"], HANG["y"]))), w=0.15),
            title("60 SEC DEAD HANG?", "start", "drop before", size=125, typed=False),
            img("hero_pullup_hang_v2", "for sixty", "drop before", enter=ENTER["jump"], **HANG),
            img("hero_drop_from_bar", "drop before", enter=ENTER["fall"], **HANG),
            title("MOST DROP AT 30", "drop before", size=125, color=RED),
        ], camera=punch("drop before", (0.5, 0.5), 1.12)),
        # why: stop gesture on "not your arms", points at the grip bubble on "It's your grip"
        sc("why", "not your arms-0.05", [
            img(ATT["stop"], "not your arms", "It's your grip", enter="cut", **BODY),
            title("NOT YOUR ARMS", "not your arms", "It's your grip"),
            img(ATT["point_r"], "It's your grip", enter="cut", **LEFT),
            title("IT'S YOUR GRIP", "It's your grip"),
            bubble("anat_muscle_forearm_grip", "It's your grip+0.2", x=0.81, size=0.3),
        ]),
        sc("gag", "Your forearms get-0.05", [
            img("gag_dead_on_floor", "Your forearms get", enter="cut", **GAG),
            title("TIRED FOREARMS", "Your forearms get", "slip off"),
            title("= HANDS SLIP OFF", "slip off"),
        ]),
        sc("fix", "Here's the fix-0.05", [
            text("HERE'S THE FIX", "Here's the fix-0.05", None, 0.47, 170, WHITE, "cut"),
        ], camera=[{"at": "Here's the fix-0.05", "zoom": 1}, {"at": "fix.+0.05", "zoom": 1}, {"at": "fix.+0.2", "zoom": 1.18}]),
        # #1: one finger on "One", then the front hang (single view, static = correct for a dead hang)
        sc("m1", "One: dead-0.05", [
            img(count(1), "One: dead", "Hang as", enter="cut", **BODY),
            title("#1 DEAD HANG", "One: dead"),
            img("hero_pullup_hang_v2", "Hang as", enter=ENTER["jump"], **HANG),
            sub("ARMS STRAIGHT", "Hang as", "three times"),
            sub("MAX TIME x3", "three times"),
        ]),
        # #2: two fingers on "Two", then the side hang with the 30 -> 60 SEC counter
        sc("m2", "Two: add-0.05", [
            img(count(2), "Two: add", "Thirty becomes", enter="cut", **BODY),
            title("#2 +5 SEC EVERY DAY", "Two: add", size=120),
            img("hero_pullup_hang", "Thirty becomes", enter="cut", **HANG),
            counter(30, 60, "Thirty becomes", " SEC", y=0.25, size=80, dur=1.2),
        ]),
        sc("after", "Do this and-0.05", [
            img(ATT["win"], "Do this and", "crazy strong", enter="cut", **BODY),
            title("DO IT DAILY", "Do this and", "crazy strong"),
            img("gag_sunglasses_thumbs", "crazy strong", enter="cut", **GAG),
            title("GRIP: LOCKED", "crazy strong"),
        ]),
        sc("cta", "Comment your-0.05", [
            img(ATT["you"], "Comment your", enter="cut", id="h", **BODY),
            title("COMMENT YOUR TIME", "Comment your", size=125),
            comment("42 sec \U0001F605", "Comment your+0.3"),
        ], camera=[{"at": "Comment your", "zoom": 1}, {"at": "time below", "zoom": 1.2, "focus": "face"}]),
    ],
    "sfx": cues([
        ("start", "enter"), ("for sixty", "drop"), ("drop before", "drop"),
        ("not your arms", "enter"), ("It's your grip", "info"),
        ("Your forearms get", "enter"), ("slip off", "info"),
        ("Here's the fix-0.05", "bumper"), ("fix.+0.15", "big"),
        ("One: dead", "enter"), ("Hang as", "tick"), ("three times", "tick"),
        ("Two: add", "enter"), ("Thirty becomes", "count"),
        ("Do this and", "enter"), ("crazy strong", "reveal"),
        ("Comment your", "enter"), ("Comment your+0.3", "cta")]),
}
validate(plan, S)
json.dump(plan, open("day3.json", "w"), indent=1, ensure_ascii=False)
