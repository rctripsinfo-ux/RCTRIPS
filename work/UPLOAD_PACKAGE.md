# After every finished LONG video: Google Drive upload package (owner rule, 22 Nov 2026)
SHORTS ARE NOT PUT IN DRIVE: the owner uploads Shorts by hand. For a Short, send the video (cover on the last frame) + title, description, tags in chat.
The owner's Chrome extension uploads every finished folder in `My Drive/YT Uploads/` to YouTube Studio (3 titles + 3 thumbnails A/B test).
- One folder per video: `YYYY-MM-DD_NN_short-slug` (new, unique, never renamed). Folders starting with `_` are ignored.
- Files: `video.mp4` (H.264+AAC, 16:9, 1080p+), `thumb_1/2/3.jpg` (3 different concepts, 1280x720, < 2 MB, <= 4 words), optional `transcript.txt`, `captions.srt`, and `metadata.json` WRITTEN LAST.
- Never create/edit/delete `upload_result.json` (the extension writes it).
- NEVER shrink or re-encode the video for a size limit. The Drive connector here cannot upload files > 10 MB: upload everything else, do NOT write metadata.json, and send the owner `video.mp4` + `metadata.json` in chat (owner adds video first, then metadata.json).
- metadata.json: template + field rules in the owner's prompt (3 titles <= 100 chars with different hooks, description <= 5000 chars with summary + chapters (0:00 first, >= 3, >= 10 s apart) + the standard block below + 3-5 hashtags, 8-15 tags <= 450 chars, category "Education", visibility "scheduled", schedule date/time local, 15-minute steps, in the future, one video per slot; no plan given -> next free day at the slot below).
- Publish slots (IST, from the owner's audience data, 26 Nov 2026; publish 1-2 h before the evening peak): Mon-Thu 16:00 (peak 17-21, best 18-20); Fri 18:30 (peak 20-21); Sat 15:00 (peak 17-22); Sun 13:30 (peak 15-20). One long video per day.
- Standard channel block, word for word:
```
New home workout and calisthenics videos every day. No gym, no equipment, just bodyweight training that works.

Subscribe and turn on notifications so you never miss a workout.

Disclaimer: This content is for general fitness education only. Start at your own level, use good form, and stop if you feel pain. If you have an injury or medical condition, check with a qualified professional before starting a new routine.
```
- Finish with a table: folder, title A, length, schedule, anything to check.
