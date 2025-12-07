"""UnitUnificator class for ensuring consistent image sizing."""

from typing import List, Tuple
from models.global_session_state import GlobalSessionState
from models.image_model import ImageModel


class UnitUnificator:
    """Ensures consistent image sizing across all images in a session."""
    
    def enforce_unified_size(self, state: GlobalSessionState) -> None:
        """
        Enforce a unified size across images in the given state.
        
        Args:
            state: GlobalSessionState instance containing images
        """
        images = state.get_all_images()
        
        if not images:
            return
        
        # Find minimum dimensions
        min_shape = self._find_min_dimensions(images)
        
        # Update state's min_shape
        state.update_min_shape(min_shape)
        
        # Resize all images to minimum dimensions
        for image in images:
            if image.shape != min_shape:
                image.resize(min_shape)
    
    def _find_min_dimensions(self, images: List[ImageModel]) -> Tuple[int, int]:
        """
        Find the minimum dimensions among a set of images.
        
        Args:
            images: List of ImageModel instances
        
        Returns:
            Tuple of (min_height, min_width)
        """
        if not images:
            raise ValueError("Cannot find min dimensions of empty image list")
        
        min_height = min(img.shape[0] for img in images)
        min_width = min(img.shape[1] for img in images)
        
        return (min_height, min_width)

