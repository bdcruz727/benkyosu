import json
from pathlib import Path

CONFIG_PATH = Path("data/config.json")
MAP_CACHE_PATH = Path("data/map_cache.json")

def load_config():
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    

def save_config(config):
    CONFIG_PATH.parent.mkdir(exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)