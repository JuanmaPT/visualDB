"""
Scoodood is asking on [Discourse](https://discourse.holoviz.org/t/how-to-capture-the-click-event-on-plotly-plot-with-panel/1360)

How to capture the click event on Plotly plot with Panel?
"""

import numpy as np
from panel.template.react import ReactTemplate
import plotly.graph_objs as go
import plotly.express as px
import panel as pn

import os

from DataLoader import *

from DataLoader import *

pn.extension("plotly")
pn.config.sizing_mode = "stretch_width"

# initialize data 

path_dir_data=  "DataExtraction/Results/MexCulture142_Keras/" 
path_dataset="Datasets/MexCulture142_Keras/"    
selected_distribution = "All"
selected_predictions = "Correct Predictions"
#selected_predictions = "All"

data = DataLoader(path_dir_data,
                  path_dataset,
                  selected_distribution, 
                  #selected_predictions)
)


df= data.df

# Callback function to update the plot and data when the widgets are changed
def update_plot_and_data(event):
    selected_distribution = distribution_selector.value
    selected_predictions = prediction_selector.value 
    print(selected_distribution,selected_predictions)

    data = DataLoader(path_dir_data,
                  path_dataset,
                  selected_distribution, 
                 )

    plot_panel.object = create_plot(data.df).to_plotly_json()
    image_pane.object = None  # Reset image when widgets change


# widget declaration 
distribution_selector = pn.widgets.Select(options=["Train", "Validation","All"], name="Select Distribution")
dataset_selector = pn.widgets.Select(options=["MexCulture"], name="Select Datasets")
#class_selector = pn.widgets.Select(options=["0", "1", "2"], name="Select Classes")
prediction_selector = pn.widgets.Select(options=["Correct Predictions", "Incorrect Predictions", "All"], name="Select")



# Callbacks for widget changes
distribution_selector.param.watch(update_plot_and_data, "value")
dataset_selector.param.watch(update_plot_and_data, "value")
#class_selector.param.watch(update_plot_and_data, "value")
prediction_selector.param.watch(update_plot_and_data, "value")


def create_plot(df):
    df['true_label'] = df['true_label'].apply(data.id2label)
    df['classified_label']= df['classified_label'].apply(data.id2label)

    hover_text = (
        'True: ' + df['true_label'] +
        '<br>Prediction: ' + df['classified_label'] +
        '<br>Score: ' + df['score'].astype(str)
    )

    # Define colors for each class
    colors = {
        data.id2label("0"): "red",
        data.id2label("1"): "blue",
        data.id2label("2"): "green"
    }

  
    # Set opacity based on selected distribution
    df['opacity'] = 1.0
    # Update opacity based on selected distribution
    if prediction_selector.value == "Correct Predictions":
        df.loc[df['true_label'] != df['classified_label'], 'opacity'] = 0.3
    elif prediction_selector.value == "Incorrect Predictions":
        df.loc[df['true_label'] == df['classified_label'], 'opacity'] = 0.3
    

    # Create the 3D scatter plot
    fig = go.Figure(
        data=px.scatter_3d(
            df, x='x', y='y', z='z',
            color='true_label',
            color_discrete_map= colors,
            custom_data=[hover_text], 
           
        )
    )

    fig.update_layout(
        title="3D Scatter Plot",
        autosize=True,
        width=1200,
        height=1000
    ) 

    # Update click events to display custom hover text
    fig.update_traces(
        marker=dict(size=5),
        hovertemplate='%{customdata[0]}<extra></extra>',
        
    )

    return fig


def create_layout(plot):
    plot_panel = pn.pane.Plotly(plot, config={"responsive": True})
    image_panel = pn.pane.PNG(object=None, height=400, width=400) 

    settings_panel = pn.WidgetBox(
        dataset_selector,
        distribution_selector,
        prediction_selector,
  
    )  
    
    template = ReactTemplate(title="Decision Boundary Visualizer Alpha")
    template.sidebar.append(settings_panel)
    template.main[:3, :6] = plot_panel
    template.main[:3, 9:] = image_panel
    return template, plot_panel, image_panel


def create_app():
    df = data.df
    plot = create_plot(df)
    return create_layout(plot)


app, plot_panel, image_panel = create_app()


@pn.depends(plot_panel.param.click_data, watch=True)
def update_image(click_data):
    print(click_data)
    if click_data is not None and 'points' in click_data:
        point_data = click_data['points'][0]
        print(point_data)
        idx = df.loc[(df['x'] == point_data['x']) & (df['y'] == point_data['y']) & (df['z'] == point_data['z'])]
        image_filename = idx['image_path'].tolist()[0]
        image_filename=  image_filename.replace("/", "\\")
        #image_filename=  image_filename.replace("\\", "/")
        print(image_filename)
    
        if os.path.exists(image_filename):
            image_panel.object = image_filename
        else:
            print("Image file does not exist:", image_filename)
            image_panel.object = None
       
    else:
        image_panel.object = None

app.servable()

