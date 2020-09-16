import pygame
from pygame.sprite import Sprite
from random import randint

POWER_UPS = ['big_bullet', 'fast_bullets']


class PowerUp(Sprite):
    """Class representing the power drops of the game."""

    def __init__(self, ai_game):
        """Initialize a power drop item."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/power_up.bmp')

        # Create a power drop rect at (random, 0) and then set
        random_x = randint(15, ai_game.settings.screen_width - 15)
        self.rect = pygame.Rect(
            random_x, 0, self.settings.power_up_width, self.settings.power_up_height)

        # Store the power up's position as a decimal value.
        # Store the power up's position as a decimal value.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """
        Move the bullet up the screen. It is called
        automatically by 'pygame.sprite.Group().update()'
        """
        # Update the decimal position of the bullet.
        self.y += self.settings.power_up_speed
        # Update the rect position.
        self.rect.y = self.y
        self.rect.x = self.x

    def draw_power_up(self):
        """Draw the power up to the screen."""
        self.screen.blit(self.image, self.rect)

    @staticmethod
    def get_random_power():
        """Return random power up."""
        return POWER_UPS[randint(0, len(POWER_UPS) - 1)]
        # END get_random_power
