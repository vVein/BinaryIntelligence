
from PIL import Image
from numpy import asarray
from Line_creation import *
from Colour_functions import *
from Edge_detection import *
from Edge_processing import *
from Segments import *


img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
numpydata = asarray(img)

edges_lat, edges_vert, edges_diag_LR, edges_diag_RL = image_edge_detection(numpydata)

edges_prio_1, edges_prio_2, edges_prio_3 = edge_prioritisation(numpydata, edges_lat, edges_vert, edges_diag_LR, edges_diag_RL)

list_of_edge_prios = [edges_prio_1, edges_prio_2, edges_prio_3]

outlines = generate_lines(numpydata, edges_prio_1, edges_prio_2, edges_prio_3)

segment_creation(numpydata, outlines, 4, 8)
segment_creation(numpydata, outlines, 3, 8)
segment_creation(numpydata, outlines, 2, 8)
