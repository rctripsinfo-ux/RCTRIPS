# Emu War short: am_fenrir, back to back (3.6-3.9 w/s), writes voice/voice.wav, voice/lines.json (s/e per line), voice/words.json
import json, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro("models/kokoro.onnx", "models/voices.bin"); SR = 24000; SPEED = 1.27
LINES = [
 "In nineteen thirty-two, Australia went to war against birds.", "And the birds won.",
 "Western Australia.", "Twenty thousand emus are eating the farmers' wheat.",
 "So the army sends Major Meredith, two soldiers, two machine guns, and ten thousand bullets.",
 "Day one: the emus simply run out of range.",
 "Two days later, a thousand emus walk toward a dam.", "Perfect ambush.",
 "The gun fires, and jams after twelve birds.",
 "Luckily, they have a truck.", "Unluckily, emus run fifty kilometers an hour across bumpy fields.", "The gunner can't even aim.",
 "You see, emus don't stay in one big herd.", "When the shooting starts, they split into tiny groups, each with one bird keeping watch.",
 "It's like trying to catch popcorn while it pops.",
 "After a week, the army goes home.", "Then it comes back.", "In the end, they fire almost ten thousand bullets.",
 "About ten bullets for every bird they hit.",
 "The wheat?", "Still being eaten.",
 "And the twist?", "Major Meredith said the emus could face machine guns with the invulnerability of tanks.",
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
