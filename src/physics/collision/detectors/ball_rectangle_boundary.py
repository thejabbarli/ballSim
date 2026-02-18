"""Collision detection between Ball and RectangleBoundary."""

import numpy as np
from ....core.types import CollisionInfo
from ....entities.ball import Ball
from ....entities.boundaries.rectangle_boundary import RectangleBoundary
from ....math import distance, normalize, magnitude, clamp, vec2


def detect_ball_rectangle_boundary(
    ball: Ball,
    boundary: RectangleBoundary,
    timestamp: float
) -> CollisionInfo | None:
    """Detect collision between a ball and a rectangle boundary.
    
    Args:
        ball: The ball to check
        boundary: The rectangle boundary to check against
        timestamp: Current simulation time
        
    Returns:
        CollisionInfo if collision detected, None otherwise
    """
    if boundary.is_containment:
        return _detect_containment(ball, boundary, timestamp)
    else:
        return _detect_obstacle(ball, boundary, timestamp)


def _detect_containment(
    ball: Ball,
    boundary: RectangleBoundary,
    timestamp: float
) -> CollisionInfo | None:
    """Detect collision when ball should stay INSIDE rectangle."""
    # Check each edge
    collisions = []
    
    # Left edge
    if ball.position[0] - ball.radius < boundary.left:
        penetration = boundary.left - (ball.position[0] - ball.radius)
        collisions.append((
            penetration,
            vec2(1.0, 0.0),  # Normal points right (inward)
            vec2(boundary.left, ball.position[1])
        ))
    
    # Right edge
    if ball.position[0] + ball.radius > boundary.right:
        penetration = (ball.position[0] + ball.radius) - boundary.right
        collisions.append((
            penetration,
            vec2(-1.0, 0.0),  # Normal points left (inward)
            vec2(boundary.right, ball.position[1])
        ))
    
    # Top edge
    if ball.position[1] - ball.radius < boundary.top:
        penetration = boundary.top - (ball.position[1] - ball.radius)
        collisions.append((
            penetration,
            vec2(0.0, 1.0),  # Normal points down (inward)
            vec2(ball.position[0], boundary.top)
        ))
    
    # Bottom edge
    if ball.position[1] + ball.radius > boundary.bottom:
        penetration = (ball.position[1] + ball.radius) - boundary.bottom
        collisions.append((
            penetration,
            vec2(0.0, -1.0),  # Normal points up (inward)
            vec2(ball.position[0], boundary.bottom)
        ))
    
    if not collisions:
        return None
    
    # Return the deepest penetration
    penetration, normal, point = max(collisions, key=lambda x: x[0])
    
    return CollisionInfo(
        entity_a=ball,
        entity_b=boundary,
        point=point,
        normal=normal,
        penetration=penetration,
        relative_velocity=magnitude(ball.velocity),
        timestamp=timestamp
    )


def _detect_obstacle(
    ball: Ball,
    boundary: RectangleBoundary,
    timestamp: float
) -> CollisionInfo | None:
    """Detect collision when ball should stay OUTSIDE rectangle (obstacle)."""
    # Find closest point on rectangle to ball center
    closest_x = clamp(ball.position[0], boundary.left, boundary.right)
    closest_y = clamp(ball.position[1], boundary.top, boundary.bottom)
    closest = vec2(closest_x, closest_y)
    
    # Check if ball center is inside rectangle
    inside = (boundary.left <= ball.position[0] <= boundary.right and
              boundary.top <= ball.position[1] <= boundary.bottom)
    
    if inside:
        # Ball center is inside rectangle - find nearest edge
        dx_left = ball.position[0] - boundary.left
        dx_right = boundary.right - ball.position[0]
        dy_top = ball.position[1] - boundary.top
        dy_bottom = boundary.bottom - ball.position[1]
        
        min_dist = min(dx_left, dx_right, dy_top, dy_bottom)
        
        if min_dist == dx_left:
            normal = vec2(-1.0, 0.0)
            penetration = ball.radius + dx_left
            point = vec2(boundary.left, ball.position[1])
        elif min_dist == dx_right:
            normal = vec2(1.0, 0.0)
            penetration = ball.radius + dx_right
            point = vec2(boundary.right, ball.position[1])
        elif min_dist == dy_top:
            normal = vec2(0.0, -1.0)
            penetration = ball.radius + dy_top
            point = vec2(ball.position[0], boundary.top)
        else:
            normal = vec2(0.0, 1.0)
            penetration = ball.radius + dy_bottom
            point = vec2(ball.position[0], boundary.bottom)
        
        return CollisionInfo(
            entity_a=ball,
            entity_b=boundary,
            point=point,
            normal=normal,
            penetration=penetration,
            relative_velocity=magnitude(ball.velocity),
            timestamp=timestamp
        )
    
    # Ball center is outside - check distance to closest point
    dist = distance(ball.position, closest)
    
    if dist >= ball.radius:
        return None
    
    penetration = ball.radius - dist
    
    if dist < 1e-10:
        # Ball center exactly on edge, use rectangle center to determine normal
        normal = normalize(ball.position - boundary.center)
    else:
        normal = normalize(ball.position - closest)
    
    return CollisionInfo(
        entity_a=ball,
        entity_b=boundary,
        point=closest,
        normal=normal,
        penetration=penetration,
        relative_velocity=magnitude(ball.velocity),
        timestamp=timestamp
    )
