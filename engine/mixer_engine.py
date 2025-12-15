import numpy as np
from typing import Dict, Optional, List, Literal, Any, Callable
from models.image_model import ImageModel


class MixerEngine:
    """Performs image mixing and reconstruction using Fourier Transform components."""

    def __init__(self):
        pass

    def run_async_task(self, inputs: Dict[str, Any],
                       progress_callback: Optional[Callable[[float], None]] = None) -> np.ndarray:
        """
        Entry point for AsyncJobManager. Unpacks inputs and routes to mixing logic.
        """
        return self.mix_images_unified(
            mode=inputs.get('mode', 'mag_phase'),
            component1_sources=inputs.get('weights1', {}),
            component2_sources=inputs.get('weights2', {}),
            images=inputs.get('images', []),
            mask=inputs.get('mask'),
            progress_callback=progress_callback
        )

    def _perform_ifft(self, complex_ft: np.ndarray) -> np.ndarray:
        """
        Centralized IFFT method:
        - Undo shift (ifftshift)
        - Compute inverse FFT
        - Return real clipped image
        """
        # Undo shift applied to FFT before masking
        unshifted_ft = np.fft.ifftshift(complex_ft)

        # Inverse FFT
        result = np.fft.ifft2(unshifted_ft)
        result = np.real(result)
        result = np.clip(result, 0, 255)
        return result

    def mix_images_mag_phase(
            self,
            magnitude_sources: Dict[int, float],
            phase_sources: Dict[int, float],
            images: List[ImageModel],
            mask: Optional[np.ndarray] = None,
            progress_callback: Optional[Callable[[float], None]] = None
    ) -> np.ndarray:
        if not images:
            raise ValueError("No images provided")

        # Report: Started
        if progress_callback: progress_callback(0.1)

        shape = images[0].shape

        # 1. Mix Magnitudes - Direct multiplication without normalization
        mixed_magnitude = np.zeros(shape, dtype=np.float64)

        for idx, weight in magnitude_sources.items():
            if idx < len(images) and images[idx] is not None and weight != 0:
                mixed_magnitude += images[idx].get_data('magnitude') * weight

        # Report: Magnitude Done
        if progress_callback: progress_callback(0.4)

        # 2. Mix Phases - Direct multiplication without normalization
        mixed_phase = np.zeros(shape, dtype=np.float64)

        for idx, weight in phase_sources.items():
            if idx < len(images) and images[idx] is not None and weight != 0:
                mixed_phase += images[idx].get_data('phase') * weight

        # Report: Phase Done
        if progress_callback: progress_callback(0.7)

        # 3. Apply Mask
        if mask is not None:
            if mask.shape == shape:
                mixed_magnitude *= mask

        # 4. Reconstruct & IFFT
        complex_ft = mixed_magnitude * np.exp(1j * mixed_phase)

        # Report: Calculating IFFT
        if progress_callback: progress_callback(0.85)

        result = self._perform_ifft(complex_ft)

        # Report: Almost Done
        if progress_callback: progress_callback(0.95)

        return result

    def mix_images_real_imag(
            self,
            real_sources: Dict[int, float],
            imag_sources: Dict[int, float],
            images: List[ImageModel],
            mask: Optional[np.ndarray] = None,
            progress_callback: Optional[Callable[[float], None]] = None
    ) -> np.ndarray:
        if not images:
            raise ValueError("No images provided")

        if progress_callback: progress_callback(0.1)
        shape = images[0].shape

        # Mix Real - Direct multiplication without normalization
        mixed_real = np.zeros(shape, dtype=np.float64)
        for idx, weight in real_sources.items():
            if idx < len(images) and images[idx] is not None and weight != 0:
                mixed_real += images[idx].get_data('real') * weight

        if progress_callback: progress_callback(0.4)

        # Mix Imag - Direct multiplication without normalization
        mixed_imag = np.zeros(shape, dtype=np.float64)
        for idx, weight in imag_sources.items():
            if idx < len(images) and images[idx] is not None and weight != 0:
                mixed_imag += images[idx].get_data('imag') * weight

        if progress_callback: progress_callback(0.7)

        # Apply Mask
        if mask is not None and mask.shape == shape:
            mixed_real *= mask
            mixed_imag *= mask

        complex_ft = mixed_real + 1j * mixed_imag

        if progress_callback: progress_callback(0.85)

        return self._perform_ifft(complex_ft)

    def mix_images_unified(
            self,
            mode: Literal['mag_phase', 'real_imag'],
            component1_sources: Dict[int, float],
            component2_sources: Dict[int, float],
            images: List[ImageModel],
            mask: Optional[np.ndarray] = None,
            progress_callback: Optional[Callable[[float], None]] = None
    ) -> np.ndarray:
        if mode == 'mag_phase':
            return self.mix_images_mag_phase(component1_sources, component2_sources, images, mask, progress_callback)
        elif mode == 'real_imag':
            return self.mix_images_real_imag(component1_sources, component2_sources, images, mask, progress_callback)
        else:
            raise ValueError(f"Unknown mode: {mode}")

    # def create_region_mask(
    #         self,
    #         shape: tuple[int, int],
    #         rect_coords: Optional[tuple[int, int, int, int]] = None,
    #         is_inner: bool = True
    # ) -> np.ndarray:
    #     return self._region_handler.create_mask(shape, rect_coords, is_inner)