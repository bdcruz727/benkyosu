import os

def parse_osu_file(file_path):
    metadata = {}
    # {title, title_unicode, artist, artist_unicode, creator, audio_filename, audio_file, bg_filename, bg_file, beatmap_id, beatmap_set_id}
    # beatmap_id is the ID of the diff, beatmap_set_id is the ID of the entire Map

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:

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
                    metadata['bg_filename'] = next_line.strip().split(",", 3)[2].strip()

            
    
    return metadata