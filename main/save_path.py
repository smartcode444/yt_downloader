import json
import os 


# Utility functions for managing save path configuration
def get_save_path():
    with open('config.json', 'r') as f:
        try:
            config = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            config = {}

    save_path = config.get('save_path', '')
    if save_path and os.path.isdir(save_path):
        return save_path
    else: 
        return None

def store_save_path(save_path):
    config = {}
    with open('config.json', 'w') as f:
        config['save_path'] = save_path
        json.dump(config, f)



