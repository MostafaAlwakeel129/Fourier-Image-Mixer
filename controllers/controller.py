"""Controller class for handling UI interactions and data flow."""

from typing import Optional, Dict, Any, Literal
import numpy as np
import plotly.graph_objs as go
from models.global_session_state import GlobalSessionState
from models.image_model import ImageModel
from utils.unit_unificator import UnitUnificator


class Controller:
    """Handles UI interactions and data flow."""
    
    def __init__(self):
        """Initialize Controller with session state and unificator."""
        self._session: GlobalSessionState = GlobalSessionState()
        self._unificator: UnitUnificator = UnitUnificator()
    
    def handle_upload(self, contents: str, index: int) -> Dict[str, Any]:
        """
        Handle image uploads.
        
        Args:
            contents: Base64 encoded image content
            index: Index of the viewport where image is uploaded
        
        Returns:
            Dictionary with status and any error messages
        """
        try:
            if contents is None:
                return {'status': 'error', 'message': 'No content provided'}
            
            # Create new ImageModel and load from contents
            image_model = ImageModel()
            image_model.load_from_contents(contents)
            
            # Store in session
            self._session.store_image(index, image_model)
            
            # Enforce unified size across all images
            self._unificator.enforce_unified_size(self._session)
            
            return {'status': 'success', 'message': f'Image {index+1} uploaded successfully'}
        
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def handle_slider_update(self, val: float, index: int) -> Dict[str, Any]:
        """
        Handle updates from sliders.
        
        Args:
            val: New slider value (weight)
            index: Index of the viewport/slider
        
        Returns:
            Dictionary with status
        """
        # Slider updates are typically handled by callbacks
        # This method can be used for validation or preprocessing
        if val < 0 or val > 1:
            return {'status': 'error', 'message': 'Weight must be between 0 and 1'}
        
        return {'status': 'success', 'value': val}
    
    def get_plotting_data(self, index: int, mode: Literal['raw', 'magnitude', 'phase', 'real', 'imag'] = 'raw') -> Optional[go.Figure]:
        """
        Retrieve data for plotting based on index and mode.
        
        Args:
            index: Index of the image to plot
            mode: Type of component to display ('raw', 'magnitude', 'phase', 'real', 'imag')
        
        Returns:
            Plotly Figure object or None if no image at index
        """
        image_model = self._session.get_image(index)
        
        if image_model is None:
            return None
        
        try:
            data = image_model.get_data(mode)
            
            # Normalize data for display
            if mode in ['magnitude', 'real', 'imag']:
                # Apply log transform for better visualization
                data = np.log(np.abs(data) + 1e-10)
            
            # Create heatmap figure
            fig = go.Figure(data=go.Heatmap(
                z=data,
                colorscale='gray',
                showscale=True
            ))
            
            fig.update_layout(
                title=f'Image {index+1} - {mode.capitalize()}',
                xaxis_title='Width',
                yaxis_title='Height',
                autosize=True
            )
            
            return fig
        
        except Exception as e:
            # Return empty figure on error
            return go.Figure()
    
    def get_session(self) -> GlobalSessionState:
        """
        Get the session state.
        
        Returns:
            GlobalSessionState instance
        """
        return self._session
    
    def get_all_weights(self) -> Dict[int, float]:
        """
        Get all current weights (placeholder - would be managed by callbacks).
        
        Returns:
            Dictionary mapping index to weight value
        """
        # This would typically be managed by Dash callbacks
        # Returning empty dict as placeholder
        return {}

