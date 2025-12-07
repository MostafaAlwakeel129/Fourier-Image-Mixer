"""RegionHandler class for handling creation of image masks."""

import numpy as np
from typing import Tuple, Optional


class RegionHandler:
    """Handles creation of image masks for region selection."""
    
    def create_mask(self, shape: Tuple[int, ...], rect_coords: Optional[Tuple[int, int, int, int]] = None, is_inner: bool = True) -> np.ndarray:
        """
        Create a mask based on shape, rectangular coordinates, and whether it's an inner or outer mask.
        
        Args:
            shape: Shape of the mask (height, width)
            rect_coords: Optional tuple of (x1, y1, x2, y2) defining rectangular region.
                        If None, returns a mask of all ones.
            is_inner: If True, mask is 1 inside the rectangle and 0 outside.
                     If False, mask is 0 inside the rectangle and 1 outside.
        
        Returns:
            NumPy array of shape 'shape' with mask values (0 or 1)
        """
        mask = np.ones(shape, dtype=np.float64)
        
        if rect_coords is None:
            return mask
        
        x1, y1, x2, y2 = rect_coords
        
        # Ensure coordinates are within bounds
        x1 = max(0, min(x1, shape[1] - 1))
        y1 = max(0, min(y1, shape[0] - 1))
        x2 = max(0, min(x2, shape[1] - 1))
        y2 = max(0, min(y2, shape[0] - 1))
        
        # Ensure x1 < x2 and y1 < y2
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        
        if is_inner:
            # Inner mask: 1 inside rectangle, 0 outside
            mask[y1:y2+1, x1:x2+1] = 1.0
            mask[:y1, :] = 0.0
            mask[y2+1:, :] = 0.0
            mask[:, :x1] = 0.0
            mask[:, x2+1:] = 0.0
        else:
            # Outer mask: 0 inside rectangle, 1 outside
            mask[y1:y2+1, x1:x2+1] = 0.0
        
        return mask

