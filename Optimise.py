
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

target_outlines_xys = []
target_blank_xys = []

for trial in range(trial_limit):
    
    # define randomised parameters
    RGB_tolerance = 120
    singular_RGB_trigger = 50
    delta_trigger = 50
    direction_weighting = [50, 40, 40, 30, 30, 20, 20]
    edges_prio_1_weighting = 125
    edges_prio_2_weighting = 60
    edges_prio_3_weighting = 30
    weighting_threshold = 300
    weighting_base = 200
    weighting_division_coefficient = 2
    rgb_delta_limit = 30
    centre_weighting_division_coefficient = 3
    weighting_base_cm = 200
    colour_match_limit = 20
    start_point_return_weighting = 5

    edges_lat, edges_vert, edges_diag_LR, edges_diag_RL = image_edge_detection(numpydata, RGB_tolerance, singular_RGB_trigger, delta_trigger)

    edges_prio_1, edges_prio_2, edges_prio_3 = edge_prioritisation(numpydata, edges_lat, edges_vert, edges_diag_LR, edges_diag_RL)

    outlines = generate_outlines(numpydata, edges_prio_1, edges_prio_2, edges_prio_3, direction_weighting, 
                      edges_prio_1_weighting, edges_prio_2_weighting, edges_prio_3_weighting, weighting_threshold,
                      weighting_base, weighting_division_coefficient, rgb_delta_limit, centre_weighting_division_coefficient,
                      weighting_base_cm, colour_match_limit, start_point_return_weighting)