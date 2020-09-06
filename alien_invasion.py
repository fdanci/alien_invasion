import sys
import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        pygame.mouse.set_visible(False)

        self.settings = Settings()
        # Set screen size.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,
             self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")
        # Initiaslize the ship object.
        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Ship movement events.
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_F11:
            if self.settings.windowed:
                self._go_fullscreen()
                self.settings.windowed = False
            else:
                self._go_windowed()
                self.settings.windowed = True

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self._get_right_label(), (10, 0))

        self.ship.update()
        self.ship.blitme()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _go_fullscreen(self):
        """Changes the window to fullscreen mode."""
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

    def _go_windowed(self):
        """Changes the window to windowed mode."""
        self.settings.reset_screen_size()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,
             self.settings.screen_height))

    def _get_right_label(self):
        """Decides between fullscreen or windowed labels and returns it."""
        if self.settings.windowed:
            return self.get_fullscreen_label()
        else:
            return self.get_windowed_label()

    def get_fullscreen_label(self):
        """Return fullscreen label."""
        font = pygame.font.SysFont(
            self.settings.text_font, self.settings.text_size)
        # apply it to text on a label
        label = font.render(
            "Press F11 for fullscreen...", 1, (123, 123, 20))
        return label

    def get_windowed_label(self):
        """Return windowed label."""
        font = pygame.font.SysFont(
            self.settings.text_font, self.settings.text_size)
        # apply it to text on a label
        label = font.render(
            "Press F11 for windowed...", 1, (123, 123, 20))
        return label


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
