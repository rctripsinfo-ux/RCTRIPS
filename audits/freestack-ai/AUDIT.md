# @freestack.ai: Instagram audit (data pulled 13 Nov 2026, 15:40 UTC)

## 0. Data sources and limits

| Source | What it gave | Cost |
|---|---|---|
| Apify `instagram-profile-scraper` | Profile: 116 followers, 61 following, 30 posts, bio, category | ~$0.003 |
| Apify `instagram-reel-scraper` + `instagram-scraper` (cross-checked) | All 30 reels: plays, likes, comments, caption, duration, date, cover, video URL, latest comments. Both actors returned **identical** numbers. | ~$0.16 |
| Apify `instagram-hashtag-scraper` | 87 top reels from #freeaitools, #aitoolshindi, #opensourceai (benchmark) | ~$0.23 |
| Apify `instagram-profile-scraper` | 8 niche competitor profiles | ~$0.05 |
| Local Whisper (faster-whisper small) | Transcripts of all 30 voiceovers (auto-transcribed, so spellings are rough) | free |
| ffmpeg | First 3 s and every 5 s of each video, and all 30 covers, inspected visually | free |

**Total Apify spend: about $0.46.**

**Public data (used here):** plays (`videoPlayCount`), likes (hidden on reels 1–2), comment count, the latest visible comments, captions, covers and video files.

**Private data I do not have**, which needs Instagram Insights or a linked Business account:
- reach and non-follower reach
- watch time and skip rate
- shares and saves
- follows per reel
- profile visits
- traffic sources
- DM counts

Wherever a conclusion depends on these, it is marked **[needs Insights]**.

## 1. Account snapshot

- **Series:** "Subscription Band Karo", 30 reels on 30 consecutive days (15 Oct to 13 Nov). Reels 4–30 went out at 06:30 UTC (12:00 IST). Posting consistency is perfect.
- **Results:** 16,985 total plays. Median 353 per reel, mean 566. 382 likes (reels 1–2 hidden), 96 comments, 116 followers.
- **Follower conversion:** about 0.7 followers per 100 plays (lifetime followers ÷ lifetime plays). The per-reel figure is **[needs Insights]**.
- **Per-viewer reaction is normal.** Median like rate is 2.30% of plays vs 2.17% in the niche benchmark.
- **Comment rate is low.** 0.48% vs 1.19% in the benchmark, even though every reel asks for a keyword comment.
- **Conclusion:** the problem is distribution (reach) and conversion, not that people dislike the content once they see it.

### Profile problems (all verifiable on the profile now)

1. **Broken bio link.** The bio ends "👇 Free AI tools list", but the profile has **no external link**. That promise leads nowhere, and the Day 30 PDF has no home either.
2. **Wrong category.** It is set to "Marketing Agency". A viewer checking the profile reads "agency", not "educator". Switch to Digital creator, or Education/Science & Tech.
3. **No highlights.** Thirty tools with no Highlights to browse them by category (Coding / Video / Voice / Agents).
4. **Bio is now outdated.** It says "New tool every day", but the series ended at Day 30.
5. **Likes are hidden on reels 1–2** (`likesCount = -1`). Probably a setting at upload, and it removes social proof from the first posts.

## 2. Video-by-video table

How to read it:
- **Index** = plays ÷ account median (353). 1.00x is a median reel.
- **KW** = the CTA keyword.
- **KW-c** = visible comments that are exactly that keyword (the scraper sees up to the latest ~10 comments per reel).
- **Hook** = the first spoken line, from Whisper. Spellings are corrected for readability only.

