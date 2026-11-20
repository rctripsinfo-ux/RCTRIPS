# usage: python3 tools/dialogue_voice.py <name> <script.txt> ['{"line text": gap_s}']
# script lines "H: ..." / "M: ..." -> H (Fenrir, deep calm) + Mini-H (Puck, high, fast) via gemini_voice.py, aligned with voice_prep.py,
# then cut line by line and joined into voice/<name>_cut.wav + voice/<name>_cut.words.json (each word has "spk")
import json, os, subprocess, sys, wave, numpy as np
name, script = sys.argv[1:3]; GAP = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(W)
import urllib.request, time
try: urllib.request.urlopen("http://127.0.0.1:3011/", timeout=3)
except Exception:  # Reel Engine server (word alignment) dies with container resets: start it
    subprocess.Popen("cd ~/reel-engine-tool && PORT=3011 setsid nohup node tools/server.mjs > /tmp/reel-server.log 2>&1 < /dev/null &", shell=True); time.sleep(5)
lines = [l.split(": ", 1) for l in open(script).read().strip().split("\n")]
cfg = {"H": (["--voice", "Fenrir", "--pitch", "deep", "--speed", "1.0", "--emotion", "calm, low and steady, confident coach with a dry sense of humour"]),
       "M": (["--voice", "Puck", "--pitch", "high", "--speed", "1.15", "--emotion", "playful, cheeky, a little whiny, like a tiny sidekick"])}
SPK = [k for k in ("H", "M") if any(s == k for s, _ in lines)]  # a part may have only one speaker
for k in SPK:
    txt = f"/tmp/{name}_{k}.txt"; open(txt, "w").write("\n".join(t for s, t in lines if s == k))
    raw = f"voice/{name}_{k.lower()}.wav"
    if not os.path.exists(raw): subprocess.run(["python3", "gemini_voice.py", txt, raw] + cfg[k], check=True)
    subprocess.run(["python3", "voice_prep.py", f"{name}_{k.lower()}", txt], check=True, env=dict(os.environ, NATURAL="1", VOICE_FILE=raw))
src = {}
for k in SPK:
    w = json.load(open(f"voice/{name}_{k.lower()}_cut.words.json"))["words"]; f = wave.open(f"voice/{name}_{k.lower()}_cut.wav")
    src[k] = (w, np.frombuffer(f.readframes(f.getnframes()), np.int16), f.getframerate())
rate = src[SPK[0]][2]; ptr = {k: 0 for k in SPK}; out = [np.zeros(int(0.15 * rate), np.int16)]; words = []; t = 0.15
for spk, txt in lines:
    n = len(txt.split()); w, a, _ = src[spk]; seg = w[ptr[spk]:ptr[spk] + n]; ptr[spk] += n
    s0 = max(0, seg[0]["start"] - 0.04); s1 = seg[-1]["end"] + 0.06; x = a[int(s0 * rate):int(s1 * rate)]; out.append(x)
    words += [dict(text=s["text"], start=round(s["start"] - s0 + t, 3), end=round(s["end"] - s0 + t, 3), spk=spk) for s in seg]
    t += len(x) / rate; g = GAP.get(txt, 0.3); out.append(np.zeros(int(g * rate), np.int16)); t += g
assert all(ptr[k] == len(src[k][0]) for k in ptr), ptr
f = wave.open(f"voice/{name}_cut.wav", "w"); f.setnchannels(1); f.setsampwidth(2); f.setframerate(rate); f.writeframes(np.concatenate(out).tobytes()); f.close()
json.dump({"words": words}, open(f"voice/{name}_cut.words.json", "w")); print(f"{name}: {t:.1f} s, {len(words)} words")
