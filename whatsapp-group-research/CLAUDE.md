# WhatsApp Group Research System — Permanent Operating Rules

Read this at the start of every session in this folder. These rules override any urge to finish a list quickly. **Quality > quantity.**

## Workflow per run
1. Ask: "Which niche or industry do you need WhatsApp groups for?" Then ask only unanswered, result-changing questions (quantity, B2B/B2C, region, language, sub-niches, exclusions, direct-link mandatory, request-to-join, LinkedIn). Check `config/research_config.json` and the `Configuration` worksheet first; never re-ask stored answers.
2. Defaults: exactly 20 per search · India first then international · English · professional B2B · direct links preferred · all previous groups excluded · no filler.
3. Build a candidate pool 3–5× the target (60–100 for 20) using varied queries (`"chat.whatsapp.com" "[NICHE]"`, `+ professionals/community/India/B2B/networking/association/business owners/suppliers/freelancers`, `site:facebook.com|instagram.com|reddit.com|youtube.com|[industry-site]`). Adapt to the niche (travel: travel agents, B2B travel, tour operators, DMC, travel trade, MICE, hotel suppliers, destination management company, travel agency owners, tourism professionals). Prefer recent sources.
4. Write candidates to `data/candidates_<date>.json` (fields documented in `scripts/run_research.py`), assigning component scores **only from public evidence**.
5. Run `python scripts/run_research.py process data/candidates_<date>.json --niche "..." --meta '{"sub_niche":"","region":"","queries":"...","platforms":"..."}'`. It canonicalizes, dedupes (local DB + live Sheet), applies LinkedIn rule, validates WhatsApp metadata, scores, saves locally immediately, appends to Sheet with read-back verification, logs Search History.
6. Resolve any `REVIEW` (≥85% name similarity) items manually. Report using the final format below.
7. "find more" / "find 20 more" = reuse `last_run` niche/filters, exclude everything previously approved/rejected.

## Source priority
Official org/community site > official social account > industry association/trade publication > founder/admin announcement > established professional community page > FB/IG post by identifiable org > Reddit with context > directories (discovery only — never sufficient alone). Reject link farms, SEO spam, affiliate redirects, fake counts, link resellers, earn-money schemes, piracy, suspicious downloads.

## LinkedIn rule
Accept only if the post visibly has ≥500 reactions **or** ≥500 comments (no combining unless user permits). Hidden/unverifiable = reject. Follower counts don't count. Never estimate. Record numbers + URL. Reconsider only if found independently via a credible non-LinkedIn source.

## Validation (scripts/validate_whatsapp.py)
- Canonical form `https://chat.whatsapp.com/<CODE>`; strip all query params. Invite code = primary key.
- HTTP 200 ≠ active. Invalid/expired invites return 200 with blank `og:title`, `og:description="WhatsApp Group Invite"`, and the default `static.whatsapp.net/rsrc.php` image. A real group photo is on `pps.whatsapp.net`.
- Name priority: `parent_group_subject` (communities) > specific `og:title` > structured metadata > browser-rendered name (`h3._9vd5`) > official source (only if WA metadata temporarily unavailable).
- Generic titles (WhatsApp Group Invite, Join WhatsApp Group, WhatsApp, Group Invite, blank, unexplained "General") = inconclusive.
- Statuses: `Active – Direct Join`, `Active – Request to Join`, `Active – Community` (approvable); `Probable Active – Metadata Partially Available` (only with strong official evidence, disclosed); `Expired`, `Revoked`, `Invalid`, `Unknown – Do Not Approve`.
- Two-stage check: fast HTTP metadata, then (when title/photo is missing) a headless Playwright render adapted from the user's `direct_join_checker.py` verifier, with a full-page screenshot saved to `data/screenshots/<code>.png` as evidence. Only the verifier is used; group discovery is done by Claude via web search. Never click Join.
- If both stages are inconclusive if still inconclusive → Unknown, do not approve. Limited retries with backoff; ≥3 s between requests.
- **Never join groups, message admins/members, harvest numbers, bypass logins/CAPTCHAs, or buy/resell links.**

## Stage 3: WhatsApp Web preview (required before approval)
After the public-page checks pass, open each new invite in the user's **already logged-in WhatsApp Web** (their own Chrome via Claude in Chrome / built-in browser; never log WhatsApp into a cloud browser). Read only the preview popup, then close it. **Never click Join / Request to join / Join community.** Record:
- Exact name shown in the popup
- Member count if shown (verified fact; store in Q "Public Member Evidence" as "WhatsApp Web preview: N members, <date>")
- Button text: "Join group" = `Active – Direct Join`; "Request to join" = `Active – Request to Join`; "Join community" / "View community" = `Active – Community` (Group or Community column = Community)
- Popup says invalid/reset/expired = Expired/Revoked
Ban-safety rules: one invite at a time, ~30–60 s randomised gap, max ~25 previews per session, no scrolling chats, no messages, no clicks other than closing the popup, stop immediately on any warning/"try again later". If WhatsApp Web is unavailable, mark the group pending and do not approve it on public metadata alone.

