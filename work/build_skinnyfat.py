import sys
sys.path.insert(0, "/root/.claude/skills/synced/370a525f-40ff-4b1d-a196-a1258fe281e4_33be9e93-4a60-43f2-9228-8bfef809efb4/reel-video-maker/scripts")
from plan_lib import *

make("skinnyfat", "Skinny arms but a soft belly? That's skinny fat",
     ["skinny", "fat", "belly", "neither", "maintenance", "protein", "push-ups", "squats", "rows", "rep", "three", "arms"],
     ["Dieting makes you", "Send this to"], [
    auto("hook", "start", "none", [
        b("start", "SKINNY FAT", "marquee", clip="clip_pushup", rate=1.3),
        b("but a soft belly", "SOFT BELLY", "echo", c=R, img="hero_beginner", impact_=True, size=200),
        b("That's skinny fat", "SKINNY FAT", c=R, img="hero_measuring_waist"),
    ], hook=True, shakes=["but a soft belly"]),
    auto("myth", "Dieting makes you-0.1", "red", [
        b("Dieting makes you", "SKINNIER", c=R, img="hero_beginner_v2"),
        b("Bulking makes you", "FATTER", c=R, img="hero_eating", impact_=True),
        b("Do neither", "NEITHER", "echo", c=G, img="hero_stop_palm"),
    ]),
    auto("eat", "Eat at maintenance-0.1", "green", [
        b("Eat at maintenance", "MAINTENANCE", img="hero_cooking", size=150),
        b("with protein in every meal", "PROTEIN", c=G, img="hero_eating_v2", prop="prop_protein_food"),
        b("eggs, dal or chicken", "EGGS • DAL", "echo", c=G, img="hero_cooking", prop="prop_eggs", size=170),
    ]),
    auto("do", "Train full body-0.1", "none", [
        b("Train full body", "3X A WEEK", clip="clip_pushup", rate=1.0),
        b("push-ups, squats", "PUSH-UPS", clip="clip_pushup", rate=1.3),
        b("squats and rows", "SQUATS", c=G, clip="clip_squat", rate=1.3),
        b("rows", "ROWS", clip="clip_inverted_row", rate=1.2),
        b("three sets of eight", "8-12", clip="clip_inverted_row", rate=1.2, size=240),
    ]),
    auto("plan", "Add one rep-0.1", "grid", [
        b("Add one rep", "+1 REP", "echo", c=G, img="hero_clipboard", size=230),
        b("In three months", "3 MONTHS", img="hero_counting_fingers"),
        b("your belly shrinks", "BELLY DOWN", c=G, img="hero_measuring_waist"),
        b("while your arms grow", "ARMS UP", c=G, img="hero_double_biceps", impact_=True),
    ], tr="zoom"),
    cta("hero_beginner", "skinny friend with a belly", "SKINNY + BELLY", "SKINNY FAT...", echo_at="Because skinny fat"),
], [("but a soft belly", "sfx_hammer"), ("Bulking makes you", "sfx_bruh"), ("Do neither", "sfx_get_out"),
    ("with protein in every meal", "sfx_ding"), ("push-ups, squats", "sfx_whip"), ("rows", "sfx_click"),
    ("eight to twelve", "sfx_counter"), ("every week", "sfx_coin"), ("In three months", "sfx_few_moments_later"),
    ("while your arms grow", "sfx_fahhh_pump")],
    "skinny friend with a belly", "Because skinny fat")
