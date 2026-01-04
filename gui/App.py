import customtkinter as ctk
from logic.song_loader import load_all_maps
from logic.config import load_config, save_config_folder
from logic.cache import load_cache, save_cache, check_cache
from tkinter import filedialog
from logic.song import Song
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("benkyosu!")
        self.geometry("500x400")
        self._set_appearance_mode("light")
        self.resizable(False, False)

        self.frame = ctk.CTkFrame(
            master = self,
            width=200,
            height=200
        )

        self.config = load_config()
        self.songs_folder = self.config.get("songs_folder")
    
        if self.songs_folder == "":
            self.selected_folder = None
        else:
            self.selected_folder = self.songs_folder

        #self.beatmaps = load_all_maps(self.selected_folder)
        
        self.folder_label = ctk.CTkLabel(
            self,
            font=("Poppins", 32),
          
            text_color="#1e1e1e",
            text="Folder: " + self.selected_folder,
            wraplength=450,
        )
        self.folder_label.pack(pady=20)

        self.select_button = ctk.CTkButton(
            master=self,
            text="Select osu! Songs Folder",
            corner_radius=32,
            bg_color='transparent',
            border_color="#FFCC70",
            border_width=2,
            command=self.select_folder
        )
        self.select_button.pack(pady=10)

    # self.beatmaps = internal database
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select osu Songs Folder")

        if not folder:
            return
        
        folder = os.path.normpath(folder)
        
        self.selected_folder = folder
        self.folder_label.configure(text=f"Selected folder:\n{folder}")
        
        self.config["songs_folder"] = folder
        save_config_folder(self.config)

        cache = load_cache()
        cached_folder = os.path.normpath(cache.get("cached_maps_folder", ""))
        cached_songs = cache.get("songs", [])

        # Valid Cache
        if folder == cached_folder and cached_songs:
            print("Using Cached Maps")
            self.beatmaps = [Song.from_dict(d) for d in cached_songs]
            print(f"Loaded {len(self.beatmaps)} maps from cache")
            return
        
        # Invalid Cache
        print("Scanning songs folder...")
        self.beatmaps = load_all_maps(folder)
        save_cache(folder, self.beatmaps)
        print(f"Scanned and cached {len(self.beatmaps)} maps")
        