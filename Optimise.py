
from PIL import Image
from numpy import asarray
from Line_creation import *
from Colour_functions import *
from Edge_detection import *
from Edge_processing import *
from Segments import *

# Schema
# define randomised parameters
# call function(s) multiple times with said parameters
# Score function against desrired output for each trial
# report best score accuracy and parameters utilised.

img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
numpydata = asarray(img)

trial_limit = 20

for trial in range(trial_limit):
    
    # define randomised parameters
    RGB_tolerance = 120
    singular_RGB_trigger = 50
    delta_trigger = 50    

    edges_lat, edges_vert, edges_diag_LR, edges_diag_RL = image_edge_detection(numpydata, RGB_tolerance, singular_RGB_trigger, delta_trigger)

    edges_prio_1, edges_prio_2, edges_prio_3 = edge_prioritisation(numpydata, edges_lat, edges_vert, edges_diag_LR, edges_diag_RL)

    list_of_edge_prios = [edges_prio_1, edges_prio_2, edges_prio_3]

    outlines = generate_outlines(numpydata, edges_prio_1, edges_prio_2, edges_prio_3)