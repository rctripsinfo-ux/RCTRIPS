# One-word thumbnails (owner, 25 Oct): the "STOP" push-up thumbnail look for 20 already-uploaded videos.
# Giant red word, red brush underline, black curved arrow into a dashed circle that shows the real muscle
# on H's body, warm off-white background. Every prompt is standalone (agents run them one by one).
OUT = "thumbnails/oneword-20-prompts.txt"

CHAR = ('Use the attached character image as the main character and build this thumbnail from it. Keep his face, '
        'head shape, skin tone, body proportions and outfit 100% identical to the reference. Do not redesign or restyle '
        'him. Same art style as the reference. Only ONE character appears.\n\n'
        'Character details: bald muscular man, warm tan skin, white letter "H" on his forehead, olive military utility '
        'belt with pouches and a silver buckle, black shorts with olive harness straps, black wrist wraps, olive combat sneakers.')

SAFE = ('CROP-SAFE SPACING (very important, follow strictly):\n'
        '- Leave a completely empty background margin at the TOP: about 15% of the image height. Nothing in it: no letters, no shapes. The headline starts only BELOW this band.\n'
        '- Leave a completely empty background margin at the BOTTOM: about 18% of the image height.\n'
        '- The headline word, the brush underline, the arrow, the circle{extra} and the whole character must all sit inside the central 67% of the image height.\n'
        '- Keep about 6% empty margin on the left and right.\n'
        '- No element, letter or body part touches or is cut off by any edge.')

BG = 'BACKGROUND: plain warm off-white (very light cream, almost white). Only a soft grey shadow on the floor under the character. No other colors, no gradients, no scenery.'

HEAD = ('1. HEADLINE (upper part of the safe area, centered): one giant word: {word}. Write only this word{punct}; never write color names or quote marks.\n'
        '   FONT: Anton (or Impact), ultra-heavy bold condensed sans-serif, ALL CAPS, very thick strokes. The word is HUGE and fills about 90% of the image width. '
        'Solid bright red letters (#E00000) with a subtle darker red shade toward the bottom of each letter, no outline. Letters are slightly hand-cut with a gentle dynamic tilt, '
        'like a bold poster stamp. Never thin, never regular weight, never a different font.\n'
        '   Directly under the word: one red brush-stroke swoosh underline, thick in the middle with tapered pointed ends, about 70% of the word width.')

ARROW = ('{n}. ARROW: one thick curved solid BLACK arrow with a thin white edge, starting just under the brush underline and curving down into the circle, the arrowhead touching the circle.')

CIRCLE = ('{n}. MUSCLE CIRCLE: a round circle drawn ON his body around the {where}, with a thick DASHED {ring} outline. Inside the circle the skin is replaced by a realistic '
          'medical-illustration view of {inside}, with clear muscle fiber lines and realistic red-pink muscle color, like an anatomy cutaway.{glow}')

STYLE = ('STYLE: clean semi-realistic comic illustration, bold black outlines, smooth shading, highly detailed and anatomically accurate muscles, strong soft top lighting, '
         'crisp shadows, high contrast, reads instantly on a small phone screen.')

AVOID = ('AVOID: any letter or element in the top 15% or bottom 18% of the image, anything touching or cut off by an edge, thin or light font, a different font, an outline on the headline, '
         'more than one word of text, extra text, labels, numbers, badges, icons, fire, pure white or colored or dark background, gradients, scenery, extra characters, changing the '
         "character's face or design, realistic photo style, 3D render, spelling errors, extra limbs, extra fingers, watermarks{more}.")

PAIN = ' A small bright orange-red pain glow with tiny sparks sits on the edge of the circle.'
GOOD = ' A soft green glow surrounds the circle edge.'

