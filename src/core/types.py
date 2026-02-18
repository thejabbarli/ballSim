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
        is_containment: bool
    ):
        self.id = id
        self.color = color
        self.thickness = thickness
        self.is_containment = is_containment
    
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
