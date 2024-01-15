import panel as pn

class NoiseManager:
    def __init__(self, update_callback):
        self.gaussian_slider = pn.widgets.IntSlider(name="Gaussian Noise", start=0, end=5,step=1, value=0)
        self.motion_slider = pn.widgets.IntSlider(name= "Motion Blur", start=0, end=5, step=1, value=0)
        self.brightness_slider = pn.widgets.IntSlider(name= "Brightness", start=0, end=5, step=1, value=0)
        
        # Set up callbacks for widget changes
        self.gaussian_slider.param.watch(update_callback, "value")
        self.motion_slider.param.watch(update_callback, "value")
        self.brightness_slider.param.watch(update_callback, "value")


    def set(self, slider, value):
        slider.value = value