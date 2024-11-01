# audio/player.py

import pygame
import os
import sys

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.sound = None
        self.is_playing = False
        self.volume = 1.0
        self.fade_duration = 1000  # milliseconds
        self.load_sound()

    def resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and PyInstaller."""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def load_sound(self):
        audio_file = self.resource_path(
            os.path.join('assets', 'audio', 'rain.wav')
        )
        if os.path.exists(audio_file):
            self.sound = pygame.mixer.Sound(audio_file)
            self.sound.set_volume(self.volume)
            self.play_sound()
        else:
            print(f"Audio file {audio_file} not found.")

    def play_sound(self):
        if self.sound:
            self.channel = self.sound.play(loops=-1, fade_ms=self.fade_duration)
            self.is_playing = True
            self.channel.set_volume(self.volume)

    def pause(self):
        if self.is_playing and self.channel:
            # Fade out and stop the channel
            self.channel.fadeout(self.fade_duration)
            self.is_playing = False

    def resume(self):
        if not self.is_playing:
            # Start playing the sound again with fade-in
            self.play_sound()

    def set_volume(self, volume):
        self.volume = volume
        if self.sound:
            # Set volume on the Sound object (affects new channels)
            self.sound.set_volume(self.volume)
        if self.channel:
            # Set volume on the currently playing channel
            self.channel.set_volume(self.volume)
