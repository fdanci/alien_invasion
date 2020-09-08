class SaveData:
    """Model for game's statistics to be saved."""

    def __init__(self, ai_game):
        """Initialize 'save data' instance."""
        self.ai_game = ai_game

    def get_data(self):
        """Return data to be saved, neatly formatted as json"""
        data = {
            'high_score': self.ai_game.stats.high_score,
            'aliens_killed': self.ai_game.stats.aliens_killed
        }
        return data
