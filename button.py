"""
Program Name: button.py
Author: Mervyn S. Philip
Purpose: This code creates the "Play" button used to start and 
         restart the game. It is styled with the game's special
         colors and font.
Starter Code: Adapted from the in-class Alien Invasion tutorial
             (base repo: https://github.com/RedBeard41/alien_Invasion_starter.git)
             It creates a button with a text label that can be clicked to start or
             restart the game.
Date: 2026-07-31
"""

import pygame.font
from settings import Settings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Button:
    """A clickable on-screen button with a text label."""

    def __init__(self, game: 'AlienInvasion', msg) -> None:
        """Build a centered button with the given message.

        Args:
            game: The running AlienInvasion instance (for screen and
                settings access).
            msg: The text to display on the button.
        """
        self.game = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings
        self.font = pygame.font.Font(self.settings.font_style, self.settings.button_font_size)
        self.rect = pygame.Rect(0, 0, self.settings.button_w, self.settings.button_h)
        self.rect.center = self.boundaries.center
        self._prep_msg(msg)

    def _prep_msg(self, msg) -> None:
        """Render the button's text into an image and center it
        within the button's rect.

        Args:
            msg: The text to render onto the button.
        """
        self.msg_image = self.font.render(msg, True, self.settings.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self) -> None:
        """Draw the button's background and text label to the screen."""
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_clicked(self, mouse_pos):
        """Check whether a given mouse position is inside the button.

        Args:
            mouse_pos: An (x, y) tuple of the mouse click position.

        Returns:
            True if mouse_pos is within the button's rect, False
            otherwise.
        """
        return self.rect.collidepoint(mouse_pos)