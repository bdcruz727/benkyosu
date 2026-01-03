import os

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
    # {title, title_unicode, artist, artist_unicode, creator, audio_filename, audio_file, bg_filename, bg_file, beatmap_id, beatmap_set_id}
    # beatmap_id is the ID of the diff, beatmap_set_id is the ID of the entire Map

    with open(file_path, 'r', encoding='utf-8') as f:

        for line in f:
            try:
                if line.startswith("AudioFilename:"):
                    metadata['audio_filename'] = line.strip().split(":", 1)[1].strip()
                
                elif line.startswith("Title:"):
                    metadata['title'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("TitleUnicode:"):
                    metadata['title_unicode'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("Artist:"):
                    metadata['artist'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("ArtistUnicode:"):
                    metadata['artist_unicode'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("Creator:"):
                    metadata['creator'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("BeatmapID:"):
                    metadata['beatmap_id'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("BeatmapSetID:"):
                    metadata['beatmap_set_id'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("//Background"):
                    next_line = next(f, None)
                    if next_line:
                        if not next_line.startswith("//"):
                            print(f"Next Line: {next_line}")
                            metadata['bg_filename'] = next_line.strip().split(",", 3)[2].strip()
                        else:
                            metadata['bg_filename'] = "NONE"
            except:
                print(f"Error Loading Map: {file_path}")
                continue

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