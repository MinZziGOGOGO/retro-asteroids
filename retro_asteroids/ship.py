"""Player ship — triangle shape, rotation, thrust, screen wrapping."""

import math
import pygame

# Screen dimensions (imported by main.py)
SCREEN_W = 800
SCREEN_H = 600

# Ship geometry
SHIP_SCALE = 20
SHIP_SHAPE = [
    (0, -SHIP_SCALE),
    (-SHIP_SCALE * 0.7, SHIP_SCALE * 0.6),
    (SHIP_SCALE * 0.7, SHIP_SCALE * 0.6),
]

ROTATION_SPEED = 5  # degrees per frame
THRUST_POWER = 0.1
MAX_VELOCITY = 6.0
FRICTION = 0.99
RESPAWN_INVULNERABILITY = 120  # frames (~2 seconds at 60fps)


class Ship:
    def __init__(self, x: float = None, y: float = None):
        self.x = x if x is not None else SCREEN_W / 2
        self.y = y if y is not None else SCREEN_H / 2
        self.angle = 0.0  # degrees, 0 = pointing up
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.radius = SHIP_SCALE * 0.7
        self.lives = 3
        self.invulnerable = 0  # frames remaining
        self.thrusting = False

    def get_vertices(self) -> list[tuple[float, float]]:
        """Return world-space vertices of the ship triangle."""
        rad = math.radians(self.angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        vertices = []
        for lx, ly in SHIP_SHAPE:
            # rotate
            rx = lx * cos_a - ly * sin_a
            ry = lx * sin_a + ly * cos_a
            vertices.append((self.x + rx, self.y + ry))
        return vertices

    def get_thrust_flame(self) -> list[tuple[float, float]]:
        """Return world-space points for the thrust flame."""
        rad = math.radians(self.angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        tip_y = SHIP_SCALE * 0.6 + SHIP_SCALE * 0.5  # bottom of ship
        left = (SHIP_SCALE * 0.35, tip_y)
        right = (-SHIP_SCALE * 0.35, tip_y)
        bottom = (0, tip_y + SHIP_SCALE * 0.8)

        pts = []
        for lx, ly in [left, bottom, right]:
            rx = lx * cos_a - ly * sin_a
            ry = lx * sin_a + ly * cos_a
            pts.append((self.x + rx, self.y + ry))
        return pts

    def rotate(self, direction: int):
        """Rotate the ship. direction: -1 = left, +1 = right."""
        self.angle += direction * ROTATION_SPEED
        self.angle %= 360

    def thrust(self):
        """Apply thrust in the facing direction."""
        rad = math.radians(self.angle)
        self.vel_x += math.sin(rad) * THRUST_POWER
        self.vel_y -= math.cos(rad) * THRUST_POWER

    def update(self):
        """Update position, apply friction, clamp velocity, handle invulnerability, wrap."""
        # friction
        self.vel_x *= FRICTION
        self.vel_y *= FRICTION

        # clamp velocity
        speed = math.hypot(self.vel_x, self.vel_y)
        if speed > MAX_VELOCITY:
            scale = MAX_VELOCITY / speed
            self.vel_x *= scale
            self.vel_y *= scale

        # position
        self.x += self.vel_x
        self.y += self.vel_y

        # screen wrapping
        self.x %= SCREEN_W
        self.y %= SCREEN_H

        # invulnerability countdown
        if self.invulnerable > 0:
            self.invulnerable -= 1

    def is_invulnerable(self) -> bool:
        return self.invulnerable > 0

    def respawn(self):
        """Reset position to center with invulnerability."""
        self.x = SCREEN_W / 2
        self.y = SCREEN_H / 2
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.angle = 0.0
        self.invulnerable = RESPAWN_INVULNERABILITY

    def draw(self, surface: pygame.Surface, color: tuple[int, int, int] = (255, 255, 255)):
        """Draw the ship. If invulnerable, blink by skipping every other ~8 frames."""
        if self.is_invulnerable() and (self.invulnerable % 16 < 8):
            return  # blink off

        vertices = self.get_vertices()
        pygame.draw.polygon(surface, color, vertices, 1)

        if self.thrusting:
            flame = self.get_thrust_flame()
            pygame.draw.polygon(surface, color, flame, 1)
