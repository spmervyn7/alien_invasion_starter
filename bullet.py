"""
Program Name: bullet.py
Author: Mervyn S. Philip
Purpose: This code creates a single laser bullet fired by the ship.
         It loads the picture of the laser, moves it straight up 
         the screen, and draws it so you can see it.
Starter Code: Adapted from the in-class Alien Invasion tutorial
             (base repo: https://github.com/RedBeard41/alien_Invasion_starter.git)
             It sets up the bullet's image, tells the game where to find pictures and
             sounds, and controls how the bullet moves and draws itself.
Date: 2026-07-31
"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Bullet(Sprite):
    """A single laser bullet fired from the player's ship."""

    def __init__(self, game: 'AlienInvasion') -> None:
        """Load the bullet image and spawn it at the ship's current
        top-center position.

        Args:
            game: The running AlienInvasion instance (for screen,
                settings, and ship position access).
        """
        super().__init__()

        self.settings = game.settings
        self.screen = game.screen

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.bullet_w, self.settings.bullet_h)
            )

        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet upward by bullet_speed for this frame."""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self) -> None:
        """Draw the bullet's current image at its current position."""
        self.screen.blit(self.image, self.rect)