"""Game state — scoring, lives, level progression, high score persistence."""

import json
import os
from .asteroid import Asteroid

HIGH_SCORE_PATH = os.path.expanduser("~/.retro_asteroids_highscore.json")

ASTEROID_SCORES = {"large": 20, "medium": 50, "small": 100}
UFO_SCORES = {"large": 200, "small": 1000}
EXTRA_LIFE_SCORE = 10000


class GameState:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.high_score = self._load_high_score()
        self._next_extra_life = EXTRA_LIFE_SCORE

    def _load_high_score(self) -> int:
        try:
            with open(HIGH_SCORE_PATH) as f:
                return json.load(f).get("high_score", 0)
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return 0

    def _save_high_score(self):
        try:
            os.makedirs(os.path.dirname(HIGH_SCORE_PATH), exist_ok=True)
            with open(HIGH_SCORE_PATH, "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except OSError:
            pass  # non-critical

    def add_score(self, amount: int):
        self.score += amount
        if self.score > self.high_score:
            self.high_score = self.score

        # extra life at every 10000 threshold, and each 10000 after
        if self.score >= self._next_extra_life:
            self.lives += 1
            self._next_extra_life += EXTRA_LIFE_SCORE

    def lose_life(self) -> bool:
        """Return True if game over."""
        self.lives -= 1
        return self.lives <= 0

    def next_level(self):
        self.level += 1

    def asteroid_count(self) -> int:
        """Starting asteroid count grows per level: 4 + (level-1)."""
        return 4 + (self.level - 1)

    def save_high_score(self):
        self._save_high_score()
