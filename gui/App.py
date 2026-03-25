import customtkinter as ctk
from logic.song_loader import load_all_maps
from logic.config import load_config, save_config_folder
from logic.cache import load_cache, save_cache, check_cache
from tkinter import filedialog
from logic.song import Song
from gui.player_ui import PlayerBar
import os
import threading
import time

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("benkyosu!")
        self.geometry("500x650")
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

        if self.selected_folder:
            self.after(100, self.autoload_maps)
        
        self.folder_label = ctk.CTkLabel(
            self,
            font=("Poppins", 32),
          
            text_color="#1e1e1e",
            text= f"Folder: {self.selected_folder}",
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

        self.song_listbox = ctk.CTkScrollableFrame(self, height=150)
        self.song_listbox.pack(fill="x", padx=20, pady=(10, 0))

        # In App.__init__:
        self.player_bar = PlayerBar(self)
        self.player_bar.pack(fill="x", side="bottom")

        

    # self.beatmaps = internal database
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select osu! Songs Folder")

        if not folder:
            return
        
        folder = os.path.normpath(folder)
        
        self.selected_folder = folder
        self.folder_label.configure(text=f"Selected folder:\n{folder}")
        
        self.config["songs_folder"] = folder
        save_config_folder(self.config)

        self.select_button.configure(state="disabled", text="Loading Beatmaps (May take awhile...)")

        thread = threading.Thread(target=self.load_maps_thread, args=(folder,), daemon=True)
        thread.start()

    def load_maps_thread(self, folder):
        cache = load_cache()
        cached_folder = os.path.normpath(cache.get("cached_maps_folder", ""))
        cached_songs = cache.get("songs", [])

        # Valid Cache
        if folder == cached_folder and cached_songs:
            print("Using Cached Maps")
            self.beatmaps = [Song.from_dict(d) for d in cached_songs]
            print(f"Loaded {len(self.beatmaps)} maps from cache")

        # Invalid Cache   
        else:
            print("Scanning songs folder...")
            self.beatmaps = load_all_maps(folder)
            save_cache(folder, self.beatmaps)
            print(f"Scanned and cached {len(self.beatmaps)} maps")

        self.after(0, self.on_maps_loaded)
 
        
    def autoload_maps(self):
        self.select_button.configure(state="disabled", text="Loading Beatmaps...")
        thread = threading.Thread(target=self.load_maps_thread, args=(self.selected_folder,), daemon=True)
        thread.start()

    def on_maps_loaded(self):
        self.select_button.configure(state="normal", text="Select osu! Songs Folder")
        self.populate_song_list()

    def populate_song_list(self):
        # Clear existing entries
        for widget in self.song_listbox.winfo_children():
            widget.destroy()

        for song in self.beatmaps:
            audio_path = song.audio_path()
            label = ctk.CTkButton(
                self.song_listbox,
                text=f"{song.artist} — {song.title}",
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray85", "gray25"),
                command=lambda s=song: self.player_bar.load_song(s, playlist=self.beatmaps),  # s=song captures correctly
            )
            label.pack(fill="x", pady=1)