class SaveData:
    """
    Model for game's save file. Contains the data written or read from the file.

    Kind of like a serializer.
    """

    def __init__(self, ai_game):
        """Initialize 'save data' instance."""
        self.ai_game = ai_game

    def get_data(self):
        """Return data to be saved, neatly formatted as json"""
        data = {
            'high_score': self.ai_game.stats.high_score,
            'enemies_killed': self.ai_game.stats.enemies_killed,
            'player': self.ai_game.settings.current_player
        }
        return data
