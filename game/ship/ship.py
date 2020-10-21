import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Ship model"""

    def __init__(self, ai_game):
        """Initialize 'Ship' instance and set initial position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load ship image and get its rect
        if ai_game.settings.current_player == '1':
            self.image = pygame.image.load('assets\\images\\florin_hero.bmp')
        elif ai_game.settings.current_player == '2':
            self.image = pygame.image.load('assets\\images\\daniela_hero.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flags.
        self.moving_right = False
        self.moving_left = False
        # self.moving_up = False
        # self.moving_down = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value,W not theW rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        # # Update the ship's y value, not the rect.
        # elif self.moving_up and self.rect.top > self.screen_rect.top:
        #     self.y -= self.settings.ship_speed
        # elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
        #     self.y += self.settings.ship_speed

        # Update rect object from self.x and self.y.
        self.rect.x = self.x
        # self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        # self.y = float(self.rect.y)
