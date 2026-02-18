"""Ball entity implementation."""

import numpy as np
from ..core.types import Entity
from ..core.config_loader import BallConfig
from ..math import from_list, magnitude_squared, shift_hue


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
            mass: float = 1.0,
            hue_shift: str = "none",
            hue_shift_speed: float = 60.0,
            hue_shift_amount: float = 30.0,
            outline: bool = False,
            outline_color: str = "#ffffff",
            outline_thickness: float = 2.0,
            glow: bool = False,
            glow_radius: float = 20.0,
            glow_intensity: float = 0.5,
            glow_color: str | None = None
    ):
        super().__init__(id, position, velocity)
        self.radius = radius
        self.base_color = color
        self.color = color
        self.restitution = restitution
        self.mass = mass
        self.hue_shift = hue_shift
        self.hue_shift_speed = hue_shift_speed
        self.hue_shift_amount = hue_shift_amount
        self._hue_offset = 0.0
        self.outline = outline
        self.outline_color = outline_color
        self.outline_thickness = outline_thickness
        self.glow = glow
        self.glow_radius = glow_radius
        self.glow_intensity = glow_intensity
        self.glow_color = glow_color

    @classmethod
    def from_config(cls, config: BallConfig) -> "Ball":
        return cls(
            id=config.id,
            position=from_list(config.position),
            velocity=from_list(config.velocity),
            radius=config.radius,
            color=config.color,
            restitution=config.restitution,
            mass=config.mass,
            hue_shift=config.hue_shift,
            hue_shift_speed=config.hue_shift_speed,
            hue_shift_amount=config.hue_shift_amount,
            outline=config.outline,
            outline_color=config.outline_color,
            outline_thickness=config.outline_thickness,
            glow=config.glow,
            glow_radius=config.glow_radius,
            glow_intensity=config.glow_intensity,
            glow_color=config.glow_color
        )

    def update(self, dt: float) -> None:
        """Update ball position based on velocity."""
        self.position += self.velocity * dt

        # Continuous hue shift
        if self.hue_shift == "continuous":
            self._hue_offset += self.hue_shift_speed * dt
            self.color = shift_hue(self.base_color, self._hue_offset)

    def on_collision(self) -> None:
        """Called when ball collides with something."""
        if self.hue_shift == "on_bounce":
            self._hue_offset += self.hue_shift_amount
            self.color = shift_hue(self.base_color, self._hue_offset)

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
