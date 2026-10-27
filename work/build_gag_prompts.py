# Funny "gag" images of H (owner, 27 Oct): the script's joke shown on screen for 1-2 s, like Captain Workout's
# spaghetti arms. One per video at most. Made with H's reference image so he stays the same.
STYLE = ("Use the attached reference image: the SAME character H, exactly as in the reference: bald, very muscular, "
         "tan skin, white letter H on his forehead, black shorts with a dark olive military belt, black wristbands, "
         "black shoes. Same semi-realistic 3D cartoon style and lighting as the reference. Funny, exaggerated cartoon "
         "expression, but H must stay clearly recognisable. Pure plain white background (#FFFFFF), no floor line, no "
         "room, only the props named. Vertical 9:16 image, his whole body and all props fully inside the frame with "
         "space around them, centered. No text, no letters, no logo, no watermark, no other people.")
G = [
 ("LAZY / SWITCHED OFF", [
  ("gag_glutes_vacation", "H stands from behind, looking back over his shoulder, tiny sunglasses and a tiny straw hat sitting on his glutes, a small cocktail glass with an umbrella balanced on top, H looks annoyed"),
  ("gag_beach_chair", "H lies on a white beach lounge chair, sunglasses on, arms behind his head, totally relaxed and smug, a small drink beside him"),
  ("gag_sleeping_desk", "H sleeps with his face on a small white desk, drooling a little, a laptop open, a big cartoon 'Zzz' cloud drawn as bubbles (no letters) above his head"),
  ("gag_couch_potato", "H sinks deep into a grey couch, holding a TV remote and a bag of chips, belly relaxed, half-asleep eyes"),
  ("gag_snooze_alarm", "H in bed under a white blanket, only his head and one arm out, slapping a red alarm clock, grumpy face"),
 ]),
 ("WEAK / BROKEN", [
  ("gag_spaghetti_arms", "H stands flexing proudly but both arms are long, floppy, yellow cooked spaghetti noodles hanging down limp, his face shocked looking at them"),
  ("gag_old_man_back", "H bent over like a very old man, one hand on his lower back, leaning on a wooden walking cane, wincing, a few sweat drops"),
  ("gag_phone_crushing", "H is tiny and a giant smartphone presses down on his upper back, bending him forward, he strains to hold it up"),
  ("gag_noodle_legs", "H tries to stand but his legs wobble like jelly, knees bending sideways, arms waving for balance, panicked face"),
  ("gag_skinny_legs", "H with his huge muscular upper body but tiny skinny stick legs, looking down at his legs embarrassed"),
 ]),
 ("PAIN / TROUBLE", [
  ("gag_back_on_fire", "H from the side holding his lower back, cartoon flames coming out of his lower back, eyes wide in pain"),
  ("gag_question_neck", "H with his head pushed far forward on a long bent neck shaped like a question mark, staring at a phone, his posture ridiculous"),
  ("gag_crying_phone", "H sitting on the floor crying big cartoon tears while holding a smartphone, dramatic sad face"),
  ("gag_knees_creak", "H doing a squat, small cartoon crack lines and dust puffs coming from his knees, his face cringing"),
  ("gag_sweating_bucket", "H standing exhausted, sweat pouring off him into a puddle at his feet, tongue out, eyes spinning"),
  ("gag_dead_on_floor", "H lying flat on his back on the floor, arms and legs spread out, tongue out, completely exhausted, a little ghost-like cartoon soul floating up from him"),
 ]),
 ("FOOD / HABITS", [
  ("gag_pizza_temptation", "H holding a big slice of pizza in one hand and a dumbbell in the other, torn, looking at both"),
  ("gag_sugar_monster", "H running away scared from a big cute cartoon donut monster chasing him"),
  ("gag_scale_shock", "H standing on a bathroom scale, looking down at it, jaw dropped in shock"),
  ("gag_hand_in_cookie_jar", "H caught with his hand in a cookie jar, guilty face, crumbs on his chin"),
 ]),
 ("WIN / SWAG", [
  ("gag_sunglasses_thumbs", "H wearing black sunglasses, big confident smile, giving a thumbs up, one eyebrow raised"),
  ("gag_superhero_cape", "H in a heroic pose, fists on his hips, a red cape flowing behind him, chest out"),
  ("gag_glowing_body", "H flexing double biceps with golden light rays shining out from behind him, sparkles around him"),
  ("gag_tiny_dumbbell", "H curling a giant heavy dumbbell easily with one finger, bored face"),
  ("gag_mirror_flex", "H flexing in front of a tall standing mirror, his reflection flexing even bigger, both admiring"),
 ]),
 ("REACTIONS", [
  ("gag_shocked", "H with eyes popping out wide, jaw dropped to his chest, hands on his cheeks, totally shocked"),
  ("gag_facepalm", "H doing a big facepalm, one hand covering his face, shaking his head, disappointed"),
  ("gag_mind_blown", "H with cartoon smoke and a small explosion puff coming out of the top of his head, eyes wide, mind blown"),
  ("gag_suspicious", "H squinting suspiciously at the viewer, one eyebrow raised, hand on his chin, leaning in"),
  ("gag_laughing_pointing", "H laughing hard and pointing at the viewer, holding his stomach, tears of laughter"),
 ]),
]
out = ["EFFORTLESS EXERCISE — FUNNY GAG IMAGES OF H (shown 1-2 s on the joke line)",
       "",
       "How to use: attach H's reference image every time (work/character/H-standing-front-white.png),",
       "paste ONE prompt, 9:16 portrait. Check H looks like the reference and the background is pure white.",
       "Save with the file name above each prompt and send all in one zip or PDF (same order is fine).",
       ""]
n = 0
for head, items in G:
    out += ["=" * 70, head, "=" * 70, ""]
    for name, scene in items:
        n += 1
        out += [f"{n}. {name}.png", f"{scene}. " + STYLE, ""]
open("gags/gag-prompts.txt", "w").write("\n".join(out))
print(n)
