class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start game in an inactive state.
        self.game_active = False

        self.score = 0
        self.level = 1
        self.aliens_killed = 0
        # High score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.score = 0
        self.level = 1
        self.ships_left = self.settings.ship_limit

    def load_saved_data(self, saved_data):
        """Load saved data into current game instance."""
        self.high_score = saved_data['high_score']
        self.aliens_killed = saved_data['aliens_killed']
