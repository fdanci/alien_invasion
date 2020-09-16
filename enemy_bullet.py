import pygame
from pygame.sprite import Sprite


class EnemyBullet(Sprite):
    """Class to manage the bullets fired by aliens."""

    def __init__(self, ai_game, alien):
        """Initialize bullet at a random enemy"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.enemy_bullet_color

        self.alien = alien

        self.image = pygame.image.load('images/bullet.bmp')

        # Create a bullet rect at (0, 0) and then set correct position underneath the alien.
        self.rect = pygame.Rect(
            0, 0, self.settings.enemy_bullet_width, self.settings.enemy_bullet_height)
        self.rect.midbottom = alien.rect.midbottom

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)  # Correct bullet x position

    def update(self):
        """
        Move the bullet up the screen. It is called
        automatically by 'pygame.sprite.Group().update()'
        """
        # Update the decimal position of the bullet.
        self.y += self.settings.enemy_bullet_speed
        # Update the rect position.
        self.rect.y = self.y
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
