"""ViewportLayout class for layout components."""

from dash import html


class Layout:
    """Layout class for the Dash application viewport."""
    
    def __init__(self):
        """Initialize ViewportLayout with dark-themed layout."""
        pass
    
    def get_layout(self) -> html.Div:
        """
        Get the complete layout with dark theme and floating cards.
        
        Returns:
            HTML Div containing the main page layout
        """
        # Dark theme colors
        dark_bg = '#1a1a1a'
        card_bg = '#2d2d2d'
        card_border = '#404040'
        text_color = '#e0e0e0'
        
        # Card style
        card_style = {
            'backgroundColor': card_bg,
            'border': f'1px solid {card_border}',
            'borderRadius': '12px',
            'padding': '24px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)',
            'color': text_color,
            'margin': '8px',  # Reduced from 16px to decrease spacing between cards
        }
        
        # Left side container (75% width)
        left_container_style = {
            'width': '75%',
            'float': 'left',
            'display': 'flex',
            'flexDirection': 'column',
            'boxSizing': 'border-box',
        }
        
        # Right side container (25% width)
        right_container_style = {
            'width': '25%',
            'float': 'right',
            'display': 'flex',
            'flexDirection': 'column',
            'boxSizing': 'border-box',
        }
        
        # Row style for cards
        row_style = {
            'display': 'flex',
            'flexDirection': 'row',
            'width': '100%',
        }
        
        # Card height for left cards (each card in a row)
        # Calculate to fit within viewport: 100vh - padding (20px with 10px padding) - margins (32px total with 8px margins) divided by 2 rows
        # Reduced padding from 20px to 10px to make cards bigger
        # Total margin space: 8px top + 8px bottom (first row) + 8px gap + 8px bottom (second row) = 32px
        # Total: 20px padding + 32px margins = 52px
        card_height = 'calc((100vh - 52px) / 2)'
        card_margin = '8px'  # Reduced from 16px to decrease spacing
        # Right card height should match the bottom of left cards
        # Left cards total: 10px top padding + 8px top margin + card_height + 8px gap + card_height + 8px bottom margin + 10px bottom padding = 52px + 2*card_height = 100vh
        # Right card: 10px top padding + 8px top margin + right_card_height + 8px bottom margin + 10px bottom padding = 100vh
        # So: right_card_height = 100vh - 36px
        right_card_height = 'calc(100vh - 36px)'  # Aligned with bottom of left cards
        
        left_card_style = {
            **card_style,
            'flex': '1',
            'height': card_height,
        }
        
        # Right card style (tall card spanning 2 rows, aligned with bottom of left cards)
        right_card_style = {
            **card_style,
            'height': right_card_height,
            'marginTop': card_margin,
            'marginBottom': card_margin,
        }
        
        return html.Div([
            # Main container with dark background
            html.Div([
                # Left portion (75% width) - 4 cards in 2x2 grid
                html.Div([
                    # First row - 2 cards
                    html.Div([
                        html.Div([
                            html.H3('Card 1', style={'margin': '0 0 16px 0', 'color': text_color}),
                            html.P('Content for card 1', style={'color': text_color, 'opacity': '0.8'})
                        ], style=left_card_style),
                        html.Div([
                            html.H3('Card 2', style={'margin': '0 0 16px 0', 'color': text_color}),
                            html.P('Content for card 2', style={'color': text_color, 'opacity': '0.8'})
                        ], style=left_card_style),
                    ], style=row_style),
                    
                    # Second row - 2 cards
                    html.Div([
                        html.Div([
                            html.H3('Card 3', style={'margin': '0 0 16px 0', 'color': text_color}),
                            html.P('Content for card 3', style={'color': text_color, 'opacity': '0.8'})
                        ], style=left_card_style),
                        html.Div([
                            html.H3('Card 4', style={'margin': '0 0 16px 0', 'color': text_color}),
                            html.P('Content for card 4', style={'color': text_color, 'opacity': '0.8'})
                        ], style=left_card_style),
                    ], style=row_style),
                ], style=left_container_style),
                
                # Right portion (25% width) - 1 tall card
                html.Div([
                    html.Div([
                        html.H3('Card 5', style={'margin': '0 0 16px 0', 'color': text_color}),
                        html.P('Content for tall card', style={'color': text_color, 'opacity': '0.8'})
                    ], style=right_card_style),
                ], style=right_container_style),
                
                # Clear float
                html.Div(style={'clear': 'both'})
            ], style={
                'backgroundColor': dark_bg,
                'height': '100vh',
                'width': '100vw',
                'padding': '10px',  # Reduced from 20px to make cards bigger
                'fontFamily': 'Arial, sans-serif',
                'overflow': 'hidden',
                'boxSizing': 'border-box',
                'margin': '0',
                'position': 'fixed',
                'top': '0',
                'left': '0',
            })
        ], style={
            'margin': '0',
            'padding': '0',
            'overflow': 'hidden',
            'height': '100vh',
            'width': '100vw',
        })

