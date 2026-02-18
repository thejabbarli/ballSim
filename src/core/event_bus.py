"""Event bus for pub/sub communication between systems."""

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Any
import numpy as np


@dataclass
class Event:
    """Base event class."""
    timestamp: float


@dataclass
class CollisionEvent(Event):
    """Emitted when a collision occurs."""
    ball: Any  # Ball type (avoiding circular import)
    other: Any  # Entity or Boundary
    point: np.ndarray
    normal: np.ndarray
    intensity: float  # relative velocity magnitude


class EventBus:
    """Simple pub/sub event system."""
    
    def __init__(self):
        self._subscribers: dict[type, list[Callable]] = defaultdict(list)
    
    def subscribe(self, event_type: type, handler: Callable[[Event], None]) -> None:
        """Subscribe a handler to an event type."""
        self._subscribers[event_type].append(handler)
    
    def unsubscribe(self, event_type: type, handler: Callable[[Event], None]) -> None:
        """Unsubscribe a handler from an event type."""
        if handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)
    
    def emit(self, event: Event) -> None:
        """Emit an event to all subscribers."""
        for handler in self._subscribers[type(event)]:
            handler(event)
