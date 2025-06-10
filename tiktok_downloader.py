#!/usr/bin/env python3
"""
Tikstalk - Simple TikTok Downloader
Author: @henrefresh
Description: Simple TikTok video downloader using yt-dlp and FFmpeg
Features: Basic video downloading, FFmpeg conversion, simple GUI
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import os
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import hashlib
from typing import Dict, List, Optional

class TikstalkSimple:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tikstalk - Simple TikTok Downloader")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Configuration
        self.username = "mrbeast"
        # Set default download folder to Downloads folder next to the Python script
        script_dir = Path(__file__).parent
        self.download_folder = str(script_dir / "Downloads")
        self.downloaded_videos = set()
        self.config_file = "tikstalk_simple_config.json"
        
        # Monitoring configuration
        self.is_monitoring = False
        self.check_interval = 10  # minutes
        self.bypass_ssl = True
        self.monitor_thread = None
        
        # Video format options (simplified)
        self.video_formats = {
            "Best Quality": "best",
            "Best MP4": "best[ext=mp4]/best",
            "720p MP4": "best[height<=720][ext=mp4]/best[ext=mp4]",
            "480p MP4": "best[height<=480][ext=mp4]/best[ext=mp4]",
            "Audio Only": "bestaudio"
        }
        
        # FFmpeg conversion options (simplified)
        self.conversion_options = {
            "No Conversion": None,
            "Convert to MP4": {
                "format": "mp4",
                "codec": "libx264"
            },
            "Compress Video": {
                "format": "mp4",
                "codec": "libx264",
                "crf": "28"
            },
            "Extract Audio (MP3)": {
                "format": "mp3",
                "codec": "libmp3lame"
            }
        }
        
        # Create download folder
        Path(self.download_folder).mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        self.load_config()
        
        # Setup GUI
        self.setup_gui()
        
        # Check dependencies
        self.check_dependencies()
    
    def setup_gui(self):
        """Setup the simple GUI interface"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(9, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Tikstalk - Simple TikTok Downloader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Username section
        ttk.Label(main_frame, text="TikTok Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar(value=self.username)
        username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=25)
        username_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Download folder section
        ttk.Label(main_frame, text="Download Folder:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.folder_var = tk.StringVar(value=self.download_folder)
        folder_entry = ttk.Entry(main_frame, textvariable=self.folder_var, width=50)
        folder_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_folder)
        browse_btn.grid(row=2, column=2, pady=5, padx=(5, 0))
        
        # Video quality section
        ttk.Label(main_frame, text="Video Quality:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.StringVar(value="Best MP4")
        quality_combo = ttk.Combobox(main_frame, textvariable=self.quality_var, 
                                   values=list(self.video_formats.keys()), state="readonly")
        quality_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Conversion section
        ttk.Label(main_frame, text="Conversion:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.conversion_var = tk.StringVar(value="No Conversion")
        conversion_combo = ttk.Combobox(main_frame, textvariable=self.conversion_var,
                                      values=list(self.conversion_options.keys()), state="readonly")
        conversion_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Video limit section
        ttk.Label(main_frame, text="Video Limit:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.limit_var = tk.StringVar(value="50")
        limit_spin = ttk.Spinbox(main_frame, from_=1, to=500, textvariable=self.limit_var, width=10)
        limit_spin.grid(row=5, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # Monitoring section
        monitor_frame = ttk.LabelFrame(main_frame, text="Auto Monitoring", padding="10")
        monitor_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Check interval
        ttk.Label(monitor_frame, text="Check every:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.check_interval_var = tk.IntVar(value=self.check_interval)
        interval_spin = ttk.Spinbox(monitor_frame, from_=1, to=60, textvariable=self.check_interval_var, width=5)
        interval_spin.grid(row=0, column=1, sticky=tk.W, pady=2, padx=(5, 0))
        ttk.Label(monitor_frame, text="minutes").grid(row=0, column=2, sticky=tk.W, pady=2, padx=(5, 0))
        
        # SSL bypass option
        self.ssl_bypass_var = tk.BooleanVar(value=self.bypass_ssl)
        ssl_check = ttk.Checkbutton(monitor_frame, text="Bypass SSL verification", variable=self.ssl_bypass_var)
        ssl_check.grid(row=0, column=3, sticky=tk.W, pady=2, padx=(20, 0))
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="Download Options", padding="10")
        options_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.metadata_var = tk.BooleanVar(value=True)
        metadata_check = ttk.Checkbutton(options_frame, text="Save metadata", variable=self.metadata_var)
        metadata_check.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.thumbnail_var = tk.BooleanVar(value=True)
        thumbnail_check = ttk.Checkbutton(options_frame, text="Save thumbnails", variable=self.thumbnail_var)
        thumbnail_check.grid(row=0, column=1, sticky=tk.W, pady=2, padx=(20, 0))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=3, pady=20)
        
        self.download_btn = ttk.Button(button_frame, text="Download Now", 
                                     command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.monitor_btn = ttk.Button(button_frame, text="Start Monitoring", 
                                    command=self.start_monitoring, style="Accent.TButton")
        self.monitor_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(button_frame, text="Clear Log", command=self.clear_log)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.reset_btn = ttk.Button(button_frame, text="Reset", command=self.reset_downloads)
        self.reset_btn.pack(side=tk.LEFT)
        
        # Status and log section
        status_frame = ttk.LabelFrame(main_frame, text="Status & Logs", padding="10")
        status_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(1, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to download")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Log area
        self.log_text = scrolledtext.ScrolledText(status_frame, height=15, width=70)
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Stats
        stats_frame = ttk.Frame(status_frame)
        stats_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.count_var = tk.StringVar(value=f"Downloaded: {len(self.downloaded_videos)}")
        count_label = ttk.Label(stats_frame, textvariable=self.count_var)
        count_label.pack(side=tk.LEFT)
    
    def browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(initialdir=self.folder_var.get())
        if folder:
            self.folder_var.set(folder)
            self.download_folder = folder
    
    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Update GUI in main thread
        self.root.after(0, lambda: self._update_log(log_entry))
    
    def _update_log(self, message):
        """Update log text widget (must be called from main thread)"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log text"""
        self.log_text.delete(1.0, tk.END)
    
    def update_status(self, status):
        """Update status label"""
        self.root.after(0, lambda: self.status_var.set(status))
    
    def update_count(self):
        """Update downloaded count"""
        self.root.after(0, lambda: self.count_var.set(f"Downloaded: {len(self.downloaded_videos)}"))
    
    def reset_downloads(self):
        """Reset downloaded videos list"""
        result = messagebox.askyesno("Reset", "Clear downloaded videos list?")
        if result:
            self.downloaded_videos.clear()
            self.update_count()
            self.save_config()
            self.log_message("Downloaded videos list cleared")
    
    def check_dependencies(self):
        """Check if required tools are installed"""
        # Check yt-dlp
        try:
            result = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                self.log_message(f"yt-dlp found: {result.stdout.strip()}")
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            self.log_message("yt-dlp not found. Installing...")
            self.install_ytdlp()
        
        # Check FFmpeg
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                self.log_message(f"FFmpeg found: {version_line}")
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            self.log_message("FFmpeg not found. Video conversion disabled.")
            messagebox.showwarning("FFmpeg Missing", 
                                 "FFmpeg not installed. Video conversion features disabled.\n\n"
                                 "To install: brew install ffmpeg")
    
    def install_ytdlp(self):
        """Install yt-dlp using pip3"""
        try:
            self.log_message("Installing yt-dlp...")
            result = subprocess.run(["pip3", "install", "yt-dlp"], capture_output=True, text=True)
            if result.returncode == 0:
                self.log_message("yt-dlp installed successfully!")
            else:
                self.log_message(f"Failed to install yt-dlp: {result.stderr}")
                messagebox.showerror("Error", "Failed to install yt-dlp. Please install manually: pip3 install yt-dlp")
        except Exception as e:
            self.log_message(f"Error installing yt-dlp: {str(e)}")
    
    def get_video_hash(self, video_id, title):
        """Generate unique hash for video to prevent duplicates"""
        unique_string = f"{video_id}_{title}"
        return hashlib.md5(unique_string.encode()).hexdigest()
    
    def convert_video_with_ffmpeg(self, input_path: str, output_path: str, conversion_options: Dict):
        """Convert video using FFmpeg"""
        try:
            cmd = ["ffmpeg", "-i", input_path, "-y"]  # -y to overwrite
            
            if conversion_options.get("codec"):
                if conversion_options["format"] == "mp3":
                    cmd.extend(["-acodec", conversion_options["codec"]])
                else:
                    cmd.extend(["-vcodec", conversion_options["codec"]])
                    if conversion_options.get("crf"):
                        cmd.extend(["-crf", conversion_options["crf"]])
            
            cmd.append(output_path)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_message(f"✓ Converted: {Path(output_path).name}")
                # Remove original file if conversion successful
                if input_path != output_path:
                    os.remove(input_path)
                return True
            else:
                self.log_message(f"✗ Conversion failed: {result.stderr[:100]}")
                return False
                
        except Exception as e:
            self.log_message(f"✗ Conversion error: {str(e)}")
            return False
    
    def download_videos(self, username: str):
        """Download videos from TikTok user"""
        try:
            # Clean username
            clean_username = username.replace('@', '')
            user_folder = Path(self.download_folder) / clean_username
            user_folder.mkdir(parents=True, exist_ok=True)
            
            # Get video list first
            self.update_status("Getting video list...")
            self.log_message(f"Getting videos for @{clean_username}")
            
            url = f"https://www.tiktok.com/@{clean_username}"
            limit = int(self.limit_var.get())
            
            # Get video info
            list_cmd = [
                "yt-dlp",
                "--flat-playlist",
                "--print", "%(id)s %(title)s",
                "--playlist-end", str(limit)
            ]
            
            # Add SSL bypass if enabled
            if self.ssl_bypass_var.get():
                list_cmd.append("--no-check-certificate")
            
            list_cmd.append(url)
            
            result = subprocess.run(list_cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                self.log_message(f"✗ Failed to get video list: {result.stderr}")
                return
            
            # Parse video list
            videos = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split(' ', 1)
                    if len(parts) >= 2:
                        video_id = parts[0]
                        title = parts[1] if len(parts) > 1 else "Unknown"
                        
                        # Check if already downloaded
                        video_hash = self.get_video_hash(video_id, title)
                        if video_hash not in self.downloaded_videos:
                            videos.append({'id': video_id, 'title': title, 'hash': video_hash})
            
            if not videos:
                self.log_message("No new videos to download")
                self.update_status("No new videos found")
                return
            
            self.log_message(f"Found {len(videos)} new videos to download")
            
            # Download videos
            self.update_status(f"Downloading {len(videos)} videos...")
            successful = 0
            
            for i, video in enumerate(videos):
                self.update_status(f"Downloading {i+1}/{len(videos)}: {video['title'][:30]}...")
                
                if self.download_single_video(clean_username, video, user_folder):
                    successful += 1
                    self.downloaded_videos.add(video['hash'])
                    self.update_count()
                
                # Small delay between downloads
                time.sleep(1)
            
            self.log_message(f"Download complete: {successful}/{len(videos)} videos downloaded")
            self.update_status(f"Complete: {successful}/{len(videos)} downloaded")
            self.save_config()
            
        except subprocess.TimeoutExpired:
            self.log_message("✗ Timeout getting video list")
        except Exception as e:
            self.log_message(f"✗ Error: {str(e)}")
        finally:
            if not self.is_monitoring:
                self.progress.stop()
                self.download_btn.config(state=tk.NORMAL)
    
    def download_single_video(self, username: str, video_info: Dict, user_folder: Path) -> bool:
        """Download a single video"""
        try:
            video_id = video_info['id']
            title = video_info['title']
            
            # Construct URL
            video_url = f"https://www.tiktok.com/@{username}/video/{video_id}"
            
            # Get selected quality format
            quality_key = self.quality_var.get()
            format_selector = self.video_formats.get(quality_key, "best")
            
            # Build filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()[:50]
            filename_template = f"{username}_{video_id}_{safe_title}.%(ext)s"
            
            # Build download command
            download_cmd = [
                "yt-dlp",
                "--format", format_selector,
                "--output", str(user_folder / filename_template),
                "--no-warnings"
            ]
            
            # Add SSL bypass if enabled
            if self.ssl_bypass_var.get():
                download_cmd.append("--no-check-certificate")
            
            # Add optional features
            if self.metadata_var.get():
                download_cmd.append("--write-info-json")
            if self.thumbnail_var.get():
                download_cmd.append("--write-thumbnail")
            
            download_cmd.append(video_url)
            
            # Execute download
            result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                # Handle video conversion if enabled
                conversion_key = self.conversion_var.get()
                if conversion_key != "No Conversion" and conversion_key in self.conversion_options:
                    conversion_opts = self.conversion_options[conversion_key]
                    if conversion_opts:
                        # Find the downloaded file
                        for file_path in user_folder.glob(f"*{video_id}*"):
                            if file_path.suffix in ['.mp4', '.webm', '.mkv']:
                                new_ext = conversion_opts['format']
                                output_path = file_path.with_suffix(f'.{new_ext}')
                                self.convert_video_with_ffmpeg(str(file_path), str(output_path), conversion_opts)
                                break
                
                self.log_message(f"✓ Downloaded: {title[:40]}")
                return True
            else:
                self.log_message(f"✗ Failed: {title[:40]} - {result.stderr[:50]}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_message(f"✗ Timeout: {title[:40]}")
            return False
        except Exception as e:
            self.log_message(f"✗ Error: {title[:40]} - {str(e)}")
            return False
    
    def start_download(self):
        """Start download in separate thread"""
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        self.download_folder = self.folder_var.get()
        
        # Disable button and start progress
        self.download_btn.config(state=tk.DISABLED)
        self.progress.start()
        
        # Start download thread
        thread = threading.Thread(target=self.download_videos, args=(username,))
        thread.daemon = True
        thread.start()
    
    def start_monitoring(self):
        """Start monitoring mode"""
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        if self.is_monitoring:
            # Stop monitoring
            self.is_monitoring = False
            self.monitor_btn.config(text="Start Monitoring")
            self.download_btn.config(state=tk.NORMAL)
            self.progress.stop()
            self.update_status("Monitoring stopped")
            self.log_message("Monitoring stopped")
        else:
            # Start monitoring
            self.is_monitoring = True
            self.monitor_btn.config(text="Stop Monitoring")
            self.download_btn.config(state=tk.DISABLED)
            self.progress.start()
            self.update_status("Monitoring started")
            self.log_message(f"Started monitoring @{username} every {self.check_interval_var.get()} minutes")
            
            # Start monitoring thread
            self.monitor_thread = threading.Thread(target=self.monitor_loop, args=(username,))
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
    
    def monitor_loop(self, username):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                self.download_videos(username)
                
                # Wait for the specified interval
                interval_minutes = self.check_interval_var.get()
                for _ in range(interval_minutes * 60):  # Convert to seconds
                    if not self.is_monitoring:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                self.log_message(f"Monitoring error: {str(e)}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.downloaded_videos = set(config.get('downloaded_videos', []))
                    self.download_folder = config.get('download_folder', self.download_folder)
        except Exception as e:
            self.log_message(f"Error loading config: {str(e)}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                'downloaded_videos': list(self.downloaded_videos),
                'download_folder': self.download_folder
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            self.log_message(f"Error saving config: {str(e)}")
    
    def on_closing(self):
        """Handle application closing"""
        self.save_config()
        self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

def main():
    """Main function"""
    app = TikstalkSimple()
    app.run()

if __name__ == "__main__":
    main()