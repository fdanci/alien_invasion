class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize game's settings."""
        # Screen settings.
        self.bg_color = (255, 255, 255)
        self.screen_width = 1200
        self.screen_height = 800
        self.ship_speed = 1.5