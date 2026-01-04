import json
from pathlib import Path
import os
from logic.song import Song

CACHE_PATH = Path("data/map_cache.json")
CONFIG_PATH = Path("data/config.json")


def load_cache():
    if not os.path.exists(CACHE_PATH):
        return {
            "cached_maps_folder": "",
            "songs": []
        }
    
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(folder, songs):
    for i, song in enumerate(songs):
        print(i, type(song))
        
    data = {
        "cached_maps_folder": folder,
        "songs": [song.to_dict() for song in songs]
    }
    
    os.makedirs("data", exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def check_cache(new_folder):
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    cached_folder = data.get("cached", "")
    if new_folder != cached_folder:
        print("Different Folder, need to load")
        return False
    
    print("Same Folder")
    return True
    

