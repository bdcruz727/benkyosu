import json
from pathlib import Path
import os

CACHE_PATH = Path("data/map_cache.json")

def load_cache():
    if not CACHE_PATH.exists():
        return None
    
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for song in data.get("songs", []):
        if not os.path.exists(song["folder"]):
            return None
    
    return data["songs"]


def save_cache(songs):
    CACHE_PATH.parent.mkdir(exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump({"songs" : songs}, f, indent=4)