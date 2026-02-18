"""Video export using imageio-ffmpeg."""

import os
from datetime import datetime
from pathlib import Path
import numpy as np
import imageio_ffmpeg as ffmpeg
from ..core.config_loader import OutputConfig


def get_output_path(requested_path: str) -> str:
    """Get a unique output path, adding timestamp if file exists."""
    if not os.path.exists(requested_path):
        return requested_path
    
    base, ext = os.path.splitext(requested_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{timestamp}{ext}"


class VideoExporter:
    """Exports rendered frames to video using imageio-ffmpeg."""
    
    def __init__(self, config: OutputConfig):
        self.width = config.width
        self.height = config.height
        self.fps = config.fps
        self.codec = config.codec
        self.bitrate = config.bitrate
        
        # Ensure output directory exists
        output_dir = Path(config.path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.path = get_output_path(config.path)
        self._writer = None
        self._frame_count = 0
        
        # Start the ffmpeg writer process
        self._start_writer()
    
    def _start_writer(self) -> None:
        """Start the ffmpeg writer process."""
        self._writer = ffmpeg.write_frames(
            self.path,
            (self.width, self.height),
            fps=self.fps,
            codec=self.codec,
            pix_fmt_in='rgb24',
            pix_fmt_out='yuv420p',
            bitrate=self.bitrate,
        )
        self._writer.send(None)  # Initialize the generator
    
    def write_frame(self, frame: np.ndarray) -> None:
        """Write a frame to the video.
        
        Args:
            frame: RGB numpy array of shape (height, width, 3)
        """
        if self._writer is None:
            raise RuntimeError("Writer not initialized")
        
        # Ensure frame is contiguous and correct type
        frame = np.ascontiguousarray(frame, dtype=np.uint8)
        self._writer.send(frame)
        self._frame_count += 1
    
    def finalize(self) -> None:
        """Finalize the video file."""
        if self._writer is not None:
            self._writer.close()
            self._writer = None
    
    @property
    def frame_count(self) -> int:
        """Return the number of frames written."""
        return self._frame_count
