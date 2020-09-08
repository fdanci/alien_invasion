import pygame
import pygame.mixer as sound_player


class SoundPlayer():
    """Model that handles game sound effects."""

    def __init__(self, ai_game):
        """Initialize 'SoundPlayer' instance."""
        self.ai_game = ai_game
        sound_player.init()

    def run_bancground_music(self):
        """Start playing background music."""
        try:
            pygame.mixer.music.load('sounds/background_1.mp3')
            pygame.mixer.music.play()
        except Exception as e:
            print(e)

    def pause_background_music(self):
        """Pause playing background music."""
        try:
            pygame.mixer.music.pause()
        except Exception as e:
            print(e)

    def stop_background_music(self):
        """Stop playing background music."""
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(e)

    def change_track(self):
        """Change current background music."""
        try:
            pygame.mixer.music.load('sounds/background_1.mp3')
        except Exception as e:
            print(e)
