import pygame
import pygame.mixer as sound_player


class SoundPlayer:
    """Class that handles game sound effects."""

    @staticmethod
    def play_background_music():
        """Start playing background music."""
        pygame.mixer.music.load('assets/sounds/background_1.mp3')
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()

    @staticmethod
    def pause_background_music():
        """Pause playing background music."""
        pygame.mixer.music.pause()

    @staticmethod
    def stop_background_music():
        """Stop playing background music."""
        pygame.mixer.music.stop()

    @staticmethod
    def shoot_bullet():
        """Play bullet sound."""
        effect = pygame.mixer.Sound('assets/sounds/bullet.wav')
        effect.set_volume(0.7)
        effect.play()

    @staticmethod
    def ship_hit():
        """Play sound when ship is hit by enemy."""
        effect = pygame.mixer.Sound('assets/sounds/ship_hit_by_alien.wav')
        effect.play()

    @staticmethod
    def ship_hit_by_bullet():
        """Play sound when ship hit by enemy bullet."""
        effect = pygame.mixer.Sound('assets/sounds/ship_hit_by_bullet.wav')
        effect.play()

    @staticmethod
    def shoot_enemy_bullet():
        """Play enemy bullet sound."""
        effect = pygame.mixer.Sound('assets/sounds/enemy_bullet.wav')
        effect.set_volume(0.6)
        effect.play()

    @staticmethod
    def enemy_hit_bottom():
        """Play sound when enemy reached the bottom of the screen."""
        effect = pygame.mixer.Sound('assets/sounds/enemy_hit_bottom.wav')
        effect.play()

    @staticmethod
    def power_up():
        """Play power up sound."""
        effect = pygame.mixer.Sound('assets/sounds/power_up.wav')
        effect.set_volume(0.6)
        effect.play()
