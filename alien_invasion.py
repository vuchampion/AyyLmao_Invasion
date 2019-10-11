import sys
from time import sleep

import pygame, random

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from scores import Scores

pygame.init()
pygame.mixer.init()

animate_ship = pygame.USEREVENT + 2

class AlienInvasion:
    # Sounds
    laser = pygame.mixer.Sound("sounds/laser7.ogg")
    death = pygame.mixer.Sound("sounds/explosion.wav")
    bg_music = pygame.mixer.Sound("sounds/alienblues.wav")
    bg_music2 = pygame.mixer.Sound("sounds/alienblues.wav")
    bg_music3 = pygame.mixer.Sound("sounds/alienblues.wav")

    def __init__(self):
        self.settings = Settings()
        self.show_scores = False
        self.play_game = False
        self.bg_music.play(99)
        self.elapsed_time = 0

        #self.screen = pygame.display.set_mode((self.HEIGHT, self.WIDTH))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics, and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.highscores = Scores(self)
        self.scores = []
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.aliens2 = pygame.sprite.Group()
        self.aliens3 = pygame.sprite.Group()

        self._create_fleet()

        # Clock
        self.watch = pygame.time.Clock()
        self.fps = 120

        # Make buttons.
        self.play_button = Button(self, "PLAY", 700, 400)
        self.exit_button = Button(self, "EXIT", 1000, 400)
        self.scores_button = Button(self, "SCORES", 850, 500)
        self.back_button = Button(self, "BACK", 100, 200)



    def messages(self, msg, xcor, ycor):
        self.font = pygame.font.Font('Fonts/SFAlienEncounters-Italic.ttf', 150)
        self.text = self.font.render(msg, True, (245, 66, 114))
        self.textRect = self.text.get_rect()
        self.textRect.center = (xcor, ycor)

    def messages_commando(self, msg, xcor, ycor):
        self.font = pygame.font.Font('Fonts/SFAlienEncountersSolid-Ital.ttf', 50)
        self.text = self.font.render(msg, True, (255, 255, 0))
        self.textRect = self.text.get_rect()
        self.textRect.center = (xcor, ycor)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.watch.tick(self.fps)
            pygame.time.set_timer(animate_ship, 200)
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_exit_button(mouse_pos)
                self._check_scores_button(mouse_pos)
                self._check_back_button(mouse_pos)
            elif event.type == animate_ship:
                pass

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.aliens2.empty()
            self.aliens3.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_exit_button(self, mouse_pos):
        """Exit the game when the player clicks Exit"""
        button_clicked = self.exit_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            sys.exit()

    def read_file(self, hiscores):
        filepath = "Highscores/Highscores.txt"
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                hiscores.append(line.strip())
                line = fp.readline()
        fp.close()

    def write_file(self, msg):
        filepath = "Highscores/Highscores.txt"
        f = open(filepath, 'a')
        f.write(msg)
        f.close()

    def test_write(self, hiscores, msg):
        count = 0
        filepath = "Highscores/Highscores.txt"
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                hiscores.append(line.strip())
                line = fp.readline()
                count += 1
        fp.close()

        filepath = "Highscores/Highscores.txt"
        f = open(filepath, 'a')
        #f.write(msg)
        if count == 10:
            print("COUNT IS 10")

        f.close()

    def _check_scores_button(self, mouse_pos):
        """Show the highscores screen"""
        button_clicked = self.scores_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self.show_scores = True
            self.read_file(self.scores)
            #self.test_write(self.scores, str(self.sb.stats.high_score) + '\n')

    def _check_back_button(self, mouse_pos):
        """Handle the back button"""
        button_clicked = self.back_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self.show_scores = False

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.laser.play()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def tick_func(self):
        if pygame.time.get_ticks() % 1000 > 990:
            self.elapsed_time += 1
        return self.elapsed_time

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        collisions2 = pygame.sprite.groupcollide(
                self.bullets, self.aliens2, True, True)
        collisions3 = pygame.sprite.groupcollide(
                self.bullets, self.aliens3, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if collisions2:
            for aliens2 in collisions2.values():
                self.stats.score += self.settings.alien2_points * len(aliens2)
            self.sb.prep_score()
            self.sb.check_high_score()
        if collisions3:
            for aliens3 in collisions3.values():
                self.stats.score += self.settings.alien3_points * len(aliens3)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens and not self.aliens2 and not self.aliens3:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
          then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()
        self.aliens2.update()
        self.aliens3.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            self.death.play()
        if pygame.sprite.spritecollideany(self.ship, self.aliens2):
            self._ship_hit()
            self.death.play()
        if pygame.sprite.spritecollideany(self.ship, self.aliens3):
            self._ship_hit()
            self.death.play()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
        for alien in self.aliens2.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
        for alien in self.aliens3.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.aliens2.empty()
            self.aliens3.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.write_file(str(self.sb.stats.high_score) + '\n')
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        ufo = Alien(self, 'images/ufo.png')
        alien = Alien(self, 'images/alien.png')
        alien2 = Alien(self, 'images/alien3.png')
        alien3 = Alien(self, 'images/alien5.png')
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = 0
        number_rows2 = 2
        number_rows3 = 4
        # Create the full fleet of aliens.
        for row_number in range(number_rows, 2):
            for alien_number in range(number_aliens_x):
                self._create_alien3(alien_number, row_number)
        for row_number in range(number_rows2, 4):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        for row_number in range(number_rows3, 6):
            for alien_number in range(number_aliens_x):
                self._create_alien2(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self, 'images/alien.png')
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_alien2(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self, 'images/alien3.png')
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens2.add(alien)

    def _create_alien3(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self, 'images/alien5.png')
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens3.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
        for alien in self.aliens2.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
        for alien in self.aliens3.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        for alien in self.aliens2.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        for alien in self.aliens3.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _screen_handler(self):
        """Handle the status of the screen"""
        if not self.show_scores and not self.stats.game_active:
            self.scores_button.draw_button()
            self.play_button.draw_button()
            self.exit_button.draw_button()
        if self.show_scores:
            self.cnt = 100
            self.back_button.draw_button()
            self.messages("Highscores", 950, 200)
            self.screen.blit(self.text, self.textRect)

            for x in range(0, 10):
                self.messages_commando(self.scores[x], 950, 250 + self.cnt)
                self.screen.blit(self.text, self.textRect)
                self.cnt += 50

        if not self.stats.game_active and not self.show_scores:
            self.messages("Alien Invasion", 950, 300)
            self.screen.blit(self.text, self.textRect)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.aliens2.draw(self.screen)
        self.aliens3.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.screen.fill((21, 30, 161))

        self._screen_handler()
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
