# logic/player.py
import pygame
import threading
import time
from logic.song import Song
import math

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self._current_path = None
        self._paused = False
        self._progress_callback = None
        self._end_callback = None
        self._monitor_thread = None
        self._running = False
        self._total_length = 0.0
        self._seek_offset = 0.0

    def load_song(self, path: str):
        """Load a track without playing it."""
        self.stop()
        pygame.mixer.music.load(path)
        self._current_path = path
        self._paused = False

    def set_duration(self, seconds: float):
        self._total_length = float(seconds) if seconds else 0.0

    def play(self):
        self._seek_offset = 0.0
        pygame.mixer.music.play()
        self._paused = False
        self._start_monitor()

    def pause(self):
        if pygame.mixer.music.get_busy() and not self._paused:
            pygame.mixer.music.pause()
            self._paused = True

    def resume(self):
        if self._paused:
            pygame.mixer.music.unpause()
            self._paused = False

    def stop(self):
        self._running = False
        pygame.mixer.music.stop()
        self._paused = False

    def seek(self, seconds: float):
        self._seek_offset = seconds
        pygame.mixer.music.play(start=seconds)
        self._paused = False

    def set_volume(self, volume: float):
        pygame.mixer.music.set_volume(volume)

    @property
    def is_playing(self):
        return pygame.mixer.music.get_busy() and not self._paused

    @property
    def position(self) -> float:
        return self._seek_offset + pygame.mixer.music.get_pos() / 1000.0

    @property
    def duration(self) -> float:
        return self._total_length

    def on_progress(self, callback):
        self._progress_callback = callback

    def on_end(self, callback):
        self._end_callback = callback

    def _start_monitor(self):
        self._running = True
        self._monitor_thread = threading.Thread(target=self._monitor, daemon=True)
        self._monitor_thread.start()

    def _monitor(self):
        while self._running:
            if not self._paused:
                pos = self.position
                if self._progress_callback:
                    self._progress_callback(pos, self._total_length)
                if not pygame.mixer.music.get_busy() and not self._paused:
                    self._running = False
                    if self._end_callback:
                        self._end_callback()
                    break
            time.sleep(0.5)