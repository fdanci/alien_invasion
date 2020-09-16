import pygame
import pygame.mixer as sound_player


class SoundPlayer():
    """Model that handles game sound effects."""

    def __init__(self, ai_game):
        """Initialize 'SoundPlayer' instance."""
        self.ai_game = ai_game
        sound_player.init()

    def play_background_music(self):
        """Start playing background music."""
        pygame.mixer.music.load('sounds/background_1.mp3')
        pygame.mixer.music.play()

    def pause_background_music(self):
        """Pause playing background music."""
        pygame.mixer.music.pause()

    def stop_background_music(self):
        """Stop playing background music."""
        pygame.mixer.music.stop()

    def shoot_bullet(self):
        """Play bullet sound."""
        effect = pygame.mixer.Sound('sounds/bullet.wav')
        effect.play()

    def ship_hit(self):
        """Play sound when ship is hit."""
        effect = pygame.mixer.Sound('sounds/hit.wav')
        effect.play()


