import os, sys
sys.path.insert(0, "/home/user/RCTRIPS/.claude/skills/reel-video-maker/scripts")
from plan_lib import *
sc = [
 auto("hook", "start", "red", [
   b("start", "STIFF NECK", "giant", c=R, img="hero_phone_scroll"),
   b("your neck feels stiff", "STIFF", "echo", c=R, img="hero_neck_stretch", impact_=True),
   b("Your shoulders are tight", "TIGHT", "echo", c=R, img="hero_sore_back"),
   b("you keep rolling", "RELIEF?", img="hero_neck_stretch"),
 ], hook=True, shakes=["your neck feels stiff"]),
 auto("why", "If that sounds like you-0.1", "yellow", [
   b("If that sounds like you", "NOT ALONE", img="hero_shrug"),
   b("simple reason", "THE REASON", img="hero_idea_bulb"),
 ]),
 auto("truth", "Your head weighs-0.1", "grid", [
   b("Your head weighs", "5 KG", img="hero_explain", size=260),
   b("When you tilt it forward", "TILT", c=R, img="hero_bad_posture_desk", tape="HEAD FORWARD", tapec=R),
   b("look down at a screen", "SCREEN", img="hero_phone_scroll"),
   b("your neck muscles", "NECK MUSCLES", c=R, img="hero_neck_stretch", size=150),
   b("much harder", "HARDER", "echo", c=R, img="hero_tired_sweating", impact_=True),
 ]),
 auto("tilt", "Research suggests-0.1", "red", [
   b("Research suggests", "RESEARCH", img="hero_reading"),
   b("deep forward tilt", "DEEP TILT", c=R, img="hero_bad_posture_desk"),
   b("many times that weight", "MANY TIMES", "echo", c=R, img="hero_mind_blown", size=190),
   b("Do that for hours", "HOURS", img="hero_phone_scroll"),
   b("gets tired and sore", "SORE", "echo", c=R, img="hero_sore_back"),
 ]),
 auto("do", "Here are three easy moves-0.1", "green", [
   b("Here are three easy moves", "3 MOVES", c=G, img="hero_count_3"),
   b("First, chin tucks", "CHIN TUCKS", img="hero_count_1"),
   b("Sit tall and gently", "SIT TALL", c=G, img="hero_good_posture_desk"),
   b("slide your chin", "CHIN BACK", "echo", c=G, img="hero_stand", size=200),
   b("making a double chin", "DOUBLE CHIN", img="hero_this_small"),
   b("Hold for three seconds", "3 SEC x 10", img="hero_check_watch"),
 ]),
 auto("door", "Second, the doorway-0.1", "yellow", [
   b("Second, the doorway", "DOORWAY", img="hero_count_2"),
   b("Put your forearms", "FOREARMS UP", img="hero_lean_wall"),
   b("step forward slowly", "STEP IN", img="hero_walk_toward"),
   b("feel your chest open", "CHEST OPEN", c=G, img="hero_side_chest", impact_=True),
   b("Hold for twenty seconds", "20 SEC", "echo", img="hero_check_watch"),
 ]),
 auto("wall", "Third, wall angels-0.1", "green", [
   b("Third, wall angels", "WALL ANGELS", img="hero_count_3"),
   b("Stand with your back", "BACK ON WALL", img="hero_stand"),
   b("slide your arms", "ARMS UP", c=G, img="hero_arm_circles"),
   b("ten times", "10 TIMES", "echo", c=G, img="hero_counting_fingers"),
 ]),
 auto("plan", "Do these every evening-0.1", "red", [
   b("Do these every evening", "EVERY EVENING", img="hero_clipboard", size=150),
   b("lift your phone", "EYE LEVEL", c=G, img="hero_selfie"),
 ], tr="zoom"),
 auto("end", "Your neck will thank-0.1", "rays", [
   b("Your neck will thank", "THANK YOU", c=G, img="hero_thumbs_up"),
   b("If the pain is sharp", "SHARP PAIN?", c=R, img="hero_stop_palm", tape="SEE A DOCTOR", tapec=R),
   b("see a doctor", "DOCTOR", "echo", c=R, img="hero_point_viewer"),
 ]),
]
sfx = [("start","sfx_whoosh_big"),("your neck feels stiff","sfx_bone_crack"),("Your shoulders are tight","sfx_stretch"),
 ("simple reason","sfx_ding"),("Your head weighs","sfx_whoosh_swipe"),("much harder","sfx_hammer"),("many times that weight","sfx_shocked"),
 ("Here are three easy moves","sfx_level_start"),("First, chin tucks","sfx_desk_bell"),("Second, the doorway","sfx_pop"),
 ("feel your chest open","sfx_stretch"),("Third, wall angels","sfx_desk_bell"),("ten times","sfx_counter"),
 ("Do these every evening","sfx_whoosh_soft"),("Research suggests","sfx_whoosh_fast"),("If that sounds like you","sfx_swish"),("lift your phone","sfx_notification"),("Your neck will thank","sfx_gold_bell"),
 ("If the pain is sharp","sfx_whoosh_big")]
plan("Why your neck hurts after screens (3 fixes)",
 ["neck","stiff","shoulders","head","kilos","forward","chin","doorway","wall","angels","evening","doctor"],
 ["Your head weighs","Your neck will thank"], sc, sfx, "work/neckpain.json")
