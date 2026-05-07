"""Main entry point — full Asteroids game loop with state machine."""

import sys
import random
import pygame
from . import ship as ship_mod
from .ship import Ship, SCREEN_W, SCREEN_H
from .asteroid import Asteroid
from .bullet import Bullet, MAX_BULLETS
from .ufo import UFO
from .particles import Particle, spawn_explosion
from .collision import circles_collide, circle_poly_collide
from .game_state import GameState
from .screens import draw_title_screen, draw_game_over_screen, draw_hud
from . import sound

# State machine
TITLE = "title"
PLAYING = "playing"
GAME_OVER = "game_over"


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("RETRO ASTEROIDS")
        self.clock = pygame.time.Clock()
        self.state = TITLE

        # game objects
        self.ship: Ship = None
        self.bullets: list[Bullet] = []
        self.asteroids: list[Asteroid] = []
        self.ufos: list[UFO] = []
        self.particles: list[Particle] = []
        self.ufo_bullets: list[Bullet] = []
        self.gs: GameState = None

        # timing
        self.ufo_timer = 0
        self.thrust_sound_timer = 0

        # font for state messages
        self._font = pygame.font.Font(None, 30)

    def run(self):
        """Main loop."""
        running = True
        while running:
            dt = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self._handle_event(event)

            self._update()
            self._draw()
            pygame.display.flip()

        self._cleanup()
        pygame.quit()

    def _handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            if self.state == TITLE:
                if event.key == pygame.K_RETURN:
                    self._start_game()

            elif self.state == GAME_OVER:
                if event.key == pygame.K_RETURN:
                    self._start_game()

    def _start_game(self):
        """Initialize or reset game state for a new game."""
        self.ship = Ship()
        self.bullets = []
        self.asteroids = []
        self.ufos = []
        self.particles = []
        self.ufo_bullets = []
        self.gs = GameState()
        self.ufo_timer = 0
        self.thrust_sound_timer = 0
        self.state = PLAYING

        # Spawn initial asteroids away from ship
        count = self.gs.asteroid_count()
        for _ in range(count):
            a = Asteroid("large")
            # keep spawning until asteroid is safely far from ship
            attempts = 0
            while attempts < 20:
                dx = a.x - self.ship.x
                dy = a.y - self.ship.y
                if dx * dx + dy * dy > 200 * 200:
                    break
                a = Asteroid("large")
                attempts += 1
            self.asteroids.append(a)

    def _update(self):
        if self.state != PLAYING:
            return

        keys = pygame.key.get_pressed()

        # --- Ship input ---
        self.ship.thrusting = False
        if keys[pygame.K_LEFT]:
            self.ship.rotate(-1)
        if keys[pygame.K_RIGHT]:
            self.ship.rotate(1)
        if keys[pygame.K_UP]:
            self.ship.thrust()
            self.ship.thrusting = True

        self.ship.update()

        # fire
        if keys[pygame.K_SPACE]:
            self._fire_bullet()

        # --- Update bullets ---
        for b in self.bullets:
            b.update()
        for b in self.ufo_bullets:
            b.update()
        self.bullets = [b for b in self.bullets if b.alive]
        self.ufo_bullets = [b for b in self.ufo_bullets if b.alive]

        # --- Update asteroids ---
        for a in self.asteroids:
            a.update()

        # --- Update UFOs ---
        self.ufo_timer += 1
        if self.ufo_timer >= 25 * 60 and len(self.ufos) == 0:
            self.ufo_timer = 0
            self.ufos.append(UFO("large"))
        elif self.ufo_timer >= 10 * 60 and len(self.ufos) == 0:
            self.ufo_timer = 0
            self.ufos.append(UFO("small"))

        for u in self.ufos:
            u.update(self.ship.x, self.ship.y)
            if u.should_shoot():
                self.ufo_bullets.append(u.fire(self.ship.x, self.ship.y))
        self.ufos = [u for u in self.ufos if u.alive]

        # --- Update particles ---
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.alive]

        # --- Collision detection ---
        self._check_collisions()

        # --- Sound ---
        if self.ship.thrusting:
            self.thrust_sound_timer += 1
            if self.thrust_sound_timer >= 8:
                self.thrust_sound_timer = 0
                sound.play_thrust()

        # --- Level complete ---
        if len(self.asteroids) == 0:
            self.gs.next_level()
            count = self.gs.asteroid_count()
            for _ in range(count):
                self.asteroids.append(Asteroid("large"))

    def _fire_bullet(self):
        """Fire a bullet from the ship if under max count."""
        if len(self.bullets) >= MAX_BULLETS:
            return
        nose_x = self.ship.x
        nose_y = self.ship.y
        import math
        rad = math.radians(self.ship.angle)
        nose_x += math.sin(rad) * ship_mod.SHIP_SCALE
        nose_y -= math.cos(rad) * ship_mod.SHIP_SCALE
        self.bullets.append(Bullet(nose_x, nose_y, self.ship.angle))
        sound.play_fire()

    def _check_collisions(self):
        """Run all collision checks: bullets vs asteroids, ship vs asteroids,
        bullets vs UFOs, ship vs UFOs, UFO bullets vs ship."""

        # --- Bullets vs asteroids ---
        for b in self.bullets[:]:
            if not b.alive:
                continue
            for a in self.asteroids[:]:
                if not a.alive if hasattr(a, 'alive') else True:
                    if circles_collide(b.x, b.y, b.radius, a.x, a.y, a.radius):
                        b.alive = False
                        self._destroy_asteroid(a)
                    break

        # Use traditional loops for clarity
        for b in list(self.bullets):
            if not b.alive:
                self.bullets.remove(b)
                continue
            for a in list(self.asteroids):
                if circles_collide(b.x, b.y, b.radius, a.x, a.y, a.radius):
                    b.alive = False
                    self._destroy_asteroid(a)
                    break

        # Cleanup dead bullets
        self.bullets = [b for b in self.bullets if b.alive]

        # --- Bullets vs UFOs ---
        for b in list(self.bullets):
            if not b.alive:
                continue
            for u in list(self.ufos):
                if circles_collide(b.x, b.y, b.radius, u.x, u.y, u.radius):
                    b.alive = False
                    u.alive = False
                    self.gs.add_score(u.score)
                    self.particles.extend(spawn_explosion(u.x, u.y, 20, (0.5, 2.5), 25))
                    sound.play_explosion()
                    break
        self.bullets = [b for b in self.bullets if b.alive]
        self.ufos = [u for u in self.ufos if u.alive]

        # --- Ship vs asteroids ---
        if not self.ship.is_invulnerable():
            for a in list(self.asteroids):
                # use circle-poly collision
                verts = a.get_vertices_world()
                if circle_poly_collide(self.ship.x, self.ship.y, self.ship.radius, verts):
                    self._kill_ship()
                    self._destroy_asteroid(a)
                    break

        # --- Ship vs UFO ---
        if not self.ship.is_invulnerable():
            for u in list(self.ufos):
                if circles_collide(self.ship.x, self.ship.y, self.ship.radius,
                                   u.x, u.y, u.radius):
                    u.alive = False
                    self.particles.extend(spawn_explosion(u.x, u.y, 20, (0.5, 2.5), 25))
                    self._kill_ship()
                    break
        self.ufos = [u for u in self.ufos if u.alive]

        # --- UFO bullets vs ship ---
        if not self.ship.is_invulnerable():
            for b in list(self.ufo_bullets):
                if circles_collide(self.ship.x, self.ship.y, self.ship.radius,
                                   b.x, b.y, b.radius):
                    b.alive = False
                    self._kill_ship()
                    break
        self.ufo_bullets = [b for b in self.ufo_bullets if b.alive]

    def _destroy_asteroid(self, a: Asteroid):
        """Destroy an asteroid: score, particles, split children."""
        self.gs.add_score(a.score)
        self.particles.extend(spawn_explosion(a.x, a.y, 20, (0.5, 2.5), 25))
        sound.play_explosion()

        children = a.split()
        self.asteroids.extend(children)

        if a in self.asteroids:
            self.asteroids.remove(a)

    def _kill_ship(self):
        """Ship destroyed: lose life, explosion, respawn or game over."""
        self.particles.extend(spawn_explosion(self.ship.x, self.ship.y, 25, (1.0, 4.0), 35))
        sound.play_explosion()

        game_over = self.gs.lose_life()
        if game_over:
            self.gs.save_high_score()
            self.state = GAME_OVER
        else:
            self.ship.respawn()

    def _draw(self):
        """Draw current state."""
        self.screen.fill((0, 0, 0))

        if self.state == TITLE:
            draw_title_screen(self.screen)
        elif self.state == GAME_OVER:
            draw_game_over_screen(self.screen, self.gs.score, self.gs.high_score)
        elif self.state == PLAYING:
            self._draw_gameplay()
            draw_hud(self.screen, self.gs.score, self.gs.lives, self.gs.level,
                     self.gs.high_score)

    def _draw_gameplay(self):
        """Draw all game objects."""
        # Asteroids
        for a in self.asteroids:
            a.draw(self.screen)

        # UFOs
        for u in self.ufos:
            u.draw(self.screen)

        # UFO bullets
        for b in self.ufo_bullets:
            b.draw(self.screen)

        # Ship bullets
        for b in self.bullets:
            b.draw(self.screen)

        # Particles
        for p in self.particles:
            p.draw(self.screen)

        # Ship (drawn last to be on top)
        self.ship.draw(self.screen)

    def _cleanup(self):
        """Save high score on exit."""
        if self.gs:
            self.gs.save_high_score()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
