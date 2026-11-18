# Claude Video Editing System — Research Blueprint
Source: 9 YouTube transcripts (5 English, 4 Hindi) on editing videos with Claude.

---

## 1. Who is selling what (competitor map)

| Creator / Video | What they sell | Price | Model |
|---|---|---|---|
| Joseph (Ultimate Editors) — "Premium Reels" + "Minimal Talking Head" | Style skill packs (short-form + long-form) + courses | $299 lifetime (anchored from $1,200/yr) | Course + skills, fake "closing forever" urgency |
| "ChatGPT + Claude Start to Finish" (AI Creator Course) | Pre-built drag-drop editor app with style presets (tier list, explainer, yap, Vox) — "26,000 lines of code" | Course price (not stated) | Free tutorial → paid ready-made app |
| "Top 1%" (Higgsfield affiliate) | Free prompts in a Skool community; earns via Higgsfield affiliate | Free | Affiliate |
| Hindi "AI video" creator | Done-for-you setup service | Not stated | Service |
| Saurabh (Hindi, AI + design) | Free prompts + "watch" skill in description | Free | Audience building |
| Hindi "5 levels" creator | Prompts PDF via comment → DM | Free (lead magnet) | Comment-to-DM funnel |
| Yonko "Creator OS" | Handbook + 11 prompts + design system | $47 | Product |

**Gap for us:** Nobody sells a clean, India-priced, Hindi+English, *tested* kit that focuses on "copy any reference reel". Free creators give scattered prompts; paid ones are $47–$299.

---

## 2. The common tech stack (all free except Claude)

| Tool | Job |
|---|---|
| Claude desktop app → **Code** tab (Pro plan, ~₹2,000 via mobile app / ₹2,400 desktop) | The editor brain |
| **FFmpeg** | Cut, merge, audio, render |
| **Whisper** | Word-by-word transcript (works for Hindi/English/Hinglish) |
| **Remotion** or **HyperFrames** (free alternative) | Code-based captions + motion graphics |
| **Node.js** | Needed by Remotion/HyperFrames |
| **yt-dlp** | Download reference videos from links |
| **Openverse** / local SFX folder / Epidemic via MCP | Music + sound effects |
| Optional: Homebrew (Mac), DaVinci Resolve Studio MCP, Premiere MCP, CapCut export, Higgsfield (paid AI gen) | Timeline editing / AI effects |

Hardware: Windows/Mac laptop, ~8 GB RAM, ~10 GB free. Not phone.

---

## 3. The master workflow (merged best practices)

### Phase A — One-time setup
1. Install Claude desktop, switch to **Code**, select a project folder, "Trust workspace".
2. **Prompt 1 (Folder setup):** create the workspace structure:
   ```
   AI-Video-Editor/
     references/   (reels whose style you want)
     raw/<project-name>/  a-roll, b-roll, screen-recording
     assets/       logo, music, sfx, PNGs
     brand-kit/    fonts, colours, layout frames
     storyboards/  (Claude writes plans/contact sheets here)
     exports/      (final renders)
     skills/
   ```
3. **Prompt 2 (Installer):** check/install FFmpeg, Node.js, Whisper, Remotion/HyperFrames, yt-dlp, SFX source; run a quick test; report versions.
4. **Brand kit:** drop font files (primary ~80%, accent ~20%), primary + accent hex colours, optional Figma layout frame (where face-cam / screen-share / text sit).

### Phase B — Teach the style (the real value)
5. Put 5–20 reference videos in `references/` (or paste links → yt-dlp).
6. **Prompt 3 (Style training):** "Make a word-by-word transcript and frame-by-frame breakdown of every reference. Study (1) design: colours, layout, fonts, effects; (2) animation logic: type, duration, easing; (3) placement/timing relative to the script. Save as a skill named `<name>-style` with: rule book (sizes, spacing, curves, speeds), look book (shapes, colours, gradients, icons), and a reference library (screenshot + keyframe notes per animation)."
7. Claude asks clarifying Qs (caption colour, language — e.g. "Hindi audio, English/Hinglish captions", logo). Answer them.
8. Pro move (Joseph): build a Figma/screenshot board of 100+ frames grouped by "principles" (captions, listicles, UI pops/counters, hooks, full-screen animations) and feed it alongside the videos.

