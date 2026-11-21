"""Collision detection — circle vs circle, circle vs polygon (SAT)."""

import math


def circles_collide(ax: float, ay: float, ar: float,
                    bx: float, by: float, br: float) -> bool:
    """Distance between centers <= sum of radii (touching counts as a hit)."""
    dx = ax - bx
    dy = ay - by
    dist_sq = dx * dx + dy * dy
    radius_sum = ar + br
    return dist_sq <= radius_sum * radius_sum


def circle_poly_collide(cx: float, cy: float, cr: float,
                        vertices: list[tuple[float, float]]) -> bool:
    """Check circle-polygon collision using closest-point-on-edge distance."""
    if len(vertices) < 3:
        return False

    # Check each edge
    for i in range(len(vertices)):
        ax, ay = vertices[i]
        bx, by = vertices[(i + 1) % len(vertices)]

        # closest point on edge AB to circle center C
        abx = bx - ax
        aby = by - ay
        acx = cx - ax
        acy = cy - ay

        t = (acx * abx + acy * aby) / max(abx * abx + aby * aby, 1e-10)
        t = max(0.0, min(1.0, t))

        px = ax + t * abx
        py = ay + t * aby

        dx = cx - px
        dy = cy - py
        if dx * dx + dy * dy < cr * cr:
            return True

    # Also check if circle center is inside polygon (point-in-poly)
    if _point_in_poly(cx, cy, vertices):
        return True

    return False


def _point_in_poly(px: float, py: float,
                   vertices: list[tuple[float, float]]) -> bool:
    """Ray-casting point-in-polygon test."""
    inside = False
    n = len(vertices)
    j = n - 1
    for i in range(n):
        xi, yi = vertices[i]
        xj, yj = vertices[j]

        if ((yi > py) != (yj > py)) and \
           (px < (xj - xi) * (py - yi) / max(yj - yi, 1e-10) + xi):
            inside = not inside
        j = i
    return inside
