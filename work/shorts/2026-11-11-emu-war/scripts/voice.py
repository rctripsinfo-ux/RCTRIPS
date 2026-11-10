# Kokoro voice per sentence -> voice/voice.wav + voice/words.json (word times spread by syllables inside each sentence)
import json, re, sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
VOICE, SPEED = sys.argv[1] if len(sys.argv) > 1 else "am_michael", float(sys.argv[2]) if len(sys.argv) > 2 else 1.08
# (text, gap after in seconds)
LINES = [
 ("Oregon once tried to make a dead whale disappear.", .12), ("Instead, they made it rain whale.", .35),
 ("November, nineteen seventy.", .1), ("A forty-five-foot sperm whale washes up on the beach at Florence.", .12), ("Eight tons.", .1), ("And it stinks.", .35),
 ("Bury it?", .05), ("The tide would dig it right back up.", .12), ("Tow it?", .05), ("Way too heavy.", .15),
 ("So the highway department has a better idea: blow it up.", .12), ("Tiny pieces, and the seagulls will clean up the rest.", .35),
 ("One man in the crowd, Walter Umenhofer, learned explosives in the army.", .12), ("He told them twenty sticks would do it.", .12),
 ("They brought twenty cases.", .1), ("Half a ton of dynamite.", .35),
 ("Crowds gather.", .08), ("Cameras roll.", .2), ("Three.", .2), ("Two.", .2), ("One.", 1.3),
 ("For one second, it's beautiful.", .15), ("Then the sky starts falling.", .12),
 ("Chunks of blubber rain on the crowd, on the dunes, all the way to the parking lot.", .35),
 ("Luckily, nobody was hurt.", .2), ("Unluckily, it was still raining whale.", .4),
 ("You see, a blast always goes where it's easiest.", .15), ("Step on a ketchup packet:", .08), ("the ketchup doesn't go into the floor.", .1),
 ("It shoots out sideways, straight at your friend.", .2), ("The packed sand wouldn't move, so all that force went the easy way.", .1),
 ("Up.", .2), ("And toward the people.", .4),
 ("And the seagulls?", .12), ("The boom scared every single one away.", .12), ("Most of the whale was still lying there.", .1),
 ("So the crew buried it anyway.", .4),
 ("And the one man who said, too much dynamite?", .25), ("The biggest chunk landed right on his car.", .8),
]
def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower()) or "a"
    n = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and len(w) > 3 else 0)
    return max(1, n)
k = Kokoro("models/kokoro.onnx", "models/voices.bin")
SR = 24000; out = [np.zeros(int(.15 * SR), np.float32)]; t = .15; words = []; lines = []
GS = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
for text, gap in LINES:
    gap = gap if gap >= 1 else gap * GS
    a, sr = k.create(text, voice=VOICE, speed=SPEED, lang="en-us"); assert sr == SR
    a = a.astype(np.float32); e = np.abs(a) > 0.01; i0 = int(np.argmax(e)); i1 = len(a) - int(np.argmax(e[::-1]))
    a = a[max(0, i0 - 240):min(len(a), i1 + 480)]; d = len(a) / SR
    ws = text.split(); wt = [syl(w) + .35 for w in ws]; tot = sum(wt); c = t
    for w, x in zip(ws, wt):
        dd = d * x / tot; words.append({"w": re.sub(r"[^\w'-]", "", w), "s": round(c, 3), "e": round(c + dd, 3)}); c += dd
    lines.append({"text": text, "s": round(t, 3), "e": round(t + d, 3)})
    out += [a, np.zeros(int(gap * SR), np.float32)]; t += d + gap
v = np.concatenate(out); v = v / max(1e-6, np.abs(v).max()) * 0.89
sf.write("voice/voice.wav", v, SR); json.dump(words, open("voice/words.json", "w"), indent=0); json.dump(lines, open("voice/lines.json", "w"), indent=1)
print(f"total {len(v)/SR:.2f}s, {len(words)} words, {len(words)/(len(v)/SR):.2f} w/s")
for l in lines: print(f'{l["s"]:6.2f} {l["e"]:6.2f}  {l["text"]}')
