"""ViewportUI class for user interface components."""

import dash
from dash import dcc, html
from typing import List


class ViewportUI:
    """User Interface Components for the Dash application."""
    
    def __init__(self, num_viewports: int = 6):
        """
        Initialize ViewportUI with specified number of viewports.
        
        Args:
            num_viewports: Number of viewport components to create (default: 6)
        """
        self.num_viewports = num_viewports
        self.image_displays: List[dcc.Graph] = []
        self.component_displays: List[dcc.Graph] = []
        self.weights_sliders: List[dcc.Slider] = []
        self.upload_components: List[dcc.Upload] = []
        self.progress_intervals: List[dcc.Interval] = []
        
        self._create_components()
    
    def _create_components(self) -> None:
        """Create all UI components for each viewport."""
        for i in range(self.num_viewports):
            # Image display graph
            self.image_displays.append(
                dcc.Graph(
                    id=f'image-display-{i}',
                    figure={'data': [], 'layout': {'title': f'Image {i+1}'}}
                )
            )
            
            # Component display graph (for magnitude, phase, etc.)
            self.component_displays.append(
                dcc.Graph(
                    id=f'component-display-{i}',
                    figure={'data': [], 'layout': {'title': f'Component {i+1}'}}
                )
            )
            
            # Weights slider
            self.weights_sliders.append(
                dcc.Slider(
                    id=f'weights-slider-{i}',
                    min=0,
                    max=1,
                    step=0.01,
                    value=0.5,
                    marks={i/10: str(i/10) for i in range(0, 11, 2)},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            )
            
            # Upload component
            self.upload_components.append(
                dcc.Upload(
                    id=f'upload-component-{i}',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Image')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    multiple=False
                )
            )
            
            # Progress interval
            self.progress_intervals.append(
                dcc.Interval(
                    id=f'progress-interval-{i}',
                    interval=1000,  # Update every second
                    n_intervals=0,
                    disabled=True
                )
            )
    
    def get_layout(self) -> html.Div:
        """
        Get the complete layout for all viewports.
        
        Returns:
            HTML Div containing all UI components
        """
        viewport_rows = []
        
        for i in range(self.num_viewports):
            viewport = html.Div([
                html.H3(f'Viewport {i+1}'),
                self.upload_components[i],
                html.Div([
                    html.Div([
                        html.Label('Image Display'),
                        self.image_displays[i]
                    ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
                    html.Div([
                        html.Label('Component Display'),
                        self.component_displays[i]
                    ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
                ]),
                html.Div([
                    html.Label('Weight'),
                    self.weights_sliders[i]
                ], style={'padding': '10px'}),
                self.progress_intervals[i]
            ], style={
                'border': '1px solid #ddd',
                'margin': '10px',
                'padding': '10px',
                'borderRadius': '5px'
            })
            
            viewport_rows.append(viewport)
        
        return html.Div([
            html.H1('Fourier Transform Mixer'),
            html.Div(viewport_rows)
        ])

