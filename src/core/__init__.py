"""Core module - types, config, and event system."""

from .types import Entity, Boundary, CollisionInfo, Renderable, Updateable
from .config_loader import Config, ConfigLoader, ConfigError
from .event_bus import EventBus, Event, CollisionEvent
from .simulation import Simulation

__all__ = [
    "Entity",
    "Boundary", 
    "CollisionInfo",
    "Renderable",
    "Updateable",
    "Config",
    "ConfigLoader",
    "ConfigError",
    "EventBus",
    "Event",
    "CollisionEvent",
    "Simulation",
]
