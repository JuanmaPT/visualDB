"""
Scoodood is asking on [Discourse](https://discourse.holoviz.org/t/how-to-capture-the-click-event-on-plotly-plot-with-panel/1360)

How to capture the click event on Plotly plot with Panel?
"""

import numpy as np
from panel.template.react import ReactTemplate
import plotly.graph_objs as go
import plotly.express as px
import panel as pn
import pandas as pd
import os

pn.extension("plotly")
pn.config.sizing_mode = "stretch_width"


def create_plot():
    # Generate random 3D coordinates and attributes
    np.random.seed(42)
    num_points = 30
    x = np.concatenate([
        np.random.uniform(-5, -3, 10),  # Group 1
        np.random.uniform(1, 3, 10),    # Group 2
        np.random.uniform(6, 8, 10)     # Group 3
    ])
    y = np.random.uniform(-5, 5, num_points)
    z = np.random.uniform(0, 10, num_points)
    true_labels =  ["jeep"] * 10 + ["labrador"] * 10 + ["fountain"] * 10
    classified_labels = [""] * num_points  # Initialize classified labels
    image_paths = ["path_to_image_{}.jpg".format(i) for i in range(num_points)]

    # Create a DataFrame
    dataframe = {
        'x': x,
        'y': y,
        'z': z,
        'true_label': true_labels,
        'classified_label': classified_labels,
        'image_path': image_paths
    }
    df = pd.DataFrame(dataframe)

    # Define colors for each class
    colors = {
        "jeep": "red",
        "labrador": "blue",
        "fountain": "green"
    }

    # Create the 3D scatter plot
    fig = go.Figure(
        data = px.scatter_3d(df, x='x', y='y', z='z', color='true_label',
                            color_discrete_map=colors,
                            hover_name='true_label')
    )

    fig.update_layout(
        title="3D Scatter Plot",
        autosize=True
    )
    return fig





def create_layout(plot):

    plot_panel = pn.pane.Plotly(plot, config={"responsive": True}, sizing_mode="stretch_both")
    image_pane = pn.pane.JPG(object=None, height=400, width=400)

    settings_panel = plot_panel.controls(jslink=True)

    template = ReactTemplate(title="Decision Boundary Visualizer Alpha")
    template.sidebar.append(settings_panel)
    template.main[0:1, :] = image_pane
    template.main[2:4, :] = plot_panel
    return template, plot_panel, image_pane


def create_app():
    plot = create_plot()
    return create_layout(plot)


app, plot_panel, image_pane = create_app()


@pn.depends(plot_panel.param.click_data, watch=True)
def update_image(click_data):
    print('Helloooooooooo')
    print(click_data)
    if click_data is not None and 'points' in click_data:
        point_data = click_data['points'][0]
        point_number = point_data['pointNumber']
        hover_text = point_data['hovertext']
        if hover_text == 'jeep':
            image_filename = 'images\ILSVRC2012_val_00006062_n03594945.JPEG'
            print('1')
        if hover_text == 'labrador':
            image_filename = 'images\ILSVRC2012_val_00018107_n02106662.JPEG'
            print('2')
        else:
            image_filename = 'images\ILSVRC2012_val_00011075_n03388043.JPEG'
            print('3')
        if os.path.exists(image_filename):
            image_pane.object = image_filename
        else:
            image_pane.object = None
    else:
        image_pane.object = None



app.servable()