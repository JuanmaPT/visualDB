import os
import panel as pn
from NoiseManager import NoiseManager
from PlotManager import PlotManager
from DataManager import DataManager
from DataLoader import DataLoader
from dbExtractor import dbExtractor
from utils import add_gaussian_noise, add_motion_blur, add_brightness_noise
import cv2 
import pandas as pd
import plotly.graph_objs as go

pn.extension(notifications=True)
pn.extension("plotly")
pn.config.sizing_mode = "stretch_width"


class AppManager:
    def __init__(self):
       
        self.data= DataLoader("MexCulture", "PCA")
        self.noiseManager = NoiseManager(self.update_noisy_image_and_trace)
        self.dataManager = DataManager(self.update_data)
        self.plotManager = PlotManager(self.data)
        self.dbManager = dbExtractor(self.data, self.update_db)
        
        #print(self.data.df.head())
        #print(self.data.df[self.data.df["distribution"]==f"GaussianNoise_1"])
        
        self.isOODAnalysis = False
        self.clickedImage = None
        self.showDecisionBoundary = False

        self.template = pn.template.ReactTemplate(title="Data Sample Visualizer")

        self.image_panel = pn.pane.PNG(object=None, height=500, width=500)             
        self.gaussian_image_panel = pn.pane.PNG(object= None, height=500, width=500)
        self.motion_image_panel = pn.pane.PNG(object= None, height=500, width=500)
        self.brightness_image_panel = pn.pane.PNG(object= None, height=500, width=500) 


        self.OOD_tabs = pn.Tabs(('Gaussian Noise', self.gaussian_image_panel), 
                                ('Motion Blur', self.motion_image_panel),
                                ('Brightness', self.brightness_image_panel),
                                visible= False)

        #self.colors = ['#B9FFB7', '#FB8B24', '#D90368']
        self.colors = ['#6564DB', '#FB8B24', '#D90368']
        
     
        #INITIATE PLOT PANEL 
        for label,color in zip(self.data.labels, self.colors):
            print(f"label {label} colour {color}")
            self.plotManager.fig.add_trace(go.Scatter3d(x=[], y=[], z=[], 
                                                mode='markers', 
                                                name=f"{label}", 
                                                marker=dict(size=5,
                                                symbol = "circle",
                                                color= color)))
        
        self.plot_panel = pn.pane.Plotly(self.plotManager.fig, config={"responsive": True}, sizing_mode="stretch_width")
        self.distribution = self.dataManager.distribution_selector.value
        self.prediction = self.dataManager.distribution_selector.value

        self.mesh_opacity = self.dbManager.opacity_slider.value

        self.warning = None
    def createApp(self):
        # set up settings 
        ood_analysis_button = pn.widgets.Button(name="OOD Analysis")            
        db_button=pn.widgets.Button(name="Show Decision Boundary")
    
                                                                        
        settings_panel = pn.WidgetBox( self.dataManager.dataset_selector,
                                    self.dataManager.distribution_selector,
                                    self.dataManager.prediction_selector,
                                    db_button,
                                    self.dbManager.checkBox,
                                    self.dbManager.opacity_slider,
                                    ood_analysis_button,
                                    self.noiseManager.gaussian_slider,
                                    self.noiseManager.motion_slider,
                                    self.noiseManager.brightness_slider,
        )

        self.dbManager.opacity_slider.visible = False
        self.dbManager.checkBox.visible = False
        self.noiseManager.gaussian_slider.visible = False
        self.noiseManager.motion_slider.visible = False
        self.noiseManager.brightness_slider.visible = False


                                    
        # tabs in template
        control_tab = pn.Tabs(('Settings', settings_panel))
        self.template.sidebar.extend([control_tab])
        self.template.main[0,:8] = pn.Tabs(('3D Data Visualization', self.plot_panel))
        self.template.main[0,8:] = pn.Tabs(('Image Panel', self.image_panel))
        self.template.main[3,8:] = self.OOD_tabs
        

        # callbacks
        self.plot_panel.param.watch(lambda event: self.update_image(event), "click_data")
        ood_analysis_button.on_click(lambda event: self.ood_analysis_callback(event))
        db_button.on_click(lambda event: self.decision_boundary_callback(event))

        # serve the template
        self.template.servable()

        return self.template
    
    
    def decision_boundary_callback(self, event):
        self.showDecisionBoundary = not self.showDecisionBoundary
        if self.showDecisionBoundary:
            # enable checkbox
            self.dbManager.checkBox.visible = True
            self.dbManager.opacity_slider.visible = True

            print(self.dbManager.checkBox.value)
            #print(self.dbManager.opacity_slider.value)    
        
        else:
            self.dbManager.checkBox.value = []
            self.dbManager.checkBox.visible = False
            self.dbManager.opacity_slider.visible= False

            self.plotManager.remove_trace("Boundary Point")
            self.plotManager.remove_trace("Boundary Mesh")


    def update_db(self, event):
        boundary_points = self.dbManager.planes
        #print( event)
        if event.obj.name == 'Mesh Opacity':
            self.plotManager.add_surface_trace("Boundary Mesh", boundary_points, event.obj.value)
          
        
        if event.obj.name == 'CheckboxGroup':
            if event.obj.value == ['Point']:
                try:
                    self.plotManager.remove_trace("Boundary Mesh")
                except:
                    pass
                print("showing points of decision boundary")    
                self.plotManager.add_scatter_trace_surface("Boundary Point" ,boundary_points, '#9ED8DB', 1, symbol = 'diamond', size =2)
            
            elif event.obj.value == ['Mesh']:
                try:
                    self.plotManager.remove_trace("Boundary Point" )
                except:
                    pass
                print('showing mesh of decision boundary')
                self.plotManager.add_surface_trace("Boundary Mesh", boundary_points, self.mesh_opacity)

            elif event.obj.value == ['Point', 'Mesh']:
                self.plotManager.add_scatter_trace_surface("Boundary Point" ,boundary_points, '#9ED8DB', 1, symbol = 'diamond', size =2)
                self.plotManager.add_surface_trace("Boundary Mesh", boundary_points, self.mesh_opacity)
            
            else:
                self.plotManager.remove_trace("Boundary Point")
                self.plotManager.remove_trace("Boundary Mesh")


    def update_image(self, event):
        if self.warning is not None:
            self.warning.destroy()
        try:
            if event.new is not None and 'points' in event.new:
                point_data = event.new['points'][0]
                df= self.data.df[(self.data.df["distribution"]== "Train") | (self.data.df["distribution"]== "Validation")]
                idx = df.loc[(df['x'] == point_data['x']) & (df['y'] == point_data['y']) & (df['z'] == point_data['z'])]
                self.clickedImage = idx['image_path'].tolist()[0]

                print("Clicked Image:", self.clickedImage)
                image_df = df[df["image_path"] == self.clickedImage]
                self.plotManager.add_scatter_trace("Clicked Image", image_df, "yellow", 1, symbol = "circle", size = 5)
                
                # restart setttings and ood traces
                self.noiseManager.set(self.noiseManager.gaussian_slider, 0)
                self.noiseManager.set(self.noiseManager.motion_slider, 0)
                self.noiseManager.set(self.noiseManager.brightness_slider, 0)

                self.plotManager.remove_trace("OOD Brightness")
                self.plotManager.remove_trace("OOD Gaussian Noise")
                self.plotManager.remove_trace("OOD Motion Blur")

                self.image_panel.object = self.clickedImage
                self.gaussian_image_panel.object = self.clickedImage
                self.motion_image_panel.object = self.clickedImage
                self.brightness_image_panel.object = self.clickedImage
                
                print("\nsliders restarted") 
                print("\nODD restared")   
                
        except:
            #if its a click in the plot but not an image
            pass
        
    
    def ood_analysis_callback(self, event):
        self.isOODAnalysis = not self.isOODAnalysis

        if self.isOODAnalysis:
            print("OOD Analysis on")
            # enable noise sliders
            self.noiseManager.set(self.noiseManager.gaussian_slider, 0)
            self.noiseManager.set(self.noiseManager.motion_slider, 0)
            self.noiseManager.set(self.noiseManager.brightness_slider, 0)

            self.noiseManager.gaussian_slider.visible = True
            self.noiseManager.motion_slider.visible = True
            self.noiseManager.brightness_slider.visible = True
            
            for label in self.data.labels:
                        self.plotManager.update_trace_opacity(label, 0.2)

            #self.plotManager.update_trace_opacity("Decision Boundary", 0.2)
          
            try:
                if len(self.clickedImage)>0:
                    self.gaussian_image_panel.object = self.clickedImage
                    self.motion_image_panel.object = self.clickedImage
                    self.brightness_image_panel = self.clickedImage
            
            except:
                #self.show_notification()
                print("Warning select an image")
                message = "Please select an image from the point cloud first."
                if self.warning == None:
                    self.warning = pn.state.notifications.warning(message, duration=0)


        else:
            print("OOD analysis off")
            self.noiseManager.gaussian_slider.object = None
            self.noiseManager.motion_slider.object = None
            self.noiseManager.brightness_slider.object = None

            self.noiseManager.gaussian_slider.visible = False
            self.noiseManager.motion_slider.visible = False
            self.noiseManager.brightness_slider.visible = False

            # delete OOD traces
            self.plotManager.remove_trace("OOD Brightness")
            self.plotManager.remove_trace("OOD Gaussian Noise")
            self.plotManager.remove_trace("OOD Motion Blur")
        
            # turn on samples
            for label in self.data.labels:
                self.plotManager.update_trace_opacity(label, 1)

        self.OOD_tabs.visible = self.isOODAnalysis

    def update_noisy_image_and_trace(self, event):
        print("\nupdate", event.obj.name, event.obj.value,)

        if self.isOODAnalysis:
            if event.obj.name == "Gaussian Noise":
                noisy_image = add_gaussian_noise(self.clickedImage, event.obj.value)
                _, img_bytes = cv2.imencode('.png', noisy_image)
                self.gaussian_image_panel.object = img_bytes.tobytes()

                #update trace in data plot
                df_OOD = self.data.df[(self.data.df["distribution"]==f"GaussianNoise_{event.obj.value}") &
                                       (self.data.df["image_path"]==self.clickedImage)]
            
                self.plotManager.add_scatter_trace("OOD Gaussian Noise", df_OOD, "red", 1, symbol = "circle", size = 5) 
                print("Gaussian noise updated")

                ## info display
                if (df_OOD['true_label'] != df_OOD['classified_label']).all():
                    message = f"OOD data sample  with Gaussian Noise level {event.obj.value} has been misclassified "
                    if event.obj.value != 0:
                            pn.state.notifications.info(message, duration=3000*2)
                
                
            if event.obj.name == "Motion Blur":
                if event.obj.value > 0:
                    noisy_image = add_motion_blur(self.clickedImage, event.obj.value)
                    _, img_bytes = cv2.imencode('.png', noisy_image)
                    self.motion_image_panel.object = img_bytes.tobytes()

                    df_OOD = self.data.df[(self.data.df["distribution"]==f"MotionBlur_{event.obj.value}") &
                                        (self.data.df["image_path"]==self.clickedImage)]
                
                    
                    self.plotManager.add_scatter_trace("OOD Motion Blur", df_OOD, "green", 1, symbol = "circle", size = 5) 
                    print("Motion blur updated")

                    ## info display
                    if (df_OOD['true_label'] != df_OOD['classified_label']).all():
                        message = f"OOD data sample with Motion Blur level {event.obj.value} has been misclassified "
                        if event.obj.value != 0:
                            pn.state.notifications.info(message, duration=3000*2)
                        
        
            if event.obj.name == "Brightness" :
                try:
                    noisy_image = add_brightness_noise(self.clickedImage, event.obj.value)
                    _, img_bytes = cv2.imencode('.png', noisy_image)
                    img =img_bytes.tobytes()
                    self.brightness_image_panel.object = img

                    df_OOD = self.data.df[(self.data.df["distribution"]==f"Brightness_{event.obj.value}") &
                                        (self.data.df["image_path"]==self.clickedImage)]
                    
                    self.plotManager.add_scatter_trace("OOD Brightness", df_OOD, "black", 1, symbol = "circle", size = 5) 
                    print("Brightness updated")

                    ## info display
                    if (df_OOD['true_label'] != df_OOD['classified_label']).all():
                        message = f"OOD data sample with Brightness level {event.obj.value} has been misclassified "
                        if event.obj.value != 0:
                            pn.state.notifications.info(message, duration=3000*2)
                except:
                    # fix the bed 
                    self.brightness_image_panel.object = self.clickedImage
                    print("This image is not available")
            

    def update_data(self, event):
        if event.obj.name == "Select Example":
            dataset = event.obj.value
        if event.obj.name == "Select Distribution":
            self.distribution = event.obj.value
        if event.obj.name == "Select Predictions":
            self.prediction = event.obj.value

        df = self.data.df
        pd.set_option('display.max_columns', None)

        if self.distribution in ["Train", "Validation"] and self.prediction == "All":
            print("\n",self.distribution, self.prediction)
    
            for label, color in zip(self.data.labels, self.colors):
                print(f"label {label} colour {color}")
                data_to_plot = df[(df["distribution"]== self.distribution)& (df["true_label"] == label)]
                
                #print(data_to_plot)
                self.plotManager.add_scatter_trace(label, data_to_plot, color, 1)



        elif self.distribution == "All" and self.prediction == "All":
            print("\n",self.distribution, self.prediction)
            for label, color in zip(self.data.labels, self.colors):
                data_to_plot = df[(df["distribution"].isin(["Train", "Validation"])) & (df["classified_label"] == label)]
                #print(data_to_plot.head())
                self.plotManager.add_scatter_trace(label, data_to_plot, color, 1)
                

        elif self.distribution in ["Train", "Validation"] and self.prediction in ["Correct", "Incorrect"]:
            print("\n",self.distribution, self.prediction)
            for label, color in zip(self.data.labels, self.colors):
                print(color)
                if self.prediction == "Correct":
                    data_to_plot = df[(df["distribution"] == self.distribution) & (df["true_label"] == df["classified_label"]) & (df["true_label"] == label)]
                    #print(data_to_plot.head())
                elif self.prediction == "Incorrect":
                    data_to_plot = df[(df["distribution"] == self.distribution) & (df["true_label"] != df["classified_label"])]

                # Filter by label after checking for incorrect predictions
                data_to_plot = data_to_plot[data_to_plot["true_label"] == label]

                if not data_to_plot.empty:
                    self.plotManager.add_scatter_trace(label, data_to_plot, color, 1)
                
                else:
                    print("empty")
                    self.plotManager.remove_trace(label)

        elif self.distribution == "All" and self.prediction in ["Correct", "Incorrect"]:
            print("\n", self.distribution, self.prediction)
            for label, color in zip(self.data.labels, self.colors):
                if self.prediction == "Correct":
                    data_to_plot = df[(df["distribution"].isin(["Train", "Validation"])) & (df["true_label"] == df["classified_label"]) & (df["true_label"] == label)]
                elif self.prediction == "Incorrect":
                    data_to_plot = df[(df["distribution"].isin(["Train", "Validation"])) & (df["true_label"] != df["classified_label"])]

                # Filter by label after checking for incorrect predictions
                data_to_plot = data_to_plot[data_to_plot["true_label"] == label]

                if not data_to_plot.empty:
                        self.plotManager.add_scatter_trace(label, data_to_plot, color, 1)
                    
                else:
                    print("empty")
                    self.plotManager.remove_trace(label)

                
            
                
        self.plotManager.remove_trace("Clicked Image")
        self.image_panel.object = None  

        # restart setttings and ood traces
        self.noiseManager.set(self.noiseManager.gaussian_slider, 0)
        self.noiseManager.set(self.noiseManager.motion_slider, 0)
        self.noiseManager.set(self.noiseManager.brightness_slider, 0)

        self.plotManager.remove_trace("OOD Brightness")
        self.plotManager.remove_trace("OOD Gaussian Noise")
        self.plotManager.remove_trace("OOD Motion Blur")

        self.image_panel.object = None           
        self.gaussian_image_panel.object = None
        self.motion_image_panel.object = None
        self.brightness_image_panel.object = None
        
               
if __name__== "__main__":
    appManager = AppManager()
    layout = appManager.createApp()
    layout.show()
    pn.serve("--autoreload", show = False)
