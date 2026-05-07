"""Quick import test for all Asteroids modules."""
import sys
sys.path.insert(0, "/home/martin/projects/retro-asteroids")

from retro_asteroids.collision import circle_circle, circle_polygon, wrap_position
from retro_asteroids.ship import Ship
from retro_asteroids.asteroid import Asteroid, spawn_asteroids
from retro_asteroids.bullet import Bullet
from retro_asteroids.ufo import Ufo, UfoBullet
from retro_asteroids.particles import ParticleSystem
from retro_asteroids.game_state import GameState
from retro_asteroids.screens import draw_hud, draw_title_screen, draw_game_over_screen
from retro_asteroids import sound
print("sound enabled:", sound.is_enabled())
print("All imports OK")
