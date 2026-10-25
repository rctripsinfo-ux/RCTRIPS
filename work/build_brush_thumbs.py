# Brush-band thumbnails (owner, 25 Oct): the "STOP THESE 5 PUSH-UP MISTAKES" look in 9:16 for the uploaded videos.
# Three stacked lines (black / big white on a rough red brush band / black), red brush underline, black curved
# arrow into a dashed circle that shows the real muscle on H's body, warm off-white background.
# Thumbnails 1-2 were written by hand in chat; this file makes 3-20. Every prompt is standalone.
OUT = "thumbnails/brush-03-20-prompts.txt"

CHAR = ('Use the attached character image as the main character and build this thumbnail from it. Keep his face, '
        'head shape, skin tone, body proportions and outfit 100% identical to the reference. Do not redesign or restyle '
        'him. Same art style as the reference. Only ONE character appears.\n\n'
        'Character details: bald muscular man, warm tan skin, white letter "H" on his forehead, olive military utility '
        'belt with pouches and a silver buckle, black shorts with olive harness straps, black wrist wraps, olive combat sneakers.')

SAFE = ('CROP-SAFE SPACING (very important, follow strictly):\n'
        '- Leave a completely empty background margin at the TOP: about 15% of the image height. Nothing in it: no letters, no shapes. The first text line starts only BELOW this band.\n'
        '- Leave a completely empty background margin at the BOTTOM: about 18% of the image height.\n'
        '- The three text lines, the red brush underline, the arrow, the circle{extra} and the whole character must all sit inside the central 67% of the image height.\n'
        '- Keep about 6% empty margin on the left and right.\n'
        '- No element, letter or body part touches or is cut off by any edge.')

BG = 'BACKGROUND: plain warm off-white (very light cream, almost white). Only a soft grey shadow on the floor under the character. No other colors, no gradients, no scenery.'

HEAD = ('1. HEADLINE TEXT (upper part of the safe area, centered, three lines stacked tightly, the block filling about 88% of the image width):\n'
        '   - Top line: {a}, written in solid black letters on the background.\n'
        '   - Middle line: {b}, the BIGGEST line (about 1.8 times taller than the other two), written in bold white letters with a thick black outline and a small black drop shadow, '
        'sitting on a rough red paint brush-stroke band behind it. The red band has ragged dry-brush edges, spans the full width of the word plus a little extra on both sides, and is slightly tilted.\n'
        '   - Bottom line: {c}, written in solid black letters on the background.\n'
        '   Write only these words; never write color names or quote marks.\n'
        '   FONT: Anton (or Impact), extra-heavy condensed bold sans-serif, ALL CAPS, very thick strokes, the same font and weight for all three lines. '
        'Black lines have a thin white outline. Never thin, never regular weight, never a different font.\n'
        '   Directly under the bottom line: one red brush-stroke swoosh underline, thick in the middle with tapered pointed ends, about 60% of the text width.')

CIRCLE = ('3. MUSCLE CIRCLE: a round circle drawn ON his body around the {where}, with a thick DASHED {ring}-and-white outline. Inside the circle the skin is replaced by a realistic '
          'medical-illustration view of {inside}, with clear muscle fiber lines and realistic red-pink muscle color, like an anatomy cutaway.{glow}')

PAIN = ' A small bright orange-red pain glow sits on the edge of the circle.'
GOOD = ' A soft green glow surrounds the circle edge.'

ARROW = ('4. ARROW: one thick curved solid BLACK arrow with a thin white edge, starting just under the headline on the {side} side and curving down into the circle, the arrowhead touching the circle.')

STYLE = ('STYLE: clean semi-realistic comic illustration, bold black outlines, smooth shading, highly detailed and anatomically accurate muscles, strong soft top lighting, '
         'crisp shadows, high contrast, reads instantly on a small phone screen.')

AVOID = ('AVOID: any letter or element in the top 15% or bottom 18% of the image, anything touching or cut off by an edge, thin or light font, a different font, mixed fonts, '
         'a smooth clean red rectangle instead of a rough brush band, any text other than the three headline lines, numbers, badges, icons, fire, pure white or colored or dark '
         "background, gradients, scenery, extra characters, changing the character's face or design, realistic photo style, 3D render, spelling errors, extra limbs, extra fingers, watermarks{more}.")

SOFT = "IMPORTANT BODY CHANGE: a slightly soft belly with a thin fat layer covering the six-pack; keep his face, the H, his arms and chest unchanged."
BELT = "The crop line at the belt sits above the bottom 18%."

