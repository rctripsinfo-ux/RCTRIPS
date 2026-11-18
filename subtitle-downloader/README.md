# SubGrab — local subtitle downloader

Paste a video link and download its subtitles as **SRT**, **VTT** or **TXT**. It handles creator-uploaded, auto-generated and auto-translated captions from YouTube and the 1000+ sites [yt-dlp](https://github.com/yt-dlp/yt-dlp) supports. Everything runs on your own computer.

## Requirements
- Node.js 18 or newer
- yt-dlp on your PATH (`pip install -U yt-dlp`, `brew install yt-dlp`, or `winget install yt-dlp`)

No npm packages are needed.

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

If YouTube answers "Sign in to confirm you're not a bot", or a video is age-restricted or private, start the app with your browser's cookies:
```bash
YTDLP_EXTRA_ARGS="--cookies-from-browser chrome" npm start
```
Keep yt-dlp up to date (`yt-dlp -U` or `pip install -U yt-dlp`), because sites change often.

## API
- `POST /api/info` with `{"url": "..."}` returns the video's details and its subtitle tracks
- `GET /api/subtitle?url=...&track=manual:en&format=srt|vtt|txt` returns the file (`&inline=1` previews it instead)
- `GET /api/health` reports the yt-dlp version

## Tests
```bash
npm test
```

Only download subtitles you have the right to use.
