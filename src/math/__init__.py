"""Math utilities module."""

from .vector2 import (
    vec2,
    from_list,
    magnitude,
    magnitude_squared,
    normalize,
    dot,
    distance,
    distance_squared,
    reflect,
    clamp,
    lerp,
)
from .color import hex_to_rgb, rgb_to_hex, shift_hue

__all__ = [
    "vec2",
    "from_list",
    "magnitude",
    "magnitude_squared",
    "normalize",
    "dot",
    "distance",
    "distance_squared",
    "reflect",
    "clamp",
    "lerp",
    "hex_to_rgb",
    "rgb_to_hex",
    "shift_hue",
]
