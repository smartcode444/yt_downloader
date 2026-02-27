import yt_dlp
from tkinter import messagebox
import json

class VideoHandler:
    """Handles video downloading and metadata extraction using yt_dlp."""
    
    def __init__(self):
        self.title = None
        self.url = None
        self.metadata = None
        self.window = None
        self.progress_callback = None 

    def fetch_metadata(self, url):
        """Fetch metadata for a given YouTube video URL."""
        try:
            ydl_opts = {'quiet': True, 'no_warnings': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.metadata = ydl.extract_info(url, download=False)
                self.title = self.metadata.get('title', 'Unknown Video')
                self.url = url
                with open('metadata.json', 'w') as f:  # Debug: Save metadata to a file
                    json.dump(self.metadata, f, indent=2)
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


    def start_download(self, format_id, save_path, output_format, progress_callback):
        """Download video in specified format with progress tracking."""
        try:
            self.progress_callback = progress_callback
            
            if output_format == 'mp3':
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'paths': {'home': save_path},
                    'ffmpeg_location': './ffmpeg.exe',
                    'outtmpl': '%(title)s.%(ext)s',
                    'quiet': False,
                    'no_warnings': False,
                    'progress_hooks': [self._progress_hook],
                }
            else:
                ydl_opts = {
                    'format': f'{format_id}+bestaudio/best',
                    'paths': {'home': save_path},
                    'ffmpeg_location': './ffmpeg.exe',
                    'outtmpl': '%(title)s.%(ext)s',
                    'merge_output_format': output_format,
                    'quiet': False,
                    'no_warnings': False,
                    'progress_hooks': [self._progress_hook],
                }
              
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            
            return True
        except Exception as e:
            raise Exception(f"Download failed: {str(e)}")

    def _progress_hook(self, d):
        """Internal progress hook for yt_dlp."""
        if self.progress_callback:
            self.progress_callback(d)
        
