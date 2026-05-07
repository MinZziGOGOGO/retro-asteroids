"""Particle effects — explosion debris for destroyed objects."""

import random
import math
import pygame


class Particle:
    def __init__(self, x: float, y: float, vel_x: float, vel_y: float,
                 lifetime: int = 30):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.alive = True

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False

    @property
    def alpha(self) -> float:
        """0.0 to 1.0, fading out."""
        return max(self.lifetime / self.max_lifetime, 0.0)

    def draw(self, surface: pygame.Surface, color: tuple[int, int, int] = (255, 255, 255)):
        """Draw as small dot with alpha fading."""
        a = int(self.alpha * 255)
        px, py = int(self.x), int(self.y)
        # pygame.draw doesn't support alpha directly, use alpha surface
        if a <= 0:
            return
        s = pygame.Surface((3, 3), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        s.set_at((1, 1), (*color, a))
        surface.blit(s, (px - 1, py - 1))


def spawn_explosion(x: float, y: float, count: int = 18,
                    speed_range: tuple[float, float] = (0.5, 3.0),
                    lifetime: int = 30) -> list[Particle]:
    """Spawn explosion particles at (x, y)."""
    particles = []
    for _ in range(count):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(*speed_range)
        vel_x = math.cos(angle) * speed
        vel_y = math.sin(angle) * speed
        particles.append(Particle(x, y, vel_x, vel_y, lifetime))
    return particles