### Phase C — Edit each video
9. **Rough cut prompt:** "Transcribe word-by-word (ms level). Remove silences (keep ~30 ms padding / 2 frames), filler words, repeated & bad takes (prefer the last good take). List every cut."
10. **Plan prompt:** "Create a planning doc: script lines on one side, for each line recommend 3–4 scene designs from my style skill; leave a notes box." → *You* choose scenes (15 min). Key insight from every top creator: **human plans, AI executes** — AI-planned edits look generic.
11. **Preview before render:** ask for a **contact sheet / storyboard** (frames per scene) or a 30-sec preview first. Fix errors here — saves time and usage.
12. **Build prompt:** "Follow the approved plan, use the style skill for the look, fetch needed assets (fonts from Google, stock from Pexels, images), build in Remotion/HyperFrames, render 1080×1920 @ 60fps (or 16:9)."
13. **Revision prompt:** numbered notes, optionally with screenshots: "1) caption touches neck — move down 30%; 2) card covers face — move to side; 3) hold spiral 1s longer…" First draft ≈ 60–70% there; expect 1–2 rounds.
14. **Sound prompt:** "Create a cue sheet of every on-screen event, add matching SFX (whoosh = transition, click = text, pop = UI), add music, duck music under voice, normalise voice loudness without clipping."
15. Optional: **Color** (apply LUT), **Export to timeline** (DaVinci/Premiere XML or CapCut project) for manual tweaks.

### Phase D — Make it one-command
16. **Skill-ify prompt:** "This edit is approved. Turn the whole process into a skill so that when I say 'edit this video' you run cut → captions → motion → sound automatically in my style. Test it once before saving."
17. Keep adding new references: "Add these 2 videos to my style library."

---

## 4. Style "keys" that make edits look premium (content for the PDF)
- **Captions:** 2 fonts — clean sans (Inter/Open Sauce) + script/serif for highlight words (Playfair Italic/Garamond). Place key word big & centre, fill rest around it smaller. Pop + blur + fade-in. Darkened/blurred lower third behind text. Never over face/neck.
- **Hook formula:** speaker eyes on upper third + hook text + supporting visual (notification, timer, counter).
- **UI pops:** before/after with arrow, software notification card with logo, circular counters, blurred list cards, chapter listicle badges.
- **Full-screen scenes:** listicle timelines, text-only scenes with quote marks, line-and-text animations, graphs with glowing grid, illustration-centre scenes, out-of-screen zooms.
- **Punch-in zooms** on key lines; **B-roll** with texture/vignette + text on top.
- **Pattern:** announce a new point → show face; describe it → show visual.
- **Sound:** cue-sheet based SFX + ducked music = "studio feel".

---

## 5. Speed (use for marketing)
**Our tested benchmark (with a mature, trained Claude skill):**
- 5-min animation-style video (multiple character poses): **~5–7 min**.
- Talking-head reel/video: **under 5–10 min**.
- One-time setup + style training: ~20–30 min.

The YouTube transcripts quote 40 min–2 hrs per edit, but that was first-time/manual workflows without a refined skill (planning docs, multiple revision rounds, full re-renders). That slowness is the pain point our ready-made skills remove — marketing angle: "Their workflow: 2 hours. Ours: 5 minutes."

---

## 6. Common pitfalls (put in a troubleshooting chapter)
- Not on paid plan / using chat instead of Code tab.
- Homebrew/permissions blocks on Mac; Windows path issues.
- Graphics covering face, captions on neck → use layout frame + preview sheet.
- Rendering full video every iteration burns usage → contact sheet first.
- Forgot to specify length/fps/aspect ratio/language in prompt.
- Music source not reachable (YouTube Audio Library) → local folder / Openverse.
- Face swaps: only use AI-generated faces, never real people.

---

## 7. What OUR kit should contain (₹1,999)
1. **PDF Handbook** (Hindi + English): setup → style training → per-video workflow → revisions → sound → skill-ify → troubleshooting.
2. **Copy-paste prompt pack** (~15): folder setup, installer, style training, reference-copy, rough cut, planning doc, contact sheet, build, revision template, sound/cue sheet, color/LUT, timeline export, skill-ify, add-to-style-library, 30-sec preview.
3. **Ready skill files**: `reference-copy` skill + 3–5 starter styles (minimal premium, Hormozi-bold captions, Hinglish talking head, listicle explainer, travel beat-sync).
4. **Brand-kit template** + layout frames (9:16, 16:9).
5. **Free SFX starter folder** (royalty-free) + practice footage.
6. **Setup video** (Windows + Mac).
7. Bonus: scene-design cheat sheet (Section 4) + planning-doc template.

Differentiators: India price, Hindi support, "copy any reference reel" angle, tested on real reels, refund guarantee.
