from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk 
import ttkbootstrap as ttk
from tkinter import messagebox, filedialog
from main.backend import Backend

class Window:
    """Manages the YouTube Downloader UI."""
    
    def __init__(self):
        self.window = ttk.Window(themename='darkly')
        self.backend = Backend(self)
        
        # URL entry
        self.url = tk.StringVar()
        
        # Format selection
        self.format_combo = None
        self.format_var = tk.StringVar()
        
        # Resolution selection
        self.res_combo = None
        self.res_var = tk.StringVar()
        
        # Video codec selection
        self.vcodec_combo = None
        self.vcodec_var = tk.StringVar()
        
        # Download button
        self.download_btn = None
        
        # Frames
        self.action_frame = None
        self.progress_frame = None
        
        # Progress widgets
        self.progress_bar = None
        self.progress_label = None

        # thumbnail and title display
        self.thumbnail_label = None
        self.title_label = None

        self.cancel_btn = None
        
    def setup(self):
        """Initialize the window and all UI elements."""
        self._setup_root()
        self._setup_title()
        self._setup_input()
        self._setup_action()
        self._setup_progress()
        self.author_info()  

    def _setup_root(self):
        """Configure the root window."""
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        window_width = 800
        window_height = 600
        window_x = int(width - window_width) // 2
        window_y = int(height - window_height) // 2
        self.window.title('YouTube Downloader')
        self.window.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
        self.window.resizable(False, False)

    def _setup_title(self):
        """Add the title label."""
        label = ttk.Label(
            master=self.window,
            text='YOUTUBE DOWNLOADER',
            font='Arial 20 bold'
        )
        label.pack(pady=10)

    def _setup_input(self):
        """Add URL input and fetch button."""
        frame = ttk.Frame(master=self.window)
        
        entry = ttk.Entry(master=frame, width=60, textvariable=self.url)
        entry.pack(side='left', padx=10)
        
        fetch_btn = ttk.Button(
            master=frame,
            text='Check Video',
            command=self.backend.fetch_video
        )
        fetch_btn.pack(side='left', padx=5)
        
        frame.pack(pady=10)

    def _setup_action(self):
        """Add selection comboboxes and download button."""
        self.action_frame = ttk.Frame(master=self.window)
        
        # Format selection
        ttk.Label(self.action_frame, text="Format:").pack(side='left', padx=5)
        self.format_combo = ttk.Combobox(
            master=self.action_frame,
            textvariable=self.format_var,
            width=10,
            state="readonly"
        )
        self.format_combo.pack(side='left', padx=5)
        self.format_combo.bind("<<ComboboxSelected>>", self.backend.on_format_selected)
        
        # Resolution selection
        ttk.Label(self.action_frame, text="Resolution:").pack(side='left', padx=5)
        self.res_combo = ttk.Combobox(
            master=self.action_frame,
            textvariable=self.res_var,
            width=10, 
            state="readonly"
        )
        self.res_combo.pack(side='left', padx=5)
        self.res_combo.bind("<<ComboboxSelected>>", self.backend.on_resolution_selected)
        
        # Video codec selection
        ttk.Label(self.action_frame, text="Codec:").pack(side='left', padx=5)
        self.vcodec_combo = ttk.Combobox(
            master=self.action_frame,
            textvariable=self.vcodec_var,
            width=20,
            state="readonly"
        )
        self.vcodec_combo.pack(side='left', padx=5)
        self.vcodec_combo.bind("<<ComboboxSelected>>", self.backend.on_codec_selected)
        
        # Download button
        self.download_btn = ttk.Button(
            master=self.action_frame,
            text='Download',
            bootstyle='success',
            command=self.backend.start_download
        )
        self.download_btn.pack(side='left', padx=20)
        
        self.action_frame.pack(pady=10)

    def _loading_indicator(self):
        """Show a loading indicator while fetching video metadata."""
        self.loading_label = ttk.Label(
            master=self.window,
            text="Loading video information...",
            font='Arial 12 italic'
        )
        self.loading_label.pack(pady=10)

    def _clear_loading_indicator(self):
        """Remove the loading indicator."""
        if hasattr(self, 'loading_label'):
            self.loading_label.destroy()

    def _setup_progress(self):
        """Add progress bar and status label."""
        self.progress_frame = ttk.Frame(master=self.window)
        
        self.progress_bar = ttk.Progressbar(
            master=self.progress_frame,
            orient='horizontal',
            mode='determinate',
            length=400,
            bootstyle="success-striped",
        )
        self.progress_bar.pack(pady=10)
        
        self.progress_label = ttk.Label(
            master=self.progress_frame,
            text="Ready",
            font='Arial 10'
        )
        self.progress_label.pack(pady=10)
        
        # Add cancel button
        self.cancel_btn = ttk.Button(
            master=self.progress_frame,
            text='Cancel',
            bootstyle='danger',
            command=self.backend.stop_download
        )
        self.cancel_btn.pack(pady=5)

        # Don't show progress frame until download starts
        self.progress_frame.pack_forget()

    def display_thumbnail_and_title(self, response, title=None):
        """Get thumbnail response and display thumbnail on the UI."""
        try:
            # Open the image using Pillow from the in-memory bytes
            image = Image.open(BytesIO(response.content))
        except IOError as e:
            print(f"Error opening image with Pillow: {e}. The thumbnail might not exist for this video/resolution.")
        thumbnail = ImageTk.PhotoImage(image)
        self.thumbnail_label = ttk.Label(self.window, image=thumbnail)
        self.thumbnail_label.image = thumbnail  # Keep a reference to avoid garbage collection
        self.thumbnail_label.pack(pady=10)

        if title:
            self.title_label = ttk.Label(master=self.window, text=title, font='Arial 12 bold')
            self.title_label.pack(pady=5)

    def clear_thumbnail_and_title(self):
        """Clear thumbnail and title display."""
        self.thumbnail_label.config(image='')  # Clear the image
        self.thumbnail_label.image = None  # Remove reference to the image
        self.thumbnail_label.pack_forget()  # Hide the label
        self.title_label.pack_forget()  # Hide the title label

    def show_error(self, title, message):
        """Display an error dialog."""
        messagebox.showerror(title, message)

    def show_info(self, title, message):
        """Display an info dialog."""
        messagebox.showinfo(title, message)

    def ask_yes_no(self, title, message):
        """Display a yes/no dialog."""
        return messagebox.askyesno(title, message)

    def ask_directory(self, initial_dir=None):
        """Show directory selection dialog."""
        return filedialog.askdirectory(initialdir=initial_dir, title="Select Download Location")

    def show_progress(self):
        """Display the progress frame."""
        self.progress_frame.pack(pady=10)

    def hide_progress(self):
        """Hide the progress frame."""
        self.progress_frame.pack_forget()

    def run(self):
        """Start the application."""
        self.window.mainloop()

    def author_info(self):
        """Display author information."""
        footer_frame = ttk.Frame(self.window)
        footer_frame.pack(side="bottom", fill="x") 

        ttk.Label(
            master=footer_frame,
            text="YouTube Downloader\n"
                 "Created by: smartcode.dev\n"
                 "GitHub: https://github.com/smartcode444/yt-downloader\n",
            font='Arial 7'
        ).pack(side="left")

if __name__ == "__main__":
    app = Window()
    app.setup()
    app.run()
