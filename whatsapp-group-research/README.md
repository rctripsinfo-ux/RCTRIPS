# WhatsApp Group Research System

Reusable pipeline to find, validate, dedupe, score and log WhatsApp groups into a Google Sheet. Operating rules: see `CLAUDE.md`.

## Setup
```bash
pip install requests gspread
cp .env.example .env   # set GOOGLE_SHEET_ID
# put service-account JSON at credentials/service_account.json (git-ignored)
python scripts/google_sheets.py test    # read-only check
python scripts/google_sheets.py setup   # create missing worksheets/headers only
python scripts/google_sheets.py import  # load existing links into exclusion DB
```

## Run
```bash
python scripts/validate_whatsapp.py https://chat.whatsapp.com/XXXX
python scripts/run_research.py process data/candidates.json --niche "B2B travel"
python scripts/run_research.py revalidate
```