| # | Date | Topic (paid → free) | Dur | Plays | Index | Likes | Cmts | KW / KW-c | Spoken hook (0–3 s) | Diagnosis |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 15 Oct | 5 tools (Otter, Grammarly, Topaz, MJ, ElevenLabs) | 60s | 430 | 1.22x | hidden | 2 | TOOLS / 0 | "Bhai tum abhi bhi in AI tools ke liye paise de rahe ho?" | Strong universal hook, but 60 s is the longest in the account. Countdown "number 5…1" pads it out. First post, so no audience yet. |
| 2 | 16 Oct | Devin → OpenHands | 37s | 213 | 0.60x | hidden | 2 | ENGINEER / 0 | "Ek AI engineer jo poora app likh de aur ek rupaya bhi na le" | Devin is unknown to a mass Indian audience, so the stakes are unclear. The cover says "Devin vs OpenHands": two unfamiliar names. |
| 3 | 17 Oct | Lovable/Bolt → bolt.diy, Dyad | 38s | 226 | 0.64x | 7 | 2 | APP / 0 | "Sirf ek line likho aur poori website ready. Bina coding." | Clear promise, but the frame-0 visual is an empty browser box on pastel. Two tools in 38 s splits attention. |
| 4 | 18 Oct | Cursor → Void, OpenCode | 43s | **1,593** | 4.52x | 49 | 8 | CODE / 0 | "Coding ke liye Cursor ka subscription? Ruk jao." | **Winner.** Names a tool the audience actually pays for and gives a direct command ("Ruk jao"). Highest like count in the account. |
| 5 | 19 Oct | Google Gemini CLI | 35s | **1,645** | 4.67x | 41 | 7 | GEMINI / 4 | "Google ne apna AI agent free mein de diya aur bahut kam log jaante hain." | **Top reel.** Brand authority (Google), a secret-knowledge frame ("kam log jaante hain") and a single tool. Most keyword comments of any early reel. |
| 6 | 20 Oct | HeyGen/D-ID → SadTalker, LatentSync | 39s | 202 | 0.57x | 12 | 3 | AVATAR / 2 | "1 photo do aur wo bolne lagegi." | Curious hook, but the opening frame is an empty white card. The payoff (talking photo) is shown with the mascot, not a real face, so there is no proof. |
| 7 | 21 Oct | Week-1 recap (5 tools) | 28s | **1,611** | 4.57x | 45 | 6 | RECAP / 4 | "Ek hafte mein maine tumhe 5 mehenge AI tools ka free version dikhaya. Kitne yaad hain?" | **Winner.** List/recap format: shortest reel, high density, and a quiz hook. Recaps are a repeatable winner (see #28). |
| 8 | 22 Oct | Suno → YuE, ACE-Step | 35s | 539 | 1.53x | 22 | 3 | MUSIC / 0 | "Suno ke paise mat do, free mein poora gaana banao vocals ke saath." | Above median. Music creation is a mass-interest topic, but the "powerful GPU" catch kills the "I can do this now" feeling. |
| 9 | 23 Oct | ElevenLabs → VoiceStudio | 35s | **1,102** | 3.13x | 31 | 8 | VOICE / 2 | "AI voiceover ke liye har mahine paise de rahe ho?" | **Winner.** A pain question aimed at creators (the audience of a creator-tools page). ElevenLabs is well known. |
| 10 | 24 Oct | VideoLingo (EN→HI dub) | 35s | **31** | 0.09x | 6 | 3 | DUB / 1 | "Koi bhi English video Hindi mein dub, automatic." | **Anomaly.** 31 plays is ~11x below the median, yet 6 likes and 3 comments, so the few viewers engaged. That pattern looks like **restricted distribution**, not a bad hook. A topic about dubbing other people's videos (copyright angle), or an upload or processing issue, are possibilities. **[needs Insights: check the reel's reach and Account Status]** |
| 11 | 25 Oct | Runway/Pika/Kling → Wan, LTX | 31s | **1,182** | 3.35x | 27 | 4 | VIDEO / 3 | "Sirf likho aur AI video bana dega." | **Winner.** AI video is the hottest mass topic in the niche (it dominates the hashtag benchmark top list). |
| 12 | 26 Oct | Meshy → TRELLIS, Hunyuan3D | 34s | 370 | 1.05x | 9 | 1 | 3D / 0 | "Ek photo do aur uska 3D model ready." | Median. Niche use case (3D printing/games) for a general audience. |
| 13 | 27 Oct | Midjourney → FLUX + ComfyUI | 32s | 175 | 0.50x | 5 | 0 | IMAGE / 0 | "Midjourney level AI images, zero rupaye mein." | Underperformed despite a famous brand. Free AI image tools (Gemini, ChatGPT, Meta AI) are now everywhere on phones, so "free images" is not news. Also needs ComfyUI and a GPU. |
| 14 | 28 Oct | InVideo/Pictory → MoneyPrinterTurbo | 32s | 566 | 1.61x | 18 | 5 | FACELESS / 2 | "Sirf ek topic do aur AI poori faceless video bana deta hai." | Above median. "Faceless video" is a known money/creator desire. |
| 15 | 29 Oct | ChatGPT Deep Research → GPT Researcher | 33s | 258 | 0.73x | 6 | 0 | RESEARCH / 0 | "ChatGPT ka Deep Research mehenga hai, ye free version dekho." | The pain is weak: most viewers never paid for Deep Research. Needs two API keys. |
| 16 | 30 Oct | NotebookLM → Podcastfy | 40s | 151 | 0.43x | 4 | 0 | PODCAST / 0 | "Koi bhi article… aur do AI hosts uspe podcast karenge." | NotebookLM is already free, so a "free alternative to a free tool" has no stakes. Second-longest reel. |
| 17 | 31 Oct | ChatGPT Plus → Ollama + Open WebUI | 34s | 190 | 0.54x | 10 | 2 | OFFLINE / 0 | "ChatGPT bina internet ke chalega, wo bhi bilkul free?" | Good hook on paper, but it's a laptop/RAM tool for a phone-first audience. One commenter pointed to a mobile offline app, a signal of what they actually want. |
| 18 | 1 Nov | Perplexity Pro → Vane | 33s | 153 | 0.43x | 3 | 0 | SEARCH / 0 | "Google se smart search jo seedha jawab de…" | Unknown tool, a renamed project, Docker self-hosting, and Perplexity Pro is often free in India via telecom bundles. Low stakes. |
| 19 | 2 Nov | Manus → OpenManus | 34s | 144 | 0.41x | 2 | 0 | MANUS / 0 | "Manus AI ka waitlist aur credits bhool jao." | The hook assumes viewers know Manus; most don't. Bottom 3. |
| 20 | 3 Nov | UI-TARS Desktop | 29s | 842 | 2.39x | 10 | **15** | AGENT / **8** | "Ye AI tumhara mouse aur keyboard khud chalata hai." | **Highest comment demand in the account** (8 "Agent" comments). A visual, almost magical claim. Low likes but high intent. |
| 21 | 4 Nov | Browser Use | 34s | 357 | 1.01x | 3 | 0 | BROWSER / 0 | "Ye AI tumhare liye websites pe khud kaam karta hai." | Same "AI does it for you" angle as #20, but less visual (browser vs whole PC) and posted the very next day: topic fatigue. |
| 22 | 5 Nov | Zapier → n8n | 32s | 144 | 0.41x | 1 | 0 | AUTOMATE / 0 | "Ek AI employee jo kabhi chhutti nahi leta." | Generic hook, an abstract workflow diagram, and fair-code/self-host caveats. Bottom 3. |
| 23 | 6 Nov | Anthropic Skills | 30s | 390 | 1.11x | 11 | 4 | SKILLS / 1 | "Claude ko ek click mein naye skills sikhao, free mein." | Median. The catch ("needs a Claude plan that supports skills") contradicts the "free" promise. |
| 24 | 7 Nov | MCP | 38s | 140 | 0.40x | 0 | 1 | MCP / 0 | "AI ko apni files, GitHub aur apps se jodo, ek standard tareeke se." | **Lowest non-anomaly reel.** A protocol, not a tool; jargon hook; no "paid tool" to save money on. Off-format for the series' own promise. |
| 25 | 8 Nov | Chatbase → Dify | 33s | 348 | 0.99x | 5 | 1 | BOT / 0 | "Bina coding apna ChatGPT jaisa chatbot banao." | Median. Chatbase is unknown; the business use case ("customers ke sawaal") suits SMBs, not this audience. |
| 26 | 9 Nov | OpusClip → SupoClip | 32s | 249 | 0.71x | 2 | 2 | CLIPS / 1 | "Ek podcast se 10 reels, automatic." | Below median, but a commenter on #28 explicitly asked for "video clipping with captions". Demand exists; the hook and demo didn't sell it. |
| 27 | 10 Nov | Topaz → Video2X | 30s | **1,093** | 3.10x | 15 | 6 | 4K / 0 | "Purani blurry video ko 4K mein badlo, free." | **Winner.** An emotional, universal use case (old family videos) with an instantly visual before/after promise. |
| 28 | 11 Nov | 3-week recap (8 tools) | 28s | **1,434** | 4.07x | 13 | 6 | LIST / 2 | "Teen hafton mein paid AI tools ke itne free versions. Kitne yaad hain?" | **Winner.** Recap format again (2 of 2 recaps were in the top 5). Two genuine content requests in its comments. |
| 29 | 12 Nov | "Kadwa sach": free ≠ free, cracked apps | 36s | **1,040** | 2.95x | 22 | 2 | TRUTH / 0 | "Ye 'free' AI tools sach mein free hain? Ek kadwa sach sun lo." | **Winner.** Opinion/contrarian content with no tool. Shows the audience responds to a point of view, not just tool drops. |
| 30 | 13 Nov | Day 30 PDF gift | 34s | 167 | (too new) | 3 | 3 | FREE / 0 | "Tees din, tees free AI tools, aur aaj ek gift." | Only ~9 h old at scrape time, so it can't be judged yet. But the PDF has no link in the bio to land on. |

