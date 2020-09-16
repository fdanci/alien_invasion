class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.bg_color = (255, 255, 255)
        self.screen_width = 1270
        self.screen_height = 800
        self.windowed = True

        # Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 20
        self.bullet_height = 15
        self.bullets_allowed = 3

        # Enemy bullet settings
        self.enemy_bullet_color = (60, 60, 60)
        self.enemy_bullet_width = 5
        self.enemy_bullet_height = 20
        self.enemy_bullet_speed = 1.0

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Alien settings
        self.fleet_drop_speed = 15
        self.fleet_direction = 1  # Fleet_direction of 1 represents right; -1 represents left
        self.alien_speed = 1.0

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # Scoring
        self.score_scale = 1.5  # How quickly the alien point values increase
        self.alien_points = 50
        # END __init__

    def reset_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 2.0
        self.enemy_bullet_speed = 1.0
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_points = 50
        # END reset_settings

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.enemy_bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # END increase_speed
