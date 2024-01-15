import panel as pn 

class DataManager:
    def __init__(self, update_callback):
        # Define options and names for each Select widget
        distribution_opts = {"All":"All", "Train": "Train", "Validation": "Validation"}
        dataset_opts = {"MexCulture": "MexCulture"}
        prediction_opts = {"All": "All", "Correct": "Correct", "Incorrect": "Incorrect"}
        #db_opts = {None: None, "None": "None", "Plane(0,1)": "Plane(0,1)", "Plane(0,2)": "Plane(0,2)", "Plane3(1,2)": "Plane3(1,2)", "All": "All"}

        # Set up Select widgets with the specified options and names
        self.distribution_selector = pn.widgets.Select(value = None, options=distribution_opts, name="Select Distribution")
        self.dataset_selector = pn.widgets.Select(options=dataset_opts, name="Select Example")
        self.prediction_selector = pn.widgets.Select(options=prediction_opts, name="Select Predictions")
        #self.db_selector= pn.widgets.Select(options=db_opts, name="Select")

        # Set up callbacks for widget changes
        self.distribution_selector.param.watch(update_callback, "value")
        self.dataset_selector.param.watch(update_callback, "value")
        self.prediction_selector.param.watch(update_callback, "value")
        #self.db_selector.param.watch(update_callback, "value")
 
        self.set(self.distribution_selector, "All")
        self.set(self.prediction_selector, "All")
     

    def set(self, selector, value):
        selector.value = value