**Comment quality (from the visible comments):**
- **Keyword-CTA comments:** about 30. These are the main real signal.
- **Bot comments:** `botsinbox` left AI-written generic comments on 8 reels (#23–#30), and a spam comment ("kaam hai… WhatsApp msg karo") appears on #23. Together these inflate the late-series comment counts.
- **Repeat emoji commenters:** a few accounts (e.g. `official_jayash.ai` ×8) left emoji-only comments.
- **Genuine content requests (#28):**
  - "video ka clipping karna with caption wala bata do"
  - "video create karne ke liye … real free ho"
- **Genuine tip (#17):** a viewer recommends a mobile offline AI app.
- **Creator replies:** none visible (the scraper returned 0 replies on every comment). Whether keyword DMs were actually sent is **[needs Insights / your DM inbox]**. If they are sent by hand, late or missing DMs teach people that commenting the keyword doesn't work.

## 3. What the top 8 have in common vs the bottom 8

**Top 8** (index ≥ 2.9): #5 Gemini CLI, #7 Week recap, #4 Cursor, #28 3-week recap, #11 AI video, #9 Voice, #27 4K, #29 Kadwa sach.

**Bottom 8** (index ≤ 0.6, excluding #10 and #30): #24 MCP, #19 OpenManus, #22 n8n, #16 Podcastfy, #18 Vane, #13 FLUX, #17 Ollama, #6 SadTalker.

| Factor | Top 8 | Bottom 8 |
|---|---|---|
| Paid tool named in the hook | Household names the viewer pays for or wants (Cursor, Google, ElevenLabs, Runway, Topaz) | Unknown (Manus, Perplexica, Chatbase), already free (NotebookLM), or no paid tool at all (MCP, n8n) |
| Hook shape | Direct challenge or question ("Ruk jao", "paise de rahe ho?", "kam log jaante hain", "kitne yaad hain?", "kadwa sach") | Feature description ("ek standard tareeke se", "AI employee jo chhutti nahi leta") |
| Format | 2 recaps + 1 opinion piece in the top 8 | 100% single-tool explainers |
| Usable today on a phone or normal laptop | Mostly yes, or a strong "wow" visual | Mostly Docker, self-host, API keys or GPU |
| Length | Median 33 s | Median 34 s |

Duration has a weak negative correlation with plays (Spearman −0.25, n=29): shorter is slightly better, but this is not decisive.

**Time pattern:** plays were under 400 for 7 of the 8 reels from #12–#19 and for all 6 reels from #21–#26. The recovery came only with recaps and opinion (#27–#29).

**Caveat:** with n=30 and no Insights, these are correlations, not proven causes. Instagram also distributes in test batches, so single-reel variance is high.

## 4. Thumbnails, first frame, editing (from frame inspection)

1. **The cover and the first frame are two different designs.** Covers are strong and scroll-stopping: saturated burst backgrounds, the mascot, a big "₹0", a "Paid vs Free" split and a crossed-out price. But in the Reels feed nobody sees the cover; autoplay starts at frame 0. Frame 0 of every reel is:
   - a pale pastel/white background
   - a small headline at the top
   - an empty UI mockup (blank terminal, blank browser, blank chat)

   The mascot doesn't appear until about 4–5 s. **Your best visual asset only works on the profile grid.** This is the single biggest fixable issue.
2. **Seconds ~2–5 are spent on branding.** Every transcript says "Subscription band karo, Day N" right after the hook, and some reels (e.g. #24) cut to a full-screen series title card at ~5 s. That is the highest drop-off window, and it carries zero value for a new viewer.
3. **All 30 reels use one identical template:** hook → series tag → "X paise leta hai" → free tool → features → catch → "Link chahiye, comment karo X" → "Kal Day N+1 mein…" → "Bye". The predictability suits a series binge, but a cold viewer in the feed can tell within 3 s it's the same video as yesterday.
4. **The "DEMO" badge promises a real demo, but the reels show illustrated mockups, not screen recordings.** In a niche full of "free tool" clickbait, real-screen proof is the trust signal (e.g. benchmark account `bunjiai`'s bio: "Real screen. Real numbers."). The mascot is a good brand asset but can't prove a tool works.
5. **The ending kills the loop.** Every reel ends "Kal Day N+1 mein … Bye", a verbal goodbye that cues the viewer to swipe. Nothing loops back to the hook.
6. **The "Catch" line is a real differentiator.** It is honest and builds trust (#29 proves the audience likes honesty). But in GPU or API-key reels it lands at about 70% of the video and deflates the promise. Keep it, but frame it as a tip ("laptop pe chalana hai? ye setting use karo"), not as a disqualifier.

## 5. Competitor benchmark (public data)

Profiles: 8 accounts, scraped now. The viral reels come from the hashtag sample. That sample is Instagram's top or recent reels for #freeaitools, #aitoolshindi and #opensourceai; it skews toward winners, so treat it as a ceiling, not an average.

| Account | Followers | Posts | Best reel in sample | What it shows |
|---|---|---|---|---|
| moksh.explains | 70.3K | 61 | 19.4M plays: "15 FREE AI TOOLS YOU NEED TO TRY IN 2026" (53 s) | A big list beats single tools. Few posts, huge reach. |
| gaurav.tools | 54.1K | 195 | 2.43M: "Comment Course to get my free AI course" | Hindi free-AI page. A lead magnet in the CTA. |
| okaashish | 195K | 708 | 1.83M: "Comment Dolphin…" (28 s) | Face on camera, single tool, keyword CTA. |
| techtipszone.in | 32.0K | 60 | 868K: "Google Flow ka FREE alternative chahiye?" (57 s) | **Hinglish** + "free alternative to a famous Google tool". The same angle as your best reels. |
| rrishijain | 256K | 1,627 | 580K: "Comment 3D…" + ebook CTA | Two CTAs: tool + lead magnet. |
| shaans_docs | 78.3K | 79 | 1.64M: "Ep 5 of AI editing ideas only with free AI tools" | **Episodic series works**, framed as creator use cases rather than tool names. |
| vikkii_tech | 5.3K | 63 | 636K: "All AI tools at one place" | A small account can hit 600K with a mass-appeal list. |
| bunjiai | 639 | 26 | n/a | Your direct size peer (1 tool/day). Positioning: "Real screen. Real numbers." |

Benchmark medians (87 reels): duration 43 s; like rate 2.17%; comment rate 1.19%; 55% use a "Comment X" CTA.

**Takeaway:** your format (Hinglish, keyword CTA, 30–45 s) is the right genre. The gaps are:
1. **Topic packaging:** mass lists and famous-brand alternatives vs your developer tools.
2. **Proof:** face or real screen.
3. **A lead magnet in the bio**, which you have (the PDF) but haven't wired up.

## 6. Key weaknesses (ranked by expected impact)

1. **The feed sees a blank pastel frame instead of your designed cover.** This is the hook-visual problem.
2. **2–3 s of series branding before any value.**
3. **Topic selection drifted to developer infrastructure** (MCP, n8n, Manus, Perplexica, Dify) that the audience doesn't pay for and can't run on a phone. 10 of the 18 reels from Day 12–29 were below the median.
4. **No working conversion path.** No bio link, no highlights, wrong category, and keyword DMs may not be automated. 17K plays turned into 116 followers.
5. **One template ×30, with no format variety.** Only 2 recaps and 1 opinion piece, and those 3 averaged 4.1x the median.
6. **No proof (real screen or face)** in a niche where the dominant viewer fear is "fake free".
7. **Day 10 was likely restricted. [needs Insights]**
8. **Comment section is diluted by bots and spam**, with no creator replies to seed conversation.

## 7. 30-day growth plan

**Format rules, applied from Day 1 (zero cost):**
- **Frame 0 = the cover.** Open on the burst background with the mascot, the "PAID ₹X → FREE ₹0" split and 3–5 big words. Show the result (output, before/after) by 1.5 s.
- **Cut the spoken "Subscription band karo, Day N".** Keep it as a small on-screen tag only.
- **Real screen-recording proof** for 3–5 s in every reel (phone or PC). Keep the mascot as narrator and reaction.
- **Pick tools that pass 2 of these 3 tests:**
  1. The viewer knows the paid tool, or pays for it.
  2. It works on a phone or normal laptop without Docker or GPU.
  3. The result is visual in 1 s.
- **Formats:** 50% single tool, 25% list or recap, 25% opinion, myth or test ("kadwa sach", "maine 5 test kiye").
- **Endings:** no "Bye". End on the CTA line and loop the last visual back to frame 0. Put the "Kal…" teaser on screen only, not spoken.
- **Length:** 25–35 s for single tools, up to 45 s for lists.

**Week 1: fix the funnel** (before posting more):
1. Add a bio link (a free Linktree/Beacons, or a Notion page) holding the **30-tools PDF and the full list**.
2. Change the category to Digital creator / Education.
3. Update the bio: "Paid AI tool ka FREE version, real demo ke saath • Hinglish • 👇 30 tools PDF".
4. Create Highlights: Coding · Video · Voice · Agents · PDF.
5. Pin #5, #7 and #29 (the top reel, the format proof, and the positioning).
6. Automate keyword DMs (ManyChat has a free tier for Instagram) so every "Comment X" gets a DM within seconds.
7. Hide or delete the bot and spam comments.
8. **[needs Insights]** Open #10 to check its reach source, and check Settings → Account Status for restrictions.

**Weeks 1–4: posting.**
- **Cadence:** 5 reels a week (quality over the daily grind; 10 of the 18 reels from Day 12–29 were below median).
- **Timing test:** keep 12:00 IST for half the posts and test 19:00–21:00 IST for the other half. Compare on non-follower reach **[needs Insights]**.
- **Trial Reels:** use Instagram's "Trial reels" (shown to non-followers first) to A/B two hooks on the same video for #1–#4 below.

**Weekly review metrics [needs Insights]:**
- 3-second hold / skip rate (target: reels with frame-0 changes beat the old median)
- average watch time
- non-follower reach %
- shares + saves per 1K plays
- follows per reel
- keyword comments per 1K plays (baseline about 1.8)

**Targets for Day 30**, extrapolated from your own top-quartile performance, not guaranteed:
- median plays ≥ 1,000 (the current top-8 level)
- 300+ followers
- ≥ 5 keyword comments per reel

## 8. Ten Reel ideas grounded in this data

| # | Idea + hook (Hinglish) | Format | Evidence |
|---|---|---|---|
| 1 | **"Video ko auto-clip karo captions ke saath, free"**: "OpusClip ke paise? Ek podcast, 10 reels, word-by-word captions, ₹0." Real screen demo, phone-friendly option. | Single tool, remake | A direct viewer request on #28. #26 covered it but underperformed on packaging, not demand. |
| 2 | **"Maine 6 'free' AI video tools test kiye. Sirf 2 sach mein free nikle."** | Test/opinion | Viewer request on #28 ("real free ho"). #11 AI video at 3.35x and #29 "kadwa sach" at 2.95x. Benchmark leader `digitalquadrate` 1.6M on "free AI video". |
| 3 | **"Google ke 5 free AI tools jo koi nahi batata"** | List | #5 Google at 4.67x (top reel). Benchmark `techtipszone.in` 868K on "Google Flow ka free alternative". |
| 4 | **"Cursor/ChatGPT Plus band karke 7 din free tools use kiye: kya hua?"** | Challenge / result | #4 Cursor at 4.52x. A challenge adds a narrative the template lacks. |
| 5 | **"ElevenLabs vs free voice: blind test. Comment karo A ya B"** | Interactive test | #9 Voice at 3.13x. Fixes the low comment rate with a non-keyword reason to comment. |
| 6 | **"Purani family photo ko HD + colour, phone pe, free"** | Single tool, before/after | #27 4K at 3.10x (emotional, visual). Upscayl is already in #1's list. |
| 7 | **"AI jo tumhara computer khud chalata hai: live test, kya ye sach mein kaam karta hai?"** | Single tool + proof | #20: most keyword comments in the account (8), but a low like count, so add real-screen proof to convert interest. |
| 8 | **Weekly "Fatafat recap: kitne yaad hain?"**, every Sunday | Recap/quiz | #7 at 4.57x and #28 at 4.07x, 2/2 recaps in the top 5. Benchmark #1 is a 15-tool list (19.4M). |
| 9 | **"Cracked Canva/CapCut Pro mat download karo: ye free open-source tools use karo"** | Opinion + list | #29 cracked-apps warning at 2.95x. Canva/CapCut are household paid tools (passes test 1). |
| 10 | **"Phone pe offline ChatGPT, bina internet, bina laptop"** | Single tool, phone demo | #17's laptop version flopped (0.54x), but a viewer recommended a mobile offline AI app there, so the demand is phone-first. |

Swap-out rule: if a hook would need the viewer to already know the tool's name (Manus, Perplexica, Chatbase, MCP), lead with the outcome instead. "AI jo tumhara kaam khud karta hai", not "OpenManus".

## 9. What only you can check (Insights)

For the top 8 vs bottom 8 reels, compare:
- 3 s hold rate and average watch time
- shares and saves
- follows from each reel
- non-follower %

If the bottom reels show a similar watch time but low reach, the problem is topic/hook packaging (sections 3–4). If they show a low watch time, the problem is the opening seconds (section 4, points 1–2).

Raw data: `data/` (profile, reels, transcripts, benchmark, competitors).
