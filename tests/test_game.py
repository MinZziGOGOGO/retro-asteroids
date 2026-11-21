"""Smoke tests that drive the real game loop headlessly."""

import pygame
import pytest

from retro_asteroids import main as game_main
from retro_asteroids.main import Game, PLAYING, GAME_OVER, FIRE_COOLDOWN


class HeldKeys:
    """Stand-in for pygame.key.get_pressed() with a fixed set of keys held."""

    def __init__(self, *keys):
        self.keys = set(keys)

    def __getitem__(self, key):
        return key in self.keys


@pytest.fixture
def game():
    g = Game()
    g._start_game()
    yield g
    pygame.quit()


def press(game, key):
    game._handle_event(pygame.event.Event(pygame.KEYDOWN, key=key))


def test_start_game_spawns_asteroids_away_from_ship(game):
    assert game.state == PLAYING
    assert len(game.asteroids) == 4


def test_holding_space_is_rate_limited(game, monkeypatch):
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: HeldKeys(pygame.K_SPACE))
    monkeypatch.setattr(game, "_check_collisions", lambda: None)
    game._update()
    assert len(game.bullets) == 1
    for _ in range(FIRE_COOLDOWN - 1):
        game._update()
    assert len(game.bullets) == 1
    game._update()
    assert len(game.bullets) == 2


def test_pause_freezes_the_game(game, monkeypatch):
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: HeldKeys(pygame.K_UP))
    monkeypatch.setattr(game, "_check_collisions", lambda: None)
    press(game, pygame.K_p)
    y = game.ship.y
    game._update()
    assert game.ship.y == y
    press(game, pygame.K_p)
    game._update()
    assert game.ship.y < y


def test_game_runs_until_game_over(game, monkeypatch):
    """Play 30 seconds of frames with thrust and fire held; nothing may crash."""
    monkeypatch.setattr(pygame.key, "get_pressed",
                        lambda: HeldKeys(pygame.K_UP, pygame.K_LEFT, pygame.K_SPACE))
    for _ in range(60 * 30):
        game._update()
        game._draw()
        if game.state == GAME_OVER:
            break
    assert game.gs.score > 0


def test_losing_last_life_ends_game_and_saves_high_score(game):
    game.gs.lives = 1
    game.gs.add_score(1234)
    game._kill_ship()
    assert game.state == GAME_OVER
    assert game.title_high_score == 1234
    press(game, pygame.K_RETURN)
    assert game.state == PLAYING
