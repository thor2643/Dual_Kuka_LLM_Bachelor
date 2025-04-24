import os
import json

def load_use_sim():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config.json'))
    print(f"[DEBUG] Reading config from: {config_path}")

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"[DEBUG] Raw config contents: {config}")
        result = config.get("use_sim", "False")
        print(f"[DEBUG] Parsed use_sim: {result}")
        return result
    except Exception as e:
        print(f"[ERROR] Failed to read config file at {config_path}: {e}")
        return False

if __name__ == "__main__":
    use_sim = load_use_sim()
    print(f"Final Result: use_sim = {use_sim}")
