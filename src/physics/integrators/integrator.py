"""Physics integration methods."""

from abc import ABC, abstractmethod
import numpy as np
from ...entities.ball import Ball


class Integrator(ABC):
    """Abstract base class for physics integrators."""
    
    @abstractmethod
    def integrate(self, ball: Ball, acceleration: np.ndarray, dt: float) -> None:
        """Update ball's velocity and position for one timestep."""
        pass


class EulerIntegrator(Integrator):
    """Semi-implicit Euler integration.
    
    velocity += acceleration * dt
    position += velocity * dt
    
    Simple and fast, slightly damped.
    """
    
    def integrate(self, ball: Ball, acceleration: np.ndarray, dt: float) -> None:
        """Update ball's velocity and position."""
        ball.velocity += acceleration * dt
        ball.position += ball.velocity * dt


class VerletIntegrator(Integrator):
    """Velocity Verlet integration.
    
    More accurate and better energy conservation.
    """
    
    def __init__(self):
        self._prev_accelerations: dict[str, np.ndarray] = {}
    
    def integrate(self, ball: Ball, acceleration: np.ndarray, dt: float) -> None:
        """Update ball's velocity and position."""
        prev_acc = self._prev_accelerations.get(ball.id, acceleration)
        
        # Position update
        ball.position += ball.velocity * dt + 0.5 * prev_acc * dt * dt
        
        # Velocity update
        ball.velocity += 0.5 * (prev_acc + acceleration) * dt
        
        # Store for next frame
        self._prev_accelerations[ball.id] = acceleration.copy()
