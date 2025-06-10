#!/bin/bash

# TikTok Downloader Launcher Script
# This script ensures dependencies are installed and launches the application

echo "🎵 TikTok Auto Stalker"
echo "=========================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip3 is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✅ pip3 found"

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
else
    echo "📦 Installing yt-dlp..."
    pip3 install yt-dlp
fi

echo "🚀 Launching TikTok Downloader..."
echo "   Close the terminal window to stop the application."
echo ""

# Launch the application
python3 tiktok_downloader.py