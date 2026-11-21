"""Run pygame headless and keep the real high score file untouched."""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest

from retro_asteroids import game_state


@pytest.fixture(autouse=True)
def temp_high_score(tmp_path, monkeypatch):
    monkeypatch.setattr(game_state, "HIGH_SCORE_PATH", str(tmp_path / "highscore.json"))
