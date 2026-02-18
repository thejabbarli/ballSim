"""Core type definitions and protocols for BallSim."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, runtime_checkable
import numpy as np


@runtime_checkable
class Renderable(Protocol):
    """Protocol for entities that can be rendered."""
    
    def get_render_data(self) -> dict:
        """Return data needed for rendering."""
        ...


@runtime_checkable
class Updateable(Protocol):
    """Protocol for entities that need per-frame updates."""
    
    def update(self, dt: float) -> None:
        """Update entity state."""
        ...


@dataclass
class CollisionInfo:
    """Information about a detected collision."""
    
    entity_a: "Entity"
    entity_b: "Entity | Boundary"
    point: np.ndarray
    normal: np.ndarray
    penetration: float
    relative_velocity: float
    timestamp: float


class Entity(ABC):
    """Abstract base class for all simulation entities."""
    
    def __init__(self, id: str, position: np.ndarray, velocity: np.ndarray):
        self.id = id
        self.position = position.astype(np.float64)
        self.velocity = velocity.astype(np.float64)
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """Update entity state for one timestep."""
        pass
    
    @abstractmethod
    def get_render_data(self) -> dict:
        """Return data needed for rendering."""
        pass


class Boundary(ABC):
    """Abstract base class for all boundaries."""

    def __init__(
        self,
        id: str,
        color: str,
        thickness: float,
        is_containment: bool,
        hue_shift: str = "none",
        hue_shift_speed: float = 60.0,
        hue_shift_amount: float = 30.0
    ):
        self.id = id
        self.base_color = color
        self.color = color
        self.thickness = thickness
        self.is_containment = is_containment
        self.hue_shift = hue_shift
        self.hue_shift_speed = hue_shift_speed
        self.hue_shift_amount = hue_shift_amount
        self._hue_offset = 0.0

    def update(self, dt: float) -> None:
        """Update boundary state (color shifting)."""
        if self.hue_shift == "continuous":
            from ..math import shift_hue
            self._hue_offset += self.hue_shift_speed * dt
            self.color = shift_hue(self.base_color, self._hue_offset)

    def on_contact(self) -> None:
        """Called when a ball hits this boundary."""
        if self.hue_shift == "on_contact":
            from ..math import shift_hue
            self._hue_offset += self.hue_shift_amount
            self.color = shift_hue(self.base_color, self._hue_offset)

    @abstractmethod
    def contains_point(self, point: np.ndarray) -> bool:
        """Check if point is inside the boundary."""
        pass

    @abstractmethod
    def get_closest_point(self, point: np.ndarray) -> np.ndarray:
        """Get the closest point on the boundary to the given point."""
        pass

    @abstractmethod
    def get_normal_at(self, point: np.ndarray) -> np.ndarray:
        """Get the outward normal at a point on the boundary."""
        pass

    @abstractmethod
    def get_render_data(self) -> dict:
        """Return data needed for rendering."""
        pass
