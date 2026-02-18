"""Rectangle boundary implementation."""

import numpy as np
from ...core.types import Boundary
from ...core.config_loader import BoundaryConfig
from ...math import from_list, normalize, clamp, vec2


class RectangleBoundary(Boundary):
    """A rectangular boundary."""

    def __init__(
        self,
        id: str,
        x: float,
        y: float,
        width: float,
        height: float,
        color: str,
        thickness: float,
        is_containment: bool,
        hue_shift: str = "none",
        hue_shift_speed: float = 60.0,
        hue_shift_amount: float = 30.0
    ):
        super().__init__(id, color, thickness, is_containment, hue_shift, hue_shift_speed, hue_shift_amount)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def center(self) -> np.ndarray:
        return vec2(self.x + self.width / 2, self.y + self.height / 2)

    @classmethod
    def from_config(cls, config: BoundaryConfig) -> "RectangleBoundary":
        """Create a RectangleBoundary from configuration."""
        if any(v is None for v in [config.x, config.y, config.width, config.height]):
            raise ValueError("RectangleBoundary requires 'x', 'y', 'width', 'height'")

        return cls(
            id=config.id,
            x=config.x,
            y=config.y,
            width=config.width,
            height=config.height,
            color=config.color,
            thickness=config.thickness,
            is_containment=config.is_containment,
            hue_shift=config.hue_shift,
            hue_shift_speed=config.hue_shift_speed,
            hue_shift_amount=config.hue_shift_amount
        )

    def contains_point(self, point: np.ndarray) -> bool:
        """Check if point is inside the rectangle."""
        return (self.left <= point[0] <= self.right and
                self.top <= point[1] <= self.bottom)

    def get_closest_point(self, point: np.ndarray) -> np.ndarray:
        """Get the closest point on the rectangle edge to the given point."""
        closest_x = clamp(point[0], self.left, self.right)
        closest_y = clamp(point[1], self.top, self.bottom)
        return vec2(closest_x, closest_y)

    def get_normal_at(self, point: np.ndarray) -> np.ndarray:
        """Get the outward normal at a point on the boundary."""
        dx_left = abs(point[0] - self.left)
        dx_right = abs(point[0] - self.right)
        dy_top = abs(point[1] - self.top)
        dy_bottom = abs(point[1] - self.bottom)

        min_dist = min(dx_left, dx_right, dy_top, dy_bottom)

        if min_dist == dx_left:
            return vec2(-1.0, 0.0)
        elif min_dist == dx_right:
            return vec2(1.0, 0.0)
        elif min_dist == dy_top:
            return vec2(0.0, -1.0)
        else:
            return vec2(0.0, 1.0)

    def get_render_data(self) -> dict:
        """Return data needed for rendering."""
        return {
            "type": "rectangle",
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "color": self.color,
            "thickness": self.thickness,
        }

    def __repr__(self) -> str:
        mode = "containment" if self.is_containment else "obstacle"
        return f"RectangleBoundary(id={self.id}, x={self.x}, y={self.y}, {self.width}x{self.height}, {mode})"
