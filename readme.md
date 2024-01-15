> # VisualDB

---

Course: 4TIV902U Management of IT Projects (Image Processing and Computer Vision MSc)  
University: Université de Bordeaux  
Project Manager: Prof. Fabien Baldacci

---

## Project Overview

VisualDB is a project developed as a part of the course "4TIV902U Management of IT Projects" at Université de Bordeaux. The goal of this project is to create an application that enables the visualization of data points corresponding to images in a dynamic 3D space. 

This application is designed to help users to explore their models though the visualization of images in the dataset and the decision boundaries in a 3D feature space. We incorporate a robustness study in which the user can explore different modifications to original data analyzing changes in the predictions, score and displacement towards decision boundary.  

Curently, we are showcasing a preliminary demostration using the MexCulture dataset and ResNet50, as a proof-of-concept. However, we plan on extending the application capabilities to enable users to analyze their own models and datasets providing a more personalized experience. 

The current implementation of the VisualDB project utilizes the following technologies:

- **3D Visualization**: We use Plotly's `scatter3D` for rendering the 3D visualization of decision boundaries.
- **User Interface**: We employ the Panel ([Documentation](https://panel.holoviz.org/getting_started/build_app.html)) library to create an interactive interface that can be accesesd in a web browser, allowing users to adjust various parameters.

In order to run the dummy implementation of the first srpint install the environment with conda by doing 

```
conda env create -f visualDB.yml
```

Then run:

```
python visualizerApp.py 
```


## Authors

- Juan Manuel Peña
- Blanca Hermosilla


## Main Functionalities

### Data Visualization in a 3D space

Extracted features are dynamically presented in a 3D space, offering enhanced visualization. Users have the flexibility to filter data points based on distribution or classes, with the added option to select all, correct or incorrect predictions, providing tailored and insightful analysis experience. 

Users can click on a data point to reveal the corresponding image in the Image Panel. Hovering over a point provides instant access to details such as the true class, predicted class, and prediction score. The selected image is highlighted in yellow

![Sprint1 Demo](https://jm-pt.eu/wp-content/uploads/2023/11/sprint1demo.gif)




### Decision Boundary Visualization
Upon clicking "Show Decision Boundary," users can opt to visualize either the points corresponding to the decision boundary or the mesh forming the decision boundary itself. Additionally, users have the flexibility to adjust the opacity of the mesh. This feature provides valuable insights into the partitioning of the region space, offering a better understanding of the model's capability to accurately classify samples.



### Robustness Analysis 
By selecting a single image and opting for "OOD Analysis," users gain insights into the model's robustness against Gaussian noise, motion blur, and brightness variations. An Out-of-Distribution (OOD) image panel with three tabs is generated, allowing users to manually select tabs corresponding to each perturbation and visualize their effects. Perturbation levels, ranging from 0 to 5, can be chosen.

For a comprehensive analysis, users can choose to also display the decision boundary, visually assessing the impact of perturbations on a sample and observing its displacement from in-distribution samples. An informative warning alerts users when perturbations alter the classification result. Hovering over OOD samples reveals details such as true prediction, classification, and score, often exposing a degradation in the score compared to the original image. This feature provides a valuable tool for users to assess and understand the model's response to diverse perturbations in a manual and customizable manner.


# Considerations


