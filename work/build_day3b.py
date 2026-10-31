# Day 3 V2 (31 Oct): dead hang, with the owner's 8 new H images and the reference techniques (REFERENCE-ANALYSIS.md
# Pass B): grip close-up hook, hang that shivers (teeth chatter + speed lines), hands slip, fall, black sad beat
# where H shrinks back, pose changes that push in from the sides (chain), stopwatch counter, grip-crush payoff.
import json
from h_kit import *

use_preset("beige")
S = open("day3b.txt").read()
HANG2 = {"autoAlign": False, "width": 0.66, "y": 0.64}   # new hang images: bar at the top of the image
CLOSE = {"autoAlign": False, "width": 1.0, "y": 0.62}    # grip close-up: bar at canvas y ~0.44
WTXT = "#FFFFFF"

plan = {
    "title": "Can You Hold a Dead Hang for 60 Seconds?",
    "canvas": {"background": P["bg"]},
    "style": {"accent": YEL},
    "captions": {"mode": "phrase", "look": "clean", "size": 58, "y": P["cap_y"], "maxWords": 3,
                 "keywords": ["sixty", "thirty", "grip", "forearms", "butter", "five", "strong", "time"],
                 "hide": [["Here's the fix-0.05", "One: dead"]]},
    "scenes": [
        # hook: hands on the bar (close-up) -> wide: H hangs and shivers -> fingers slip -> he falls
        sc("hook", "start", [
            img("hero_grip_closeup", "start", "for sixty", enter=ENTER["rise"], **CLOSE),
            title("60 SEC DEAD HANG?", "start", "Most people", size=125, typed=False),
            shiver(img("hero_hang_struggle", "for sixty", "Most people", enter=ENTER["jump"], **HANG2), 0.6),
            speed_lines("for sixty", "Most people"),
            shiver(img("hero_hang_slip", "Most people", "drop before", enter="cut", **HANG2), 0.9),
            title("MOST DROP AT 30", "Most people", size=125, color=RED),
            img("hero_drop_from_bar", "drop before", enter={"type": "down", "duration": 0.25}, **HANG2),
        ], camera=punch("drop before", (0.5, 0.5), 1.12)),
        # black sad beat: H sits on the floor, the camera slowly pulls back (he shrinks)
        sad_beat("sad", "It's not your-0.05", [
            img("hero_sad_floor", "It's not your", enter="fade", **BODY),
            text("NOT YOUR ARMS", "It's not your", None, P["title_y"], 140, WTXT, "pop"),
        ], "It's your grip"),
        # why: pose changes push in from the sides
        sc("why", "It's your grip-0.05", [
            *chain([("hero_point_right", "It's your grip", "push", LEFT),
                    ("hero_forearm_burn", "Your forearms get"),
                    ], until="slide off", **BODY),
            title("IT'S YOUR GRIP", "It's your grip", "Your forearms get"),
            bubble("anat_muscle_forearm_grip", "It's your grip+0.2", "Your forearms get", x=0.81, size=0.3),
            title("TIRED FOREARMS", "Your forearms get", "slide off"),
            img("hero_hang_slip", "slide off", enter=ENTER["slide"], **HANG2),
            title("HANDS SLIP OFF", "slide off"),
        ]),
        sc("fix", "Here's the fix-0.05", [
            text("HERE'S THE FIX", "Here's the fix-0.05", None, 0.47, 170, WHITE, "cut"),
        ], camera=[{"at": "Here's the fix-0.05", "zoom": 1}, {"at": "fix.+0.05", "zoom": 1}, {"at": "fix.+0.2", "zoom": 1.18}]),
        # #1: one finger, then he jumps up into a perfect dead hang
        sc("m1", "One: dead-0.05", [
            *chain([(count(1), "One: dead", "push", BODY), ("hero_hang_perfect", "Hang as", "up", HANG2)]),
            title("#1 DEAD HANG", "One: dead"),
            sub("ARMS STRAIGHT", "Hang as", "three times"),
            sub("MAX TIME x3", "three times"),
        ]),
        # #2: stopwatch, 30 -> 60 SEC counter
        sc("m2", "Two: add-0.05", [
            *chain([(count(2), "Two: add", "push", BODY), ("hero_stopwatch", "every day")], **BODY),
            title("#2 +5 SEC EVERY DAY", "Two: add", size=120),
            counter(30, 60, "Thirty becomes", " SEC", y=0.218, size=70, dur=1.2),
        ]),
        # payoff + CTA
        sc("after", "Do this and-0.05", [
            *chain([(ATT["win"], "Do this and", "push", BODY), ("hero_grip_crush", "grip gets crazy"),
                    (ATT["you"], "Comment your")], **BODY),
            title("DO IT DAILY", "Do this and", "grip gets crazy"),
            title("GRIP: LOCKED", "grip gets crazy", "Comment your"),
            title("COMMENT YOUR TIME", "Comment your", size=125),
            comment("42 sec \U0001F605", "Comment your+0.3"),
        ], camera=[{"at": "Do this and", "zoom": 1}, {"at": "Comment your", "zoom": 1.05}, {"at": "time below", "zoom": 1.2, "focus": "face"}]),
    ],
    "sfx": cues([
        ("start", "enter"), ("for sixty", "shiver"), ("Most people", "info"), ("drop before", "drop"),
        ("It's not your", "sad"),
        ("It's your grip", "enter"), ("Your forearms get", "enter"), ("slide off", "enter"),
        ("Here's the fix-0.05", "bumper"), ("fix.+0.15", "big"),
        ("One: dead", "enter"), ("Hang as", "drop"), ("three times", "tick"),
        ("Two: add", "enter"), ("every day", "enter"), ("Thirty becomes", "count"),
        ("Do this and", "enter"), ("grip gets crazy", "reveal"),
        ("Comment your", "enter"), ("Comment your+0.3", "cta")]),
}
tidy(plan)
validate(plan, S)
json.dump(plan, open("day3b.json", "w"), indent=1, ensure_ascii=False)
