"""Configuration loading and validation."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import yaml


class ConfigError(Exception):
    """Configuration file errors."""
    pass


@dataclass
class SimulationConfig:
    """Simulation timing settings."""
    duration_seconds: float
    substeps: int = 4


@dataclass
class OutputConfig:
    """Video output settings."""
    width: int
    height: int
    fps: int
    path: str
    codec: str = "libx264"
    bitrate: str = "8M"


@dataclass
class PhysicsConfig:
    """Physics engine settings."""
    gravity: list[float]
    integrator: str = "euler"


@dataclass
class BackgroundConfig:
    """Background rendering settings."""
    color: str


@dataclass
class BallConfig:
    """Individual ball configuration."""
    id: str
    radius: float
    color: str
    position: list[float]
    velocity: list[float]
    restitution: float = 0.9
    mass: float = 1.0
    # Color shifting
    hue_shift: str = "none"
    hue_shift_speed: float = 60.0
    hue_shift_amount: float = 30.0
    # Border
    outline: bool = False
    outline_color: str = "#ffffff"
    outline_thickness: float = 2.0
    # Glow
    glow: bool = False
    glow_radius: float = 20.0  # extra radius beyond ball edge
    glow_intensity: float = 0.5  # 0.0 to 1.0
    glow_color: str | None = None  # None = same as ball color


@dataclass
class BoundaryConfig:
    """Individual boundary configuration."""
    type: str
    id: str
    color: str
    thickness: float
    is_containment: bool
    # Circle-specific
    center: list[float] | None = None
    radius: float | None = None
    # Rectangle-specific
    x: float | None = None
    y: float | None = None
    width: float | None = None
    height: float | None = None
    # Color shifting
    hue_shift: str = "none"  # "none", "continuous", "on_contact"
    hue_shift_speed: float = 60.0
    hue_shift_amount: float = 30.0


@dataclass
class TrailConfig:
    """Trail system settings."""
    enabled: bool = False
    mode: str = "snapshot"  # "snapshot" or "particle"
    # Snapshot mode settings
    interval: float = 0.2
    max_count: int = 50
    max_age: float = 0.5
    spawn_rate: int = 2
    fade_curve: str = "exponential"
    size_decay: bool = True
    size_decay_factor: float = 0.3
    inherit_color: bool = True
    base_alpha: float = 0.7


@dataclass
class LoggingConfig:
    """Logging settings."""
    level: str = "INFO"
    file: str | None = None
    console: bool = True


@dataclass
class Config:
    """Complete simulation configuration."""
    simulation: SimulationConfig
    output: OutputConfig
    physics: PhysicsConfig
    background: BackgroundConfig
    balls: list[BallConfig]
    boundaries: list[BoundaryConfig]
    trails: TrailConfig = field(default_factory=TrailConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)


class ConfigLoader:
    """Loads and validates configuration from YAML files."""
    
    @staticmethod
    def load(path: str | Path) -> Config:
        """Load configuration from a YAML file."""
        path = Path(path)
        
        if not path.exists():
            raise ConfigError(f"Configuration file not found: {path}")
        
        with open(path, 'r') as f:
            raw = yaml.safe_load(f)
        
        ConfigLoader._validate(raw)
        return ConfigLoader._parse(raw)
    
    @staticmethod
    def _validate(raw: dict[str, Any]) -> None:
        """Validate required configuration sections."""
        required = ['simulation', 'output', 'physics', 'boundaries', 'balls']
        for key in required:
            if key not in raw:
                raise ConfigError(f"Missing required section: {key}")
        
        # Validate simulation
        sim = raw['simulation']
        if 'duration_seconds' not in sim:
            raise ConfigError("simulation.duration_seconds is required")
        
        # Validate output
        out = raw['output']
        for field in ['width', 'height', 'fps', 'path']:
            if field not in out:
                raise ConfigError(f"output.{field} is required")
        
        # Validate physics
        physics = raw['physics']
        if 'gravity' not in physics:
            raise ConfigError("physics.gravity is required")
        
        # Validate balls
        for i, ball in enumerate(raw['balls']):
            for field in ['id', 'radius', 'color', 'position', 'velocity']:
                if field not in ball:
                    raise ConfigError(f"Ball {i} missing required field: {field}")
        
        # Validate boundaries
        for i, boundary in enumerate(raw['boundaries']):
            for field in ['type', 'id', 'color', 'thickness', 'is_containment']:
                if field not in boundary:
                    raise ConfigError(f"Boundary {i} missing required field: {field}")
            
            if boundary['type'] == 'circle':
                if 'center' not in boundary or 'radius' not in boundary:
                    raise ConfigError(f"Circle boundary {i} requires 'center' and 'radius'")
            elif boundary['type'] == 'rectangle':
                for field in ['x', 'y', 'width', 'height']:
                    if field not in boundary:
                        raise ConfigError(f"Rectangle boundary {i} requires '{field}'")
    
    @staticmethod
    def _parse(raw: dict[str, Any]) -> Config:
        """Parse raw config dict into typed Config object."""
        simulation = SimulationConfig(
            duration_seconds=raw['simulation']['duration_seconds'],
            substeps=raw['simulation'].get('substeps', 4)
        )
        
        output = OutputConfig(
            width=raw['output']['width'],
            height=raw['output']['height'],
            fps=raw['output']['fps'],
            path=raw['output']['path'],
            codec=raw['output'].get('codec', 'libx264'),
            bitrate=raw['output'].get('bitrate', '8M')
        )
        
        physics = PhysicsConfig(
            gravity=raw['physics']['gravity'],
            integrator=raw['physics'].get('integrator', 'euler')
        )
        
        background = BackgroundConfig(
            color=raw.get('background', {}).get('color', '#000000')
        )

        balls = [
            BallConfig(
                id=b['id'],
                radius=b['radius'],
                color=b['color'],
                position=b['position'],
                velocity=b['velocity'],
                restitution=b.get('restitution', 0.9),
                mass=b.get('mass', 1.0),
                hue_shift=b.get('hue_shift', 'none'),
                hue_shift_speed=b.get('hue_shift_speed', 60.0),
                hue_shift_amount=b.get('hue_shift_amount', 30.0),
                outline=b.get('outline', False),
                outline_color=b.get('outline_color', '#ffffff'),
                outline_thickness=b.get('outline_thickness', 2.0),
                glow=b.get('glow', False),
                glow_radius=b.get('glow_radius', 20.0),
                glow_intensity=b.get('glow_intensity', 0.5),
                glow_color=b.get('glow_color', None)
            )
            for b in raw['balls']
        ]

        boundaries = [
            BoundaryConfig(
                type=b['type'],
                id=b['id'],
                color=b['color'],
                thickness=b['thickness'],
                is_containment=b['is_containment'],
                center=b.get('center'),
                radius=b.get('radius'),
                x=b.get('x'),
                y=b.get('y'),
                width=b.get('width'),
                height=b.get('height'),
                hue_shift=b.get('hue_shift', 'none'),
                hue_shift_speed=b.get('hue_shift_speed', 60.0),
                hue_shift_amount=b.get('hue_shift_amount', 30.0)
            )
            for b in raw['boundaries']
        ]

        trails_raw = raw.get('trails', {})
        trails = TrailConfig(
            enabled=trails_raw.get('enabled', False),
            mode=trails_raw.get('mode', 'snapshot'),
            interval=trails_raw.get('interval', 0.2),
            max_count=trails_raw.get('max_count', 50),
            max_age=trails_raw.get('max_age', 0.5),
            spawn_rate=trails_raw.get('spawn_rate', 2),
            fade_curve=trails_raw.get('fade_curve', 'exponential'),
            size_decay=trails_raw.get('size_decay', True),
            size_decay_factor=trails_raw.get('size_decay_factor', 0.3),
            inherit_color=trails_raw.get('inherit_color', True),
            base_alpha=trails_raw.get('base_alpha', 0.7)
        )
        
        logging_raw = raw.get('logging', {})
        logging = LoggingConfig(
            level=logging_raw.get('level', 'INFO'),
            file=logging_raw.get('file'),
            console=logging_raw.get('console', True)
        )
        
        return Config(
            simulation=simulation,
            output=output,
            physics=physics,
            background=background,
            balls=balls,
            boundaries=boundaries,
            trails=trails,
            logging=logging
        )
