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
├── path.py          # Utilities for storing/retrieving save and ffmpeg directory
├── window.py        # Tkinter/ttkbootstrap GUI implementation
├── config.json      # Stores the last used download directory, and ffmpeg directory
└── README.md        # This file
```

## Requirements

- Python 3.8+
- `yt_dlp` for video handling
- `ttkbootstrap` for styled Tkinter widgets
- `Pillow` for thumbnail image display
- `ffmpeg` executable located in project root or provide the directory path in config.json.

## Installation

1. Clone or download the repository.
2. Install dependencies:
   ```sh
   pip install yt-dlp ttkbootstrap Pillow
   ```
4. Ensure `ffmpeg.exe` is available in the project directory or or provide the directory path in config.json.

## Usage

1. Run the application:
   ```sh
   python -m main.window
   ```
2. Enter a YouTube URL and click **Check Video**.
3. Choose desired format, resolution, and codec (if applicable).
4. Click **Download** and select a save directory if prompted.
5. During downloading a **Cancel** button will appear – click it to abort the transfer.  
   The download will stop and a partial file may remain; delete or restart as needed.
6. Monitor progress in the UI; open folder after completion if prompted.


## Installing FFmpeg

FFmpeg is required for merging video/audio streams and MP3 conversion. Follow these steps:

### Windows

1. Go to [ffmpeg.org/download](https://ffmpeg.org/download.html).
2. Under **Get packages & executable files**, click the **Windows** icon.
3. On the next page, under **Windows EXE Files**, you'll see precompiled builds from gyan.dev:
   - Click **ffmpeg-git-essentials.7z** (minimal, ~50 MB) or **ffmpeg-git-full.7z** (complete, ~150 MB).
   - Extract the `.7z` file to a folder like `C:\ffmpeg`.
4. Add the extracted folder to your system PATH, or update `config.json`:
   ```json
   {
     "ffmpeg_path": "C:/ffmpeg/bin"
   }
   ```
5. Verify installation by opening PowerShell and running:
   ```powershell
   ffmpeg -version
   ffprobe -version
   ```
   Both should print version info. If not, check your PATH or `config.json` setting.

### macOS

1. Using Homebrew (easiest):
   ```sh
   brew install ffmpeg
   ```
2. Or download from [ffmpeg.org](https://ffmpeg.org/download.html) and build from source.
3. Update `config.json` if needed:
   ```json
   {
     "ffmpeg_path": "/usr/local/bin"
   }
   ```

### Linux

1. Using package manager (Debian/Ubuntu):
   ```sh
   sudo apt update
   sudo apt install ffmpeg
   ```
2. Or use your distribution's package manager (yum, pacman, etc.).
3. Update `config.json` if the binary is in a non-standard location.

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
