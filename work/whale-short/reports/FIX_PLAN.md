# Fix plan

Priority P1 = largest measured gap. Difficulty S/M/L. "Done in test" = implemented and rendered in the 0-269 test segment.

| # | Area | Change | Expected improvement (metric) | Depends on | Diff. | Prio | Status |
|---|---|---|---|---|---|---|---|
| F0 | Evidence | Upload the user's 88 reference frames into the repo (e.g. `references/frames_user/`) and re-run `analysis/measure.py` on them; until then every reference number is from the 38-frame skill set only | correct targets | user upload | S | P0 | blocked |
| F1 | Analysis method | Get the 20 reference videos into `references/vids/`, then re-run motion (phase correlation per frame), cut, caption-timing and audio-level measurement with `analysis/measure.py` + a motion script | resolves the cut/hold contradiction; real camera curves | user supplies videos/URLs | M | P1 | blocked (needs files) |
| F2 | QA gate | Every render: run `measure.py` and fail the shot if lum_mean > 0.50, sat < 0.42, edge_frac < 0.08, p2 > 0.10 | stops "bright & flat" drifting back | — | S | P1 | done (script) |
| F3 | Light/colour | Beach beats in late-afternoon light (warm side-back key az 40 el 20, violet shade [0.27,0.26,0.46], sat 1.12); keep night for the explanation | lum_mean 0.63 → ~0.5; sat ↑; dark mass ↑ | — | S | P1 | done in test |
| F4 | Typography | ~~Word captions~~ **CANCELLED**: the user didn't ask for captions, and the user's 88 reference frames reportedly contain none | — | — | — | — | captions disabled by default |
| F5 | Texture/detail | Sand with footprints, shells, stronger ripples; 2x beach grass; kelp toned down | edge_frac, detail_hf ↑ | — | S | P1 | done in test |
| F6 | Scene design | Per shot: at least 3 depth layers (foreground prop, subject, busy background) and an "event" every ~1 s | new_picture_frac 0.68 → 0.9 | — | M | P1 | partial (foreground props done) |
| F7 | Editing | Replace hard cuts with: 4-frame flash (done for the hook), camera travel between subjects, follow-the-chunk moves, 6-8 f dissolves on place changes; target ≤ 3 plain cuts | smoother, continuous feel | camera rewrite | L | P1 | partial (1 cut → flash) |
| F8 | Pacing | Re-time the narration to < 1 s total pauses (keep each line at its natural fenrir speed), then re-time all shot keys from the new `words.json` | dead air 8.6 s → < 1 s; ~3.7 w/s | F7 | M | P1 | not started (needs a full re-time) |
| F9 | Character animation | Idle head sway (±2-3°) on standing characters; gesture on key words; weight shift | less static | — | S | P2 | done in test (sway) |
| F10 | Assets | Higher-detail cars (done), truck/dozer rebuild; or user-supplied CC0 model pack (Kenney "Car Kit", "Nature Kit") | realism, detail | user upload if wanted | M | P2 | partial |
| F11 | Explanation shot | Rim/lamp light on the whale at night, bigger arrows | readability of the core idea | — | S | P2 | not started |
| F12 | Sharpness | DOF only on CU/MS beats; cInf ≤ 8 on MS; encode crf 15 | lap-var ↑ | — | S | P2 | not started |
| F13 | Rendering | Keep 1080 native; render only changed shots (chunk by shot) and splice; measure after each | faster iterations | — | S | P2 | in use |
| F14 | Audio | Keep user's low music level; ensure -14 LUFS two-pass loudnorm | consistent loudness | — | S | P3 | done (one pass) |
