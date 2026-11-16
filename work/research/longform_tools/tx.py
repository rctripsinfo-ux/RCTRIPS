import sys, json, os, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=2)
for f in sys.argv[1:]:
    out = f.replace(".mp4", ".words.json")
    if os.path.exists(out): continue
    a = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout, np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(a, word_timestamps=True, vad_filter=False)
    S = [dict(start=s.start, end=s.end, text=s.text.strip(), words=[dict(w=w.word.strip(), s=round(w.start, 2), e=round(w.end, 2)) for w in s.words]) for s in segs]
    json.dump(S, open(out, "w")); open(f.replace(".mp4", ".txt"), "w").write("\n".join(f"[{s['start']:.1f}] {s['text']}" for s in S)); print("done", f, flush=True)