# (title, word, scene, circle: (where, ring, inside, pain?), extra in safe list, extra avoid)
V = [
    ("Abs workout hurts your back", "OUCH!",
     "pure side view, H lying on his back on the floor doing a sit-up, halfway up, knees bent, both feet flat on the floor, hands behind his head, his lower back visibly arching and straining. Face: teeth clenched, eyes squeezed, clear pain.",
     ("lower back", "red", "the lower spine and lower-back muscles, the spine bones glowing red-orange like inflammation", True), "", ", hands off his head, legs straight"),
    ("Leg raises hurting your back", "STOP!",
     "pure side view, H lying on his back doing a leg raise, propped on his forearms, both palms flat on the floor beside his hips. Exactly two legs: straight together, raised high toward the upper right at about 60 degrees. His lower back is visibly arched off the floor. Face: teeth clenched, clear pain. His raised feet stay below the headline.",
     ("lower back where it lifts off the floor", "red", "the lower spine and lower-back muscles, the spine bones glowing red-orange like inflammation", True), "", ", more than two legs, legs bent"),
    ("Always starting tomorrow", "TODAY!",
     "pure side view, H bursting forward into a powerful sprint start, front knee high, rear leg pushing off the floor, arms pumping, fierce determined face, motion energy. Full body visible.",
     ("front thigh", "green", "the thigh muscles (quadriceps) firing", False), "", ", sitting or lying pose"),
    ("Crunches won't burn belly fat", "MYTH!",
     "front view, H standing, looking down at his belly and pinching a small fold of belly fat with both hands, doubtful face. IMPORTANT BODY CHANGE: a slightly soft belly with a thin fat layer covering the six-pack; keep his face, the H, his arms and chest unchanged.",
     ("belly", "red", "a layer of yellow belly fat under the skin sitting on top of the six-pack muscles", True), "", ", visible sharp six-pack"),
    ("Obliques make you look bigger", "WIDER?",
     "front view, H standing straight, hands on his head, showing a thick blocky waist. Two short red horizontal double-headed arrows point outward from both sides of his waist.",
     ("side of the waist (side abs)", "red", "the side ab muscles (obliques), thick and bulky", True), ", the two waist arrows", ""),
    ("Muscle that makes arms thick", "THICK!",
     "pure side view, upper body from the head down to the belt, H pressing his straight arm down and back to flex the back of the upper arm hard, confident face. The crop line at the belt sits above the bottom 18%.",
     ("back of the upper arm", "green", "the three-headed triceps muscle, big and full", False), "", ""),
    ("Skinny wrists", "SKINNY?",
     "upper body from the head down to the belt, H holding his forearm up in front of him, fist closed, looking at his own wrist with a worried face. NO wrist wraps on this arm so the wrist is visible. The wrist looks thin compared to his big arm. The crop line at the belt sits above the bottom 18%.",
     ("wrist", "red", "the wrist and lower forearm with thin tendons and small forearm muscles", True), "", ", wrist wraps on the raised arm"),
    ("Box body and V-taper", "V-SHAPE!",
     "back view, H doing a lat spread: elbows out, fists on his waist, the upper back wide and the waist narrow, a clear V shape. His head turned slightly to the side so the H on his forehead is visible.",
     ("side of the upper back (lats)", "green", "the wide back muscles (lats) spreading like wings", False), "", ", front view"),
    ("100 push-ups, flat chest", "FLAT?",
     "pure side view, H at the top of a push-up, both palms flat on the floor under his shoulders, arms straight, body in one straight line, both feet on his toes, sweating and tired face.",
     ("chest", "red", "the chest muscle (pec), looking thin and flat", True), "", ", hands off the floor, more than two legs, knees on the floor"),
    ("Sweat versus fat loss", "SWEAT?",
     "front view, H standing, drenched in sweat, big sweat drops dripping off his head and body onto the floor, wiping his forehead with one forearm, doubtful face. IMPORTANT BODY CHANGE: a slightly soft belly with a thin fat layer; keep his face and the H unchanged.",
     ("belly", "red", "a layer of yellow belly fat under the skin that has not changed", True), ", the sweat drops", ", sweat covering the H"),
    ("Long stretches before workout", "WAIT!",
     "pure side view, H sitting on the floor in a long hamstring stretch, both legs straight in front of him, reaching for his toes, strained face.",
     ("back of the thigh", "red", "the hamstring muscles, cold and overstretched", True), "", ", standing pose"),
    ("Boulder shoulders", "BOULDERS!",
     "3/4 front view, upper body from the head down to the belt, H in a front double-biceps pose showing huge round shoulders, proud face. The crop line at the belt sits above the bottom 18%.",
     ("shoulder", "green", "the round three-part shoulder muscle (deltoid), big like a boulder", False), "", ""),
    ("Signs you're skinny fat", "SKINNY FAT?",
     "front view, H standing, arms down, looking down at his body with a confused face. IMPORTANT BODY CHANGE: skinny-fat body: thin arms and narrow chest with a soft round belly and no visible abs; keep his face, the H and his outfit unchanged.",
     ("belly", "red", "a soft layer of yellow fat over weak, thin ab muscles", True), "", ", a muscular body, visible six-pack"),
    ("Double your push-ups", "DOUBLE!",
     "pure side view, H doing a powerful push-up halfway down, both palms flat on the floor under his shoulders, elbows at 45 degrees, body in one straight line, both feet on his toes, fierce strong face.",
     ("chest and back of the upper arm", "green", "the chest muscle (pec) and the triceps working hard", False), "", ", hands off the floor, more than two legs, knees on the floor"),
    ("Dead hang for forearms", "GRIP!",
     "front view, H hanging from a black horizontal pull-up bar with both hands, arms straight, feet off the ground, legs straight together, focused strong face. NO wrist wraps so the forearms are visible. The bar sits below the headline, inside the safe area.",
     ("forearm", "green", "the forearm muscles and grip tendons, thick and strong", False), ", the pull-up bar", ", wrist wraps, bar touching the headline"),
    ("Sharp jawline", "JAWLINE!",
     "pure side profile, head, neck and shoulders, H with his chin slightly raised, calm confident face, a sharp defined jaw. The crop line at the chest sits above the bottom 18%.",
     ("jaw and neck", "green", "the jaw muscle (masseter) and the side neck muscles", False), "", ", front view"),
    ("Abs exercise nobody does", "ABS!",
     "front view, H standing, hands on his hips, pulling his belly in tight, focused face.",
     ("lower belly", "green", "the deep inner ab muscle that wraps around the waist like a corset, under the six-pack", False), "", ""),
    ("Push-up mistake", "WRONG!",
     "pure side view, H at the top of a push-up, both palms flat on the floor, arms straight, both feet on his toes, BUT his shoulders are shrugged up toward his ears and rolled forward. Strained face.",
     ("shoulder", "red", "the shoulder joint and upper shoulder muscles, strained and glowing red", True), "", ", hands off the floor, more than two legs"),
    ("Thicker wrists", "THICKER!",
     "upper body from the head down to the belt, H holding his forearm up in front of him, fist clenched hard, flexing his thick forearm, proud face. NO wrist wraps on this arm. The crop line at the belt sits above the bottom 18%.",
     ("forearm and wrist", "green", "thick forearm muscles and wrist tendons", False), "", ", wrist wraps on the raised arm"),
    ("Running and belly fat", "RUNNING?",
     "pure side view, H running on a simple grey treadmill, mid-stride, sweating, doubtful face. IMPORTANT BODY CHANGE: a slightly soft belly with a thin fat layer; keep his face and the H unchanged. The whole treadmill sits inside the safe area.",
     ("belly", "red", "a layer of yellow belly fat under the skin", True), ", the treadmill", ", treadmill cut off"),
]


