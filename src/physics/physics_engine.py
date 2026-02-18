"""Physics engine implementation."""

import numpy as np
from ..core.config_loader import PhysicsConfig
from ..entities.ball import Ball
from ..math import from_list
from .integrators import Integrator, EulerIntegrator, VerletIntegrator


class PhysicsEngine:
    """Manages physics simulation for all entities."""
    
    def __init__(self, config: PhysicsConfig):
        self.gravity = from_list(config.gravity)
        self.integrator = self._create_integrator(config.integrator)
    
    def _create_integrator(self, name: str) -> Integrator:
        """Create the appropriate integrator."""
        if name == "verlet":
            return VerletIntegrator()
        return EulerIntegrator()
    
    def update(self, balls: list[Ball], dt: float) -> None:
        """Update physics for all balls.
        
        Args:
            balls: List of balls to update
            dt: Time step in seconds
        """
        for ball in balls:
            self.integrator.integrate(ball, self.gravity, dt)
    
    def set_gravity(self, gravity: np.ndarray) -> None:
        """Set the gravity vector."""
        self.gravity = gravity.astype(np.float64)
