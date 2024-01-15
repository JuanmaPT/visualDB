import cv2
import numpy as np
import json

def add_gaussian_noise(image_path, noise_level):
    image = cv2.imread(image_path)
    row, col, ch = image.shape
    mean = 0
    var = noise_level ** 2
    sigma = var ** 0.5
    noise_factor = 3
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    noisy_image = image + gauss*noise_factor
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return noisy_image


def add_motion_blur(image_path, noise_level):
    image = cv2.imread(image_path)
    noise_factor = 3
    kernel_size = noise_level * noise_factor
    kernel_motion_blur = np.zeros((kernel_size, kernel_size))
    kernel_motion_blur[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
    kernel_motion_blur = kernel_motion_blur / kernel_size
    noisy_image = cv2.filter2D(image, -1, kernel_motion_blur)
    return noisy_image

   
def add_brightness_noise(image_path, noise_level):
    image = cv2.imread(image_path)
    # Adjust the alpha parameter to control the brightness change
    adjusted_alpha = 1 + noise_level / 10.0
    noisy_image = cv2.convertScaleAbs(image, alpha=adjusted_alpha, beta=0)
    return noisy_image

def create_planes_from_json(json_filename, scale_factor =1):
    with open(json_filename, 'r') as json_file:
        hyperplanes = json.load(json_file)
    
    planes= {}
    for class_label, hyperplane_info in hyperplanes.items():
        # Extract hyperplane coefficients and intercept
        coef = np.array(hyperplane_info["coef"])
        intercept = hyperplane_info["intercept"]

        # Create a grid of points for the plane
        x_range = np.linspace(-1, 1, 100)
        y_range = np.linspace(-1, 1, 100)
        x_grid, y_grid = np.meshgrid(x_range, y_range)

        # Calculate corresponding z values for the plane
        z_grid = (-coef[0] * x_grid - coef[1] * y_grid - intercept) / coef[2]

        # Save plane information
        planes[f'Plane_{class_label}'] = {
            'x': x_grid.flatten() * scale_factor,
            'y': y_grid.flatten() * scale_factor,
            'z': z_grid.flatten() * scale_factor,
        }

    return planes


    



def id2label(id_, labels):
    return labels[int(id_)]


