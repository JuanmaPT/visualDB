import numpy as np
from itertools import combinations
from sklearn.svm import SVC 
import tensorflow as tf
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
import pandas as pd
from scipy.ndimage import gaussian_filter
import panel as pn

class dbExtractor:
    # arreglar lo de las decison boundaries 
    def __init__(self, data, update_callback):
        self.data = data
        self.planes = self.loadPlane()
        self.checkBox = pn.widgets.CheckBoxGroup(name='CheckboxGroup', options=['Point', 'Mesh'], inline=False)
        self.opacity_slider = pn.widgets.FloatSlider(name="Mesh Opacity", start=0, end=1, step=0.1, value = 1)

        self.checkBox.param.watch(update_callback, "value")
        self.opacity_slider.param.watch(update_callback,"value")

    def loadPlane(self):
        svm = SVC(kernel='rbf')
        X_train = self.data.df[self.data.df["distribution"] == "Train"][["x", "y", "z"]]
        y_train = self.data.df[self.data.df["distribution"] == "Train"]["true_label"]
        svm.fit(X_train, y_train)

        # Return the three planes that seperate X_train
     
        x_range = np.linspace(self.data.df['x'].min(), self.data.df['x'].max(), 100) 
        y_range = np.linspace(self.data.df['y'].min(), self.data.df['y'].max(), 100)
        z_range = np.linspace(self.data.df['z'].min(), self.data.df['z'].max(), 100)

        x_grid, y_grid, z_grid = np.meshgrid(x_range, y_range, z_range)

        # Make predictions over the grid 
        predicted_grid = svm.predict(np.c_[x_grid.ravel(), y_grid.ravel(), z_grid.ravel()])
        predicted_grid = predicted_grid.reshape(x_grid.shape)
       
        interp_grid = np.vstack([x_grid.ravel(), y_grid.ravel(), z_grid.ravel()]).T
        

        # Extract the surface where there is a change in prediction
        boundary_points = [[], [],[]]
        for i in range(1, len(x_range)):
            for j in range(1, len(y_range)):
                for k in range(1, len(z_range)):
                    if predicted_grid[i, j, k] != predicted_grid[i-1, j, k]:
                        boundary_points[0].append(x_range[i])
                        boundary_points[1].append(y_range[j])
                        boundary_points[2].append(z_range[k])

        boundary_df = pd.DataFrame({"x": boundary_points[0], "y": boundary_points[1], "z": boundary_points[2]})

        # Apply Gaussian smoothing to the boundary points
        sigma = 0.2 
        smoothed_x = gaussian_filter(boundary_df["x"], sigma=sigma)
        smoothed_y = gaussian_filter(boundary_df["y"], sigma=sigma)
        smoothed_z = gaussian_filter(boundary_df["z"], sigma=sigma)

    
    
        return {"x": smoothed_x.tolist(), "y": smoothed_y.tolist(), "z": smoothed_z.tolist()}
        
        
      

