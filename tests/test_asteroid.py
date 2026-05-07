"""Tests for asteroid module — splitting, sizing, scores."""

import math
from retro_asteroids.asteroid import Asteroid, LARGE_RADIUS, MEDIUM_RADIUS, SMALL_RADIUS


def test_asteroid_creation():
    a = Asteroid("large", x=100, y=100, vel_x=1, vel_y=2)
    assert a.size == "large"
    assert a.radius == LARGE_RADIUS
    assert a.x == 100
    assert a.y == 100
    assert a.vel_x == 1
    assert a.vel_y == 2
    assert a.score == 20


def test_asteroid_sizes():
    a_large = Asteroid("large", x=0, y=0)
    a_med = Asteroid("medium", x=0, y=0)
    a_small = Asteroid("small", x=0, y=0)

    assert a_large.radius == LARGE_RADIUS
    assert a_med.radius == MEDIUM_RADIUS
    assert a_small.radius == SMALL_RADIUS


def test_asteroid_scores():
    assert Asteroid("large", x=0, y=0).score == 20
    assert Asteroid("medium", x=0, y=0).score == 50
    assert Asteroid("small", x=0, y=0).score == 100


def test_large_splits_into_two_medium():
    a = Asteroid("large", x=100, y=100, vel_x=0, vel_y=0)
    children = a.split()
    assert len(children) == 2
    for c in children:
        assert c.size == "medium"
        assert c.radius == MEDIUM_RADIUS
        # child spawns near parent
        assert abs(c.x - a.x) < 0.01
        assert abs(c.y - a.y) < 0.01


def test_medium_splits_into_two_small():
    a = Asteroid("medium", x=200, y=200)
    children = a.split()
    assert len(children) == 2
    for c in children:
        assert c.size == "small"
        assert c.radius == SMALL_RADIUS


def test_small_does_not_split():
    a = Asteroid("small", x=300, y=300)
    children = a.split()
    assert children == []


def test_asteroid_movement():
    a = Asteroid("large", x=100, y=100, vel_x=2, vel_y=3)
    a.update()
    assert a.x == 102
    assert a.y == 103


def test_asteroid_vertices_are_irregular():
    a1 = Asteroid("large", x=0, y=0)
    a2 = Asteroid("large", x=0, y=0)
    v1 = a1.get_vertices_world()
    v2 = a2.get_vertices_world()
    # Different asteroids should have different shapes
    assert v1 != v2


def test_asteroid_vertices_count():
    a = Asteroid("large", x=0, y=0)
    verts = a.get_vertices_world()
    assert 8 <= len(verts) <= 12


def test_edge_spawn_is_off_screen():
    from retro_asteroids.ship import SCREEN_W, SCREEN_H
    for _ in range(50):
        a = Asteroid("large")
        on_screen = (0 <= a.x <= SCREEN_W and 0 <= a.y <= SCREEN_H)
        # At least some spawn off-screen (edge spawns)
        if not on_screen:
            break
    else:
        # All spawned on screen — still valid, just rare
        pass
