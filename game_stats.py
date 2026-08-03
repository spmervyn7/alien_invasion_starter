"""
Program Name: game_stats.py
Author: Mervyn S. Philip
Purpose: This code keeps track of the game numbers, like your current
         score, top score, level, and remaining lives. It also saves
         the high score to a file on your computer so it stays saved 
         even after you close the game.
Starter Code: Adapted from the in-class Alien Invasion tutorial
             (base repo: https://github.com/RedBeard41/alien_Invasion_starter.git)
             It sets up the game stats, tells the game where to find pictures and
             sounds, and controls how the game tracks scores and levels.
Date: 2026-07-31
"""

from pathlib import Path
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class GameStats():
    """Tracks score, level, and ships-remaining for the current game,
    and persists the all-time high score to disk."""

    def __init__(self, game: 'AlienInvasion') -> None:
        """Load any previously saved high score and reset stats for
        a new game.

        Args:
            game: The running AlienInvasion instance (for settings
                access).
        """
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self) -> None:
        """Load the saved high score from the scores JSON file if it
        exists and is valid; otherwise start from zero and create the
        file."""
        self.path = self.settings.scores_file
        if self.path.exists() and self.path.stat().__sizeof__() > 20:
            try:
                contents = self.path.read_text()
                scores = json.loads(contents)
                self.high_score = scores.get('high_score', 0)
            except json.JSONDecodeError:
                self.high_score = 0
                self.save_scores()
        else:
            self.high_score = 0
            self.save_scores()

    def save_scores(self) -> None:
        """Write the current high score to the scores JSON file on
        disk, creating parent folders if needed."""
        scores = {'high_score': self.high_score}
        contents = json.dumps(scores, indent=4)
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(contents)
        except Exception as e:
            print(f'Error saving scores: {e}')

    def reset_stats(self) -> None:
        """Reset ships remaining, score, and level to their starting
        values for a new game."""
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1

    def update(self, collisions) -> None:
        """Update score, max score, and high score after a batch of
        alien collisions.

        Args:
            collisions: This keeps a list of which aliens were
            hit by which bullets or items during the game.
        """
        self._update_score(collisions)
        self._update_max_score()
        self._update_high_score()

    def _update_max_score(self) -> None:
        """Update max_score if the current score is now higher."""
        if self.score > self.max_score:
            self.max_score = self.score

    def _update_high_score(self) -> None:
        """Update and persist the all-time high score if the current
        score is now higher."""
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_scores()

    def _update_score(self, collisions) -> None:
        """Add points for every alien destroyed in this collision
        batch.

        Args:
            collisions: A dict of destroyed aliens mapped to the
                sprites they collided with.
        """
        for alien in collisions.values():
            self.score += self.settings.alien_points

    def update_level(self) -> None:
        """Advance to the next level after a fleet is fully destroyed."""
        self.level += 1
        print(self.level)