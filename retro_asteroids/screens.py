"""Screens — title, game over, HUD rendering."""

import pygame
from .ship import SCREEN_W, SCREEN_H


# Font cache
_fonts: dict[int, pygame.font.Font] = {}


def _get_font(size: int) -> pygame.font.Font:
    if size not in _fonts:
        _fonts[size] = pygame.font.Font(None, size)
    return _fonts[size]


def draw_title_screen(surface: pygame.Surface, high_score: int = 0):
    """Draw the title screen with ASTEROIDS text and instructions."""
    surface.fill((0, 0, 0))

    # Title
    title_font = _get_font(72)
    title = title_font.render("ASTEROIDS", True, (255, 255, 255))
    tr = title.get_rect(center=(SCREEN_W // 2, SCREEN_H // 3))
    surface.blit(title, tr)

    # Instructions
    small_font = _get_font(24)
    lines = [
        "PRESS ENTER TO START",
        "",
        "ARROW KEYS - ROTATE / THRUST",
        "SPACE - FIRE      P - PAUSE",
        "",
        "BEWARE OF ASTEROIDS AND UFOs",
    ]
    for i, line in enumerate(lines):
        surf = small_font.render(line, True, (200, 200, 200))
        rect = surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + i * 30))
        surface.blit(surf, rect)

    if high_score > 0:
        hs_surf = small_font.render(f"HIGH SCORE: {high_score}", True, (150, 150, 255))
        hs_rect = hs_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H - 60))
        surface.blit(hs_surf, hs_rect)


def draw_game_over_screen(surface: pygame.Surface, score: int, high_score: int):
    """Draw game over screen with final score."""
    surface.fill((0, 0, 0))

    title_font = _get_font(48)
    title = title_font.render("GAME OVER", True, (255, 255, 255))
    tr = title.get_rect(center=(SCREEN_W // 2, SCREEN_H // 3))
    surface.blit(title, tr)

    score_font = _get_font(36)
    score_surf = score_font.render(f"SCORE: {score}", True, (255, 255, 255))
    sr = score_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
    surface.blit(score_surf, sr)

    if score >= high_score and score > 0:
        hs_surf = score_font.render("NEW HIGH SCORE!", True, (255, 255, 100))
        hsr = hs_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 50))
        surface.blit(hs_surf, hsr)

    small_font = _get_font(24)
    restart = small_font.render("PRESS ENTER TO PLAY AGAIN", True, (200, 200, 200))
    rr = restart.get_rect(center=(SCREEN_W // 2, SCREEN_H - 80))
    surface.blit(restart, rr)


def draw_pause_overlay(surface: pygame.Surface):
    """Draw a centered PAUSED label over the frozen game."""
    font = _get_font(48)
    text = font.render("PAUSED", True, (255, 255, 255))
    surface.blit(text, text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2)))


def draw_hud(surface: pygame.Surface, score: int, lives: int, level: int,
             high_score: int):
    """Draw HUD overlay: score top-left, high score top-center, lives top-right."""
    font = _get_font(24)

    # Score
    score_surf = font.render(f"{score}", True, (255, 255, 255))
    surface.blit(score_surf, (20, 10))

    # High score
    hs_surf = font.render(f"HIGH: {high_score}", True, (150, 150, 255))
    hs_rect = hs_surf.get_rect(center=(SCREEN_W // 2, 20))
    surface.blit(hs_surf, hs_rect)

    # Level
    level_surf = font.render(f"LVL {level}", True, (200, 200, 200))
    level_rect = level_surf.get_rect(center=(SCREEN_W // 2, 50))
    surface.blit(level_surf, level_rect)

    # Lives as ship icons top-right
    for i in range(lives):
        _draw_ship_icon(surface, SCREEN_W - 30 - i * 30, 25)


def _draw_ship_icon(surface: pygame.Surface, x: int, y: int):
    """Draw a tiny outlined ship used as a life counter."""
    pts = [
        (x, y - 8),
        (x - 6, y + 6),
        (x + 6, y + 6),
    ]
    pygame.draw.polygon(surface, (255, 255, 255), pts, 1)
