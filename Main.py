
from PIL import Image
from numpy import asarray
from Line_creation import *
from Colour_functions import *
from Edge_detection import *


img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
numpydata = asarray(img)

edges_prio_1, edges_prio_2, edges_prio_3 = image_edge_detection(numpydata)

list_of_edge_prios = [edges_prio_1, edges_prio_2, edges_prio_3]

generate_lines(numpydata, edges_prio_1, edges_prio_2, edges_prio_3)


