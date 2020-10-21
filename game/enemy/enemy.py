from pygame.sprite import Sprite


class Enemy(Sprite):
    """Enemy model"""

    def __init__(self, ai_game, enemy_model):
        """Initialize the enemy and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # Load the enemy image and set its rect attribute.
        self.image = enemy_model
        self.rect = self.image.get_rect()
        # Start each new enemy near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the enemy's exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """Move the enemy to the right."""
        self.x += (self.settings.enemy_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if enemy is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
