"""Main application file for the Fourier Transform Mixer."""

import dash
from dash import html
from ui.layouts.layout import Layout
from ui.callbacks.callbacks import Callbacks
from ui.styles import INDEX_STRING

app = dash.Dash(__name__, external_scripts=['/assets/double_click_upload.js'])
app.index_string = INDEX_STRING
app.layout = html.Div([Layout().get_layout()])
Callbacks(app)

if __name__ == '__main__':
    app.run(debug=True, port=8050)