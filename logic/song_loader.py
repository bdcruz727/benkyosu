import os
from pathlib import Path

### Returns a list of all beatmap folders, more specifically a list of dicts with set_id, folder_path, and name ###
### Does not do any parsing, just scans the songs folder ###
def get_beatmap_set(songs_folder):
    beatmap_sets=[]

    for map in os.listdir(songs_folder):
        full_path = os.path.join(songs_folder, map)

        if os.path.isdir(full_path):
            parts = map.split(" ", 1)
            if parts[0].isdigit():
                beatmap_sets.append({
                    "set_id" : int(parts[0]),
                    "folder_path" : full_path,
                    "name" : map
                })
    
    return beatmap_sets


### Takes a map file path and extracts the metadata ###
def parse_osu_file(file_path):
    print(f"Loading File: {file_path}")
    metadata = {}
    # {beatmap_id, beatmap_set_id, title, artist, creator, audio_filename}
    # beatmap_id is the ID of the diff, beatmap_set_id is the ID of the entire Map

    with open(file_path, 'r', encoding='utf-8') as f:

        for line in f:
            try:

                if line.startswith("BeatmapID:"):
                    metadata['beatmap_id'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("BeatmapSetID:"):
                    metadata['beatmap_set_id'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("Title:"):
                    metadata['title'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("Artist:"):
                    metadata['artist'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("Creator:"):
                    metadata['creator'] = line.strip().split(":", 1)[1].strip()
                
                elif line.startswith("AudioFilename:"):
                    metadata['audio_filename'] = line.strip().split(":", 1)[1].strip()
                

            except:
                print(f"Error Loading Map: {file_path}")
                return

    metadata['folder'] = str(Path(file_path).parent)
    return metadata

### Loads all beatmaps in the song folder ###
### Internal call to parse_osu_file to get metadata of each map, stores in list of maps ###
def load_all_maps(songs_folder):
    maps = []

    for folder in os.listdir(songs_folder):
        folder_path = os.path.join(songs_folder, folder)
        if not os.path.isdir(folder_path):
            continue

        for file in os.listdir(folder_path):
            if file.endswith(".osu"):
                osu_path = os.path.join(folder_path, file)
                info = parse_osu_file(osu_path)

                if "beatmap_id" in info:
                    maps.append(info)
                else:
                    print("ERROR")

    print(f"Length: {len(maps)}")
    return maps