"""UFOs — large and small saucer enemies with movement and shooting."""

import math
import random
import pygame
from .ship import SCREEN_W, SCREEN_H
from .bullet import Bullet

LARGE_UFO_RADIUS = 20
SMALL_UFO_RADIUS = 12
LARGE_UFO_SCORE = 200
SMALL_UFO_SCORE = 1000

LARGE_UFO_INTERVAL = 25 * 60  # frames (~25 seconds)
SMALL_UFO_INTERVAL = 10 * 60  # frames (~10 seconds)

UFO_SHOOT_COOLDOWN = 60  # frames between shots
UFO_BULLET_SPEED = 5.0


class UFO:
    """Base UFO class. size: 'large' or 'small'."""

    def __init__(self, size: str = "large"):
        self.size = size
        if size == "large":
            self.radius = LARGE_UFO_RADIUS
            self.score = LARGE_UFO_SCORE
            self.speed = 1.5
        else:
            self.radius = SMALL_UFO_RADIUS
            self.score = SMALL_UFO_SCORE
            self.speed = 3.0

        # spawn from left or right edge
        if random.random() < 0.5:
            self.x = -self.radius
            self.vel_x = self.speed
        else:
            self.x = SCREEN_W + self.radius
            self.vel_x = -self.speed

        self.y = random.uniform(SCREEN_H * 0.15, SCREEN_H * 0.85)
        self.vel_y = 0.0

        # small UFO moves vertically too
        if size == "small":
            self.vel_y = random.choice([-1.0, 1.0])
            self._dir_timer = random.randint(30, 90)

        self.shoot_timer = random.randint(30, 120)
        self.alive = True

    def update(self, ship_x: float = None, ship_y: float = None):
        """Move UFO, aim shots for small UFO."""
        self.x += self.vel_x
        self.y += self.vel_y

        # small UFO: erratic vertical movement
        if self.size == "small":
            self._dir_timer -= 1
            if self._dir_timer <= 0:
                self.vel_y = random.choice([-1.0, 0.0, 1.0])
                self._dir_timer = random.randint(30, 90)

        # bounce off top/bottom
        if self.y < self.radius:
            self.y = self.radius
            self.vel_y = abs(self.vel_y) if self.vel_y < 0 else self.vel_y
        elif self.y > SCREEN_H - self.radius:
            self.y = SCREEN_H - self.radius
            self.vel_y = -abs(self.vel_y) if self.vel_y > 0 else self.vel_y

        # die when off-screen
        if self.x < -self.radius * 2 or self.x > SCREEN_W + self.radius * 2:
            self.alive = False

        self.shoot_timer -= 1

    def should_shoot(self) -> bool:
        return self.shoot_timer <= 0

    def fire(self, ship_x: float = None, ship_y: float = None) -> Bullet:
        """Create a bullet. Small UFO aims at player."""
        self.shoot_timer = random.randint(40, 100) + random.randint(0, 40)

        angle = 90.0  # default: shoot downward-ish

        if self.size == "small" and ship_x is not None and ship_y is not None:
            # aim toward player
            dx = ship_x - self.x
            dy = ship_y - self.y
            angle = math.degrees(math.atan2(dx, -dy))

        if self.size == "large":
            angle = random.uniform(0, 360)

        b = Bullet(self.x, self.y, 0)
        rad = math.radians(angle)
        b.vel_x = math.sin(rad) * UFO_BULLET_SPEED
        b.vel_y = -math.cos(rad) * UFO_BULLET_SPEED
        b.lifetime = 120
        return b

    def draw(self, surface: pygame.Surface, color: tuple[int, int, int] = (255, 255, 255)):
        """Draw classic saucer shape."""
        ox, oy = int(self.x), int(self.y)
        r = self.radius

        # top dome
        pygame.draw.arc(surface, color,
                        (ox - r, oy - r * 1.2, r * 2, r * 2),
                        math.pi, 0, 1)
        # bottom line
        pygame.draw.line(surface, color,
                         (ox - r * 1.2, oy + r * 0.3),
                         (ox + r * 1.2, oy + r * 0.3), 1)
        # antenna if small
        if self.size == "small":
            pygame.draw.line(surface, color,
                             (ox, oy - r * 1.2),
                             (ox, oy - r * 1.7), 1)
