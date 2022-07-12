
from PIL import Image
from numpy import asarray
from Line_creation import *
from Colour_functions import *
from Edge_detection import *
from Segments import *


img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
numpydata = asarray(img)

edges_lat, edges_vert, edges_diag_LR, edges_diag_RL = image_edge_detection(numpydata, RGB_tolerance = 120, singular_RGB_trigger = 50)

outlines = generate_outlines(numpydata, edges_lat, edges_vert, edges_diag_LR, edges_diag_RL)

segment_creation(numpydata, outlines, 2, 8)
