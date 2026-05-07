"""Bullets — small circles with velocity, lifetime, and screen wrapping."""

import math
import pygame
from .ship import SCREEN_W, SCREEN_H

BULLET_RADIUS = 2
BULLET_SPEED = 10.0
BULLET_LIFETIME = 60  # frames
MAX_BULLETS = 4


class Bullet:
    def __init__(self, x: float, y: float, angle_degrees: float):
        self.x = x
        self.y = y
        self.radius = BULLET_RADIUS

        rad = math.radians(angle_degrees)
        self.vel_x = math.sin(rad) * BULLET_SPEED
        self.vel_y = -math.cos(rad) * BULLET_SPEED

        self.lifetime = BULLET_LIFETIME
        self.alive = True

    def update(self):
        """Move, decrement lifetime, wrap around screen."""
        self.x += self.vel_x
        self.y += self.vel_y

        self.x %= SCREEN_W
        self.y %= SCREEN_H

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False

    def draw(self, surface: pygame.Surface, color: tuple[int, int, int] = (255, 255, 255)):
        """Draw bullet as small circle (point)."""
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
