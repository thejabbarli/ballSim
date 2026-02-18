"""Main simulation orchestrator."""

import logging
import sys


# Try to import tqdm, fallback to simple progress bar
try:
    from tqdm import tqdm
except ImportError:
    # Simple fallback progress bar
    class tqdm:
        def __init__(self, total, desc="", unit=""):
            self.total = total
            self.desc = desc
            self.unit = unit
            self.n = 0
            self._last_percent = -1
        
        def __enter__(self):
            return self
        
        def __exit__(self, *args):
            print()  # Final newline
        
        def update(self, n=1):
            self.n += n
            percent = int(100 * self.n / self.total)
            if percent != self._last_percent:
                self._last_percent = percent
                bar_len = 40
                filled = int(bar_len * self.n / self.total)
                bar = '█' * filled + '░' * (bar_len - filled)
                print(f'\r{self.desc}: |{bar}| {percent}% ({self.n}/{self.total} {self.unit})', end='', flush=True)

from .config_loader import Config
from .event_bus import EventBus, CollisionEvent
from .types import Boundary
from ..entities.ball import Ball
from ..physics.physics_engine import PhysicsEngine
from ..physics.collision import CollisionDispatcher, CollisionResolver
from ..rendering.cairo_renderer import CairoRenderer
from ..export.video_exporter import VideoExporter


logger = logging.getLogger('ballsim.simulation')


class Simulation:
    """Main simulation orchestrator - coordinates all systems."""

    def __init__(
            self,
            config: Config,
            balls: list[Ball],
            boundaries: list[Boundary],
            physics_engine: PhysicsEngine,
            collision_dispatcher: CollisionDispatcher,
            collision_resolver: CollisionResolver,
            renderer: CairoRenderer,
            video_exporter: VideoExporter,
            event_bus: EventBus,
            trail_system: "TrailSystem"
    ):
        self.config = config
        self.balls = balls
        self.boundaries = boundaries
        self.physics_engine = physics_engine
        self.collision_dispatcher = collision_dispatcher
        self.collision_resolver = collision_resolver
        self.renderer = renderer
        self.video_exporter = video_exporter
        self.event_bus = event_bus
        self.trail_system = trail_system

        # Calculate timing
        self.duration = config.simulation.duration_seconds
        self.fps = config.output.fps
        self.substeps = config.simulation.substeps
        self.total_frames = int(self.duration * self.fps)
        self.frame_dt = 1.0 / self.fps
        self.physics_dt = self.frame_dt / self.substeps

        self.current_time = 0.0
        self.current_frame = 0
    
    def run(self) -> None:
        """Run the complete simulation."""
        logger.info(f"Starting simulation: {self.duration}s at {self.fps}fps ({self.total_frames} frames)")
        logger.info(f"Physics: {self.substeps} substeps/frame (dt={self.physics_dt:.6f}s)")
        
        # Main loop with progress bar
        with tqdm(total=self.total_frames, desc="Rendering", unit="frame") as pbar:
            for frame in range(self.total_frames):
                self._simulate_frame()
                self._render_frame()
                pbar.update(1)
        
        logger.info("Simulation complete. Encoding video...")
        self.video_exporter.finalize()
        logger.info(f"Video saved to: {self.video_exporter.path}")

    def _simulate_frame(self) -> None:
        """Run physics simulation for one frame (multiple substeps)."""
        for _ in range(self.substeps):
            # Update physics (gravity, integration)
            self.physics_engine.update(self.balls, self.physics_dt)

            # Update ball effects (color shifting)
            for ball in self.balls:
                ball.update(self.physics_dt)

            # Detect collisions
            collisions = self.collision_dispatcher.detect_all(
                self.balls,
                self.boundaries,
                self.current_time
            )

            # Resolve collisions
            for collision in collisions:
                self.collision_resolver.resolve(collision)

                # Trigger ball color change on bounce
                if isinstance(collision.entity_a, Ball):
                    collision.entity_a.on_collision()
                if isinstance(collision.entity_b, Ball):
                    collision.entity_b.on_collision()

                # Emit collision event
                if isinstance(collision.entity_a, Ball):
                    event = CollisionEvent(
                        timestamp=self.current_time,
                        ball=collision.entity_a,
                        other=collision.entity_b,
                        point=collision.point,
                        normal=collision.normal,
                        intensity=collision.relative_velocity
                    )
                    self.event_bus.emit(event)

            self.current_time += self.physics_dt

        # Update trails ONCE per frame, after physics
        self.trail_system.update(self.balls, self.frame_dt)

        self.current_frame += 1

    def _render_frame(self) -> None:
        """Render and export one frame."""
        self.renderer.render_frame(
            self.config.background.color,
            self.boundaries,
            self.balls,
            self.trail_system
        )

        frame_array = self.renderer.get_frame_as_array()
        self.video_exporter.write_frame(frame_array)
