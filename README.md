# YouTube Downloader

A simple Python GUI application for downloading YouTube videos and audio using `yt_dlp`.

## Features

- Fetch video metadata (title, available video-only formats).
- Display video thumbnail and title.
- Choose output format: `mp4`, `mkv`, or `mp3`.
- Select resolution and video codec for `mp4`/`mkv` downloads.
- Download audio only (MP3) with automatic conversion via `ffmpeg`.
- Shows download progress with percentage, speed, ETA, and transferred size.
- Configurable save directory stored in `config.json`.
- Background download thread to keep the UI responsive.

## Project Structure

```
yt_downloader/
├── backend.py       # Business logic connecting UI and VideoHandler
├── handler.py       # Wraps yt_dlp for metadata and downloading
├── save_path.py     # Utilities for storing/retrieving save directory
├── window.py        # Tkinter/ttkbootstrap GUI implementation
├── config.json      # Stores the last used download directory
└── README.md        # This file
```

## Requirements

- Python 3.8+
- `yt_dlp` for video handling
- `ttkbootstrap` for styled Tkinter widgets
- `Pillow` for thumbnail image display
- `ffmpeg` executable located in project root or PATH

## Installation

1. Clone or download the repository.
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```sh
   pip install yt-dlp ttkbootstrap Pillow
   ```
4. Ensure `ffmpeg.exe` is available in the project directory or ffmpeg path provided in config.json.

## Usage

1. Run the application:
   ```sh
   python ui.py
   ```
2. Enter a YouTube URL and click **Check Video**.
3. Choose desired format, resolution, and codec (if applicable).
4. Click **Download** and select a save directory if prompted.
5. During downloading a **Cancel** button will appear – click it to abort the transfer.  
   The download will stop and a partial file may remain; delete or restart as needed.
6. Monitor progress in the UI; open folder after completion if prompted.

## Configuration

The application saves the chosen download directory in `config.json`. By default the file is created with an empty string as the path:
```json
{"save_path": ""}
```
You can edit or delete this file to reset the path.

## License

This project is provided as-is under the MIT License.

## Acknowledgments

- Built with `yt_dlp` for downloading and metadata.
- GUI styled using `ttkbootstrap`.

Enjoy downloading your favorite videos!

## Packaging & Installation

- Install from source (editable):

```sh
python -m pip install -e .
```

- Or install dependencies first and run directly:

```sh
python -m pip install -r requirements.txt
python -m main.window
```

## Usage Examples

- GUI: Run `python -m main.window`, enter a YouTube URL, click **Check Video**, choose format/resolution/codec, then **Download**.

- CLI (headless, basic): you can create a small wrapper that calls the handler directly if you need automation. Example (pseudo):

```py
from main.handler import VideoHandler
vh = VideoHandler()
vh.fetch_metadata('https://youtu.be/VIDEO_ID')
vh.start_download(format_id, 'C:/Downloads', 'mp4', lambda d: print(d))
```

## Troubleshooting

- FFmpeg not found: If you see an FFmpeg error, ensure `ffmpeg`/`ffprobe` are installed and the `ffmpeg_path` in `main/config.json` points to the directory containing the executables (not the executable itself). Example config:

```json
{
   "save_path": "C:/Users/you/Downloads",
   "ffmpeg_path": "C:/ffmpeg/bin"
}
```

- HTTP 416 (Requested range not satisfiable) after cancelling and restarting:
   - This usually means a partial `.part` file remains from the interrupted download and the server rejected the resume range. Fixes:
      - Delete the `.part` file for the video in your download folder and retry.
      - Or enable the "Force restart" behavior (disable resume) so a fresh download starts. The code supports `continuedl` in `yt_dlp` options — set to `False` to avoid range requests.

- Rate limiting (HTTP 429): Try again later or use a proxy/VPN. You can add a proxy in `yt_dlp` options via the `proxy` setting.

- Geo-restricted content: Enable `geo_bypass` in `yt_dlp` options or use a VPN/proxy to access the content.

- Permissions issues when opening folders:
   - On Windows, the app uses `os.startfile` to open folders; ensure your user has access rights.
   - On macOS/Linux the repository provides a small test script `scripts/test_platform.py` that attempts to open a file using the platform default opener — run it to verify your system opener is available.

## Screenshots

Add screenshots to `images/screenshots/` and reference them in the README using relative paths. Example markdown image tag:

```md
![Main window](images/screenshots/main-window.png)
```

Tips: capture screenshots on Windows (`Win+Shift+S`), macOS (`Cmd+Shift+4`), or Linux (varies by distro). Commit the images to the repository before publishing.

## Testing cross-platform behavior

1. Run the included platform opener test to verify opening files/folders on your platform:

```sh
python scripts/test_platform.py
```

2. For GUI file dialogs we use Tkinter's `filedialog.askdirectory()` — it maps to the native file picker on Windows/macOS/Linux. If you see issues:
    - Ensure a display server is available on Linux (X11/Wayland) when running the GUI.
    - On macOS you may need to allow accessibility or automation permissions for Python when opening file dialogs.

## Contributing

Contributions welcome — open issues or PRs on the GitHub repo linked at the top of this README.
