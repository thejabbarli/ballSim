"""Trail system - manages trail snapshots or particles for all balls."""

from ..core.config_loader import TrailConfig
from ..entities.ball import Ball
from .trail_particle import TrailParticle


class TrailSystem:
    """Manages trails for all balls."""

    def __init__(self, config: TrailConfig):
        self.enabled = config.enabled
        self.mode = config.mode

        # Snapshot mode
        self.interval = config.interval
        self.max_count = config.max_count
        self._time_accumulators: dict[str, float] = {}  # ball_id -> time since last snapshot
        self._snapshots: dict[str, list[TrailParticle]] = {}  # ball_id -> list of snapshots

        # Particle mode
        self.max_age = config.max_age
        self.spawn_rate = config.spawn_rate
        self.fade_curve = config.fade_curve
        self.size_decay = config.size_decay
        self.size_decay_factor = config.size_decay_factor
        self.base_alpha = config.base_alpha
        self._particles: list[TrailParticle] = []

    def update(self, balls: list[Ball], dt: float) -> None:
        """Update trail system."""
        if not self.enabled:
            return

        if self.mode == "snapshot":
            self._update_snapshot(balls, dt)
        else:
            self._update_particle(balls, dt)

    def _update_snapshot(self, balls: list[Ball], dt: float) -> None:
        """Snapshot mode: spawn ghost at fixed intervals."""
        for ball in balls:
            # Initialize if new ball
            if ball.id not in self._time_accumulators:
                self._time_accumulators[ball.id] = 0.0
                self._snapshots[ball.id] = []

            self._time_accumulators[ball.id] += dt

            # Time to spawn a snapshot?
            if self._time_accumulators[ball.id] >= self.interval:
                self._time_accumulators[ball.id] = 0.0

                snapshot = TrailParticle(
                    position=ball.position,
                    color=ball.color,  # captures current color
                    radius=ball.radius,
                    max_age=float('inf'),  # never dies from age
                    base_alpha=0.5  # slightly transparent
                )
                self._snapshots[ball.id].append(snapshot)

                # Enforce max count (0 = unlimited)
                if self.max_count > 0 and len(self._snapshots[ball.id]) > self.max_count:
                    self._snapshots[ball.id].pop(0)  # remove oldest

    def _update_particle(self, balls: list[Ball], dt: float) -> None:
        """Particle mode: spawn fading particles every frame."""
        for ball in balls:
            for _ in range(self.spawn_rate):
                particle = TrailParticle(
                    position=ball.position,
                    color=ball.color,
                    radius=ball.radius,
                    max_age=self.max_age,
                    base_alpha=self.base_alpha
                )
                self._particles.append(particle)

        for particle in self._particles:
            particle.update(dt)

        self._particles = [p for p in self._particles if p.alive]

    def get_particles(self) -> list[TrailParticle]:
        """Get all trail elements for rendering."""
        if self.mode == "snapshot":
            # All snapshots from all balls, oldest first
            all_snapshots = []
            for snapshots in self._snapshots.values():
                all_snapshots.extend(snapshots)
            return all_snapshots
        else:
            return sorted(self._particles, key=lambda p: p.age, reverse=True)

    def clear(self) -> None:
        """Clear all trails."""
        self._particles.clear()
        self._snapshots.clear()
        self._time_accumulators.clear()
