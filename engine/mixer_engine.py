"""MixerEngine class for performing image mixing and reconstruction."""

import numpy as np
from typing import Dict, Optional, List
from models.image_model import ImageModel
from utils.region_handler import RegionHandler


class MixerEngine:
    """Performs image mixing and reconstruction using Fourier Transform components."""
    
    def __init__(self):
        """Initialize MixerEngine with RegionHandler."""
        self._region_handler = RegionHandler()
    
    def mix_images(self, images: List[ImageModel], weights_dict: Dict[int, float], mask: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Mix multiple images using specified weights and an optional mask.
        
        Args:
            images: List of ImageModel instances to mix
            weights_dict: Dictionary mapping image index to weight value
            mask: Optional mask array for region-based mixing
        
        Returns:
            NumPy array representing the mixed image
        """
        if not images:
            raise ValueError("No images provided for mixing")
        
        if not weights_dict:
            raise ValueError("No weights provided for mixing")
        
        # Get the shape from the first image
        shape = images[0].shape
        
        # Initialize mixed components
        mixed_magnitude = np.zeros(shape, dtype=np.complex128)
        mixed_phase = np.zeros(shape, dtype=np.complex128)
        
        # Normalize weights
        total_weight = sum(weights_dict.values())
        if total_weight == 0:
            total_weight = 1.0
        
        # Mix magnitude and phase components
        for idx, image in enumerate(images):
            if idx not in weights_dict:
                continue
            
            weight = weights_dict[idx] / total_weight
            
            # Get magnitude and phase
            magnitude = image.get_data('magnitude')
            phase = image.get_data('phase')
            
            # Apply weights
            weighted_magnitude = self._apply_weights(magnitude, weight)
            weighted_phase = self._apply_weights(phase, weight)
            
            # Accumulate
            mixed_magnitude += weighted_magnitude
            mixed_phase += weighted_phase
        
        # Apply mask if provided
        if mask is not None:
            if mask.shape != shape:
                raise ValueError(f"Mask shape {mask.shape} does not match image shape {shape}")
            mixed_magnitude *= mask
            mixed_phase *= mask
        
        # Reconstruct complex array from magnitude and phase
        complex_data = self._reconstruct_complex(mixed_magnitude, mixed_phase)
        
        # Perform inverse FFT
        result = self._perform_ifft(complex_data)
        
        # Normalize to valid image range
        result = np.real(result)
        result = np.clip(result, 0, 255)
        
        return result
    
    def _apply_weights(self, component: np.ndarray, weight: float) -> np.ndarray:
        """
        Apply weights to an image component.
        
        Args:
            component: Image component array (magnitude, phase, etc.)
            weight: Weight value to apply
        
        Returns:
            Weighted component array
        """
        return component * weight
    
    def _reconstruct_complex(self, mag: np.ndarray, phase: np.ndarray) -> np.ndarray:
        """
        Reconstruct complex data from magnitude and phase.
        
        Args:
            mag: Magnitude array
            phase: Phase array
        
        Returns:
            Complex array
        """
        return mag * np.exp(1j * phase)
    
    def _perform_ifft(self, complex_data: np.ndarray) -> np.ndarray:
        """
        Perform the Inverse Fast Fourier Transform.
        
        Args:
            complex_data: Complex frequency domain data
        
        Returns:
            Spatial domain image data
        """
        return np.fft.ifft2(complex_data)

