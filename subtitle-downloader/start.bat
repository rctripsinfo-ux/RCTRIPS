@echo off
title SubGrab
rem To force a tools update, delete the file .deps-installed in this folder.
cd /d "%~dp0"

where node >nul 2>nul || (
  echo Node.js is not installed. Opening the download page - install the LTS version, then run this again.
  start "" https://nodejs.org
  pause
  exit /b
)

set "PYTHON="
where python >nul 2>nul && python -c "import sys" >nul 2>nul && set "PYTHON=python"
if not defined PYTHON where py >nul 2>nul && set "PYTHON=py"
if not defined PYTHON (
  echo Python is not installed. Opening the download page - install it and tick "Add python.exe to PATH", then run this again.
  start "" https://www.python.org/downloads/
  pause
  exit /b
)

if not exist ".deps-installed" (
  echo Installing / updating tools: yt-dlp, gallery-dl, faster-whisper.
  echo This happens once and may take a few minutes...
  %PYTHON% -m pip install --user -U -r requirements.txt
  if errorlevel 1 (
    echo Installation failed. Check your internet connection and run this again.
    pause
    exit /b
  )
  echo done> ".deps-installed"
)

if not defined COOKIES_FROM_BROWSER if exist "%APPDATA%\Mozilla\Firefox\Profiles" set "COOKIES_FROM_BROWSER=firefox"

echo.
echo SubGrab is starting. Your browser will open in a moment.
echo Keep this window open while you use it. Close it to stop SubGrab.
echo For Instagram: stay logged in to instagram.com in Firefox.
echo The first AI transcription downloads the speech model (1.5-3 GB) once.
echo.
start "" cmd /c "timeout /t 2 >nul & start http://127.0.0.1:3000"
node server.js
pause
