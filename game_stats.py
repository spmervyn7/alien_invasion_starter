from pathlib import Path
import json 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats():

    def __init__(self, game: 'AlienInvasion') -> None:
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self) -> None:
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
        scores = {'high_score': self.high_score}
        contents = json.dumps(scores, indent = 4)
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(contents)
        except Exception as e:
            print(f'Error saving scores: {e}')

    def reset_stats(self) -> None:
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1

    def update(self, collisions) -> None:
        self._update_score(collisions)
        self._update_max_score()
        self._update_high_score()

    def _update_max_score(self) -> None:
        if self.score > self.max_score:
            self.max_score = self.score

    def _update_high_score(self) -> None:
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_scores()

    def _update_score(self, collisions) -> None:
        for alien in collisions.values():
            self.score += self.settings.alien_points

    def update_level(self) -> None:
        self.level += 1