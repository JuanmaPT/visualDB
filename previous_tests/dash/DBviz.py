import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Create a Dash app
app = dash.Dash(__name__)

# Sample data with image file paths
data = [
    {'x': 1, 'y': 2, 'z': 3, 'details': 'Point 1 Details', 'image_path': 'images\ILSVRC2012_val_00006062_n03594945.JPEG'},
    {'x': 2, 'y': 3, 'z': 1, 'details': 'Point 2 Details', 'image_path': 'images\ILSVRC2012_val_00011075_n03388043.JPEG'},
    {'x': 3, 'y': 1, 'z': 2, 'details': 'Point 3 Details', 'image_path': 'images\ILSVRC2012_val_00018107_n02106662.JPEG'},
    # Add more data points here with associated image file paths
]

# Create the 3D scatter plot using Plotly Express
fig = px.scatter_3d(data_frame=data, x='x', y='y', z='z', text='details', title='3D Scatter Plot')

# Define the app layout
app.layout = html.Div([
    # First column with data selection controls
    html.Div([
        # Add buttons and sliders here to control data selection
        # You can use dcc.Button and dcc.Slider components
    ], style={'width': '30%', 'display': 'inline-block'}),

    # Center column with 3D scatter plot
    html.Div([
        dcc.Graph(figure=fig, id='scatter-plot')
    ], style={'width': '40%', 'display': 'inline-block'}),

    # Third column for displaying details and selected image
    html.Div([
        html.Div(id='selected-point-details'),
        html.Img(id='selected-image', src='', style={'max-width': '100%'})
    ], style={'width': '30%', 'display': 'inline-block'})
])

# Define callback to update the details and image of the selected point
@app.callback(
    [Output('selected-point-details', 'children'), Output('selected-image', 'src')],
    [Input('scatter-plot', 'selectedData')]
)
def update_selected_point(selectedData):
    if selectedData is not None and 'points' in selectedData:
        selected_indices = [point['pointIndex'] for point in selectedData['points']]
        if selected_indices:
            # For simplicity, take the first selected point
            selected_point = data[selected_indices[0]]
            details = selected_point['details']
            image_path = selected_point['image_path']
            return f'Selected Point Details: {details}', image_path
    return '', ''

if __name__ == '__main__':
    app.run_server(debug=True)
