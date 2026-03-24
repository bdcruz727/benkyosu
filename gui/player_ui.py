import customtkinter as ctk
from logic.player import AudioPlayer

class PlayerBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.player = AudioPlayer()
        self._seeking = False  # prevent slider feedback loop

        # Song title
        self.title_label = ctk.CTkLabel(
            self, text="No track selected",
            font=("Poppins", 13),
            wraplength=300
        )
        self.title_label.pack(pady=(10, 4))

        # Seek slider
        self.seek_slider = ctk.CTkSlider(
            self, from_=0, to=100, command=self._on_seek_drag
        )
        self.seek_slider.set(0)
        self.seek_slider.pack(fill="x", padx=20)

        # Time labels
        time_frame = ctk.CTkFrame(self, fg_color="transparent")
        time_frame.pack(fill="x", padx=20)
        self.elapsed_label = ctk.CTkLabel(time_frame, text="0:00", font=("Poppins", 11))
        self.elapsed_label.pack(side="left")
        self.total_label = ctk.CTkLabel(time_frame, text="0:00", font=("Poppins", 11))
        self.total_label.pack(side="right")

        # Playback controls
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(pady=6)

        self.play_btn = ctk.CTkButton(
            controls, text="Play", width=80,
            corner_radius=20, command=self._toggle_play
        )
        self.play_btn.grid(row=0, column=1, padx=6)

        ctk.CTkButton(
            controls, text="Stop", width=60,
            corner_radius=20, command=self._stop
        ).grid(row=0, column=2, padx=6)

        # Volume
        vol_frame = ctk.CTkFrame(self, fg_color="transparent")
        vol_frame.pack(pady=(0, 10))
        ctk.CTkLabel(vol_frame, text="Vol", font=("Poppins", 11)).pack(side="left", padx=(0, 6))
        self.vol_slider = ctk.CTkSlider(
            vol_frame, from_=0, to=1, width=100,
            command=lambda v: self.player.set_volume(v)
        )
        self.vol_slider.set(0.8)
        self.player.set_volume(0.8)
        self.vol_slider.pack(side="left")

        # Wire up callbacks
        self.player.on_progress(self._on_progress)
        self.player.on_end(self._on_track_end)

    def load_song(self, name: str, audio_path: str):
        """Call this when the user selects a song."""
        self.player.load(audio_path)
        self.player.play()
        self.title_label.configure(text=name)
        self.play_btn.configure(text="Pause")
        total = self.player.duration
        self.total_label.configure(text=self._fmt(total))
        self.seek_slider.configure(to=max(total, 1))

    def _toggle_play(self):
        if self.player.is_playing:
            self.player.pause()
            self.play_btn.configure(text="Play")
        else:
            self.player.resume()
            self.play_btn.configure(text="Pause")

    def _stop(self):
        self.player.stop()
        self.play_btn.configure(text="Play")
        self.seek_slider.set(0)
        self.elapsed_label.configure(text="0:00")

    def _on_seek_drag(self, value):
        """User is dragging the slider — seek on release."""
        self._seeking = True
        self.elapsed_label.configure(text=self._fmt(float(value)))
        # Debounce: seek after dragging settles
        self.after(200, self._commit_seek, float(value))

    def _commit_seek(self, value):
        self._seeking = False
        self.player.seek(value)

    def _on_progress(self, current: float, total: float):
        """Called from monitor thread — must use after() to touch UI."""
        if not self._seeking:
            self.after(0, self._update_ui, current, total)

    def _update_ui(self, current: float, total: float):
        self.elapsed_label.configure(text=self._fmt(current))
        if total > 0:
            self.seek_slider.set(current)

    def _on_track_end(self):
        self.after(0, self._stop)

    @staticmethod
    def _fmt(seconds: float) -> str:
        s = int(seconds)
        return f"{s // 60}:{s % 60:02d}"