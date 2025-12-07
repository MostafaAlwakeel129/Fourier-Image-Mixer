"""Main DashApplication class for the Fourier Transform Mixer."""

import dash
from dash import html
from ui.viewport_ui import ViewportUI
from controllers.controller import Controller
from engine.async_job_manager import AsyncJobManager


class DashApplication:
    """Top-level Dash application for image processing."""
    
    def __init__(self):
        """Initialize DashApplication with layout and components."""
        self.app = dash.Dash(__name__)
        self.layout = ViewportUI(num_viewports=6)
        self.image_controller = Controller()
        self.async_job_manager = AsyncJobManager()
        
        # Set app layout
        self.app.layout = html.Div([
            self.layout.get_layout()
        ])
        
        # Register callbacks
        self.register_callbacks()
    
    def register_callbacks(self) -> None:
        """Register interactive callbacks for the Dash application."""
        from dash.dependencies import Input, Output, State
        from functools import partial
        
        # Register upload callbacks for each viewport
        for i in range(self.layout.num_viewports):
            # Create closure to capture viewport index
            def make_upload_callback(viewport_idx):
                @self.app.callback(
                    Output(f'image-display-{viewport_idx}', 'figure'),
                    Input(f'upload-component-{viewport_idx}', 'contents'),
                    prevent_initial_call=True
                )
                def update_image_display(contents):
                    """Update image display when image is uploaded."""
                    if contents is None:
                        return {'data': [], 'layout': {'title': f'Image {viewport_idx+1}'}}
                    
                    # Handle upload
                    result = self.image_controller.handle_upload(contents, viewport_idx)
                    
                    if result['status'] == 'success':
                        # Get plotting data
                        fig = self.image_controller.get_plotting_data(viewport_idx, 'raw')
                        return fig if fig else {'data': [], 'layout': {'title': f'Image {viewport_idx+1}'}}
                    else:
                        return {'data': [], 'layout': {'title': f'Error: {result.get("message", "Unknown error")}'}}
                
                return update_image_display
            
            make_upload_callback(i)
            
            # Create closure for component display callback
            def make_component_callback(viewport_idx):
                @self.app.callback(
                    Output(f'component-display-{viewport_idx}', 'figure'),
                    Input(f'image-display-{viewport_idx}', 'figure'),
                    prevent_initial_call=True
                )
                def update_component_display(image_fig):
                    """Update component display based on image."""
                    if image_fig is None or not image_fig.get('data'):
                        return {'data': [], 'layout': {'title': f'Component {viewport_idx+1}'}}
                    
                    # Show magnitude component by default
                    fig = self.image_controller.get_plotting_data(viewport_idx, 'magnitude')
                    return fig if fig else {'data': [], 'layout': {'title': f'Component {viewport_idx+1}'}}
                
                return update_component_display
            
            make_component_callback(i)
            
            # Create closure for slider callback
            def make_slider_callback(viewport_idx):
                @self.app.callback(
                    Output(f'progress-interval-{viewport_idx}', 'disabled'),
                    Input(f'weights-slider-{viewport_idx}', 'value'),
                    prevent_initial_call=True
                )
                def handle_slider_update(value):
                    """Handle slider updates and trigger mixing if needed."""
                    result = self.image_controller.handle_slider_update(value, viewport_idx)
                    
                    # If multiple images are loaded, trigger mixing job
                    session = self.image_controller.get_session()
                    if session.get_image_count() > 1:
                        # Prepare inputs for mixing
                        images = session.get_all_images()
                        weights_dict = {idx: value if idx == viewport_idx else 0.5 
                                       for idx in range(len(images))}
                        
                        # Start async mixing job
                        inputs = {
                            'images': images,
                            'weights_dict': weights_dict,
                            'mask': None
                        }
                        
                        def mixing_callback(result):
                            """Callback when mixing completes."""
                            # Update displays with result
                            pass
                        
                        self.async_job_manager.start_mixing_job(inputs, mixing_callback)
                    
                    return False  # Enable progress interval
                
                return handle_slider_update
            
            make_slider_callback(i)
    
    def run_server(self, debug: bool = True, port: int = 8050) -> None:
        """
        Start the Dash application server.
        
        Args:
            debug: Enable debug mode
            port: Port number to run the server on
        """
        self.app.run(debug=debug, port=port)


if __name__ == '__main__':
    app = DashApplication()
    app.run_server(debug=True)

