"""CSS styles for the Dash application."""

# Global CSS to prevent scrolling
INDEX_STRING = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
        
        <style>
            :root {
                --accent-color: #4CAF50;
                --bg-dark: #1a1a1a;
                --card-bg: #2d2d2d;
            }

            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }
            
            html, body {
                height: 100%;
                width: 100%;
                overflow: hidden;
                margin: 0;
                padding: 0;
                background-color: var(--bg-dark);
                color: #e0e0e0;
            }
            
            #react-entry-point {
                height: 100vh;
                width: 100vw;
                overflow: hidden;
            }

            /* --- Custom Scrollbar --- */
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: #1a1a1a; 
            }
            ::-webkit-scrollbar-thumb {
                background: #444; 
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #555; 
            }

            /* --- Slider Customization (Green Theme) --- */
            .rc-slider-track {
                background-color: var(--accent-color) !important;
            }
            .rc-slider-handle {
                border-color: var(--accent-color) !important;
                box-shadow: none !important;
            }
            .rc-slider-handle:hover {
                border-color: #66bb6a !important;
            }
            .rc-slider-handle:active {
                box-shadow: 0 0 5px var(--accent-color) !important;
            }
            .rc-slider-rail {
                background-color: #444 !important;
            }

            /* --- Upload Zone Hover Effect --- */
            .upload-zone {
                transition: all 0.3s ease;
                border: 1px dashed #555 !important;
            }
            .upload-zone:hover {
                border-color: var(--accent-color) !important;
                background-color: rgba(76, 175, 80, 0.1) !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''