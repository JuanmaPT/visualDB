import json
import pandas as pd
import os

class DataLoader:
    def __init__(self, path_dir, path_dataset, selected_distribution):
        self.path_dir = path_dir
        self.selected_distribution = selected_distribution
        #self.selected_classes = selected_classes 
        #self.correct_predictions = correct_predictions
        self.df = self.load_df()
        self.labels = os.listdir(path_dataset+ "images_train/")
    
    def load_df(self):

        data = json.load(open(self.path_dir + "data.json" , 'r'))
        
        # Define conditions for filtering
        if self.selected_distribution == "All":
            distribution_condition = lambda entry: True
        else:
            distribution_condition = lambda entry: self.selected_distribution in data[entry]["distribution"]

        #if self.selected_classes is None:
            #classes_condition = lambda entry: True
        #else:
            #classes_condition = lambda entry: str(data[entry]["true_class"]) in str(self.selected_classes)
        
        #if self.correct_predictions == "Correct Predictions":
            #predictions_condition = lambda entry: str(data[entry].get("true_class")) == str(data[entry].get("predicted_class"))
        
        #elif self.correct_predictions == "Incorrect Predictions":
            #predictions_condition = lambda entry: str(data[entry].get("true_class")) != str(data[entry].get("predicted_class"))
          
        #else:
            #predictions_condition = lambda entry: True
     
        
        # Combine conditions 
        condition = lambda entry: distribution_condition(entry) 

             
        selected_entries = [entry for entry in data if condition(entry)]
        
        #load selected entries
        x = [data[entry]["xyz_PCA"][0] for entry in selected_entries]
        y = [data[entry]["xyz_PCA"][1] for entry in selected_entries]
        z = [data[entry]["xyz_PCA"][2] for entry in selected_entries]

        true_labels = [str(data[entry]["true_class"]) for entry in selected_entries]
        classified_labels = [str(data[entry]["predicted_class"]) for entry in selected_entries]
        image_scores = [(data[entry]["score"]) for entry in selected_entries]
        image_paths= [(data[entry]["image_path"]) for entry in selected_entries]
        

        dataframe = {
            'x': x,
            'y': y,
            'z': z,
            'true_label': true_labels,
            'classified_label': classified_labels,
            'image_path': image_paths,
            'score': image_scores
            
        }

        df = pd.DataFrame(dataframe)
        return df
    

    def id2label(self, id_):
        label = self.labels[int(id_)]
        return label
