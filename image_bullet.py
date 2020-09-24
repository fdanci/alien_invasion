import pygame
from pygame.sprite import Sprite


class ImageBullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # If big bullet power up active, load bigger bullet image, else default image.
        if ai_game.settings.power_up_active and \
                ai_game.settings.power_up == 'big_bullet':
            self.image = pygame.image.load('assets/images/big_bullet.bmp')
        else:
            self.image = pygame.image.load('assets/images/bullet.bmp')

        # Create a bullet rect at (0, 0) and then set correct position on top of the ship.
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x - 5)  # Correct bullet x position

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
