import json
import os

DEFAULT_CONFIG = {"save_path": "", "ffmpeg_path": "ffmpeg.exe"}

# if getattr(sys, 'frozen', False):
#     base_path = os.path.dirname(sys.executable)
# else:
#     base_path = os.path.dirname(os.path.abspath(__file__))

base_path = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(base_path, 'config.json')
print(f"Config path: {CONFIG_PATH}")  # Debug: Print the config path being used

def _load():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_CONFIG.copy()

def _save(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)


def get_save_path():
    config = _load()
    path = config.get("save_path", "")
    if path and os.path.isdir(path):
        return path
    else:
        return None

def store_save_path(save_path):
    config = _load()
    config["save_path"] = save_path
    _save(config)

def get_ffmpeg_path():
    config = _load()
    return config.get('ffmpeg_path', DEFAULT_CONFIG['ffmpeg_path'])

# def store_ffmpeg_path(ffmpeg_path):
#     config = _load()
#     config['ffmpeg_path'] = ffmpeg_path
#     _save(config)

