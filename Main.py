
from PIL import Image
from numpy import asarray
from Line_creation import *
from Colour_functions import *
from Edge_detection import *
from Edge_processing import *


img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
numpydata = asarray(img)

edges_lat, edges_vert, edges_diag_LR, edges_diag_RL = image_edge_detection(numpydata)

lat_edge_processing(numpydata, edges_lat, 50, 120, 5)

vert_edge_processing(numpydata, edges_vert, 50, 120, 5)

edges_prio_1, edges_prio_2, edges_prio_3 = edge_prioritisation(numpydata, edges_lat, edges_vert, edges_diag_LR, edges_diag_RL)

list_of_edge_prios = [edges_prio_1, edges_prio_2, edges_prio_3]

generate_lines(numpydata, edges_prio_1, edges_prio_2, edges_prio_3)