def prompt(word, scene, circ, extra, more):
    where, ring, inside, pain = circ
    punct = " and its punctuation mark" if word[-1] in "!?" else ""
    return "\n\n".join([
        "IMAGE SIZE: 1080x1920, 9:16 vertical YouTube Shorts thumbnail.",
        CHAR,
        SAFE.format(extra=extra),
        f"CORE IDEA: one giant word, {word}, tells the topic in one second, and the image proves it: a black arrow points into a circle on H's body that shows the real {where.split(' (')[0]} muscle.",
        BG,
        "LAYOUT (top to bottom):\n" + "\n".join([
            HEAD.format(word=word, punct=punct),
            f"2. CHARACTER (lower part of the safe area, large, filling most of the safe width): {scene}",
            CIRCLE.format(n=3, where=where, ring=ring, inside=inside, glow=PAIN if pain else GOOD),
            ARROW.format(n=4)]),
        STYLE,
        AVOID.format(more=more)])


N = len(V)
parts = [f"CREATE ALL IMAGES FOR THESE {N} THUMBNAILS. Make each one as a SEPARATE image ({N} images total). Treat every prompt "
         "below as a completely separate, independent image request. Attach the same character reference image to every single "
         "one. Follow each prompt exactly as written."]
for i, (title, word, scene, circ, extra, more) in enumerate(V, 1):
    parts.append(f"===== THUMBNAIL {i} OF {N}: {title} =====\n\n" + prompt(word, scene, circ, extra, more))
open(OUT, "w").write("\n\n\n".join(parts) + "\n")
print(OUT, sum(len(p.split()) for p in parts), "words")
