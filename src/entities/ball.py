"""Ball entity implementation."""

import numpy as np
from ..core.types import Entity
from ..core.config_loader import BallConfig
from ..math import from_list, magnitude_squared


class Ball(Entity):
    """A bouncing ball entity."""
    
    def __init__(
        self,
        id: str,
        position: np.ndarray,
        velocity: np.ndarray,
        radius: float,
        color: str,
        restitution: float = 0.9,
        mass: float = 1.0
    ):
        super().__init__(id, position, velocity)
        self.radius = radius
        self.color = color
        self.restitution = restitution
        self.mass = mass
    
    @classmethod
    def from_config(cls, config: BallConfig) -> "Ball":
        """Create a Ball from configuration."""
        return cls(
            id=config.id,
            position=from_list(config.position),
            velocity=from_list(config.velocity),
            radius=config.radius,
            color=config.color,
            restitution=config.restitution,
            mass=config.mass
        )
    
    def update(self, dt: float) -> None:
        """Update ball position based on velocity."""
        self.position += self.velocity * dt
    
    def get_render_data(self) -> dict:
        """Return data needed for rendering."""
        return {
            "type": "ball",
            "id": self.id,
            "position": self.position.copy(),
            "radius": self.radius,
            "color": self.color,
        }
    
    def get_kinetic_energy(self) -> float:
        """Calculate the ball's kinetic energy."""
        speed_squared = magnitude_squared(self.velocity)
        return 0.5 * self.mass * speed_squared
    
    def __repr__(self) -> str:
        return f"Ball(id={self.id}, pos={self.position}, vel={self.velocity})"
