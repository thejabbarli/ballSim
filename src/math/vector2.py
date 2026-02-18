"""2D vector math utilities backed by numpy."""

import numpy as np
from typing import Sequence


def vec2(x: float, y: float) -> np.ndarray:
    """Create a 2D vector."""
    return np.array([x, y], dtype=np.float64)


def from_list(coords: Sequence[float]) -> np.ndarray:
    """Create a vector from a list or tuple."""
    return np.array(coords, dtype=np.float64)


def magnitude(v: np.ndarray) -> float:
    """Calculate the magnitude (length) of a vector."""
    return float(np.linalg.norm(v))


def magnitude_squared(v: np.ndarray) -> float:
    """Calculate the squared magnitude of a vector (faster, no sqrt)."""
    return float(np.dot(v, v))


def normalize(v: np.ndarray) -> np.ndarray:
    """Return a unit vector in the same direction. Returns zero vector if input is zero."""
    mag = magnitude(v)
    if mag < 1e-10:
        return vec2(0.0, 0.0)
    return v / mag


def dot(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate the dot product of two vectors."""
    return float(np.dot(a, b))


def distance(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate the distance between two points."""
    return magnitude(b - a)


def distance_squared(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate the squared distance between two points (faster, no sqrt)."""
    diff = b - a
    return magnitude_squared(diff)


def reflect(v: np.ndarray, normal: np.ndarray) -> np.ndarray:
    """Reflect vector v around a normal."""
    return v - 2.0 * dot(v, normal) * normal


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(max_val, value))


def lerp(a: np.ndarray, b: np.ndarray, t: float) -> np.ndarray:
    """Linear interpolation between two vectors."""
    return a + (b - a) * t
