"""
Program Name: alien_fleet.py
Author: Mervyn S. Philip
Purpose: This code creates and controls a group of alien characters.
         Instead of a normal grid, it arranges the aliens in a row using
         triangles pointing up and down. It also moves the whole group together,
         makes them turn and drop down when they hit the edge of the screen, and 
         checks if they crash into anything or get destroyed.
Starter Code: Adapted from the in-class Alien Invasion tutorial
             (base repo: https://github.com/RedBeard41/alien_Invasion_starter.git)
             It sets up the alien fleet, tells the game where to find pictures and
             sounds, and controls how the aliens move and interact with the ship 
             and bullets.
Date: 2026-07-31
"""

import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class AlienFleet:
    """Creates and manages the group of aliens as a single fleet."""

    def __init__(self, game='AlienInvasion') -> None:
        """This prepares an empty group of aliens and sets up the starting pattern made of alternating triangles.
        Args:
            game: The active game session (used to check the game settings).
        """
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        self.create_Fleet()

    def create_Fleet(self) -> None:
        """This removes any current aliens and creates a fresh group of triangle-shaped clusters that
        fit nicely on the screen.

        It clears the old ones first so you can safely restart a level without accidentally
        duplicating the aliens.
        """
        self.fleet.empty()

        alien_w = self.settings.alien_w
        screen_w = self.settings.screen_w
        alien_h = self.settings.alien_h
        screen_h = self.settings.screen_h

        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)
        x_offset, y_offset = self.calculate_offsets(alien_w, screen_w, alien_h, fleet_w, fleet_h)

        self._create_triangle_cluster_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _create_triangle_cluster_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset) -> None:
        """This arranges the aliens in a zigzag pattern of triangles instead
        of a regular box grid. The triangles alternate pointing up and down
        across the screen and are centered as a group.

        Args:
        alien_w: Width of one alien in pixels.
        alien_h: Height of one alien in pixels.
        fleet_w: Total width space available on the screen.
        fleet_h: Total height space available for the aliens.
        x_offset: Extra left-or-right shift applied to every alien's position.
        y_offset: Extra up-or-down shift applied to every alien's position.
        """
        triangle_rows = min(fleet_h, 5)
        triangle_cols = 2 * (triangle_rows - 1) + 1

        num_clusters = max(1, fleet_w // triangle_cols)
        used_cols = num_clusters * triangle_cols
        leading_gap = (fleet_w - used_cols) // 2

        for cluster_index in range(num_clusters):
            cluster_start_col = leading_gap + cluster_index * triangle_cols
            points_down = (cluster_index % 2 == 0)

            for row in range(triangle_rows):
                if points_down:
                    # Upright triangle: apex at top, widens going down.
                    aliens_in_row = 2 * row + 1
                else:
                    # Inverted triangle: apex at bottom, narrows going down.
                    aliens_in_row = 2 * (triangle_rows - 1 - row) + 1

                row_start_col = cluster_start_col + (triangle_cols - aliens_in_row) // 2

                for i in range(aliens_in_row):
                    col = row_start_col + i
                    current_x = alien_w * col + x_offset
                    current_y = alien_h * row + y_offset
                    self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_w, screen_w, alien_h, fleet_w, fleet_h) -> tuple[int, int]:
        """Calculate the pixel offsets used to position the fleet.

        Returns:
            A tuple of (x_offset, y_offset) in pixels.
        """
        x_offset = 0
        y_offset = 0
        return x_offset, y_offset

    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h) -> tuple[int, int]:
        """Calculate how many alien columns and rows fit on screen.

        Returns:
            A tuple of (fleet_w, fleet_h) giving the max number of
            columns and rows the wedge formation may use.
        """
        fleet_w = (screen_w / alien_w)
        fleet_h = ((screen_h / 2) // alien_h)

        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2

        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2

        return int(fleet_w), int(fleet_h)

    def _create_alien(self, current_x: int, current_y: int) -> None:
        """Create a single Alien at the given position and add it to
        the fleet group."""
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        """Check whether any alien has reached a screen edge, and if
        so, drop the whole fleet and reverse its direction."""
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break

    def _drop_alien_fleet(self) -> None:
        """Move every alien in the fleet down by fleet_drop_speed."""
        for alien in self.fleet:
            alien.y += self.fleet_drop_speed

    def update_fleet(self) -> None:
        """Check for edge collisions and update every alien's
        position for the current frame."""
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self) -> None:
        """Draw every alien currently in the fleet."""
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group) -> dict[any, list]:
        """Check for collisions between the fleet and another sprite
        group (e.g. the ship's bullets), destroying both sprites on
        collision.

        Args:
            other_group: A pygame sprite Group to test collisions
                against.

        Returns:
            A dict mapping each destroyed alien to the list of
            sprites it collided with.
        """
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)

    def check_fleet_bottom(self):
        """Check whether any alien has reached the bottom of the
        screen.

        Returns:
            True if any alien's bottom edge is at or past the
            screen's bottom edge, False otherwise.
        """
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False

    def check_destroyed_status(self) -> bool:
        """Check whether the entire fleet has been destroyed.

        Returns:
            True if no aliens remain in the fleet, False otherwise.
        """
        return len(self.fleet) == 0