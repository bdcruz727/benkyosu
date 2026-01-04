import os

class Song:
    def __init__(self, id, set_id, title, artist, creator, version, audio, folder, length=None):
        self.id = id
        self.set_id = set_id
        self.title = title
        self.artist = artist
        self.creator = creator
        self.version = version
        self.audio = audio
        self.folder = folder
        self.length = length

    def key(self):
        return (self.folder, self.audio)
    
    def audio_path(self):
        return os.path.join(self.folder, self.audio)
    
    def to_dict(self):
        return{
            "id": self.id,
            "set_id": self.set_id,
            "title": self.title,
            "artist": self.artist,
            "creator": self.creator,
            "version": self.version,
            "audio": self.audio,
            "folder": self.folder,
            "length": self.length
        }
    
    @staticmethod
    def from_dict(d):
        return Song(
            id = d["id"],
            set_id = d["set_id"],
            title = d["title"],
            artist = d["artist"],
            creator = d["creator"],
            version = d["version"],
            audio = d["audio"],
            folder = d["folder"],
            length = d["length"]
        )

