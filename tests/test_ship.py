"""Tests for ship mechanics — rotation, thrust, screen wrapping, invulnerability."""

from retro_asteroids.ship import Ship, SCREEN_W, SCREEN_H, RESPAWN_INVULNERABILITY


def test_ship_initial_position():
    s = Ship()
    assert s.x == SCREEN_W / 2
    assert s.y == SCREEN_H / 2
    assert s.lives == 3


def test_ship_custom_position():
    s = Ship(x=100, y=200)
    assert s.x == 100
    assert s.y == 200


def test_ship_rotation():
    s = Ship()
    assert s.angle == 0.0
    s.rotate(1)
    assert s.angle == 5.0
    s.rotate(-1)
    assert s.angle == 0.0


def test_ship_rotation_wraps():
    s = Ship()
    s.angle = 358
    s.rotate(1)
    assert s.angle == 3.0  # wraps around


def test_ship_thrust_changes_velocity():
    s = Ship()
    s.angle = 90  # pointing right
    s.thrust()
    assert s.vel_x > 0
    assert abs(s.vel_y) < 0.0001


def test_ship_friction():
    s = Ship()
    s.vel_x = 5.0
    s.vel_y = 0.0
    s.update()
    assert s.vel_x == 4.95


def test_ship_max_velocity():
    s = Ship()
    s.vel_x = 10.0
    s.vel_y = 0.0
    s.update()
    speed = (s.vel_x ** 2 + s.vel_y ** 2) ** 0.5
    assert speed <= 6.0


def test_ship_screen_wrap_right():
    s = Ship(x=SCREEN_W + 10, y=50)
    s.vel_x = 0
    s.vel_y = 0
    s.update()
    assert s.x == 10


def test_ship_screen_wrap_left():
    s = Ship(x=-10, y=50)
    s.update()
    assert s.x == SCREEN_W - 10


def test_ship_screen_wrap_bottom():
    s = Ship(x=100, y=SCREEN_H + 20)
    s.vel_y = 0
    s.update()
    assert s.y == 20


def test_ship_invulnerability_on_respawn():
    s = Ship()
    assert not s.is_invulnerable()
    s.respawn()
    assert s.is_invulnerable()
    assert s.invulnerable == RESPAWN_INVULNERABILITY


def test_invulnerability_expires():
    s = Ship()
    s.respawn()
    s.invulnerable = 1
    s.update()
    assert s.invulnerable == 0
    assert not s.is_invulnerable()


def test_ship_vertices_count():
    s = Ship()
    verts = s.get_vertices()
    assert len(verts) == 3


def test_ship_vertices_rotated():
    s = Ship()
    s.angle = 90
    verts = s.get_vertices()
    # vertices should have been rotated
    assert verts != [(0, -20), (-14, 12), (14, 12)]  # not default


def test_ship_starts_center():
    s = Ship()
    assert s.x == SCREEN_W / 2
    assert s.y == SCREEN_H / 2
