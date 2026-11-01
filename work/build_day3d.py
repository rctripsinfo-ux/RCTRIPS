# Day 3 V4 (1 Nov): owner review fixes on V3 — one H on screen at a time (sequential chain), no teeth/ringtone
# sounds, no repeated hang images in the level test, clean cutouts (clean_cutout.py), full-frame backgrounds,
# captions hidden where the heading already says the same words, new CTA pose.
import json
from h_kit import *

use_preset("beige")
S = open("day3d.txt").read()
HANG2 = {"autoAlign": False, "width": 0.66, "y": 0.64}
CLOSE = {"autoAlign": False, "width": 1.0, "y": 0.62}
WT = "#FFFFFF"
OUT = {"type": "flyLeft", "duration": 0.25}

plan = {
    "title": "Can You Hold a Dead Hang for 60 Seconds?",
    "canvas": {"background": P["bg"]},
    "style": {"accent": YEL},
    "audio": {"autoSfx": False},  # no automatic sounds (the comment bubble's double ring came from here)
    "captions": {"mode": "phrase", "look": "clean", "size": 54, "y": P["cap_y"], "maxWords": 3,
                 "keywords": ["sixty", "thirty", "forearms", "butter", "five", "time"],
                 # hidden where the heading already shows the same words (no duplicated text)
                 "hide": [["Under twenty-0.05", "Your forearms get-0.05"], ["Here's the fix-0.05", "One: dead"],
                          ["Now comment-0.05", "be honest+2"]]},
    "scenes": [
        # 0-5 s HOOK: grip close-up -> jumps up and shivers on the impact background -> fingers slip -> falls -> test
        sc("hook", "start", [
            img("hero_grip_closeup", "start", "for sixty", enter=ENTER["rise"], **CLOSE),
            title("60 SEC DEAD HANG?", "start", "for sixty", size=125, typed=False),
            bg("bg_impact", "for sixty", "Most people", enter="cut"),
            shiver(img("hero_hang_struggle", "for sixty", "Most people", enter=ENTER["jump"], **HANG2), 0.5),
            title("60 SEC DEAD HANG?", "for sixty", "Most people", size=125, typed=False),
            shiver(img("hero_hang_slip", "Most people", "drop before", enter="cut", **HANG2), 0.8),
            title("MOST DROP AT 30", "Most people", "Let's test", size=125, color=RED),
            {**img("hero_drop_from_bar", "drop before", "Let's test", enter={"type": "down", "duration": 0.25}, **HANG2), "exit": OUT},
            img(ATT["you"], "Let's test", enter={"type": "flyRight", "duration": 0.25}, **WAIST),
            title("LET'S TEST YOU", "Let's test", size=130),
        ], camera=punch("drop before", (0.5, 0.5), 1.1)),
        # level test: a different pose per level (no repeated hang images), tag + verdict
        sc("levels", "Under twenty-0.05", [
            bg("bg_sunburst", "Ninety plus", None, enter="fade"),
            *chain([("hero_sad_crying_v2", "Under twenty", "push", BODY),
                    ("hero_shrug", "Thirty seconds", "push", BODY),
                    ("hero_thumbs_up", "Sixty seconds#2", "push", BODY),
                    ("hero_double_biceps", "Ninety plus", "push", BODY)]),
            tag("UNDER 20 SEC", "Under twenty", "Thirty seconds"),
            title("WEAK GRIP", "Under twenty", "Thirty seconds", color=RED),
            tag("30 SEC", "Thirty seconds", "Sixty seconds#2"),
            title("AVERAGE", "Thirty seconds", "Sixty seconds#2"),
            tag("60 SEC", "Sixty seconds#2", "Ninety plus"),
            title("STRONG", "Sixty seconds#2", "Ninety plus"),
            tag("90+ SEC", "Ninety plus"),
            title("BEAST MODE", "Ninety plus"),
        ]),
        # black sad beat
        sad_beat("sad", "Dropped early-0.05", [
            img("hero_sad_floor", "Dropped early", enter="fade", **BODY),
            text("DROPPED EARLY?", "Dropped early", "It's not your", P["title_y"], 130, WT, "pop"),
            text("NOT YOUR ARMS", "It's not your", None, P["title_y"], 140, WT, "pop"),
        ], "It's your grip"),
        # why: points at the grip bubble -> forearm burns -> facepalm (hands slip like butter)
        sc("why", "It's your grip-0.05", [
            *chain([("hero_point_right", "It's your grip", "push", LEFT),
                    ("hero_forearm_burn", "Your forearms get", "push", BODY),
                    ("hero_facepalm", "slide off", "push", BODY)]),
            title("IT'S YOUR GRIP", "It's your grip", "Your forearms get"),
            bubble("anat_muscle_forearm_grip", "It's your grip+0.2", "Your forearms get-0.25", x=0.81, size=0.3),
            title("TIRED FOREARMS", "Your forearms get", "slide off"),
            title("SLIPS LIKE BUTTER", "slide off"),
        ]),
        sc("bumper", "Here's the fix-0.05", [
            img(count(1), "Here's the fix-0.05", enter=ENTER["rise"], width=0.72, y=0.7),
            *kinetic([("HERE'S", 0.17, 120, INK, 0), ("THE FIX", 0.27, 220, RED, "the fix")], "Here's the fix-0.05"),
        ], camera=[{"at": "Here's the fix-0.05", "zoom": 1}, {"at": "fix.+0.05", "zoom": 1}, {"at": "fix.+0.2", "zoom": 1.15}]),
        sc("m1", "One: dead-0.05", [
            *section_card(1, "DEAD HANGS", "One: dead-0.05", "Hang as-0.3"),
            img("hero_hang_perfect", "Hang as-0.3", enter=ENTER["rise"], **HANG2),
            title("#1 DEAD HANG", "Hang as"),
            sub("ARMS STRAIGHT", "Hang as", "three times"),
            sub("MAX TIME x3", "three times"),
        ], drift=False),
        sc("m2", "Two: add-0.05", [
            *section_card(2, "+5 SEC A DAY", "Two: add-0.05", "every day-0.3"),
            img("hero_stopwatch", "every day-0.3", enter=ENTER["slide"], **WAIST),
            title("#2 +5 SEC EVERY DAY", "every day", size=120),
            counter(30, 60, "Thirty becomes", " SEC", y=0.218, size=70, dur=1.2),
        ], drift=False),
        # payoff on the sunburst, then a new CTA pose: H points his stick at the comment
        sc("end", "Do this and-0.05", [
            bg("bg_sunburst", "Do this and", "Now comment", enter="fade"),
            *chain([("hero_grip_crush", "Do this and", "push", BODY),
                    ("hero_teacher_pointer", "Now comment", "push", {**BODY, "x": 0.4})]),
            title("GRIP: LOCKED", "grip gets crazy", "Now comment"),
            title("COMMENT YOUR TIME", "Now comment", size=125),
            comment("42 sec, be honest \U0001F605", "Now comment+0.4"),
        ], camera=[{"at": "Do this and", "zoom": 1}, {"at": "be honest", "zoom": 1.06}]),
    ],
    "sfx": cues([
        ("start", "enter"), ("for sixty", "drop"), ("Most people", "info"), ("drop before", "drop"), ("Let's test", "enter"),
        ("Under twenty", "enter"), ("Thirty seconds", "enter"), ("Sixty seconds#2", "enter"),
        ("Ninety plus", "enter"), ("Beast mode", "reveal"),
        ("Dropped early", "sad"),
        ("It's your grip", "enter"), ("Your forearms get", "enter"), ("slide off", "enter"),
        ("Here's the fix-0.05", "bumper"), ("fix.+0.15", "big"),
        ("One: dead", "info"), ("Hang as", "drop"), ("three times", "tick"),
        ("Two: add", "info"), ("every day", "enter"), ("Thirty becomes", "count"),
        ("Do this and", "enter"), ("grip gets crazy", "reveal"), ("Now comment", "enter")]),
}
tidy(plan)
validate(plan, S)
json.dump(plan, open("day3d.json", "w"), indent=1, ensure_ascii=False)
