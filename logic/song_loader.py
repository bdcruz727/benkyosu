import os
from pathlib import Path
from logic.song import Song
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis
from mutagen import MutagenError

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
                    metadata['id'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("BeatmapSetID:"):
                    metadata['set_id'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("Title:"):
                    metadata['title'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("Artist:"):
                    metadata['artist'] = line.strip().split(":", 1)[1].strip()

                elif line.startswith("Creator:"):
                    metadata['creator'] = line.strip().split(":", 1)[1].strip()
                
                elif line.startswith("Version"):
                    metadata['version'] = line.strip().split(":", 1)[1].strip()
                
                elif line.startswith("AudioFilename:"):
                    metadata['audio'] = line.strip().split(":", 1)[1].strip()
                

            except:
                print(f"Error Loading Map: {file_path}")
                return None

    file_folder = str(Path(file_path).parent)
    metadata['folder'] = file_folder

    if "audio" not in metadata:
        return None

    audio_file_path = os.path.join(file_folder, metadata['audio'])
    audio_length = get_audio_duration(audio_file_path)
    if audio_length == -1:
        print(f"Error getting audio length for map: {file_path}")
        return

    metadata['length'] = str(audio_length)
    return metadata

### Loads all beatmaps in the song folder ###
### Internal call to parse_osu_file to get metadata of each map, stores in list of maps ###
def load_all_maps(songs_folder):
    maps = []
    seen_keys = set()

    for folder in os.listdir(songs_folder):
        folder_path = os.path.join(songs_folder, folder)
        if not os.path.isdir(folder_path):
            continue

        for file in os.listdir(folder_path):
            if not file.endswith(".osu"):
                continue

            osu_path = os.path.join(folder_path, file)
            info = parse_osu_file(osu_path)
            # print(info)

            if not info:
                print("not info")
                continue

            if "artist" not in info or "title" not in info or "audio" not in info:
                print("chungus")
                continue

            song_key = (folder_path, info["audio"])
            if song_key in seen_keys:
                continue
            seen_keys.add(song_key)
            try:
                song = Song(
                    id = info["id"],
                    set_id = info["set_id"],
                    title = info["title"],
                    artist = info["artist"],
                    creator = info["creator"],
                    version = info["version"],
                    audio = info["audio"],
                    folder = folder_path,
                    length = info["length"]
                )

                maps.append(song)
            except:
                print(f"failed to append key: {song_key}")
                continue

    print(f"Scanned {len(maps)} unique songs")
    return maps
        
"""
def get_audio_duration(file_path):
    if file_path.lower().endswith(".mp3"):
        audio = MP3(file_path)
    elif file_path.lower().endswith(".wav"):
        audio = WAVE(file_path)
    elif file_path.lower().endswith(".ogg"):
        audio = OggVorbis(file_path)
    
    if audio and audio.info:
        return audio.info.length
    else:
        return -1
"""

def get_audio_duration(file_path):
    if not os.path.exists(file_path):
        return -1

    try:
        ext = file_path.lower()

        if ext.endswith(".mp3"):
            audio = MP3(file_path)
        elif ext.endswith(".wav"):
            audio = WAVE(file_path)
        elif ext.endswith(".ogg"):
            audio = OggVorbis(file_path)
        elif ext.endswith(".flac"):
            from mutagen.flac import FLAC
            audio = FLAC(file_path)
        else:
            return -1

        return audio.info.length if audio.info else -1

    except MutagenError:
        return -1
    except Exception:
        return -1