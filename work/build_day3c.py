# Day 3 V3 (31 Oct): dead hang, best version from the existing library, closing the gaps in PUSHDEMO-AUDIT.md:
# 5-second hook (close-up -> shiver hang on an impact background -> slip -> fall -> "let's test you"),
# a level ladder (ref V04/V05 test format) with side-push pose changes and tags, a black sad beat with our sad sting,
# kinetic "HERE'S THE FIX" with H, section cards with a ghost #N, waist-up crops for scale, louder music bed.
import json
from h_kit import *

use_preset("beige")
S = open("day3c.txt").read()
HANG2 = {"autoAlign": False, "width": 0.66, "y": 0.64}
CLOSE = {"autoAlign": False, "width": 1.0, "y": 0.62}
WT = "#FFFFFF"

plan = {
    "title": "Can You Hold a Dead Hang for 60 Seconds?",
    "canvas": {"background": P["bg"]},
    "style": {"accent": YEL},
    "captions": {"mode": "phrase", "look": "clean", "size": 54, "y": P["cap_y"], "maxWords": 3,
                 "keywords": ["sixty", "thirty", "twenty", "ninety", "grip", "forearms", "butter", "five", "strong", "time", "honest"],
                 "hide": [["Here's the fix-0.05", "One: dead"]]},
    "scenes": [
        # 0-5 s HOOK: grip close-up rises in -> he jumps up and shivers on an impact background -> fingers slip -> falls
        sc("hook", "start", [
            img("hero_grip_closeup", "start", "for sixty", enter=ENTER["rise"], **CLOSE),
            title("60 SEC DEAD HANG?", "start", "for sixty", size=125, typed=False),
            bg("bg_impact", "for sixty", "Most people", enter="cut"),
            shiver(img("hero_hang_struggle", "for sixty", "Most people", enter=ENTER["jump"], **HANG2), 0.6),
            title("60 SEC DEAD HANG?", "for sixty", "Most people", size=125, typed=False),  # heading on top of the background
            shiver(img("hero_hang_slip", "Most people", "drop before", enter="cut", **HANG2), 0.9),
            title("MOST DROP AT 30", "Most people", "Let's test", size=125, color=RED),
            {**img("hero_drop_from_bar", "drop before", "Let's test", enter={"type": "down", "duration": 0.25}, **HANG2), "exit": {"type": "flyLeft", "duration": 0.28}},
            img(ATT["you"], "Let's test-0.28", enter={"type": "flyRight", "duration": 0.28}, **WAIST),
            title("LET'S TEST YOU", "Let's test", size=130),
        ], camera=punch("drop before", (0.5, 0.5), 1.1)),
        # level ladder: each level pushes in from the other side, tag top-left, verdict heading
        sc("levels", "Under twenty-0.05", [
            bg("bg_sunburst", "Ninety plus", None, enter="fade"),
            *chain([("hero_hang_slip", "Under twenty", "push", HANG2),
                    ("hero_hang_struggle", "Thirty seconds", "push", HANG2),
                    ("hero_hang_perfect", "Sixty seconds#2", "push", HANG2),
                    ("gag_sunglasses_thumbs", "Ninety plus", "push", GAG)]),
            tag("UNDER 20 SEC", "Under twenty", "Thirty seconds"),
            title("WEAK GRIP", "Weak grip", "Thirty seconds", color=RED),
            tag("30 SEC", "Thirty seconds", "Sixty seconds#2"),
            title("AVERAGE", "Average", "Sixty seconds#2"),
            tag("60 SEC", "Sixty seconds#2", "Ninety plus"),
            title("STRONG", "Sixty seconds#2+0.5", "Ninety plus"),
            tag("90+ SEC", "Ninety plus"),
            title("BEAST MODE", "Beast mode"),
        ]),
        # black sad beat: H on the floor, camera pulls back, our sad sting
        sad_beat("sad", "Dropped early-0.05", [
            img("hero_sad_floor", "Dropped early", enter="fade", **BODY),
            text("DROPPED EARLY?", "Dropped early", "It's not your", P["title_y"], 130, WT, "pop"),
            text("NOT YOUR ARMS", "It's not your", None, P["title_y"], 140, WT, "pop"),
        ], "It's your grip"),
        # why: stop -> point at the grip bubble -> forearm burns -> hands slide off (each pose pushes the last one out)
        sc("why", "It's your grip-0.05", [
            *chain([("hero_point_right", "It's your grip", "push", LEFT),
                    ("hero_forearm_burn", "Your forearms get", "push", WAIST),
                    ("hero_hang_slip", "slide off", "push", HANG2)]),
            title("IT'S YOUR GRIP", "It's your grip", "Your forearms get"),
            bubble("anat_muscle_forearm_grip", "It's your grip+0.2", "Your forearms get", x=0.81, size=0.3),
            title("TIRED FOREARMS", "Your forearms get", "slide off"),
            title("SLIPS LIKE BUTTER", "slide off"),
        ]),
        # kinetic bumper with H pointing up (ref "LET ME FIX THAT"), our words
        sc("bumper", "Here's the fix-0.05", [
            img(count(1), "Here's the fix-0.05", enter=ENTER["rise"], width=0.72, y=0.7),
            *kinetic([("HERE'S", 0.17, 120, INK, 0), ("THE FIX", 0.27, 220, RED, "the fix")], "Here's the fix-0.05"),
        ], camera=[{"at": "Here's the fix-0.05", "zoom": 1}, {"at": "fix.+0.05", "zoom": 1}, {"at": "fix.+0.2", "zoom": 1.15}]),
        # #1: section card, then he jumps into a perfect dead hang
        sc("m1", "One: dead-0.05", [
            *section_card(1, "DEAD HANGS", "One: dead-0.05", "Hang as-0.3"),
            img("hero_hang_perfect", "Hang as-0.3", enter=ENTER["rise"], **HANG2),
            title("#1 DEAD HANG", "Hang as"),
            sub("ARMS STRAIGHT", "Hang as", "three times"),
            sub("MAX TIME x3", "three times"),
        ], drift=False),
        # #2: section card, stopwatch (waist-up), 30 -> 60 SEC counter
        sc("m2", "Two: add-0.05", [
            *section_card(2, "+5 SEC A DAY", "Two: add-0.05", "every day-0.3"),
            img("hero_stopwatch", "every day-0.3", enter=ENTER["slide"], **WAIST),
            title("#2 +5 SEC EVERY DAY", "every day", size=120),
            counter(30, 60, "Thirty becomes", " SEC", y=0.218, size=70, dur=1.2),
        ], drift=False),
        # payoff + CTA: grip crush on the sunburst -> points at you, comment bubble, punch on the face
        sc("end", "Do this and-0.05", [
            bg("bg_sunburst", "Do this and", "Now comment", enter="fade"),
            *chain([("hero_grip_crush", "Do this and", "push", WAIST), (ATT["you"], "Now comment", "push", BODY)]),
            title("GRIP: LOCKED", "grip gets crazy", "Now comment"),
            title("COMMENT YOUR TIME", "Now comment", size=125),
            comment("42 sec, be honest \U0001F605", "Now comment+0.4"),
        ], camera=[{"at": "Do this and", "zoom": 1}, {"at": "Now comment", "zoom": 1.03}, {"at": "be honest", "zoom": 1.18, "focus": "face"}]),
    ],
    "sfx": cues([
        ("start", "enter"), ("for sixty", "shiver"), ("Most people", "info"), ("drop before", "drop"), ("Let's test", "enter"),
        ("Under twenty", "enter"), ("Weak grip", "info"), ("Thirty seconds", "enter"), ("Sixty seconds#2", "enter"),
        ("Ninety plus", "enter"), ("Beast mode", "reveal"),
        ("Dropped early", "sad"),
        ("It's your grip", "enter"), ("Your forearms get", "enter"), ("slide off", "enter"),
        ("Here's the fix-0.05", "bumper"), ("fix.+0.15", "big"),
        ("One: dead", "info"), ("Hang as", "drop"), ("three times", "tick"),
        ("Two: add", "info"), ("every day", "enter"), ("Thirty becomes", "count"),
        ("Do this and", "enter"), ("grip gets crazy", "reveal"), ("Now comment", "enter"), ("Now comment+0.4", "cta")]),
}
tidy(plan)
validate(plan, S)
json.dump(plan, open("day3c.json", "w"), indent=1, ensure_ascii=False)
