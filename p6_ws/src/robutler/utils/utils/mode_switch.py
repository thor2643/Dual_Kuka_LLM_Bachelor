import json

CONFIG_PATH = 'src/robutler/config.json'

def load_use_sim():
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        return config.get("use_sim", False)
    except Exception as e:
        print(f"[ERROR] Failed to read config at {CONFIG_PATH}: {e}")
        return False

def set_use_sim(mode: bool):
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}

    config['use_sim'] = mode 

    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Failed to write config at {CONFIG_PATH}: {e}")

    return config['use_sim']
