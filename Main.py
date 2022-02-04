
from PIL import Image
from numpy import asarray
from Line_creation import *
from Colour_functions import *
from Edge_detection import *
from Edge_processing import *


img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
numpydata = asarray(img)

edges_lat, edges_vert, edges_diag_LR, edges_diag_RL = image_edge_detection(numpydata)
thickness_threshold = 3
reduced_lat_edges, remaining_lat_edges = lat_edge_processing(numpydata, edges_lat, 50, 120, thickness_threshold)
reduced_vert_edges, remaining_vert_edges = vert_edge_processing(numpydata, edges_vert, 50, 120, thickness_threshold)
reduced_diag_LR_edges, remaining_diag_LR_edges = diag_LR_edge_processing(numpydata, edges_diag_LR, 50, 120, thickness_threshold)
reduced_diag_RL_edges, remaining_diag_RL_edges = diag_RL_edge_processing(numpydata, edges_diag_RL, 50, 120, thickness_threshold)

edges_prio_1, edges_prio_2, edges_prio_3 = edge_prioritisation(numpydata, edges_lat, edges_vert, edges_diag_LR, edges_diag_RL)
reduced_edges_prio_1, reduced_edges_prio_2, reduced_edges_prio_3 = edge_prioritisation(numpydata, reduced_lat_edges, reduced_vert_edges,
                                                                                       reduced_diag_LR_edges, reduced_diag_RL_edges)
remaining_edges_prio_1, remaining_edges_prio_2, remaining_edges_prio_3 = edge_prioritisation(numpydata, remaining_lat_edges, remaining_vert_edges,
                                                                                       remaining_diag_LR_edges, remaining_diag_RL_edges)

if 2 == 2:
    x_cords_6, y_cords_6 = zip(*remaining_edges_prio_3)
    plt.scatter(*zip(*remaining_edges_prio_3),marker='.', s=0.1, color='purple')
    plt.scatter(x_cords_6, y_cords_6, marker='.', s=0.5, color='purple')
    x_cords_5, y_cords_5 = zip(*remaining_edges_prio_2)
    plt.scatter(*zip(*remaining_edges_prio_2),marker='.', s=0.1, color='pink')
    plt.scatter(x_cords_5,y_cords_5,marker='.', s=0.5, color='pink')
    x_cords_4, y_cords_4 = zip(*remaining_edges_prio_1)
    plt.scatter(*zip(*remaining_edges_prio_1),marker='.', s=0.1, color='aqua')
    plt.scatter(x_cords_4,y_cords_4,marker='.', s=0.5, color='aqua')


    x_cords_3, y_cords_3 = zip(*reduced_edges_prio_3)
    plt.scatter(*zip(*reduced_edges_prio_3),marker='.', s=0.1, color='green')
    plt.scatter(x_cords_3, y_cords_3, marker='.', s=0.5, color='green')
    x_cords_2, y_cords_2 = zip(*reduced_edges_prio_2)
    plt.scatter(*zip(*reduced_edges_prio_2),marker='.', s=0.1, color='orange')
    plt.scatter(x_cords_2,y_cords_2,marker='.', s=0.5, color='orange')
    x_cords, y_cords = zip(*reduced_edges_prio_1)
    plt.scatter(*zip(*reduced_edges_prio_1),marker='.', s=0.1, color='red')
    plt.scatter(x_cords,y_cords,marker='.', s=0.5, color='red')
    plt.gca().invert_yaxis()
    plt.legend()
    img = Image.fromarray(numpydata, 'RGB')
    img.save('my.png')
    plt.imshow(img)
    plt.show()

list_of_edge_prios = [edges_prio_1, edges_prio_2, edges_prio_3]

generate_lines(numpydata, edges_prio_1, edges_prio_2, edges_prio_3)


