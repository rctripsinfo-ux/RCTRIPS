import subprocess, numpy as np, json, sys
cuts = {l.split(" cuts: ")[0]: [float(x) for x in l.split(" cuts: ")[1].split()] for l in open("/tmp/ref/an/cuts.txt")}
out = {}
for i in range(1, 11):
    v = f"V{i:02d}"; f = f"/tmp/ref/v/{v}.mp4"
    # --- motion: 30 fps grayscale 54x96
    raw = subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-i",f,"-map","0:v:0","-vf","fps=30,scale=54:96,format=gray","-f","rawvideo","-"],capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 96, 54).astype(np.float32)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))  # per-frame change
    moving = d > 0.35
    # longest run of no change
    best = run = 0; bstart = 0; s = 0
    for k, m in enumerate(moving):
        if not m:
            if run == 0: s = k
            run += 1
            if run > best: best, bstart = run, s
        else: run = 0
    first_move = next((k for k, m in enumerate(moving) if m and k > 3), None)
    hook = moving[:90]
    # --- audio: 16 kHz mono
    a = subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-i",f,"-map","0:a:0","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout
    x = np.frombuffer(a, np.float32)
    hop = 160; win = 512
    n = (len(x) - win) // hop
    frames = np.lib.stride_tricks.as_strided(x, (n, win), (x.strides[0]*hop, x.strides[0]))
    S = np.abs(np.fft.rfft(frames * np.hanning(win), axis=1))
    fq = np.fft.rfftfreq(win, 1/16000)
    hi = S[:, fq > 4000].sum(1); lo = S[:, fq < 150].sum(1); tot = S.sum(1) + 1e-9
    flux = np.maximum(0, np.diff(np.log1p(S), axis=0)).sum(1)
    thr = np.median(flux) + 4 * flux.std()
    on = [k for k in range(1, len(flux)-1) if flux[k] > thr and flux[k] >= flux[k-1] and flux[k] >= flux[k+1]]
    ev = []; last = -1
    for k in on:
        t = (k+1) * hop / 16000
        if t - last < 0.15: continue
        last = t
        seg = slice(k+1, min(k+40, len(hi)))  # 0.4 s after onset
        hf = float((hi[seg] / tot[seg]).mean()); lf = float((lo[seg] / tot[seg]).mean())
        e = S[seg].sum(1); dur = float((e > e.max() * 0.3).sum() * hop / 16000)
        kind = "impact/bass" if lf > 0.25 else ("whoosh/noise" if hf > 0.12 and dur > 0.15 else ("click/pop" if dur <= 0.12 else "tonal/other"))
        near = min((abs(t - c) for c in cuts[v]), default=9)
        ev.append({"t": round(t, 2), "kind": kind, "hf": round(hf, 2), "lf": round(lf, 2), "dur": round(dur, 2), "on_cut": near < 0.12})
    # music bed: energy in quietest 10% of frames vs median (narration gaps)
    rms = np.sqrt((frames**2).mean(1)); q = np.percentile(rms, 10) / (np.median(rms) + 1e-9)
    out[v] = {"dur": round(len(x)/16000, 2), "cuts": len(cuts[v]), "cuts_per_10s": round(len(cuts[v]) / (len(x)/16000) * 10, 1),
              "first_motion_s": round(first_move / 30, 2) if first_move else None,
              "hook_motion_pct": round(float(hook.mean()) * 100), "motion_pct": round(float(moving.mean()) * 100),
              "longest_static_s": round(best / 30, 2), "longest_static_at": round(bstart / 30, 2),
              "music_floor_ratio": round(float(q), 2), "sfx_onsets": ev}
json.dump(out, open("/tmp/ref/an/measure.json", "w"), indent=1)
for v, o in out.items():
    ks = {}
    for e in o["sfx_onsets"]: ks[e["kind"]] = ks.get(e["kind"], 0) + 1
    oc = sum(e["on_cut"] for e in o["sfx_onsets"])
    print(v, {k: o[k] for k in o if k != "sfx_onsets"}, "onsets", len(o["sfx_onsets"]), ks, "on_cut", oc,
          "hook:", [(e["t"], e["kind"]) for e in o["sfx_onsets"] if e["t"] < 3.2])