## Names & dedupe
Save the exact WhatsApp name verbatim (case, punctuation, emojis). Normalized name = lowercase, no emojis/punctuation, generic suffixes (official, group, WhatsApp group, community, network, updates) and numbered subgroup labels removed. If source name ≠ WA name, use WA name and explain in notes.
Dedupe on: invite code, canonical URL, exact name, normalized name, parent community, source org, fuzzy similarity (≥85% → manual review, not auto-approve), same-community subgroups. Reject regenerated links of known groups, numbered sibling subgroups, multiple destination groups from the same DMC (unless requested). Don't reject distinct groups merely for sharing generic niche words.

## Quality score (0–100)
Relevance 0–30 · Credibility 0–25 · Activity evidence 0–20 · Size evidence 0–15 · Networking/commercial value 0–10.
Tiers: 85+ Excellent · 75–84 Strong · 65–74 Acceptable · 50–64 Weak · <50 Reject. Approve only ≥65. If fewer qualify, return fewer and explain. Never lower the bar silently.
Activity: only public evidence (recent posts, invite updates, admin announcements). Size: org network size ≠ group membership.
B2B travel: prioritize agency owners, tour operators, DMCs, MICE, corporate travel, hotel/ground suppliers, visa partners, ticketing, travel tech, trade-fair operators, tourism boards, associations, B2B package providers. Reject/downgrade traveller chats, backpackers, trip companions, consumer deals, dating/friendship, photo groups, consumer spam.

## Facts vs claims
Keep separate: Verified facts · Source claims (label "claimed") · Inferences (label) · Unknown (`Not publicly available`). Never invent names, member counts, activity, B2B status, or LinkedIn engagement.

## Google Sheet rules
Worksheets: `Approved Groups` (30 cols A–AD), `Rejected Groups` (11 cols), `Search History` (13 cols), `Configuration`. Append only; never overwrite/delete. Confirm target sheet before first write. ISO dates. Formula-like cells escaped. Re-read inserted range to verify. On failure: keep local JSON + `data/pending_uploads.json`, report clearly, never claim saved; `python scripts/google_sheets.py flush` once fixed. Revalidation updates only Status/Verification Date/Notes; expired groups are kept, never deleted.

## Final response format
| No. | Exact Group Name | Focus | WhatsApp Link | Status | Quality Score | Evidence |
Then: niche · candidates researched · approved · rejected · duplicates removed · expired removed · LinkedIn rejected · Sheet rows added · worksheet · limitations. Always distinguish verified active invite / public membership claim / proven activity / inferred quality. Never say "all highly active" unless proven.

## Commands
`python scripts/google_sheets.py test|setup|import|flush` · `python scripts/run_research.py process <file> | revalidate | stats` · add `--no-sheet` for "find but don't save yet".

## Setup status
Sheet: **WhatsApp Group Research** — ID `117t_FVH1uMFcuat5LwO1J8lwIfhoa1qz5MAWXKre_1w` (owner's Drive). Auth: **Google Sheets MCP connector** (`mcp__Google_Sheets__*`).
MCP write flow: `run_research.py process` writes `data/sheet_outbox_<date>.json` → Claude calls `append_values` for each worksheet (`'Approved Groups'!A1`, etc.) → re-reads the appended range with `get_values` to verify → then clears the outbox file. Before dedupe each run, read all invite codes from the Sheet (`'Approved Groups'!H2:H`, `'Rejected Groups'!D2:D`) and merge into local DB.
Legacy exclusions (imported 2026-11-14 via `scripts/import_legacy.py`): 7,057 unique invite codes from the user's old sheets "Master groups" (1_…/10CsLnKCBPXvrHbGEqLrz1yuA7-KU5jPvQHDtcFlMEew), "New 50 groups" (1_S3wFLTZq3osuYEaDYjpteAY4-62KTzWeqhzFD4_6nY), "New 50 IT groups" (1cEMaY1VQsZ_wDWdYQ5B8t-TUo4UPyVQlm6KMfFk96Uw), "NEW 50 IT GROUPS" (1LG1hVzIhzFdW-jF6fRzRPbKbjJ8MW6QVcMacOdLciGc). Stored in `data/previous_groups.json` (4,689) and `data/rejected_groups.json` (2,368, legacy-invalid). Never re-supply any of them, nor regenerated links of the same groups (name dedupe). Several old sheets hide links behind "Join Now" hyperlinks — read with `get_spreadsheet` + `includeGridData` and `sheets.data.rowData.values` to get `hyperlink`.
See `config/research_config.json` → `sheet`. Credentials live only in `credentials/` (git-ignored) and `.env`.
