"""
Program Name: alien_invasion.py
Author: Mervyn S. Philip
Purpose: This is the main controller that runs the Alien Invasion 
         game. It starts up the graphics and sounds, creates all 
         the game items (like the ship, weapons, alien group, score
         screen, and start button), runs the main gameplay loop,
         listens for player button presses, and handles crashes, 
         restarting levels, and game over screens.
Date: 2026-07-31
"""

import pygame, sys, pathlib
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet
from game_stats import GameStats
from time import sleep
from button import Button
from hud import HUD


class AlienInvasion:
    """Top-level class that owns and coordinates every game object
    and runs the main game loop."""

    def __init__(self) -> None:
        """Initialize pygame, load settings and assets, and create
        the ship, alien fleet, HUD, and play button."""
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
            )
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg,
            (self.settings.screen_w, self.settings.screen_h))

        self.game_stats = GameStats(self)
        self.HUD = HUD(self)
        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)

        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)

        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)

        self.play_button = Button(self, 'Play')
        self.game_active = False

    def run_game(self) -> None:
        """Run the main game loop: process events, update game
        objects while active, redraw the screen, and cap the frame
        rate."""
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_collisions(self) -> None:
        """Check all collision types for the current frame: ship vs
        aliens, aliens reaching the bottom of the screen, bullets vs
        aliens, and a fully destroyed fleet."""
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_stats()

        if self.alien_fleet.check_fleet_bottom():
            self._check_game_stats()

        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.game_stats.update(collisions)
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
            self.HUD.update_scores()

        if self.alien_fleet.check_destroyed_status():
            self._reset_level()
            self.settings.increase_difficulty()
            self.game_stats.update_level()
            self.HUD.update_level()

    def _check_game_stats(self) -> None:
        """Handle a lost life: decrement ships remaining and reset
        the level, or end the game if no ships remain."""
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False

    def _reset_level(self) -> None:
        """Clear all bullets and aliens, then rebuild a fresh fleet."""
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_Fleet()

    def restart_game(self):
        """Fully restart the game: reset settings, stats, HUD, and
        level, re-center the ship, and hide the mouse cursor."""
        self.settings.initialize_dynamic_settings()
        self.game_stats.reset_stats()
        self.HUD.update_scores()
        self._reset_level()
        self.ship._center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)

    def _update_screen(self) -> None:
        """Redraw the background, ship, bullets, aliens, and HUD;
        show the play button and mouse cursor when the game is
        inactive."""
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        self.ship.arsenal.draw()
        self.alien_fleet.draw()
        self.HUD.draw()

        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)

        pygame.display.flip()

    def _check_events(self) -> None:
        """Poll and dispatch all pending pygame events (quit,
        keydown, keyup, mouse click)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_stats.save_scores()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        """Start the game if the play button was clicked while the
        game is inactive."""
        mouse_pos = pygame.mouse.get_pos()
        if not self.game_active and self.play_button.check_clicked(mouse_pos):
            self.restart_game()

    def _check_keyup_events(self, event) -> None:
        """Stop ship movement when a movement key is released.

        Args:
            event: The pygame KEYUP event to handle.
        """
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _check_keydown_events(self, event) -> None:
        """Start ship movement, fire a bullet, or quit the game based
        on the key pressed.

        Args:
            event: The pygame KEYDOWN event to handle.
        """
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and self.game_active:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
        elif event.key == pygame.K_q:
            self.running = False
            self.game_stats.save_scores()
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()