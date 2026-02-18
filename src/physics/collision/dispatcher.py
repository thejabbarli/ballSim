"""Collision dispatcher - routes collision detection to appropriate detectors."""

from ...core.types import CollisionInfo, Boundary
from ...entities.ball import Ball
from ...entities.boundaries.circle_boundary import CircleBoundary
from ...entities.boundaries.rectangle_boundary import RectangleBoundary
from .detectors.ball_circle_boundary import detect_ball_circle_boundary
from .detectors.ball_rectangle_boundary import detect_ball_rectangle_boundary
from .detectors.ball_ball import detect_ball_ball


class CollisionDispatcher:
    """Routes collision detection to the appropriate detector based on entity types."""
    
    def detect_all(
        self,
        balls: list[Ball],
        boundaries: list[Boundary],
        timestamp: float
    ) -> list[CollisionInfo]:
        """Detect all collisions in the simulation.
        
        Args:
            balls: List of all balls
            boundaries: List of all boundaries
            timestamp: Current simulation time
            
        Returns:
            List of detected collisions
        """
        collisions: list[CollisionInfo] = []
        
        # Ball-Boundary collisions
        for ball in balls:
            for boundary in boundaries:
                collision = self._detect_ball_boundary(ball, boundary, timestamp)
                if collision:
                    collisions.append(collision)
        
        # Ball-Ball collisions
        for i, ball_a in enumerate(balls):
            for ball_b in balls[i + 1:]:
                collision = detect_ball_ball(ball_a, ball_b, timestamp)
                if collision:
                    collisions.append(collision)
        
        return collisions
    
    def _detect_ball_boundary(
        self,
        ball: Ball,
        boundary: Boundary,
        timestamp: float
    ) -> CollisionInfo | None:
        """Dispatch to the correct ball-boundary detector."""
        if isinstance(boundary, CircleBoundary):
            return detect_ball_circle_boundary(ball, boundary, timestamp)
        elif isinstance(boundary, RectangleBoundary):
            return detect_ball_rectangle_boundary(ball, boundary, timestamp)
        
        return None
