import sys
from time import sleep
import pygame
from random import randint as rand

# Settings
from .gui.game_over import GameOver
from .settings.game_stats import GameStats
from .settings.settings import Settings

# GUI
from .gui.button import Button
from .gui.scoreboard import Scoreboard
from .gui.player_button import PlayerButton

# Save & File management
from .save.save_data import SaveData
from .save.progress_saver import ProgressSaver

# Sound
from .sound.sound_player import SoundPlayer

# Models
from .enemy.enemy import Enemy
from .enemy.enemy_models import ENEMY_MODELS_DANIELA
from .enemy.enemy_models import ENEMY_MODELS_FLORIN
from .enemy.bullet import Bullet as enemy_bullet
from .ship.ship import Ship
from .ship.bullet import Bullet as ship_bullet
from .ship.power_up import PowerUp


class Game:
    """Main game file.

    Manage game assets and behavior. Put together everything. Handles the game loop.
    """

    def __init__(self):
        """Initialize the game, and create game resources."""
        self.SHOOT_NOT_MULTIPLE_ENEMIES = True

        pygame.init()

        self.settings = Settings()
        # Set screen size.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,
             self.settings.screen_height))

        pygame.display.set_caption("Invaders")

        # Create an instance to store game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.font = pygame.font.SysFont(None, 48)

        # Initialize saving components.
        self.save_data = SaveData(self)
        self.saving_management = ProgressSaver(self.save_data)
        self.load_saved_data()

        # Initialize the ship object.
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.enemy_model = None
        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")
        self.player1_button = PlayerButton(self, player="1",
                                           neighbour=self.play_button.rect)
        self.player2_button = PlayerButton(self, player="2",
                                           neighbour=self.play_button.rect)
        self.exit_button = Button(self, "Exit",
                                  neighbour_rect_above=self.play_button.rect,
                                  color=(255, 0, 0))

        self.game_over = GameOver(self)

        # Set game's icon.
        game_icon = pygame.image.load('assets/images/game_logo.png')
        pygame.display.set_icon(game_icon)

        # Initialize the sound mixer.
        pygame.mixer.init()

    def load_saved_data(self):
        """Load saved data from the save file and write it to scoreboard."""
        # Try loading saved data if any.
        saved_data = self.saving_management.get_saved_data()
        if saved_data:
            self.stats.load_saved_data(saved_data)
            self.settings.current_player = saved_data['player']
            self.sb.prep_high_score()
        # END load_saved_data

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            self.enemy_bullets.empty()
            self.power_ups.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Cancel Power Up
            self.settings.exit_power_mode(self)
            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.saving_management.save()  # Save data
            self.screen.fill(self.settings.bg_color)

            # Game Over
            self.game_over.show_game_over()
            pygame.display.flip()
            sleep(2.2)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.

        if self.settings.current_player == '1':
            self.enemy_model = pygame.image.load(
                ENEMY_MODELS_DANIELA[rand(
                    0, len(ENEMY_MODELS_DANIELA) - 1)])  # Set random enemy model
        elif self.settings.current_player == '2':
            self.enemy_model = pygame.image.load(
                ENEMY_MODELS_FLORIN[rand(
                    0, len(ENEMY_MODELS_FLORIN) - 1)])  # Set random enemy model

        alien = Enemy(self, self.enemy_model)
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
        alien = Enemy(self, self.enemy_model)
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
                self._update_power_ups()
                self._update_screen()
            else:
                # Show the mouse cursor.
                self.screen.fill(self.settings.bg_color)
                pygame.mouse.set_visible(True)
                # Draw the play button if the game is inactive.
                self.play_button.draw_button()
                self.exit_button.draw_button()
                self.player1_button.draw_button()
                self.player2_button.draw_button()
                self.show_highscore()
                # Make the most recently drawn screen visible.
                pygame.display.flip()

    def show_highscore(self):
        """Draw high score to the menu screen."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "HIGHSCORE - {:,}".format(high_score)
        high_score_image = self.font.render(
            high_score_str, True, (30, 30, 30), self.settings.bg_color)
        # Center the high score at the top of the screen.
        high_score_rect = high_score_image.get_rect()
        high_score_rect.centerx = self.screen.get_rect().centerx
        high_score_rect.top = self.screen.get_rect().top
        high_score_rect.y = high_score_rect.y + 20

        self.screen.blit(high_score_image, high_score_rect)

    def _check_events(self):
        """Respond to key presses and mouse events."""
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.saving_management.save()  # Save data
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_exit_button(mouse_pos)
                self._check_play_button(mouse_pos)
                self._check_player_1_button(mouse_pos)
                self._check_player_2_button(mouse_pos)
            # Ship movement events.
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
        # END _check_events

    def _check_player_1_button(self, mouse_pos):
        """Check if current player switched to player 1.

        This will cause some game settings to change.
        """
        button_clicked = self.player1_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.current_player = '1'
            # Reinitialize the ship object.
            self.ship = Ship(self)

    def _check_player_2_button(self, mouse_pos):
        """Check if current player switched to player 2.

        This will cause some game settings to change.
        """
        button_clicked = self.player2_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.current_player = '2'
            # Reinitialize the ship object.
            self.ship = Ship(self)

    def _check_exit_button(self, mouse_pos):
        """Exit the game when user clicks the exit button."""
        button_clicked = self.exit_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.saving_management.save()  # Save data
            sys.exit()
        # [END _check_exit_button]

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.reset_settings()
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
            self.enemy_bullets.empty()
            self.power_ups.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
            # Start music during gameplay.
            SoundPlayer.play_background_music(self.settings.current_player)
        # END _check_play_button

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
        # END _check_fleet_edges

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        # END _change_fleet_direction

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()
        self._fire_enemy_bullet()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            SoundPlayer.ship_hit()
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()
        # END _update_aliens

    def get_alien_randomly(self):
        """Return a random alien that will shoot a bullet."""
        # Chances for a alien to shoot a bullet this frame.
        if 1 == rand(0, self.settings.enemy_bullet_probability):
            return self.get_random_alien()
        # END shoot_randomly

    def get_random_alien(self):
        """Return a random chosen alien from the existing fleet."""
        random_alien_index = rand(0, len(self.aliens.sprites()) - 1)
        return self.aliens.sprites()[random_alien_index]
        # END get_random_alien

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            SoundPlayer.shoot_bullet()
            new_bullet = ship_bullet(self)
            self.bullets.add(new_bullet)

        # Consume a bulled of powered up ammo.
        if self.settings.power_up_active:
            if self.settings.powered_up_bullets > 0:
                self.settings.powered_up_bullets -= 1
            else:
                self.settings.exit_power_mode(self)
                self.settings.power_up_active = False
        # END _fire_bullet

    def _fire_enemy_bullet(self):
        """Create new enemy bullet and fire it downwards from the current alien position."""
        random_alien = self.get_alien_randomly()

        if random_alien:
            SoundPlayer.shoot_enemy_bullet()
            new_alien_bullet = enemy_bullet(self, random_alien)
            self.enemy_bullets.add(new_alien_bullet)
        # END _fire_alien_bullet

    def _drop_power_up(self):
        """Randomly, drop a power up item on the screen."""
        if not self.settings.power_up_active \
                and 1 == rand(0, self.settings.power_up_chance):
            power_up = PowerUp(self)
            self.power_ups.add(power_up)
        # END _drop_power_up

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_SPACE and self.stats.game_active:
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
            self.saving_management.save()  # Save data
            sys.exit()
        # END _check_keydown_events

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
        """Update images on the screen for current frame, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.update()
        self.ship.blitme()

        # Update bullet positions.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Update enemy bullet positions.
        for bullet in self.enemy_bullets.sprites():
            bullet.draw_bullet()

        # Update power ups positions.
        for power_up in self.power_ups.sprites():
            power_up.draw_power_up()

        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Make the most recently drawn screen visible.
        pygame.display.flip()
        # END _update_screen

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.update_ship_bullets()
        self.update_enemy_bullets()
        # END _update_bullets

    def _update_power_ups(self):
        """Update position of power ups."""
        self._drop_power_up()  # Spawn a power up maybe
        # Update any existing power ups.
        self.power_ups.update()
        # Get rid of power ups that are out of the screen.
        for power_up in self.power_ups.copy():
            if power_up.rect.top > self.screen.get_rect().bottom:
                self.power_ups.remove(power_up)

        self._check_power_up_ship_collision()
        # END update_power_ups

    def _check_power_up_ship_collision(self):
        """If any power up collided with the ship, remove that power up."""
        if not self.settings.power_up_active:
            if pygame.sprite.spritecollide(
                    self.ship, self.power_ups, dokill=True):
                self.power_up_the_ship()
        # END _check_power_up_ship_collision

    def power_up_the_ship(self):
        """Make ship stronger."""
        self.settings.enter_power_mode(self)
        SoundPlayer.power_up()
        # END power_up_the_ship

    def update_enemy_bullets(self):
        """Update the bullets fired by the enemy aliens."""
        self.enemy_bullets.update()
        # Get rid of bullets that are out of the screen.
        for bullet in self.enemy_bullets.copy():
            if bullet.rect.top > self.screen.get_rect().bottom:
                self.enemy_bullets.remove(bullet)

        self._check_enemy_bullet_ship_collision()
        # END update_enemy_bullets

    def _check_enemy_bullet_ship_collision(self):
        """Respond to bullet-ship collision."""
        if pygame.sprite.spritecollideany(self.ship, self.enemy_bullets):
            SoundPlayer.ship_hit_by_bullet()
            self._ship_hit()
        # END _check_enemy_bullet_ship_collision

    def update_ship_bullets(self):
        """Update the bullets fired by the ship."""
        # Update bullet positions. Will automatically call update on each bullet.
        self.bullets.update()
        # Get rid of bullets that are out of the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        # END update_ship_bullets

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, self.SHOOT_NOT_MULTIPLE_ENEMIES, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.stats.aliens_killed += 1
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.start_new_level()
        # END _check_bullet_alien_collisions

    def start_new_level(self):
        """Starts new level, increments level, resets ship."""
        # Destroy existing bullets and create new fleet.
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level.
        self.stats.level += 1
        self.sb.prep_level()
        # END start_new_level

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                SoundPlayer.enemy_hit_bottom()
                self._ship_hit()
                break
        # END _check_aliens_bottom
