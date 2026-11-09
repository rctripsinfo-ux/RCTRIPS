# Pisa short: am_fenrir, back to back (3.6-3.9 w/s), writes voice/voice.wav, voice/lines.json (s/e per line), voice/words.json
import json, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro("models/kokoro.onnx", "models/voices.bin"); SR = 24000; SPEED = 1.18
LINES = [
 "Pisa spent two hundred years building a tower that started falling over before it was even finished.",
 "Eleven seventy-three.", "The city wants the most beautiful bell tower in Italy.", "White marble.", "Eight floors.",
 "Five years later, floor three goes up, and the whole tower starts to lean.",
 "Luckily, a war stops the work for almost a hundred years.", "Unluckily, when the builders come back, it is still leaning.",
 "So they have an idea.", "Build the new floors taller on the short side.", "The tower doesn't straighten.", "It bends.",
 "Today it's shaped like a banana.",
 "You see, the tower stands on soft clay and sand.", "It's like standing on a mattress.", "Lean on one foot, and that side sinks.",
 "The heavier the tower got, the deeper it sank.",
 "By nineteen ninety, it leans five and a half degrees.", "They close it.",
 "Engineers wrap it in steel cables, stack heavy lead weights on the high side, and slowly pull soil out from under it.",
 "It works.", "The tower straightens by about forty centimeters.",
 "And then they stop.", "On purpose.", "Nobody comes to Pisa to see a straight tower.",
 "And the twist?", "The soft ground that made it lean has also saved it from four big earthquakes.",
 "The mud wobbles, so the tower doesn't break.",
]
def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower()) or "a"; n = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and len(w) > 3 else 0); return max(1, n)
t = 0.1; parts = [np.zeros(int(t * SR), np.float32)]; lines = []; words = []
for text in LINES:
    a, _ = k.create(text, voice="am_fenrir", speed=SPEED, lang="en-us"); a = a.astype(np.float32)
    e = np.abs(a) > 0.012; i0 = int(np.argmax(e)); i1 = len(a) - int(np.argmax(e[::-1])); a = a[max(0, i0 - 60):min(len(a), i1 + 200)]
    d = len(a) / SR; ws = text.split(); wt = [syl(w) + .35 for w in ws]; c = t
    for w, x in zip(ws, wt): dd = d * x / sum(wt); words.append({"w": w, "s": round(c, 3), "e": round(c + dd, 3)}); c += dd
    lines.append({"text": text, "s": round(t, 3), "e": round(t + d, 3)})
    gap = 0.16 if text.endswith((".", "?", "!")) else 0.06
    parts += [a, np.zeros(int(gap * SR), np.float32)]; t += d + gap
v = np.concatenate(parts + [np.zeros(int(0.6 * SR), np.float32)])
sf.write("voice/voice.wav", v / np.abs(v).max() * 0.89, SR); json.dump(lines, open("voice/lines.json", "w"), indent=0); json.dump(words, open("voice/words.json", "w"))
print(f"dur {len(v)/SR:.2f}s frames {round(len(v)/SR*30)} words {len(words)} rate {len(words)/(words[-1]['e']-words[0]['s']):.2f}")
for l in lines: print(f"{l['s']:6.2f} f{round(l['s']*30):5d}  {l['text'][:60]}")
