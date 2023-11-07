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
    description_panel = pn.layout.Card(
        __doc__, header="# How to capture Plotly Click Events?", sizing_mode="stretch_both"
    )
    plot_panel = pn.pane.Plotly(plot, config={"responsive": True}, sizing_mode="stretch_both")
    settings_panel = plot_panel.controls(jslink=True)

    template = ReactTemplate(title="Decision Boundary Visualizer Alpha")
    template.sidebar.append(settings_panel)
    template.main[0, :] = description_panel
    template.main[1:4, :] = plot_panel
    return template


def create_app():
    plot = create_plot()
    return create_layout(plot)


app = create_app()
app.servable()