from power_up import PowerUp


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.bg_color = (234, 229, 229)
        self.screen_width = 1270
        self.screen_height = 800
        self.windowed = True

        # Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 50
        self.bullet_height = 30
        self.bullets_allowed = 3

        # Power Ups
        self.power_up_speed = 1.5
        self.power_up_width = 32
        self.power_up_height = 32
        self.power_up_chance = 3_300
        self.power_up_active = False
        self.power_up = None
        self.powered_up_bullets = 0
        self.settings_before_power_up = {}

        # Enemy bullet settings
        self.enemy_bullet_color = (60, 60, 60)
        self.enemy_bullet_width = 5
        self.enemy_bullet_height = 20
        self.enemy_bullet_speed = 1.0

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Alien settings
        self.enemy_bullet_probability = 600
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
        self.enemy_bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        if not self.power_up_active:
            self.bullet_speed *= self.speedup_scale
        # END increase_speed

    def enter_power_mode(self, ai_game):
        """Change bullet settings depending on what power has been picked up."""
        if not self.power_up_active:
            self.power_up = PowerUp.get_random_power()

            self.backup_settings()
            if self.power_up == 'fast_bullets':
                self.bullet_speed *= 4.0
                self.powered_up_bullets = 12
            elif self.power_up == 'big_bullet':
                self.powered_up_bullets = 5
                self.bullet_width *= 5
                self.bullet_height *= 5
                ai_game.SHOOT_NOT_MULTIPLE_ENEMIES = False
                pass

            self.power_up_active = True
        # END enter_power_mode

    def backup_settings(self):
        """Save previous settings before power up will be activated."""
        self.settings_before_power_up['bullet_speed'] = self.bullet_speed
        self.settings_before_power_up['bullet_width'] = self.bullet_width
        self.settings_before_power_up['bullet_height'] = self.bullet_height
        # END backup_settings

    def exit_power_mode(self, ai_game):
        """Restore settings to values before last power up."""
        self.bullet_speed = self.settings_before_power_up['bullet_speed']
        self.bullet_width = self.settings_before_power_up['bullet_width']
        self.bullet_height = self.settings_before_power_up['bullet_height']
        self.power_up = None
        ai_game.SHOOT_NOT_MULTIPLE_ENEMIES = True
        # END exit_power_mode
