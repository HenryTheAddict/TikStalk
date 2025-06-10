# Tikstalk - Easy TikTok Scraper
Yeah, its cool trust me.
## 🚀 Features

### Core Functionality
- **Multi-Content Scraping**: Download videos, reposts, and liked videos
- **Full Account Scraping**: Complete account download with everything the bot can find.
- **Automated Monitoring**: Configurable interval checking for new content
- **Concurrent Downloads**: Multi-threaded downloading for improved speed!
- **Duplicate Prevention**: Smart tracking to avoid re-downloading content

### Advanced Features
- **FFmpeg Integration**: Video conversion and compression options
- **Quality Selection**: Choose from multiple video quality options
- **Batch Processing**: Download from multiple users simultaneously
- **Content Organization**: Automatic folder organization by content type and date
- **Metadata Extraction**: Optional download of video info, thumbnails, and subtitles

### User Interface
- **Tabbed Interface**: Organized main settings and batch download tabs
- **Real-time Progress**: Live download progress and speed monitoring
- **Comprehensive Logging**: Detailed activity logs with timestamps
- **Persistent Settings**: All preferences saved between sessions

## 📋 Requirements

- Python 3.7+
- yt-dlp (automatically installed)
- FFmpeg (optional, for video conversion)
- tkinter (usually included with Python)

## 🛠 Installation

### Quick Start
1. Clone or download this repository
2. Run the launcher script for your platform:
   - **macOS/Linux**: `./launch.sh`
   - **Windows**: `launch.bat`

### Manual Installation
```bash
pip3 install yt-dlp
python3 tiktok_downloader.py
```

### FFmpeg Installation (Optional For Most)
- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt install ffmpeg`
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## 🎯 Usage

### Basic Setup
1. **Launch Tikstalk**
2. **Configure Target Account**
   - Enter TikTok username (without @ <or with it i didnt check>)
   - Select download folder
   - Set check interval

### Content Selection
- **Videos**: Regular TikTok posts
thats all!

### Quantity Controls
- Set limits. Whitch is something you dont do if you use this!

### Advanced Options
- **Video Quality**: Choose from Best, 720p, 480p, Audio Only
- **Organization**: Date-based folder structure (i wish she took me on a date😭)
- **Metadata**: Download video info, thumbnails, subtitles

### Batch Downloads
1. Switch to "Batch Downloads" tab
2. Enter multiple usernames (one per line)
3. Configure content types and limits
4. Start batch processing

## 📁 File Structure

```
project/
├── tiktok_downloader.py    # Main Tikstalk application
├── requirements.txt        # Python dependencies
├── launch.sh              # macOS/Linux launcher
├── launch.bat             # Windows launcher
├── README.md              # Documentation
└── Downloads/             # Default download folder
    └── Tikstalk_username/ # User-specific folders
        ├── Videos/        # Regular videos
        ├── Reposts/       # Reposted content
        └── Liked/         # Liked videos
```

## ⚙️ Configuration

Settings are saved in `tikstalk_config.json`:
- Downloaded content tracking.
- User preferences and limits
- Download folder location
- Scraping preferences
- Performance settings

## 🎥 Video Conversion Options

- **MP4 (H.264)**: Standard compatibility
- **WebM (VP9)**: Modern web format
- **Compressed**: Smaller file sizes
- **Audio Only**: MP3 extraction
- **Custom FFmpeg**: Advanced users can modify conversion settings

## 🚨 Troubleshooting

### SSL Certificate Errors
The application includes `--no-check-certificate` flag to bypass SSL issues common on macOS. (oof)

### Rate Limiting
Tikstalk respects platform rate limits with built-in delays and timeout handling.

### Memory Usage
For large batch downloads, monitor system resources and adjust concurrent worker count.

### FFmpeg Issues
Ensure FFmpeg is properly installed and accessible in system PATH for conversion features.

## 📊 Content Type Details

### Videos
- User's original TikTok posts
- Highest quality available
- Includes all metadata

### Reposts
- Content the user has shared/reposted
- Original creator attribution maintained
- Organized in separate folder

### Liked Videos
- Videos the user has liked (if profile is public)
- May have limited availability based on privacy settings
- Bulk download with quantity controls

### Full Account Scrape
- Comprehensive download of all available content
- Automatically enables all content types
- Sets optimized limits for complete coverage
- Ideal for archival purposes

## 🔒 Privacy & Ethics

- Respects TikTok's terms of service*
- Only downloads publicly available content
- Maintains original creator attribution
- For personal/educational use only

## 📈 Performance Metrics

- Real-time download speed monitoring
- Progress tracking for batch operations
- Detailed logging of all operations
- Success/failure statistics

## 🆕 Recent Updates

- **v2.0**: Complete rewrite as "Tikstalk"
- Added reposts and liked videos support
- Implemented full account scraping
- Enhanced UI with tabbed interface
- FFmpeg integration for video conversion
- Concurrent download support
- Batch processing capabilities

## 📄 License

This project is for educational and personal use. Please respect content creators' rights and TikTok's terms of service. I Like Nadja! thanks for slopping by.
