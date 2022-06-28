
from PIL import Image
from numpy import asarray
from Line_creation import *
from Colour_functions import *
from Edge_detection import *
from Edge_processing import *
from Segments import *


img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
numpydata = asarray(img)

edges_lat, edges_vert, edges_diag_LR, edges_diag_RL = image_edge_detection(numpydata, RGB_tolerance = 120, singular_RGB_trigger = 50)

edges_prio_1, edges_prio_2, edges_prio_3 = edge_prioritisation(numpydata, edges_lat, edges_vert, edges_diag_LR, edges_diag_RL)

outlines = generate_outlines(numpydata, edges_prio_1, edges_prio_2, edges_prio_3)

segment_creation(numpydata, outlines, 2, 8)
