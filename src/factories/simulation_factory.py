"""Factory for creating simulation instances from config."""

import logging
from pathlib import Path
from ..trails import TrailSystem

from ..core.config_loader import Config, ConfigLoader
from ..core.event_bus import EventBus
from ..core.simulation import Simulation
from ..entities.ball import Ball
from ..entities.boundaries.circle_boundary import CircleBoundary
from ..entities.boundaries.rectangle_boundary import RectangleBoundary
from ..physics.physics_engine import PhysicsEngine
from ..physics.collision import CollisionDispatcher, CollisionResolver
from ..rendering.cairo_renderer import CairoRenderer
from ..export.video_exporter import VideoExporter


def setup_logging(config: Config) -> None:
    """Configure logging based on config."""
    logger = logging.getLogger('ballsim')
    logger.setLevel(getattr(logging, config.logging.level))
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
    )
    
    if config.logging.file:
        log_dir = Path(config.logging.file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(config.logging.file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    if config.logging.console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


class SimulationFactory:
    """Creates fully assembled Simulation instances from config."""
    
    @staticmethod
    def create_from_config(config_path: str | Path) -> Simulation:
        """Create a complete simulation from a config file.
        
        Args:
            config_path: Path to the YAML configuration file
            
        Returns:
            Fully assembled Simulation instance
        """
        # Load config
        config = ConfigLoader.load(config_path)
        
        # Setup logging
        setup_logging(config)
        
        logger = logging.getLogger('ballsim.factory')
        logger.info(f"Creating simulation from: {config_path}")
        
        # Create event bus (shared)
        event_bus = EventBus()
        
        # Create balls
        balls = [Ball.from_config(b) for b in config.balls]
        logger.info(f"Created {len(balls)} ball(s)")
        
        # Create boundaries
        boundaries = []
        for b in config.boundaries:
            if b.type == "circle":
                boundaries.append(CircleBoundary.from_config(b))
            elif b.type == "rectangle":
                boundaries.append(RectangleBoundary.from_config(b))
            else:
                logger.warning(f"Unknown boundary type: {b.type}")
        logger.info(f"Created {len(boundaries)} boundary(ies)")
        
        # Create physics engine
        physics_engine = PhysicsEngine(config.physics)
        
        # Create collision system
        collision_dispatcher = CollisionDispatcher()
        collision_resolver = CollisionResolver()
        
        # Create renderer
        renderer = CairoRenderer(config.output.width, config.output.height)
        
        # Create video exporter
        video_exporter = VideoExporter(config.output)

        # Create trail system
        trail_system = TrailSystem(config.trails)

        # Assemble simulation
        return Simulation(
            config=config,
            balls=balls,
            boundaries=boundaries,
            physics_engine=physics_engine,
            collision_dispatcher=collision_dispatcher,
            collision_resolver=collision_resolver,
            renderer=renderer,
            video_exporter=video_exporter,
            trail_system=trail_system,
            event_bus=event_bus
        )
