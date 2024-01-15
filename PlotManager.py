import plotly.graph_objs as go
import numpy as np
from scipy.interpolate import griddata

class PlotManager():
    def __init__(self, data):
        self.init_data = data
        self.fig = go.Figure()
        self.init_plot()
       
    def init_plot(self):
        self.fig.update_layout(
            autosize=False,
            width=1000,
            height=1000,
            scene=dict(
                camera=dict(eye=dict(x=1.87, y=1, z=-0.64)),)
            ) 
      
        df = self.init_data.df[(self.init_data.df["distribution"].isin(["Train", "Validation"]))]
        for label, color in zip(self.init_data.labels, ['#6564DB', '#FB8B24', '#D90368']):
            data_to_plot = df[df["true_label"] == label]
            self.add_scatter_trace(label, data_to_plot, color, 1)

        # Add a dummy trace to avoid error
        empty_trace = go.Scatter3d(
                        x=[],
                        y=[],
                        z=[],
                        mode='markers',
                        marker=dict(color='rgba(0,0,0,0)'),
                        name='Empty Trace'
                    )
        self.fig.add_trace(empty_trace)
                
    
    
    def add_scatter_trace(self, label, data, color, opacity, symbol = 'circle', size=5):
        try:
            self.remove_trace(label)
            print(f"remove {label}")
        except:
            print(f"trace {label} created")
            pass
      
        hover_text = (
        'True: ' + data['true_label'].astype(str) +
        '<br>Prediction: ' + data['classified_label'].astype(str) +
        '<br>Score: ' + data['score'].astype(str)
        )

        trace = go.Scatter3d(x=data['x'], 
                             y=data['y'], 
                             z=data['z'], 
                             mode = "markers", 
                             name=label, 
                             hoverinfo='text',
                             hovertext = hover_text,
                             marker=dict(opacity = opacity,
                                         size=size, 
                                         symbol= symbol, 
                                         color= color)
                             )
        
        self.fig.add_trace(trace)
        print(f"trace {label} added")


    def add_scatter_trace_surface(self, label, data, color, opacity, symbol = 'circle', size=2):
        try:
            self.remove_trace(label)
            #print(f"remove {label}")
        except:
            print(f"trace {label} created")
            pass
        trace = go.Scatter3d(x=data['y'], 
                             y=data['x'], 
                             z=data['z'], 
                             mode = "markers", 
                             name=label, 
                             hoverinfo='none',
                             marker=dict(opacity = opacity,
                                         size=size, 
                                         symbol= symbol, 
                                         color= color)
                             )
        
        self.fig.add_trace(trace)
        print(f"trace {label} added")
   
    def add_surface_trace(self, label, data, opacity):
        try:
            self.remove_trace(label)
            #print(f"remove {label}")
        except:
            print(f"trace {label} created")
            pass
   
        trace = go.Mesh3d(
            x=np.array(data['y']),
            y=np.array(data['x']),
            z=np.array(data['z']),
            alphahull= -1,
            name= label,
            color='#9ED8DB',
            opacity = opacity,
            showscale= False,
            flatshading= True,
            hoverinfo= 'none'

    
        )

        self.fig.add_trace(trace)
        


    def update_trace(self, name, data, color, opacity ):
        hover_text = (
            'True: ' + data['true_label'].astype(str) +
            '<br>Prediction: ' + data['classified_label'].astype(str) +
            '<br>Score: ' + data['score'].astype(str)
            )
        
        for trace in self.fig.data:
            if trace.name == name:
                trace.x = data["x"]
                trace.y = data["y"]
                trace.z = data["z"]
                trace.marker.opacity = opacity
                trace.marker.color = color
                trace.hoverinfo='text'
                trace.hovertext = hover_text
                
    
    def update_trace_opacity(self, name, opacity):
        for trace in self.fig.data:
            if trace.name == name:
                trace.marker.opacity = opacity
                #print("opacity updated")


    def remove_trace(self, name):
        data_list = list(self.fig.data)
        for trace in data_list:
            if trace.name == name:
                data_list.remove(trace)
        self.fig.data = tuple(data_list)
        #print("trace removed")
                
            



    



