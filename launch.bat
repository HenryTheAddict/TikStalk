@echo off
REM TikTok Downloader Launcher Script for Windows
REM This script ensures dependencies are installed and launches the application

echo 🎵 TikTok Auto Stalker
echo ==========================================

REM Check if Python 3 is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo ✅ pip found

REM Install dependencies
if exist requirements.txt (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
) else (
    echo 📦 Installing yt-dlp...
    pip install yt-dlp
)

echo 🚀 Launching TikTok Downloader...
echo    Close this window to stop the application.
echo.

REM Launch the application
python tiktok_downloader.py

pause