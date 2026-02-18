"""Circle boundary implementation."""

import numpy as np
from ...core.types import Boundary
from ...core.config_loader import BoundaryConfig
from ...math import from_list, distance, normalize


class CircleBoundary(Boundary):
    """A circular boundary."""

    def __init__(
        self,
        id: str,
        center: np.ndarray,
        radius: float,
        color: str,
        thickness: float,
        is_containment: bool,
        hue_shift: str = "none",
        hue_shift_speed: float = 60.0,
        hue_shift_amount: float = 30.0
    ):
        super().__init__(id, color, thickness, is_containment, hue_shift, hue_shift_speed, hue_shift_amount)
        self.center = center.astype(np.float64)
        self.radius = radius

    @classmethod
    def from_config(cls, config: BoundaryConfig) -> "CircleBoundary":
        """Create a CircleBoundary from configuration."""
        if config.center is None or config.radius is None:
            raise ValueError("CircleBoundary requires 'center' and 'radius'")

        return cls(
            id=config.id,
            center=from_list(config.center),
            radius=config.radius,
            color=config.color,
            thickness=config.thickness,
            is_containment=config.is_containment,
            hue_shift=config.hue_shift,
            hue_shift_speed=config.hue_shift_speed,
            hue_shift_amount=config.hue_shift_amount
        )

    def contains_point(self, point: np.ndarray) -> bool:
        """Check if point is inside the circle."""
        return distance(point, self.center) < self.radius

    def get_closest_point(self, point: np.ndarray) -> np.ndarray:
        """Get the closest point on the circle to the given point."""
        direction = normalize(point - self.center)
        return self.center + direction * self.radius

    def get_normal_at(self, point: np.ndarray) -> np.ndarray:
        """Get the outward normal at a point on the boundary."""
        return normalize(point - self.center)

    def get_render_data(self) -> dict:
        """Return data needed for rendering."""
        return {
            "type": "circle",
            "id": self.id,
            "center": self.center.copy(),
            "radius": self.radius,
            "color": self.color,
            "thickness": self.thickness,
        }

    def __repr__(self) -> str:
        mode = "containment" if self.is_containment else "obstacle"
        return f"CircleBoundary(id={self.id}, center={self.center}, radius={self.radius}, {mode})"
