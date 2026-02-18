"""Cairo-based renderer implementation."""

import math
import cairo
import numpy as np
from ..core.types import Boundary
from ..entities.ball import Ball
from ..entities.boundaries.circle_boundary import CircleBoundary
from ..entities.boundaries.rectangle_boundary import RectangleBoundary


def hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    """Convert hex color string to RGB tuple (0-1 range)."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b)


class CairoRenderer:
    """Renders simulation frames using Cairo."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.ctx = cairo.Context(self.surface)
        self.ctx.set_antialias(cairo.ANTIALIAS_BEST)
    
    def begin_frame(self) -> None:
        """Prepare for a new frame (clear surface)."""
        self.ctx.set_operator(cairo.OPERATOR_SOURCE)
        self.ctx.set_source_rgba(0, 0, 0, 1)
        self.ctx.paint()
        self.ctx.set_operator(cairo.OPERATOR_OVER)
    
    def render_background(self, color: str) -> None:
        """Render the background color."""
        r, g, b = hex_to_rgb(color)
        self.ctx.set_source_rgb(r, g, b)
        self.ctx.paint()
    
    def render_boundary(self, boundary: Boundary) -> None:
        """Render a boundary."""
        if isinstance(boundary, CircleBoundary):
            self._render_circle_boundary(boundary)
        elif isinstance(boundary, RectangleBoundary):
            self._render_rectangle_boundary(boundary)
    
    def _render_circle_boundary(self, boundary: CircleBoundary) -> None:
        """Render a circle boundary."""
        r, g, b = hex_to_rgb(boundary.color)
        
        self.ctx.arc(
            boundary.center[0],
            boundary.center[1],
            boundary.radius,
            0,
            2 * math.pi
        )
        self.ctx.set_source_rgb(r, g, b)
        self.ctx.set_line_width(boundary.thickness)
        self.ctx.stroke()
    
    def _render_rectangle_boundary(self, boundary: RectangleBoundary) -> None:
        """Render a rectangle boundary."""
        r, g, b = hex_to_rgb(boundary.color)
        
        self.ctx.rectangle(
            boundary.x,
            boundary.y,
            boundary.width,
            boundary.height
        )
        self.ctx.set_source_rgb(r, g, b)
        self.ctx.set_line_width(boundary.thickness)
        self.ctx.stroke()
    
    def render_ball(self, ball: Ball) -> None:
        """Render a ball."""
        r, g, b = hex_to_rgb(ball.color)
        
        # Draw filled circle
        self.ctx.arc(
            ball.position[0],
            ball.position[1],
            ball.radius,
            0,
            2 * math.pi
        )
        self.ctx.set_source_rgb(r, g, b)
        self.ctx.fill()

    def render_trail_particle(
            self,
            particle: "TrailParticle",
            fade_curve: str,
            size_decay: bool,
            size_decay_factor: float,
            mode: str = "snapshot"
    ) -> None:
        """Render a single trail particle."""
        r, g, b = hex_to_rgb(particle.color)

        if mode == "snapshot":
            alpha = particle.base_alpha  # constant, no fade
            radius = particle.radius  # constant, no shrink
        else:
            alpha = particle.get_alpha(fade_curve)
            radius = particle.get_radius(size_decay, size_decay_factor)

        self.ctx.arc(
            particle.position[0],
            particle.position[1],
            radius,
            0,
            2 * math.pi
        )
        self.ctx.set_source_rgba(r, g, b, alpha)
        self.ctx.fill()
    
    def end_frame(self) -> cairo.ImageSurface:
        """Finalize and return the frame surface."""
        return self.surface

    def render_frame(
            self,
            background_color: str,
            boundaries: list[Boundary],
            balls: list[Ball],
            trail_system: "TrailSystem | None" = None
    ) -> cairo.ImageSurface:
        """Render a complete frame."""
        self.begin_frame()
        self.render_background(background_color)

        for boundary in boundaries:
            self.render_boundary(boundary)

        # Render trails before balls (behind)
        if trail_system and trail_system.enabled:
            for particle in trail_system.get_particles():
                self.render_trail_particle(
                    particle,
                    trail_system.fade_curve,
                    trail_system.size_decay,
                    trail_system.size_decay_factor,
                    trail_system.mode
                )

        for ball in balls:
            self.render_ball(ball)

        return self.end_frame()
    
    def get_frame_as_array(self) -> np.ndarray:
        """Get the current frame as a numpy array (RGB format)."""
        # Get raw buffer data
        buf = self.surface.get_data()
        
        # Convert to numpy array (Cairo uses BGRA format)
        arr = np.ndarray(
            shape=(self.height, self.width, 4),
            dtype=np.uint8,
            buffer=buf
        ).copy()  # Copy because buffer is read-only
        
        # Convert BGRA to RGB
        rgb = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        rgb[:, :, 0] = arr[:, :, 2]  # R from B channel position
        rgb[:, :, 1] = arr[:, :, 1]  # G stays
        rgb[:, :, 2] = arr[:, :, 0]  # B from R channel position
        
        return rgb
