class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize game's settings."""
        # Screen settings
        self.bg_color = (255, 255, 255)
        self.screen_width = 1270
        self.screen_height = 800
        self.windowed = True
        # Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        # Ship settings
        self.ship_speed = 1.5
        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

