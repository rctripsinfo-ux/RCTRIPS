# Owner voice -> cut voice + word times for director.py (same steps as fast_render.py, no render):
# Gemini (gemini_voice.py, cached voice/<name>.wav) or VOICE_FILE; word alignment through the Reel Engine server
# (pocketsphinx); every gap cut to a short breath (0.22 s sentence end, 0.1 s comma, 0.04 s word), holds from HOLD.
# usage: python3 voice_prep.py day05 day05.txt ['{"it.": 0.35}']  -> voice/day05_cut.wav + voice/day05_cut.words.json
import json, os, subprocess, sys, urllib.request, wave
name, script = sys.argv[1:3]; HOLD = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
W = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.expanduser("~/reel-engine-tool"); pdir = f"{TOOL}/public/projects/{name}"
def api(path, body=None):
    req = urllib.request.Request(f"http://127.0.0.1:3011{path}", data=body, method="POST" if body is not None else "GET", headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=600).read() or b"{}")
src = os.environ.get("VOICE_FILE") or f"{W}/voice/{name}.wav"
if not os.path.exists(src): subprocess.run(["python3", f"{W}/gemini_voice.py", script, src], check=True)
tmp = f"/tmp/{name}-v.wav"; subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "44100", "-sample_fmt", "s16", tmp], check=True)
os.makedirs(pdir, exist_ok=True); api(f"/api/projects/{name}/voice?filename=voice.wav", open(tmp, "rb").read())
txt = " ".join(open(script, encoding="utf-8-sig").read().split())
r = api(f"/api/projects/{name}/sync", json.dumps({"script": txt}).encode()); print("sync:", r)
words = json.load(open(f"{pdir}/words.json"))["words"]
w = wave.open(tmp); prm = w.getparams(); rate = w.getframerate(); audio = w.readframes(w.getnframes()); w.close(); bpf = prm.sampwidth * prm.nchannels
def chunk(a, b): return audio[int(a * rate) * bpf:int(b * rate) * bpf]
def want(t): return HOLD.get(t, 0.22 if t[-1:] in ".?!:" else 0.1 if t[-1:] in ",;" else 0.04)
out = bytearray(bytes(int(0.05 * rate) * bpf)); t = 0.05; new = []
for i, x in enumerate(words):
    s0, e0 = x["start"], x["end"]; out += chunk(s0, e0); new.append((t, t + e0 - s0)); t += e0 - s0
    nxt = words[i + 1]["start"] if i + 1 < len(words) else e0 + 0.3; g = nxt - e0
    gw = 0.3 if i + 1 == len(words) else (HOLD[x["text"]] if x["text"] in HOLD else min(g, want(x["text"])))
    out += chunk(e0, e0 + gw) if gw <= g else chunk(e0, nxt) + bytes(int((gw - g) * rate) * bpf); t += gw
for x, (a, b) in zip(words, new): x["start"], x["end"] = round(a, 3), round(b, 3)
o = wave.open(f"{W}/voice/{name}_cut.wav", "wb"); o.setparams(prm); o.writeframes(bytes(out)); o.close()
json.dump({"words": words}, open(f"{W}/voice/{name}_cut.words.json", "w"))
print(f"{name}: {len(audio) / bpf / rate:.1f} s -> {len(out) / bpf / rate:.1f} s, {len(words)} words")
