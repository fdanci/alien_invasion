import pygame.font

from game.sound.sound_player import SoundPlayer


class GameOver:
    """Game over screen."""

    def __init__(self, ai_game, msg="Game Over", color=(0, 255, 0)):
        """Initialize game over attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 300, 100
        self.background_color = ai_game.settings.bg_color
        self.text_color = (255, 10, 0)
        self.font = pygame.font.SysFont(None, 100, bold=True)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the game over screen."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.background_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def show_game_over(self):
        """Stop game music and play game over sound and display game over message."""
        SoundPlayer.stop_background_music()
        SoundPlayer.game_over()
        self.screen.fill(self.background_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
