"""ImageModel class representing an individual image and its data."""

import base64
import io
import numpy as np
from PIL import Image
from typing import Tuple, Optional, Literal


class ImageModel:
    """Represents an individual image and its data."""
    
    def __init__(self):
        """Initialize ImageModel with empty data."""
        self._ndarray_raw_pixels: Optional[np.ndarray] = None
        self._ndarray_complex_arr: Optional[np.ndarray] = None
        self.shape: Tuple[int, ...] = ()
        self._ndarray_cached_magnitude: Optional[np.ndarray] = None
        self._ndarray_cached_phase: Optional[np.ndarray] = None
        self._ndarray_cached_real: Optional[np.ndarray] = None
        self._ndarray_cached_imag: Optional[np.ndarray] = None
    
    def load_from_contents(self, base64_string: str) -> None:
        """
        Load image data from a base64 string.
        
        Args:
            base64_string: Base64 encoded image string
        """
        # Decode base64 string
        header, encoded = base64_string.split(',', 1)
        image_data = base64.b64decode(encoded)
        
        # Load image using PIL
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to grayscale if needed
        if image.mode != 'L':
            image = image.convert('L')
        
        # Convert to numpy array
        self._ndarray_raw_pixels = np.array(image, dtype=np.float64)
        self.shape = self._ndarray_raw_pixels.shape
        
        # Reset cached data
        self._reset_cache()
    
    def resize(self, target_shape: Tuple[int, ...]) -> None:
        """
        Resize the image to a target shape.
        
        Args:
            target_shape: Target shape tuple (height, width)
        """
        if self._ndarray_raw_pixels is None:
            return
        
        # Resize using PIL
        image = Image.fromarray(self._ndarray_raw_pixels.astype(np.uint8))
        image = image.resize((target_shape[1], target_shape[0]), Image.Resampling.LANCZOS)
        
        # Update raw pixels and shape
        self._ndarray_raw_pixels = np.array(image, dtype=np.float64)
        self.shape = target_shape
        
        # Reset cached data
        self._reset_cache()
    
    def get_data(self, component_type: Literal['raw', 'magnitude', 'phase', 'real', 'imag']) -> np.ndarray:
        """
        Retrieve specific image data based on component type.
        
        Args:
            component_type: Type of component to retrieve ('raw', 'magnitude', 'phase', 'real', 'imag')
        
        Returns:
            NumPy array containing the requested component data
        """
        if self._ndarray_raw_pixels is None:
            raise ValueError("No image data loaded")
        
        if component_type == 'raw':
            return self._ndarray_raw_pixels.copy()
        
        # Compute FFT if not already computed
        if self._ndarray_complex_arr is None:
            self._compute_fft()
        
        if component_type == 'magnitude':
            if self._ndarray_cached_magnitude is None:
                self._ndarray_cached_magnitude = np.abs(self._ndarray_complex_arr)
            return self._ndarray_cached_magnitude.copy()
        
        elif component_type == 'phase':
            if self._ndarray_cached_phase is None:
                self._ndarray_cached_phase = np.angle(self._ndarray_complex_arr)
            return self._ndarray_cached_phase.copy()
        
        elif component_type == 'real':
            if self._ndarray_cached_real is None:
                self._ndarray_cached_real = np.real(self._ndarray_complex_arr)
            return self._ndarray_cached_real.copy()
        
        elif component_type == 'imag':
            if self._ndarray_cached_imag is None:
                self._ndarray_cached_imag = np.imag(self._ndarray_complex_arr)
            return self._ndarray_cached_imag.copy()
        
        else:
            raise ValueError(f"Unknown component type: {component_type}")
    
    def _compute_fft(self) -> None:
        """Private method to compute the Fast Fourier Transform."""
        if self._ndarray_raw_pixels is None:
            raise ValueError("No image data to compute FFT")
        
        self._ndarray_complex_arr = np.fft.fft2(self._ndarray_raw_pixels)
    
    def _apply_log_transform(self, data: np.ndarray) -> np.ndarray:
        """
        Private method to apply a log transform to data.
        
        Args:
            data: Input data array
        
        Returns:
            Log-transformed data
        """
        # Apply log transform with small epsilon to avoid log(0)
        return np.log(np.abs(data) + 1e-10)
    
    def _reset_cache(self) -> None:
        """Reset all cached data."""
        self._ndarray_complex_arr = None
        self._ndarray_cached_magnitude = None
        self._ndarray_cached_phase = None
        self._ndarray_cached_real = None
        self._ndarray_cached_imag = None

