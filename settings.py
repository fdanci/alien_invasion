class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize game's settings."""
        # Screen settings.
        self.bg_color = (255, 255, 255)
        self.screen_width = 1200
        self.screen_height = 800
        self.ship_speed = 1.5
        self.text_size = 15
        self.text_font = "Comic Sans MS"
        self.windowed = True

    def reset_screen_size(self):
        """Reset screen size to initial values."""
        self.screen_width = 1200
        self.screen_height = 800