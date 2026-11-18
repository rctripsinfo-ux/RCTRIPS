# SubGrab — local subtitle downloader

Paste a video link and download its subtitles as **SRT**, **word-by-word SRT**, **VTT** or **TXT**. **Bulk mode** takes many links at once (pasted, or uploaded as a .txt/.csv file) and gives you one ZIP. You can also paste a **YouTube channel or playlist link**, load all its videos, tick the ones you want, and download all their transcripts in one ZIP. It handles creator-uploaded, auto-generated and auto-translated captions from YouTube and the 1000+ sites [yt-dlp](https://github.com/yt-dlp/yt-dlp) supports. Everything runs on your own computer.

## Requirements
- Node.js 18 or newer
- Python 3.9+ with the tools in `requirements.txt`:
  `python -m pip install --user -U -r requirements.txt`
  - **yt-dlp** reads videos and subtitles
  - **gallery-dl** lists the reels on an Instagram profile
  - **faster-whisper** is the free, local AI speech-to-text (Whisper) used for videos without subtitles, like Instagram reels

No npm packages are needed. On Windows, `start.bat` installs everything automatically.

## Instagram
Instagram doesn't publish subtitles, so SubGrab downloads the reel's audio and transcribes it on your computer with Whisper (word-level timings included).
- **Single reel:** paste the reel link and choose *Transcribe the audio*.
- **Whole profile:** go to *Bulk links*, paste `https://www.instagram.com/username/` into *Fetch a whole channel…*, and load the reels.
- Instagram requires a login: stay logged in to instagram.com in **Firefox** (on Windows, `start.bat` uses Firefox's cookies automatically). You can also set `COOKIES_FROM_BROWSER=firefox|chrome|edge`.
- **AI quality:** *Accurate* (`large-v3-turbo`, the default) or *Most accurate* (`large-v3`, which is better for Hindi/Hinglish but slower). The model downloads once (about 1.5–3 GB). An NVIDIA GPU is used automatically when available.

## Run
```bash
cd subtitle-downloader
npm start
```
Then open http://127.0.0.1:3000.

On Windows you can instead double-click `start.bat`. It finds or installs yt-dlp and opens your browser.

## Configuration (environment variables)
| Variable | Default | Purpose |
|---|---|---|
| `PORT` | `3000` | Port to listen on |
| `HOST` | `127.0.0.1` | Set `0.0.0.0` to allow other devices on your LAN |
| `YTDLP_PATH` | `yt-dlp` | Path to the yt-dlp executable |
| `YTDLP_EXTRA_ARGS` | — | Extra yt-dlp flags, e.g. `--cookies-from-browser chrome` |
| `YTDLP_TIMEOUT_MS` | `90000` | Timeout for each extractor call |
| `COOKIES_FROM_BROWSER` | — | Browser to read login cookies from (`firefox`, `chrome`, `edge`) |
| `PYTHON` | `python3` / `python` | Python used for the AI transcription and tool fallback |
| `WHISPER_DEVICE` | `auto` | `cpu` or `cuda` |

If YouTube answers "Sign in to confirm you're not a bot", or a video is age-restricted or private, start the app with your browser's cookies:
```bash
YTDLP_EXTRA_ARGS="--cookies-from-browser chrome" npm start
```
Keep yt-dlp up to date (`yt-dlp -U` or `pip install -U yt-dlp`), because sites change often.

## API
- `POST /api/info` with `{"url": "..."}` returns the video's details and its subtitle tracks
- `GET /api/subtitle?url=...&track=manual:en&format=srt|words|vtt|txt` returns the file (`&inline=1` previews it instead)
- `POST /api/list` with `{"url": "<channel or playlist>", "limit": 0, "sections": ["videos","shorts","streams"]}` lists a channel's or playlist's videos
- `GET /api/health` reports the yt-dlp version

## Tests
```bash
npm test
```

Only download subtitles you have the right to use.
