> # VisualDB

---

Course: 4TIV902U Management of IT Projects (Image Processing and Computer Vision MSc)  
University: Université de Bordeaux  
Project Manager: Prof. Fabien Baldacci

---

## Project Overview

VisualDB is a project developed as a part of the course "4TIV902U Management of IT Projects" at Université de Bordeaux. The goal of this project is to create an application for visualizing decision boundaries. This application is designed to help users understand and interact with data by visualizing the decision boundaries in a three-dimensional space.

## Authors

- Juan Manuel Peña
- Blanca Hermosilla

## Project Progress

### Sprint 1 (Weeks 40-44)

In the first sprint, which lasted for four weeks, we conducted extensive research to identify available options for visualizing decision boundaries. We explored various frameworks and libraries to select the most suitable one for our project.
![Sprint1 Demo](https://jm-pt.eu/wp-content/uploads/2023/11/sprint1demo.gif)

### Current Implementation

The current implementation of the VisualDB project utilizes the following technologies:

- **3D Visualization**: We use Plotly's `scatter3D` for rendering the 3D visualization of decision boundaries.
- **User Interface**: We employ the Panel ([Documentation](https://panel.holoviz.org/getting_started/build_app.html)) library to create an interactive interface that can be accesesd in a web browser, allowing users to adjust various parameters.

In order to run the dummy implementation of the first srpint install the environment with conda by doing 

```
conda env create -f environment.yml
```

Then call the panel app by doing:

```
panel serve visualDBdummy_sprint1.py --show --autoreload

```

### Data Generation

At the end of the first sprint, we have developed a functional prototype with synthetic data. This dummy app serves as a proof of concept, enabling us to test the visualization capabilities of the selected libraries.

## Considerations

The information collected during the first sprint has been invaluable. We explored multiple intermediate versions to experiment with different 3D frameworks for point representation. Ultimately, we chose Plotly's 3D visualization due to its ability to resize, rotate, and zoom in on different regions of the space. Additionally, it allows users to click on individual data points for detailed representations.

We are excited about the progress made in Sprint 1, and we look forward to the next phases of development in the VisualDB project.
