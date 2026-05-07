"""Tests for collision detection."""

import math
from retro_asteroids.collision import circles_collide, circle_poly_collide


def test_circles_collide_when_overlapping():
    assert circles_collide(0, 0, 10, 15, 0, 10)  # touching at edge
    assert circles_collide(0, 0, 10, 15, 0, 5)   # 5 < 15


def test_circles_not_collide_when_far():
    assert not circles_collide(0, 0, 5, 100, 100, 5)


def test_circles_collide_exact_touch():
    assert circles_collide(0, 0, 10, 20, 0, 10)  # centers 20 apart, radii 10+10


def test_circles_collide_contained():
    # small circle inside large circle
    assert circles_collide(0, 0, 50, 5, 5, 5)


def test_circle_poly_collide_hit():
    # Circle at origin, small polygon near it
    poly = [(5, 0), (15, 10), (5, 20), (-5, 10)]
    assert circle_poly_collide(0, 0, 10, poly)


def test_circle_poly_collide_no_hit():
    poly = [(50, 50), (70, 50), (70, 70), (50, 70)]
    assert not circle_poly_collide(0, 0, 10, poly)


def test_circle_poly_collide_inside():
    # circle center inside polygon
    poly = [(-50, -50), (50, -50), (50, 50), (-50, 50)]
    assert circle_poly_collide(0, 0, 5, poly)


def test_circle_poly_collide_empty():
    assert not circle_poly_collide(0, 0, 10, [])
    assert not circle_poly_collide(0, 0, 10, [(0, 0)])


def test_circle_poly_collide_edge_touch():
    # circle at (10, 0) radius 5, polygon edge from (5,-10) to (5,10)
    poly = [(5, -10), (5, 10), (10, 10), (10, -10)]
    assert circle_poly_collide(10, 0, 5, poly)
