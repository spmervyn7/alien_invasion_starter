"""
Program Name: arsenal.py
Author: Mervyn S. Philip
Purpose: This code manages the bullets shot by the ship. It creates 
         new bullets (up to a set limit), moves them forward, deletes
         them when they go off the screen, and draws them on the 
         display.
Starter Code: Adapted from the in-class Alien Invasion tutorial
             (base repo: https://github.com/RedBeard41/alien_Invasion_starter.git)
             It sets up the arsenal of bullets, tells the game where to find pictures and
             sounds, and controls how the bullets move and draw themselves.
Date: 2026-07-31
"""

import pygame
from bullet import Bullet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Arsenal:
    """Manages the ship's active bullets as a pygame sprite Group."""

    def __init__(self, game: 'AlienInvasion') -> None:
        """Set up an empty group to hold the ship's bullets.

        Args:
            game: The running AlienInvasion instance (for settings
                access).
        """
        self.game = game
        self.settings = game.settings
        self.laser_sound = self.settings.laser_sound
        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self) -> None:
        """Update every bullet's position and remove any that have
        left the top of the screen."""
        self.arsenal.update()
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self) -> None:
        """Remove bullets whose bottom edge has scrolled past the
        top of the screen, so the group doesn't grow unbounded."""
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)

    def draw(self) -> None:
        """Draw every active bullet to the screen."""
        for bullet in self.arsenal:
            bullet.draw_bullet()

    def fire_bullet(self) -> bool:
        """Create and add a new bullet if under the bullet limit.

        Returns:
            True if a new bullet was created, False if the arsenal
            was already at bullet_amount.
        """
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False