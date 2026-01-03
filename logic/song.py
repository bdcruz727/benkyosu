import os

class Song:
    def __init__(self, id, set_id, title, artist, creator, audio, folder, length=None):
        self.id = id
        self.set_id = set_id
        self.title = title
        self.artist = artist
        self.creator = creator
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
            "audio": self.audio,
            "folder": self.folder,
            "length": self.length
        }
