"""Collision detection between Ball and CircleBoundary."""

import numpy as np
from ....core.types import CollisionInfo
from ....entities.ball import Ball
from ....entities.boundaries.circle_boundary import CircleBoundary
from ....math import distance, normalize, magnitude


def detect_ball_circle_boundary(
    ball: Ball, 
    boundary: CircleBoundary, 
    timestamp: float
) -> CollisionInfo | None:
    """Detect collision between a ball and a circle boundary.
    
    Args:
        ball: The ball to check
        boundary: The circle boundary to check against
        timestamp: Current simulation time
        
    Returns:
        CollisionInfo if collision detected, None otherwise
    """
    dist = distance(ball.position, boundary.center)
    
    if boundary.is_containment:
        # Ball should stay INSIDE the boundary
        # Collision occurs when ball tries to exit (dist + radius > boundary.radius)
        penetration = (dist + ball.radius) - boundary.radius
        
        if penetration <= 0:
            return None
        
        # Normal points toward center (inward) to push ball back inside
        if dist < 1e-10:
            # Ball at center, use arbitrary direction
            normal = np.array([0.0, -1.0])
        else:
            normal = normalize(boundary.center - ball.position)
        
        # Collision point is on the boundary
        collision_point = boundary.center + normalize(ball.position - boundary.center) * boundary.radius
        
    else:
        # Ball should stay OUTSIDE the boundary (it's an obstacle)
        # Collision occurs when ball penetrates (dist - radius < boundary.radius)
        penetration = boundary.radius - (dist - ball.radius)
        
        if penetration <= 0:
            return None
        
        # Normal points away from center (outward) to push ball away
        if dist < 1e-10:
            # Ball at center, use arbitrary direction
            normal = np.array([0.0, 1.0])
        else:
            normal = normalize(ball.position - boundary.center)
        
        # Collision point is on the boundary
        collision_point = boundary.center + normal * boundary.radius
    
    # Calculate relative velocity (ball velocity toward the boundary)
    relative_velocity = magnitude(ball.velocity)
    
    return CollisionInfo(
        entity_a=ball,
        entity_b=boundary,
        point=collision_point,
        normal=normal,
        penetration=penetration,
        relative_velocity=relative_velocity,
        timestamp=timestamp
    )
