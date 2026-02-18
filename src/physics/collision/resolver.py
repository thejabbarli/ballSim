"""Collision resolution - calculates and applies collision response."""

import numpy as np
from ...core.types import CollisionInfo, Boundary
from ...entities.ball import Ball
from ...math import dot


class CollisionResolver:
    """Resolves collisions by adjusting velocities and positions."""
    
    def resolve(self, collision: CollisionInfo) -> None:
        """Resolve a single collision."""
        ball = collision.entity_a
        other = collision.entity_b

        if not isinstance(ball, Ball):
            return

        if isinstance(other, Boundary):
            self._resolve_ball_boundary(ball, collision)
        elif isinstance(other, Ball):
            self._resolve_ball_ball(ball, other, collision)

    def _resolve_ball_boundary(self, ball: Ball, collision: CollisionInfo) -> None:
        """Resolve collision between ball and static boundary."""
        normal = collision.normal

        # Decompose velocity into normal and tangent components
        v_n = dot(ball.velocity, normal) * normal
        v_t = ball.velocity - v_n

        # Reflect normal component with restitution
        ball.velocity = v_t - ball.restitution * v_n

        # Position correction - push ball out of collision
        ball.position += normal * collision.penetration

    def _resolve_ball_ball(
        self,
        ball_a: Ball,
        ball_b: Ball,
        collision: CollisionInfo
    ) -> None:
        """Resolve collision between two balls using conservation of momentum."""
        normal = collision.normal

        # Relative velocity
        v_rel = ball_a.velocity - ball_b.velocity

        # Velocity along collision normal
        v_rel_n = dot(v_rel, normal)

        # Only apply impulse if balls are approaching (not separating)
        if v_rel_n >= 0:
            # Combined restitution
            e = min(ball_a.restitution, ball_b.restitution)

            # Impulse scalar
            j = -(1 + e) * v_rel_n / (1 / ball_a.mass + 1 / ball_b.mass)

            # Apply impulse
            impulse = j * normal
            ball_a.velocity += impulse / ball_a.mass
            ball_b.velocity -= impulse / ball_b.mass

        # ALWAYS correct position if overlapping
        if collision.penetration > 0:
            total_mass = ball_a.mass + ball_b.mass
            # Slight extra push to prevent sticking
            correction = collision.penetration * 1.01
            ball_a.position += normal * correction * (ball_b.mass / total_mass)
            ball_b.position -= normal * correction * (ball_a.mass / total_mass)
