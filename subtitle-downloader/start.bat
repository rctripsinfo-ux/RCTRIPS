@echo off
title SubGrab
cd /d "%~dp0"

where node >nul 2>nul || (
  echo Node.js is not installed. Opening the download page - install the LTS version, then run this again.
  start "" https://nodejs.org
  pause
  exit /b
)

where yt-dlp >nul 2>nul && goto run
call :find
if defined YTDLP_PATH goto run

echo Installing yt-dlp...
python -m pip install --user -U yt-dlp || py -m pip install --user -U yt-dlp
where yt-dlp >nul 2>nul && goto run
call :find
if defined YTDLP_PATH goto run
echo Could not find or install yt-dlp. Install Python from https://www.python.org and run this again.
pause
exit /b

:find
for /d %%D in ("%APPDATA%\Python\Python3*") do if exist "%%D\Scripts\yt-dlp.exe" set "YTDLP_PATH=%%D\Scripts\yt-dlp.exe"
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do if exist "%%D\Scripts\yt-dlp.exe" set "YTDLP_PATH=%%D\Scripts\yt-dlp.exe"
exit /b

:run
echo.
echo SubGrab is starting. Your browser will open in a moment.
echo Keep this window open while you use it. Close it to stop SubGrab.
echo.
start "" cmd /c "timeout /t 2 >nul & start http://127.0.0.1:3000"
node server.js
pause
