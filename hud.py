"""
Program Name: hud.py
Author: Mervyn S. Philip
Purpose: This code creates the scoreboard on the screen. It shows
         the player's current score, top score, game level, and how 
         many lives are left (using little ship pictures) in a special font.
Date: 2026-07-31
"""

import pygame.font
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class HUD:
    """Renders score, level, and remaining-lives info to the screen."""

    def __init__(self, game: 'AlienInvasion') -> None:
        """Set up fonts and render the initial HUD text and life icon.

        Args:
            game: The running AlienInvasion instance (for screen,
                settings, and game_stats access).
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.game_stats = game.game_stats
        self.font = pygame.font.Font(self.settings.font_style, self.settings.HUD_font_size)
        self.padding = 20
        self.update_scores()
        self._setup_life_image()
        self.update_level()

    def _setup_life_image(self) -> None:
        """Load and scale the ship image used to represent remaining
        lives in the HUD."""
        self.life_image = pygame.image.load(self.settings.ship_file)
        self.life_image = pygame.transform.scale(self.life_image, (self.settings.ship_w, self.settings.ship_h))
        self.life_rect = self.life_image.get_rect()

    def update_scores(self) -> None:
        """Re-render the score, max score, and high score text
        images, (e.g. after a collision changes the score)."""
        self._update_score()
        self._update_max_score()
        self._update_high_score()

    def _update_score(self):
        """Render the current score text and position it in the
        top-right corner."""
        score_str = f'Score: {self.game_stats.score:,}'
        self.score_image = self.font.render(score_str, True, self.settings.text_color, None)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.boundaries.right - self.padding
        self.score_rect.top = self.padding

    def _update_max_score(self) -> None:
        """Render the max score text (currently drawn over by score;
        kept for HUD layout reference)."""
        max_score_str = f'Max Score: {self.game_stats.max_score:,}'
        self.max_score_image = self.font.render(max_score_str, True, self.settings.text_color, None)
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.right = self.boundaries.right - self.padding
        self.max_score_rect.top = self.padding

    def _update_high_score(self) -> None:
        """Render the high score text and position it top-center."""
        high_score_str = f'High Score: {self.game_stats.high_score:,}'
        self.high_score_image = self.font.render(high_score_str, True, self.settings.text_color, None)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = (self.boundaries.centerx, self.padding)

    def update_level(self):
        """Render the current level text and position it top-left,
        below the life icons."""
        level_str = f'Level: {self.game_stats.level:,}'
        self.level_image = self.font.render(level_str, True, self.settings.text_color, None)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.padding
        self.level_rect.top = self.life_rect.bottom + self.padding

    def _draw_lives(self):
        """Draw one ship icon per remaining life along the top-left
        of the screen."""
        current_x = self.padding
        current_y = self.padding
        for _ in range(self.game_stats.ships_left):
            self.screen.blit(self.life_image, (current_x, current_y))
            current_x += self.life_rect.width + self.padding

    def draw(self) -> None:
        """Draw the full HUD: high score, max score, score, level,
        and remaining lives."""
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.max_score_image, self.max_score_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self._draw_lives()