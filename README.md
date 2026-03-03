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
4. Ensure `ffmpeg.exe` is available in the project directory or system PATH.

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

The application stores settings in `config.json` located in the `main/` directory. By default it contains:
```json
{
  "save_path": "",
  "ffmpeg_path": "ffmpeg.exe"
}
```

- **save_path**: Directory where downloaded videos are saved. Leave empty to prompt on each download.
- **ffmpeg_path**: Full path to the `ffmpeg` binary or directory containing `ffmpeg.exe` and `ffprobe.exe`. Examples:
  - Windows: `"C:/ffmpeg/bin"` (folder containing executables) or `"ffmpeg.exe"` (if in PATH)
  - macOS/Linux: `"/usr/local/bin"` (folder) or `"ffmpeg"` (if in PATH)

You can edit this file directly or delete it to reset settings to defaults.

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
python main/window.py
```

## Usage Examples

- GUI: Run `python main/window.py`, enter a YouTube URL, click **Check Video**, choose format/resolution/codec, then **Download**.

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

```md
![screenshot1](https://github.com/user-attachments/assets/08134d7b-eac2-4129-bd6f-6cb88b7b2ba0)
![screenshot2](https://github.com/user-attachments/assets/738255c4-93a6-469f-838a-707348ed949d)
```

## Running the unit tests

Run the full suite from the project root with pytest so Python can find the package:

```sh
python -m pytest tests
```

Avoid invoking individual test files directly with `python` as that bypasses package resolution and leads to `ModuleNotFoundError: No module named 'main'`. Using `-m pytest` ensures the root directory is on `PYTHONPATH`

## Contributing

Contributions welcome — open issues or PRs on the GitHub repo linked at the top of this README.
