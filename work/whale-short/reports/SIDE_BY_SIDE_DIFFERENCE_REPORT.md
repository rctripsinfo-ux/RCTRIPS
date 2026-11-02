# Side-by-side difference report (test segment v6 vs reference)

Sheet: `analysis/sbs_test.jpg`. Row 1 = approved reference stills (short04_0060, short05_0060, short12_0180,
short18_0180, short13_0060), row 2 = v4, row 3 = v6 at the same story points (new frames 30, 200, 280, 330, 470).
The reference stills are matched by **shot type**, not story: we only have stills, not the 20 videos. So motion and
timing rows compare against the skill author's UNVERIFIED numbers.

| # | Time (v6) | Reference behaviour | Ours | Measured / observed difference | Severity | Likely cause | Next correction |
|---|---|---|---|---|---|---|---|
| D1 | whole segment | dense sets: buildings, signs, props, people in every layer (edge density 0.099, detail 0.017) | open beach, sand + sky fill 50-70 % of the frame | edges 0.066 (0.67x), detail 0.012 (0.7x) | **high** | scene choice + procedural primitives; no model library | Every shot gets ≥ 3 depth layers. Beach-side props: lifeguard tower, parked cars, news van, picnic crowd with umbrellas, signs, fence. Raise grass and driftwood density near the camera paths. Gate: edge_frac ≥ 0.08 per still. |
| D2 | whole segment | sharpness 0.009 | 0.003 (v4 0.005) | 0.33x | **high** | darker grade + warm fog/haze + lens blur + h264 | Fog starts later (fogNear 50 -> 90 m on the beach). Lens blur only on CU beats. Ink width +20 %. Encode crf 15. Re-measure. |
| D3 | 0:09-0:10 (f 280) | subject reads instantly, lit side to the camera | whale side in shade = flat saturated royal blue; eye and wrinkles lost | observed in sbs col. 3 | **high** | sun from behind the sea in shots 2-4; shaded flank × violet shade colour | Give shots 2-4 a sun from camera-left-front (az 120-140) so the flank is lit; cap the whale shade saturation. |
| D4 | 6.7-7.4 s, 9.5-10.1 s | strong moves peak ≤ ~38 px/f, 8-10 f attack/release | peaks 56-100 px/f | 1.5-2.6x too fast | medium | near-field parallax: the camera passes 3-6 m from the whale and the grass | Raise the path (keep ≥ 8 m from the whale) or lengthen to 80-90 f; re-run `camfit.py`, gate p90 ≤ 20 px/f. |
| D5 | whole segment | 10 % holds (camera still) | 0 % holds | never still | low | every key has a push-in, plus kicks | Allow 6-12 f true holds at the end of acting beats. |
| D6 | 0:00-0:02 | MS/CU character with the frame filled, eye level | hook CU works; Umenhofer centred, cloud behind | matches the framing intent | — | — | keep |
| D7 | 0:13-0:16 (f 470) | characters act on the word (gestures, props) | engineer grins and waves; plunger box in front | close | low | — | keep |
| D8 | whole segment | voice 3.5-4.1 w/s, no dead air (UNVERIFIED) | 3.71 w/s, breath gaps ≤ 0.16 s | within the target | — | — | keep for the full video |
| D9 | whole segment | captions on every frame | none | user decision (no captions) | n/a | — | none unless the user asks (the code exists: `inputProps.captions`) |
| D10 | 0:04, 0:07, 0:10 | place changes: flash / dissolve / travel | flash, travel, 6-f dissolve | matches the grammar | — | — | keep |

## Overall
v6 is measurably closer on **colour (saturation closed), darks, pacing and continuity**. It is **not** closer, or is worse,
on **detail, sharpness and subject readability (the shaded whale)**. Those three need asset/scene work (D1),
haze/encode work (D2) and lighting direction (D3) before a full render.
