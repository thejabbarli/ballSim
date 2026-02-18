"""Color manipulation utilities."""

import colorsys


def hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    """Convert hex color to RGB (0-1 range)."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b)


def rgb_to_hex(r: float, g: float, b: float) -> str:
    """Convert RGB (0-1 range) to hex color."""
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def shift_hue(hex_color: str, degrees: float) -> str:
    """Shift the hue of a color by given degrees."""
    r, g, b = hex_to_rgb(hex_color)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h = (h + degrees / 360.0) % 1.0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return rgb_to_hex(r, g, b)
