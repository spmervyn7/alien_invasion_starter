"""
Program Name: ship.py
Author: Mervyn S. Philip
Purpose: This code creates the player's spaceship. It keeps track of the
         ship's picture, where it is on the screen, how it moves left and 
         right, how it shoots bullets, and whether it crashes into the alien ships.
Starter Code: Adapted from the in-class Alien Invasion tutorial
             (base repo: https://github.com/RedBeard41/alien_Invasion_starter.git)
             It sets up the ship's image, tells the game where to find pictures and
             sounds, and controls how the ship moves and fires.
Date: 2026-07-31
"""

import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal


class Ship:
    """Represents the player's ship: its image, movement, and firing."""

    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal') -> None:
        """Load the ship image, center it on screen, and link it to
        its Arsenal of bullets.

        Args:
            game: the ship knows how big the screen is and what the game rules are
            arsenal: the ship knows how to shoot bullets.
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.ship_w, self.settings.ship_h)
            )

        self.rect = self.image.get_rect()
        self._center_ship()
        self.moving_right = False
        self.moving_left = False

        self.arsenal = arsenal

    def _center_ship(self) -> None:
        """This moves the ship back to the bottom middle of the screen.

        This happens when the game first starts or when the ship gets hit, so the
        player always restarts from the same safe spot.
        """
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)

    def update(self) -> None:
        """Update the ship's position and its arsenal of bullets for
        the current frame."""
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self) -> None:
        """Move the ship left or right based on current input flags,
        clamped to the screen boundaries."""
        temp_speed = self.settings.ship_speed
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed

        self.rect.x = self.x

    def draw(self) -> None:
        """Draw the ship's current image at its current position."""
        self.screen.blit(self.image, self.rect)

    def fire(self) -> bool:
        """Attempt to fire a bullet from the ship's arsenal.

        Returns:
            True if a bullet was successfully fired, False if the
            arsenal was already at its bullet limit.
        """
        return self.arsenal.fire_bullet()

    def check_collisions(self, other_group) -> bool:
        """Check whether the ship has collided with any sprite in
        other_group (the alien fleet).

        If a collision is found, the ship is re-centered to indicate
        a life was lost.

        Args:
            other_group: A pygame sprite Group to test collisions
                against (typically the alien fleet).

        Returns:
            True if a collision occurred, False otherwise.
        """
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False