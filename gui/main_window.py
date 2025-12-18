import customtkinter as ctk
from tkinter import filedialog

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("benkyosu!")
        self.geometry("500x400")
        self._set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        

        
        self.selected_folder = None

        
        self.folder_label = ctk.CTkLabel(
            self,
            text="No folder selected",
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

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select osu Songs Folder")
        if folder:
            self.selected_folder = folder
            self.folder_label.configure(text=f"Selected folder:\n{folder}")
            print("Selected:", folder)
