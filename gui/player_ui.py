# gui/player_ui.py
import customtkinter as ctk
from logic.player import AudioPlayer
from logic.song import Song
import math

class PlayerBar(ctk.CTkFrame):
    def __init__(self, master, on_tracklist=None, on_info=None, **kwargs):
        super().__init__(
            master,
            fg_color="#1a1a2e",
            corner_radius=0,
            **kwargs
        )

        self.player = AudioPlayer()
        self._seeking = False
        self.on_tracklist = on_tracklist
        self.on_info = on_info

        # ── Top row: "Now Playing" tag + song title ──────────────────────
        top_row = ctk.CTkFrame(self, fg_color="transparent")
        top_row.pack(fill="x", padx=16, pady=(10, 2))

        self.now_playing_tag = ctk.CTkLabel(
            top_row,
            text="Now Playing ♪",
            font=("Poppins", 10, "bold"),
            text_color="#a78bfa",
        )
        self.now_playing_tag.pack(side="left")

        self.title_label = ctk.CTkLabel(
            top_row,
            text="No track selected",
            font=("Poppins", 13, "bold"),
            text_color="#e2e8f0",
            anchor="w",
        )
        self.title_label.pack(side="left", padx=(10, 0))

        # ── Progress bar + timestamps ─────────────────────────────────────
        progress_row = ctk.CTkFrame(self, fg_color="transparent")
        progress_row.pack(fill="x", padx=16, pady=(2, 0))

        self.elapsed_label = ctk.CTkLabel(
            progress_row, text="0:00",
            font=("Poppins", 10), text_color="#94a3b8", width=36
        )
        self.elapsed_label.pack(side="left")

        self.seek_slider = ctk.CTkSlider(
            progress_row,
            from_=0, to=100,
            height=14,
            button_color="#a78bfa",
            button_hover_color="#c4b5fd",
            progress_color="#a78bfa",
            fg_color="#2d2d4e",
            command=self._on_seek_drag,
        )
        self.seek_slider.set(0)
        self.seek_slider.pack(side="left", fill="x", expand=True, padx=8)

        self.total_label = ctk.CTkLabel(
            progress_row, text="0:00",
            font=("Poppins", 10), text_color="#94a3b8", width=36
        )
        self.total_label.pack(side="left")

        # ── Controls row ──────────────────────────────────────────────────
        controls_row = ctk.CTkFrame(self, fg_color="transparent")
        controls_row.pack(pady=(4, 10))

        btn_style = dict(
            width=36, height=36,
            corner_radius=18,
            fg_color="transparent",
            hover_color="#2d2d4e",
            text_color="#e2e8f0",
            font=("Segoe UI Symbol", 15),
        )

        self.prev_btn = ctk.CTkButton(
            controls_row, text="⏮", **btn_style,
            command=self._prev
        )
        self.prev_btn.grid(row=0, column=0, padx=4)

        self.play_btn = ctk.CTkButton(
            controls_row, text="▶",
            width=44, height=44,
            corner_radius=22,
            fg_color="#a78bfa",
            hover_color="#c4b5fd",
            text_color="#1a1a2e",
            font=("Segoe UI Symbol", 17, "bold"),
            command=self._toggle_play
        )
        self.play_btn.grid(row=0, column=1, padx=6)

        self.pause_btn = ctk.CTkButton(
            controls_row, text="⏸", **btn_style,
            command=self._toggle_play
        )
        self.pause_btn.grid(row=0, column=2, padx=4)

        self.stop_btn = ctk.CTkButton(
            controls_row, text="⏹", **btn_style,
            command=self._stop
        )
        self.stop_btn.grid(row=0, column=3, padx=4)

        self.next_btn = ctk.CTkButton(
            controls_row, text="⏭", **btn_style,
            command=self._next
        )
        self.next_btn.grid(row=0, column=4, padx=4)

        # Separator
        ctk.CTkLabel(
            controls_row, text="", width=12, fg_color="transparent"
        ).grid(row=0, column=5)

        self.info_btn = ctk.CTkButton(
            controls_row, text="ℹ", **btn_style,
            command=lambda: self.on_info(self._current_song) if self.on_info and self._current_song else None
        )
        self.info_btn.grid(row=0, column=6, padx=4)

        self.tracklist_btn = ctk.CTkButton(
            controls_row, text="≡", **btn_style,
            command=lambda: self.on_tracklist() if self.on_tracklist else None
        )
        self.tracklist_btn.grid(row=0, column=7, padx=4)

        # Volume (right side)
        vol_frame = ctk.CTkFrame(self, fg_color="transparent")
        vol_frame.pack(side="right", padx=16, pady=(0, 8))

        ctk.CTkLabel(
            vol_frame, text="🔊",
            font=("Segoe UI Symbol", 12), text_color="#94a3b8"
        ).pack(side="left", padx=(0, 4))

        self.vol_slider = ctk.CTkSlider(
            vol_frame, from_=0, to=0.5, width=80,
            button_color="#a78bfa",
            button_hover_color="#c4b5fd",
            progress_color="#a78bfa",
            fg_color="#2d2d4e",
            command=self._set_volume
        )
        self.vol_slider.set(0.5)          # start at slider midpoint
        self._set_volume(0.5)  
        self.vol_slider.pack(side="left")

        # State
        self._current_song: Song | None = None
        self._playlist: list[Song] = []
        self._playlist_index: int = -1

        # Wire callbacks
        self.player.on_progress(self._on_progress)
        self.player.on_end(self._on_track_end)

    # ── Public API ────────────────────────────────────────────────────────

    def load_song(self, song: Song, playlist: list[Song] = None):
        """Play a song. Optionally pass the full playlist for prev/next."""
        if playlist:
            self._playlist = playlist
            self._playlist_index = playlist.index(song) if song in playlist else 0
        self._play_song(song)

    # ── Internal playback ─────────────────────────────────────────────────

    def _play_song(self, song: Song):
        self._current_song = song
        self.player.load_song(song.audio_path())
        self.player.set_duration(song.length or 0.0)
        self.player.play()

        self.title_label.configure(text=f"{song.artist}  —  {song.title}")
        self.play_btn.configure(text="▶", fg_color="#a78bfa", text_color="#1a1a2e")

        total = self.player.duration
        self.total_label.configure(text=self._fmt(total))
        self.seek_slider.configure(to=max(total, 1))
        self.seek_slider.set(0)

    def _toggle_play(self):
        if self.player.is_playing:
            self.player.pause()
            self.play_btn.configure(text="▶")
        else:
            self.player.resume()
            self.play_btn.configure(text="▶")

    def _stop(self):
        self.player.stop()
        self.play_btn.configure(text="▶")
        self.seek_slider.set(0)
        self.elapsed_label.configure(text="0:00")

    def _prev(self):
        if self._playlist and self._playlist_index > 0:
            self._playlist_index -= 1
            self._play_song(self._playlist[self._playlist_index])

    def _next(self):
        if self._playlist and self._playlist_index < len(self._playlist) - 1:
            self._playlist_index += 1
            self._play_song(self._playlist[self._playlist_index])

    def _on_seek_drag(self, value):
        self._seeking = True
        self.elapsed_label.configure(text=self._fmt(float(value)))
        self.after(200, self._commit_seek, float(value))

    def _commit_seek(self, value):
        self._seeking = False
        self.player.seek(value)

    def _on_progress(self, current: float, total: float):
        if not self._seeking:
            self.after(0, self._update_ui, current, total)

    def _update_ui(self, current: float, total: float):
        self.elapsed_label.configure(text=self._fmt(current))
        if total > 0:
            self.seek_slider.set(current)

    def _on_track_end(self):
        self.after(0, self._next) if self._playlist else self.after(0, self._stop)

    def _set_volume(self, value: float):
        """Logarithmic curve: slider 0→1 maps to volume 0→0.3"""
        max_volume = 0.2  # tweak this to taste
        if value <= 0:
            vol = 0.0
        else:
            # log curve feels natural for volume
            vol = max_volume * (math.log(1 + value * 9) / math.log(10))
        self.player.set_volume(vol)

    @staticmethod
    def _fmt(seconds: float) -> str:
        s = int(seconds)
        return f"{s // 60}:{s % 60:02d}"