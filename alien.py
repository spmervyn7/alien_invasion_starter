"""
Program Name: alien.py
Author: Mervyn S. Philip
Purpose: This defines a single enemy alien that is part of the alien group.
         It handles loading the alien picture, moving sideways with the 
         other aliens, checking if it hits the edge of the screen, and 
         drawing itself on the display.
Date: 2026-07-31
"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from alien_fleet import AlienFleet


class Alien(Sprite):
    """A single alien sprite that moves as part of an AlienFleet."""

    def __init__(self, fleet: 'AlienFleet', x: float, y: float) -> None:
        """Load the alien image and place it at the given position.

        Args:
            fleet: The AlienFleet this alien belongs to.
            x: Starting x-coordinate for this alien.
            y: Starting y-coordinate for this alien.
        """
        super().__init__()

        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.alien_w, self.settings.alien_h)
            )

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien horizontally according to the fleet's
        current direction and speed."""
        temp_speed = self.settings.fleet_speed

        self.x += temp_speed * self.fleet.fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self) -> bool:
        """Check whether this alien has reached the left or right
        edge of the screen.

        Returns:
            True if the alien's rect touches or passes either
            screen edge, False otherwise.
        """
        return (self.rect.right >= self.boundaries.right
                or self.rect.left <= self.boundaries.left)

    def draw_alien(self) -> None:
        """Draw this alien's current image at its current position."""
        self.screen.blit(self.image, self.rect)