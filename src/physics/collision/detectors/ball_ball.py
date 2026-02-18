"""Collision detection between two Balls."""

import numpy as np
from ....core.types import CollisionInfo
from ....entities.ball import Ball
from ....math import distance, normalize, magnitude, dot


def detect_ball_ball(
    ball_a: Ball,
    ball_b: Ball,
    timestamp: float
) -> CollisionInfo | None:
    """Detect collision between two balls.
    
    Args:
        ball_a: First ball
        ball_b: Second ball
        timestamp: Current simulation time
        
    Returns:
        CollisionInfo if collision detected, None otherwise
    """
    dist = distance(ball_a.position, ball_b.position)
    min_dist = ball_a.radius + ball_b.radius
    
    penetration = min_dist - dist
    
    if penetration <= 0:
        return None
    
    # Normal points from A to B
    if dist < 1e-10:
        # Balls at same position, use arbitrary direction
        normal = np.array([1.0, 0.0])
    else:
        normal = normalize(ball_b.position - ball_a.position)
    
    # Collision point is midway between ball surfaces
    collision_point = ball_a.position + normal * (ball_a.radius - penetration / 2)
    
    # Relative velocity (A relative to B)
    rel_vel = ball_a.velocity - ball_b.velocity
    relative_velocity = abs(dot(rel_vel, normal))
    
    return CollisionInfo(
        entity_a=ball_a,
        entity_b=ball_b,
        point=collision_point,
        normal=normal,
        penetration=penetration,
        relative_velocity=relative_velocity,
        timestamp=timestamp
    )
