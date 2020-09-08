import sys
import pygame
from random import randint as rand


from game_stats import GameStats

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from button import Button
from scoreboard import Scoreboard
from save_data import SaveData
from saving_management import SavingManagement
from enemy_models import ENEMY_MODELS


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        # pygame.mouse.set_visible(False)

        self.settings = Settings()
        # Set screen size.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,
             self.settings.screen_height))

        pygame.display.set_caption("Daniela Invadeaza Lumea")

        # Create an instance to store game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Initiaslize the ship object.
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.enemy_model = None
        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

        self.init_saving_mechanism()

    def init_saving_mechanism(self):
        """Initialize saving and loading settings components."""
        # Initialize highscore, aliens killed saving management.
        self.save_data = SaveData(self)
        self.saving_management = SavingManagement(self.save_data)

        # Try loading saved data if any.
        saved_data = self.saving_management.get_saved_data()
        if saved_data:
            self.stats.load_saved_data(saved_data)
            self.sb.prep_high_score()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.

        self.enemy_model = pygame.image.load(
            ENEMY_MODELS[rand(0, len(ENEMY_MODELS) - 1)])  # Set random enemy model

        alien = Alien(self, self.enemy_model)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            # Create row of aliens.
            for alien_number in range(number_aliens_x):
                # Create an alien and place it in the row.
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self, self.enemy_model)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self._update_bullets()
                self._update_aliens()
                self._update_screen()
            else:
                # Show the mouse cursor.
                self.screen.fill(self.settings.bg_color)
                pygame.mouse.set_visible(True)
                # Draw the play button if the game is inactive.
                if not self.stats.game_active:
                    self.play_button.draw_button()
                # Make the most recently drawn screen visible.
                pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            # Ship movement events.
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True

            # Game info
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()

            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # elif event.key == pygame.K_UP:
        #     self.ship.moving_up = True
        # elif event.key == pygame.K_DOWN:
        #     self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        # elif event.key == pygame.K_UP:
        #     self.ship.moving_up = False
        # elif event.key == pygame.K_DOWN:
        #     self.ship.moving_down = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        self.ship.update()
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        # Will automatically call update on each bullet.
        self.bullets.update()
        # Get rid of bullets that are out of the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        # The sprite.groupcollide() function compares the rects of each element
        # in one group with the rects of each element in another group. In this case,
        # it compares each bullet’s rect with each alien’s rect and returns a dictionary
        # containing the bullets and aliens that have collided. Each key in the
        # dictionary will be a bullet, and the corresponding value will be the alien that
        # was hit.
        # To make a high-powered
        # bullet that can travel to the top of the screen, destroying every alien in its
        # path, you could set the first Boolean argument to False and keep the second
        # Boolean argument set to True.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.stats.aliens_killed += 1
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.start_new_level()

    def start_new_level(self):
        """Starts new level, increments level, resets ship"""
        # Destroy existing bullets and create new fleet.
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level.
        self.stats.level += 1
        self.sb.prep_level()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break


def main():
    """Make a game instance, run the game, save data before exit."""
    try:
        ai = AlienInvasion()
        ai.run_game()
    except Exception:
        pass
    finally:
        ai.saving_management.save()


if __name__ == '__main__':
    main()