# number, title, (top, middle, bottom), idea, scene, (where, ring, inside, pain), arrow side, extra safe items, extra avoid
V = [
    (3, "Always starting tomorrow", ("STOP SAYING", "TOMORROW", "START TODAY"),
     "H is done waiting and bursts into action, legs firing",
     "pure side view, H bursting forward into a powerful sprint start, front knee high, rear leg pushing off the floor, arms pumping, fierce determined face, motion energy. Full body visible.",
     ("front thigh", "green", "the thigh muscles (quadriceps) firing", False), "left", "", ", sitting or lying pose"),
    (4, "Crunches won't burn belly fat", ("CRUNCHES", "WON'T BURN", "BELLY FAT"),
     "H does crunches but the fat on his belly stays",
     f"pure side view, H lying on his back on the floor doing a crunch, shoulders lifted, knees bent, both feet flat on the floor, hands behind his head, frustrated face. {SOFT}",
     ("belly", "red", "a layer of yellow belly fat under the skin sitting on top of the six-pack muscles", True), "right", "", ", visible sharp six-pack, more than two legs"),
    (5, "Obliques make you look bigger", ("SIDE ABS MAKE", "WIDER", "YOUR WAIST"),
     "heavy side-ab training makes H's waist thick and blocky",
     "front view, H standing straight, hands behind his head, showing a thick blocky waist. Two short red horizontal double-headed arrows point outward from both sides of his waist.",
     ("side of the waist (side abs)", "red", "the side ab muscles (obliques), thick and bulky", True), "left", ", the two waist arrows", ""),
    (6, "Muscle that makes arms thick", ("THIS MUSCLE MAKES", "THICK", "ARMS"),
     "the back of the arm (triceps) is what makes arms look thick",
     f"pure side view, upper body from the head down to the belt, H pressing his straight arm down and back to flex the back of the upper arm hard, confident face. {BELT}",
     ("back of the upper arm", "green", "the three-headed triceps muscle, big and full", False), "left", "", ""),
    (7, "Skinny wrists", ("FIX YOUR", "SKINNY", "WRISTS"),
     "H looks at his thin wrist, holding a water bottle, the simple fix",
     f"upper body from the head down to the belt, H holding his forearm up in front of him, gripping a plain clear water bottle, looking at his own wrist with a worried face. NO wrist wraps on this arm so the wrist is visible; the wrist looks thin compared to his big arm. {BELT}",
     ("wrist", "red", "the wrist and lower forearm with thin tendons and small forearm muscles", True), "right", ", the water bottle", ", wrist wraps on the raised arm, text on the bottle"),
    (8, "Box body and V-taper", ("FROM BOX BODY", "TO V-TAPER", "WIDE BACK, SMALL WAIST"),
     "a wide back and narrow waist turn a box body into a V shape",
     "back view, H doing a lat spread: elbows out, fists on his waist, the upper back wide and the waist narrow, a clear V shape. His head turned slightly to the side so the H on his forehead is visible.",
     ("side of the upper back (lats)", "green", "the wide back muscles (lats) spreading like wings", False), "left", "", ", front view"),
    (9, "100 push-ups, flat chest", ("100 PUSH-UPS", "FLAT", "CHEST?"),
     "H does push-up after push-up but his chest stays flat",
     "pure side view, H at the top of a push-up, both palms flat on the floor under his shoulders, arms straight, body in one straight line, both feet on his toes, sweating, tired face.",
     ("chest", "red", "the chest muscle (pec), looking thin and flat", True), "left", "", ", hands off the floor, more than two legs, knees on the floor"),
    (10, "Sweat versus fat loss", ("DOES MORE", "SWEAT", "BURN MORE FAT?"),
     "H is dripping with sweat but the belly fat has not changed",
     f"front view, H standing, drenched in sweat, big sweat drops dripping off his head and body onto the floor, wiping his forehead with one forearm, doubtful face. {SOFT}",
     ("belly", "red", "a layer of yellow belly fat under the skin that has not changed", True), "left", ", the sweat drops", ", sweat covering the H"),
    (11, "Long stretches before workout", ("STOP LONG", "STRETCHES", "BEFORE WORKOUT"),
     "a long cold stretch before training strains the muscle",
     "pure side view, H sitting on the floor in a long hamstring stretch, both legs straight in front of him, reaching for his toes, strained face.",
     ("back of the thigh", "red", "the hamstring muscles, cold and overstretched", True), "right", "", ", standing pose"),
    (12, "Boulder shoulders", ("BUILD", "BOULDER", "SHOULDERS"),
     "big round shoulders like boulders",
     f"3/4 front view, upper body from the head down to the belt, H in a front double-biceps pose showing huge round shoulders, proud face. {BELT}",
     ("shoulder", "green", "the round three-part shoulder muscle (deltoid), big like a boulder", False), "left", "", ""),
    (13, "Signs you're skinny fat", ("ARE YOU", "SKINNY FAT?", "CHECK THESE SIGNS"),
     "thin arms and chest but a soft belly: the skinny-fat body",
     "front view, H standing, arms down, looking down at his body with a confused face. IMPORTANT BODY CHANGE: skinny-fat body: thin arms and narrow chest with a soft round belly and no visible abs; keep his face, the H and his outfit unchanged.",
     ("belly", "red", "a soft layer of yellow fat over weak, thin ab muscles", True), "left", "", ", a muscular body, visible six-pack"),
    (14, "Double your push-ups", ("HOW TO", "DOUBLE", "YOUR PUSH-UPS"),
     "H does strong push-ups with the chest and triceps working hard",
     "pure side view, H doing a powerful push-up halfway down, both palms flat on the floor under his shoulders, elbows at 45 degrees, body in one straight line, both feet on his toes, fierce strong face.",
     ("chest and back of the upper arm", "green", "the chest muscle (pec) and the triceps working hard", False), "left", "", ", hands off the floor, more than two legs, knees on the floor"),
    (15, "Dead hang for forearms", ("DEAD HANG FOR", "GRIP", "AND FOREARMS"),
     "hanging from a bar builds a strong grip and thick forearms",
     "front view, H hanging from a black horizontal pull-up bar with both hands, arms straight, feet off the ground, legs straight together, focused strong face. NO wrist wraps so the forearms are visible. The bar sits below the headline, inside the safe area.",
     ("forearm", "green", "the forearm muscles and grip tendons, thick and strong", False), "right", ", the pull-up bar", ", wrist wraps, bar touching the headline"),
    (16, "Sharp jawline", ("GET A", "SHARP", "JAWLINE"),
     "a sharp, defined jaw and neck",
     "pure side profile, head, neck and shoulders, H with his chin slightly raised, calm confident face, a sharp defined jaw. The crop line at the chest sits above the bottom 18%.",
     ("jaw and neck", "green", "the jaw muscle (masseter) and the side neck muscles", False), "left", "", ", front view"),
    (17, "Abs exercise nobody does", ("THE ABS EXERCISE", "NOBODY", "DOES"),
     "the deep inner ab muscle most people never train",
     "front view, H standing, hands on his hips, pulling his belly in tight, focused face.",
     ("lower belly", "green", "the deep inner ab muscle that wraps around the waist like a corset, under the six-pack", False), "left", "", ""),
    (18, "Push-up mistake", ("THIS PUSH-UP", "MISTAKE", "HURTS YOUR SHOULDERS"),
     "shrugged, rolled-forward shoulders in a push-up strain the shoulder",
     "pure side view, H at the top of a push-up, both palms flat on the floor, arms straight, both feet on his toes, BUT his shoulders are shrugged up toward his ears and rolled forward. Strained face.",
     ("shoulder", "red", "the shoulder joint and upper shoulder muscles, strained", True), "left", "", ", hands off the floor, more than two legs"),
    (19, "Thicker wrists", ("HOW TO GET", "THICKER", "WRISTS"),
     "a thick, strong forearm and wrist",
     f"upper body from the head down to the belt, H holding his forearm up in front of him, fist clenched hard, flexing his thick forearm, proud face. NO wrist wraps on this arm. {BELT}",
     ("forearm and wrist", "green", "thick forearm muscles and wrist tendons", False), "right", "", ", wrist wraps on the raised arm"),
    (20, "Running and belly fat", ("CAN RUNNING", "BURN", "BELLY FAT?"),
     "H runs on a treadmill but the belly fat stays",
     f"pure side view, H running on a simple grey treadmill, mid-stride, sweating, doubtful face. {SOFT} The whole treadmill sits inside the safe area.",
     ("belly", "red", "a layer of yellow belly fat under the skin", True), "left", ", the treadmill", ", treadmill cut off, more than two legs"),
]


def prompt(lines, idea, scene, circ, side, extra, more):
    a, b, c = lines
    where, ring, inside, pain = circ
    return "\n\n".join([
        "IMAGE SIZE: 1080x1920, 9:16 vertical YouTube Shorts thumbnail.",
        CHAR,
        SAFE.format(extra=extra),
        f'CORE IDEA: A bold three-line headline says "{a} {b} {c}" and the image proves it: {idea}, and a black arrow points into a circle on his body that shows the real muscle.',
        BG,
        "LAYOUT (top to bottom):\n" + "\n".join([
            HEAD.format(a=a, b=b, c=c),
            f"2. CHARACTER (lower part of the safe area, large, filling most of the safe width): {scene}",
            CIRCLE.format(where=where, ring=ring, inside=inside, glow=PAIN if pain else GOOD),
            ARROW.format(side=side)]),
        STYLE,
        AVOID.format(more=more)])


parts = []
for n, title, lines, idea, scene, circ, side, extra, more in V:
    parts.append(f"===== THUMBNAIL {n}: {title} =====\n\n" + prompt(lines, idea, scene, circ, side, extra, more))
open(OUT, "w").write("\n\n\n".join(parts) + "\n")
print(OUT, len(parts), "prompts")
