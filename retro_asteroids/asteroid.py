"""Asteroids — procedural irregular polygons with splitting behaviour."""

import math
import random
import pygame
from .ship import SCREEN_W, SCREEN_H

# Sizes
LARGE_RADIUS = 50
MEDIUM_RADIUS = 25
SMALL_RADIUS = 12

# How far from the player to avoid spawning
SAFE_SPAWN_DISTANCE = 200


def _random_asteroid_vertices(radius: float) -> list[tuple[float, float]]:
    """Generate irregular polygon vertices around a circle radius."""
    num_verts = random.randint(8, 12)
    vertices = []
    for i in range(num_verts):
        angle = (2 * math.pi * i) / num_verts
        r = radius * random.uniform(0.7, 1.3)
        vertices.append((r * math.cos(angle), r * math.sin(angle)))
    return vertices


class Asteroid:
    """A single asteroid. Size: 'large', 'medium', or 'small'."""

    SIZE_PARAMS = {
        "large": {"radius": LARGE_RADIUS, "score": 20, "next_size": "medium", "split_count": 2},
        "medium": {"radius": MEDIUM_RADIUS, "score": 50, "next_size": "small", "split_count": 2},
        "small": {"radius": SMALL_RADIUS, "score": 100, "next_size": None, "split_count": 0},
    }

    def __init__(self, size: str = "large", x: float = None, y: float = None,
                 vel_x: float = None, vel_y: float = None):
        self.size = size
        params = self.SIZE_PARAMS[size]
        self.radius = params["radius"]
        self.score = params["score"]

        # position — spawn from edge if not given
        if x is not None and y is not None:
            self.x = x
            self.y = y
        else:
            self.x, self.y = self._edge_spawn()

        # velocity
        if vel_x is not None and vel_y is not None:
            self.vel_x = vel_x
            self.vel_y = vel_y
        else:
            speed = random.uniform(0.5, 2.5)
            angle = random.uniform(0, 2 * math.pi)
            self.vel_x = math.cos(angle) * speed
            self.vel_y = math.sin(angle) * speed

        # local-space vertices (rotated by random angle)
        self.vertices_local = _random_asteroid_vertices(self.radius)
        self.rotation = random.uniform(0, 2 * math.pi)
        self.rotation_speed = random.uniform(-0.02, 0.02)

    def _edge_spawn(self):
        """Spawn at a random edge position, avoiding the center area."""
        edge = random.randint(0, 3)
        if edge == 0:  # top
            return random.uniform(0, SCREEN_W), -self.radius
        elif edge == 1:  # right
            return SCREEN_W + self.radius, random.uniform(0, SCREEN_H)
        elif edge == 2:  # bottom
            return random.uniform(0, SCREEN_W), SCREEN_H + self.radius
        else:  # left
            return -self.radius, random.uniform(0, SCREEN_H)

    def get_vertices_world(self) -> list[tuple[float, float]]:
        """Return world-space vertices."""
        cos_r = math.cos(self.rotation)
        sin_r = math.sin(self.rotation)
        verts = []
        for lx, ly in self.vertices_local:
            rx = lx * cos_r - ly * sin_r
            ry = lx * sin_r + ly * cos_r
            verts.append((self.x + rx, self.y + ry))
        return verts

    def update(self):
        """Move and rotate."""
        self.x += self.vel_x
        self.y += self.vel_y
        self.rotation += self.rotation_speed

        # screen wrapping
        self.x %= SCREEN_W
        self.y %= SCREEN_H

    def split(self) -> list["Asteroid"]:
        """Return children if this asteroid is destroyed. Small asteroids produce none."""
        params = self.SIZE_PARAMS[self.size]
        if params["split_count"] == 0:
            return []

        children = []
        for _ in range(params["split_count"]):
            speed = random.uniform(1.0, 3.0)
            angle = random.uniform(0, 2 * math.pi)
            cvx = math.cos(angle) * speed + self.vel_x * 0.3
            cvy = math.sin(angle) * speed + self.vel_y * 0.3
            children.append(
                Asteroid(
                    size=params["next_size"],
                    x=self.x,
                    y=self.y,
                    vel_x=cvx,
                    vel_y=cvy,
                )
            )
        return children

    def draw(self, surface: pygame.Surface, color: tuple[int, int, int] = (255, 255, 255)):
        """Draw the asteroid as a wireframe polygon."""
        verts = self.get_vertices_world()
        if len(verts) >= 3:
            pygame.draw.polygon(surface, color, verts, 1)
