import threading
import re
import os
from main.handler import VideoHandler
from main.thumbnail import fetch_thumbnail_response
from main.path import get_save_path, store_save_path

class Backend:
    """Handles business logic between UI and video handler."""
    
    def __init__(self, window):
        self.window = window
        self.handler = VideoHandler()
        self.video_data = None
        self.selected_format = None
        self.cancel_event = threading.Event()

    def validate_url(self, url):
        """Basic validation for YouTube URLs."""
        pattern = re.match(
            r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)[\w-]{11}(.*)?$', 
            url, 
            re.IGNORECASE 
        )
        return bool(pattern)

    def fetch_video(self):
        """Fetch metadata for the entered YouTube URL."""
        url = self.window.url.get().strip()

        if not url:
            self.window.show_error("Input Error", "Please enter a YouTube URL")
            return
        
        if not self.validate_url(url):
            self.window.show_error("Input Error", "Please enter a valid YouTube URL")
            return

        try:
            # Show loading message
            self.window._loading_indicator()
            self.window.window.update() # 
            
            # Fetch metadata
            self.video_data = self.handler.fetch_metadata(url)
            
            self.window.format_combo['values'] = ['mkv', 'mp4', 'mp3']
            self.window.format_combo.current(0)
            
            self.window._clear_loading_indicator()
            self.window.show_info("Success", f"Video loaded: {self.handler.title}")

            # Fetch and display thumbnail
            if self.window.thumbnail_label and self.window.title_label:
                self.window.clear_thumbnail_and_title()
           
            thumbnail_response = fetch_thumbnail_response(self.handler.metadata.get('id'))
            title = self.handler.title
            if thumbnail_response:
                self.window.display_thumbnail_and_title(thumbnail_response, title=title)
            
        except Exception as e:
            self.window.hide_progress()
            self.window.show_error(
                "Error",
                f"Could not fetch video: {str(e)}\n\nPlease check:\n• Internet connection\n• Valid YouTube URL"
            )
 

    def on_format_selected(self, event=None):
        """Handle format selection change."""
        selected_format = self.window.format_var.get()
        self.selected_format = selected_format
        
        if selected_format == "mp3":
            # For MP3, no resolution or codec selection needed
            self.window.res_combo.set('')
            self.window.res_combo['values'] = []
            self.window.vcodec_combo.set('')
            self.window.vcodec_combo['values'] = []
        else:
            # For MP4/MKV, show resolutions
            self._populate_resolutions()

    def resolutions(self):
        """Get resolutions from video data."""
        if not self.video_data:
            return []
        
        # Extract unique resolutions, filtering out very small ones
        to_remove = {27, 45, 90}
        resolutions = [v['res'] for v in self.video_data if v['res'] not in to_remove]
        resolutions = sorted(set(resolutions), reverse=True)
        
        # Format as strings with 'p'
        res_strings = [f"{res}p" for res in resolutions]
        return res_strings
    
    def _populate_resolutions(self):
        """Populate resolution dropdown."""
        res_strings = self.resolutions()
        self.window.res_combo['values'] = res_strings
        if res_strings:
            self.window.res_combo.current(0)

    def codecs_for_resolution(self, resolution):
        """Get codecs available for a given resolution."""
        if not self.video_data:
            return []
        
        codecs = [
            v['vcodec_name'] for v in self.video_data
            if v['res'] == resolution
        ]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_codecs = []
        for codec in codecs:
            if codec not in seen:
                seen.add(codec)
                unique_codecs.append(codec)
        
        return unique_codecs

    def on_resolution_selected(self, event=None):
        """Handle resolution selection change."""
        resolution_str = self.window.res_var.get()
        if not resolution_str:
            return
        
        resolution = int(resolution_str.replace('p', ''))
        
        codecs = self.codecs_for_resolution(resolution)
        
        self.window.vcodec_combo['values'] = codecs
        if codecs:
            self.window.vcodec_combo.current(0)

    def on_codec_selected(self, event=None):
        """Handle codec selection (currently just updates state)."""
        pass

    def start_download(self):
        """Initiate the download process."""
        selected_format = self.window.format_var.get()
        
        if not selected_format:
            self.window.show_error("Selection Error", "Please select a format")
            return
        
        # Get format-specific parameters
        format_id = None
        if selected_format in ["mp4", "mkv"]:
            resolution_str = self.window.res_var.get()
            codec_name = self.window.vcodec_var.get()
            
            if not resolution_str or not codec_name:
                self.window.show_error("Selection Error", "Please select resolution and codec")
                return
            
            resolution = int(resolution_str.replace('p', ''))
            
            # Find the format ID matching selection
            for video in self.video_data:
                if video['res'] == resolution and video['vcodec_name'] == codec_name:
                    format_id = video['id']
                    break
            
            if not format_id:
                self.window.show_error("Error", "Could not find matching format")
                return
        
        # Get stored save path or ask user to select one
        self.save_path = get_save_path()
        if self.save_path:
            self.save_path = self.window.ask_directory(initial_dir=self.save_path)
            store_save_path(self.save_path)
        else:
            self.save_path = self.window.ask_directory()
            store_save_path(self.save_path)
        
        # Clear the cancel event before starting new download
        self.cancel_event.clear()

        # Start download in background thread
        self.window.show_progress()
        download_thread = threading.Thread(
            target=self._download_worker,
            args=(format_id, self.save_path, selected_format),
            daemon=True
        )
        download_thread.start()

    def stop_download(self):
        """Signal the download thread to stop."""
        self.cancel_event.set()


    def _download_worker(self, format_id, save_path, output_format):
        """Background worker for downloading video."""
        try:
            self.handler.start_download(
                format_id,
                save_path,
                output_format,
                self._progress_callback,
                self.cancel_event
            )
            
            # Success
            self.window.window.after(0, self._on_download_complete)
            
        except Exception as e:
            error_msg = str(e)
            if self.cancel_event.is_set():
                error_msg = "Download cancelled by user"
            self.window.window.after(
                0,
                lambda: self.window.show_error("Download Error", error_msg)
            )
        finally:
            self.window.window.after(0, self.window.hide_progress)

    def _on_download_complete(self):
        """Called when download completes successfully."""
        self.window.show_info("Success", "Download completed!")
        
        if self.window.ask_yes_no("Success", "Open download folder?"):
            os.startfile(self.save_path)

    def _progress_callback(self, d):
        """Callback for yt_dlp progress updates."""
        status = d.get('status')
        
        if status == 'downloading':
            # Extract and clean progress data
            percent_str = d.get('_percent_str', '0%').replace('%', '').strip()
            percent_str = re.sub(r'\x1b\[[0-9;]*m', '', percent_str)
            
            try:
                percent = float(percent_str)
            except (ValueError, TypeError):
                percent = 0.0
            
            speed = d.get('_speed_str', 'N/A')
            speed = re.sub(r'\x1b\[[0-9;]*m', '', speed).strip()
            
            eta = d.get('_eta_str', 'N/A')
            eta = re.sub(r'\x1b\[[0-9;]*m', '', eta).strip()
            
            dl_bytes = d.get('downloaded_bytes', 0)
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            
            # Update UI from main thread
            self.window.window.after(
                0,
                self._update_progress_ui,
                percent,
                speed,
                eta,
                dl_bytes,
                total_bytes
            )
        
        elif status == 'finished':
            self.window.window.after(
                0,
                lambda: self.window.progress_label.config(
                    text="Processing... Please wait",
                    foreground="orange"
                )
            )

    def _update_progress_ui(self, percent, speed, eta, dl_bytes, total_bytes):
        """Update progress bar and label."""
        self.window.progress_bar['value'] = percent
        
        dl_mb = dl_bytes / (1024 * 1024)
        total_mb = total_bytes / (1024 * 1024) if total_bytes else 0
        
        status_text = (
            f"{int(percent)}%  |  {speed}  |  {eta}  |  "
            f"{dl_mb:.1f}/{total_mb:.1f} MB"
        )
        self.window.progress_label.config(text=status_text)

