import pygame
from pygame.sprite import Sprite
from random import randint


class PowerDrop(Sprite):
    """Class representing the power drops of the game."""

    def __init__(self, ai_game, alien):
        """Initialize a power drop item."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/bullet.bmp')

        # Create a power drop rect at (0, 0) and then set
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)

        # self.rect.midtop = ai_game.screen.get_rect().midtop
        self.rect.x = randint(15, ai_game.settings.screen_width - 15)

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x) - 15.0  # Correct bullet x position

    def update(self):
        """
        Move the bullet up the screen. It is called
        automatically by 'pygame.sprite.Group().update()'
        """
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)
