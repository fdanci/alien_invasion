"""Application entry point."""
from game.invasion import Game

if __name__ == '__main__':
    ai = Game()
    ai.run_game()
