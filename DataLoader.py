import json
import pandas as pd
import os


class DataLoader:
    def __init__(self, dataset, mode):
        self.dataset = dataset
        #self.distribution = distribution
        #self.predictions = predictions
        self.mode = mode

        self.labels = self.load_labels() 
        self.df = self.load_df()

    def load_labels(self):
        if self.dataset == "MexCulture": 
            path_dataset = "DataExtraction/Datasets/MexCulture142_Keras/"
            return os.listdir(path_dataset + "images_train/")
    
    def load_df(self):
        if self.dataset == "MexCulture":
            path_dir_data = "DataExtraction/Results/MexCulture142_Keras/"
        
        data = json.load(open(path_dir_data + "datav2.json" , 'r'))

        ##### Define conditions for filtering
        # Distribution
        #if self.distribution == "All":
        distribution_condition = lambda entry: True
        #else:
            #distribution_condition = lambda entry: self.distribution in data[entry]["distribution"]

        #if self.selected_classes is None:
            #classes_condition = lambda entry: True
        #else:
            #classes_condition = lambda entry: str(data[entry]["true_class"]) in str(self.selected_classes)
        
        #Prediction
        #if self.correct_predictions == "Correct":
            #predictions_condition = lambda entry: str(data[entry].get("true_class")) == str(data[entry].get("predicted_class"))
        
        #elif self.correct_predictions == "Incorrect":
            #predictions_condition = lambda entry: str(data[entry].get("true_class")) != str(data[entry].get("predicted_class"))
          
        #else:
            #predictions_condition = lambda entry: True
     
        
        #### Combine conditions & select entries 
        condition = lambda entry: distribution_condition(entry)     
        selected_entries = [entry for entry in data if condition(entry)]
        
        #load selected entries
        x = [data[entry][f"xyz_{self.mode}"][0] for entry in selected_entries]
        y = [data[entry][f"xyz_{self.mode}"][1] for entry in selected_entries]
        z = [data[entry][f"xyz_{self.mode}"][2] for entry in selected_entries]

        true_labels = [str(data[entry]["true_class"]) for entry in selected_entries]
        classified_labels = [str(data[entry]["predicted_class"]) for entry in selected_entries]
        image_scores = [(data[entry]["score"]) for entry in selected_entries]
        image_paths= [(data[entry]["image_path"]) for entry in selected_entries]
        distribution =  [(data[entry]["distribution"]) for entry in selected_entries]
        
        dataframe = {
            'x': x,
            'y': y,
            'z': z,
            'true_label': true_labels,
            'classified_label': classified_labels,
            'image_path': image_paths,
            'score': image_scores,
            'distribution':distribution
            
        }

        df = pd.DataFrame(dataframe)
        df['true_label'] = df['true_label'].apply(self.id2label)
        df['classified_label']= df['classified_label'].apply(self.id2label)

        return df
   

    def id2label(self, id_):
        label = self.labels[int(id_)]
        return label
