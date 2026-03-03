import yt_dlp
import os
from tkinter import messagebox
from main.path import get_ffmpeg_path

class VideoHandler:
    """Handles video downloading and metadata extraction using yt_dlp."""
    
    def __init__(self):
        self.title = None
        self.url = None
        self.metadata = None
        self.window = None
        self.progress_callback = None 
        self.ffmpeg_path = get_ffmpeg_path()

    def _ensure_ffmpeg(self):
        if not self.ffmpeg_path or not os.path.isdir(self.ffmpeg_path):
                messagebox.showerror(
                "FFmpeg Error",
                "FFmpeg and FFprobe executable not found." 
                "High-quality downloads and MP3 conversions will fail without these."
                "Please download it from "
                "https://ffmpeg.org and either put `ffmpeg.exe` and `ffprobe.exe` in the "
                "project directory or specify their directory absolute path in config.json."
            )

    def fetch_metadata(self, url):
        """Fetch metadata for a given YouTube video URL."""
        try:
            ydl_opts = {'quiet': True, 'no_warnings': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.metadata = ydl.extract_info(url, download=False)
                self.title = self.metadata.get('title', 'Unknown Video')
                self.url = url
                return self._parse_formats()
        except Exception as e:
            raise Exception(f"Failed to fetch video metadata: {str(e)}")

    def _parse_formats(self):
        """Parse and return available video formats."""
        formats = self.metadata.get('formats', [])
        
        def simplify_vcodec(vcodec):
            """Simplify video codec names for display."""
            if 'av01' in vcodec:
                return "Best Quality (AV1)"
            if 'vp9' in vcodec:
                return "High Quality (VP9)"
            if 'avc1' in vcodec:
                return "Most Compatible (H.264)"
            return vcodec

        metadata_list = []
        # Extract video-only formats (no audio)
        for fmt in formats:
            if fmt.get('height') and fmt.get('acodec') == 'none':
                metadata_list.append({
                    'id': fmt['format_id'],
                    'res': fmt['height'],
                    'fps': fmt.get('fps'),
                    'vcodec_raw': fmt['vcodec'],
                    'vcodec_name': simplify_vcodec(fmt['vcodec']),
                    'size': fmt.get('filesize', 0)
                }) 
        
        # Sort by resolution and fps
        metadata_list.sort(key=lambda x: (x['res'], x['fps'] or 0), reverse=True)
        return metadata_list


    def start_download(self, format_id, save_path, output_format, progress_callback, cancel_event=None):
        """Download video in specified format with progress tracking."""
        self._ensure_ffmpeg()


        try:
            self.progress_callback = progress_callback
            self.cancel_event = cancel_event
            
            if output_format == 'mp3':
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'paths': {'home': save_path},
                    'ffmpeg_location': self.ffmpeg_path,
                    'outtmpl': '%(title)s.%(ext)s',
                    'quiet': False,
                    'no_warnings': False,
                    'progress_hooks': [self._progress_hook],
                    'continuedl': True, # Allow resuming downloads if interrupted
                    'noncheckcertificate': True, # Bypass SSL certificate checks for better compatibility
                    'fixup': 'detect_or_warn', # Automatically fix common issues with downloaded files
                }
            else:
                ydl_opts = {
                    'format': f'{format_id}+bestaudio/best',
                    'paths': {'home': save_path},
                    'ffmpeg_location': self.ffmpeg_path,
                    'outtmpl': '%(title)s.%(ext)s',
                    'merge_output_format': output_format,
                    'quiet': False,
                    'no_warnings': False,
                    'progress_hooks': [self._progress_hook],
                    'continuedl': True, # Allow resuming downloads if interrupted
                    'noncheckcertificate': True, # Bypass SSL certificate checks for better compatibility
                    'fixup': 'detect_or_warn', # Automatically fix common issues with downloaded files
                }
              
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            
            return True
        except Exception as e:
            if self.cancel_event and self.cancel_event.is_set():
                raise Exception("Download cancelled by user")
            raise Exception(f"Download failed: {str(e)}")

    def _progress_hook(self, d):
        """Internal progress hook for yt_dlp."""
        # Check if cancel was requested
        if self.cancel_event and self.cancel_event.is_set():
            raise Exception("Download cancelled by user")
        if self.progress_callback:
            self.progress_callback(d)
        
