"""Individual trail particle."""

import numpy as np


class TrailParticle:
    """A single particle in a trail."""

    def __init__(
            self,
            position: np.ndarray,
            color: str,
            radius: float,
            max_age: float,
            base_alpha: float
    ):
        self.position = position.copy()
        self.color = color
        self.radius = radius
        self.max_age = max_age
        self.base_alpha = base_alpha
        self.age = 0.0

    @property
    def alive(self) -> bool:
        return self.age < self.max_age

    @property
    def life_ratio(self) -> float:
        """0.0 = just born, 1.0 = about to die."""
        return min(1.0, self.age / self.max_age)

    def update(self, dt: float) -> None:
        self.age += dt

    def get_alpha(self, fade_curve: str) -> float:
        """Get current alpha based on age and fade curve."""
        if fade_curve == "exponential":
            import math
            return self.base_alpha * math.exp(-3 * self.life_ratio)
        else:  # linear
            return self.base_alpha * (1.0 - self.life_ratio)

    def get_radius(self, size_decay: bool, size_decay_factor: float) -> float:
        """Get current radius, optionally decayed."""
        if size_decay:
            scale = 1.0 - (1.0 - size_decay_factor) * self.life_ratio
            return self.radius * scale
        return self.radius
