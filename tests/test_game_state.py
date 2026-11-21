"""Tests for game state — scoring, lives, level progression."""

from retro_asteroids import game_state
from retro_asteroids.game_state import GameState, load_high_score

def test_initial_state():
    gs = GameState()
    assert gs.score == 0
    assert gs.lives == 3
    assert gs.level == 1


def test_add_score():
    gs = GameState()
    gs.add_score(20)
    assert gs.score == 20
    gs.add_score(50)
    assert gs.score == 70


def test_high_score_tracks():
    gs = GameState()
    gs.add_score(500)
    assert gs.high_score == 500
    gs.add_score(300)
    assert gs.high_score == 800


def test_lose_life():
    gs = GameState()
    assert gs.lives == 3
    assert gs.lose_life() is False
    assert gs.lives == 2
    assert gs.lose_life() is False
    assert gs.lives == 1
    assert gs.lose_life() is True  # game over
    assert gs.lives == 0


def test_extra_life_at_10000():
    gs = GameState()
    assert gs.lives == 3
    gs.add_score(10000)
    assert gs.lives == 4


def test_extra_life_every_10000():
    gs = GameState()
    gs.add_score(10000)
    assert gs.lives == 4
    gs.add_score(10000)
    assert gs.lives == 5  # second extra life at 20000


def test_level_progression():
    gs = GameState()
    assert gs.level == 1
    assert gs.asteroid_count() == 4
    gs.next_level()
    assert gs.level == 2
    assert gs.asteroid_count() == 5
    gs.next_level()
    assert gs.level == 3
    assert gs.asteroid_count() == 6


def test_high_score_persistence():
    gs = GameState()
    gs.add_score(5000)
    gs.save_high_score()

    # Load again
    gs2 = GameState()
    assert gs2.high_score == 5000


def test_add_score_reports_extra_life():
    gs = GameState()
    assert gs.add_score(9990) is False
    assert gs.add_score(20) is True
    assert gs.add_score(20) is False


def test_load_high_score_handles_corrupt_file():
    with open(game_state.HIGH_SCORE_PATH, "w") as f:
        f.write("not json")
    assert load_high_score() == 0
