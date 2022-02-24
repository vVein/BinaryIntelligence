
from PIL import Image
from numpy import asarray
from Line_creation import *
from Colour_functions import *
from Edge_detection import *
from Edge_processing import *


img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
numpydata = asarray(img)

edges_lat, edges_vert, edges_diag_LR, edges_diag_RL = image_edge_detection(numpydata)
thickness_threshold = 5
reduced_lat_edges, remaining_lat_edges, void_buffer_lat = lat_edge_processing(numpydata, edges_lat, 50, 120, thickness_threshold)
reduced_vert_edges, remaining_vert_edges, void_buffer_vert = vert_edge_processing(numpydata, edges_vert, 50, 120, thickness_threshold)
reduced_diag_LR_edges, remaining_diag_LR_edges, void_buffer_diag_LR = diag_LR_edge_processing(numpydata, edges_diag_LR, 50, 120, thickness_threshold)
reduced_diag_RL_edges, remaining_diag_RL_edges, void_buffer_diag_RL = diag_RL_edge_processing(numpydata, edges_diag_RL, 50, 120, thickness_threshold)

void_buffer = void_buffer_lat + void_buffer_vert + void_buffer_diag_LR + void_buffer_diag_RL
remaining_lat_edges_no_void = [edge for edge in remaining_lat_edges if edge not in void_buffer]
remaining_lat_edges = remaining_lat_edges_no_void
remaining_vert_edges_no_void = [edge for edge in remaining_vert_edges if edge not in void_buffer]
remaining_vert_edges = remaining_vert_edges_no_void
remaining_diag_LR_edges_no_void = [edge for edge in remaining_diag_LR_edges if edge not in void_buffer]
remaining_diag_LR_edges = remaining_diag_LR_edges_no_void
remaining_diag_RL_edges_no_void = [edge for edge in remaining_diag_RL_edges if edge not in void_buffer]
remaining_diag_RL_edges = remaining_diag_RL_edges_no_void

#reduced_lat_edges_no_void = [edge for edge in reduced_lat_edges if edge not in void_buffer]
#reduced_lat_edges = reduced_lat_edges_no_void
#reduced_vert_edges_no_void = [edge for edge in reduced_vert_edges if edge not in void_buffer]
#reduced_vert_edges = reduced_vert_edges_no_void
#reduced_diag_LR_edges_edges_no_void = [edge for edge in reduced_diag_LR_edges if edge not in void_buffer]
#reduced_diag_LR_edges = reduced_diag_LR_edges_edges_no_void
#reduced_diag_RL_edges_edges_no_void = [edge for edge in reduced_diag_RL_edges if edge not in void_buffer]
#reduced_diag_RL_edges = reduced_diag_RL_edges_edges_no_void

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
    plt.scatter(*zip(*reduced_edges_prio_3),marker='.', s=0.1, color='lawngreen')
    plt.scatter(x_cords_3, y_cords_3, marker='.', s=0.5, color='lawngreen')
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
    
if 20 == 2:
    x_cords_4, y_cords_4 = zip(*void_buffer_diag_RL)
    plt.scatter(*zip(*void_buffer_diag_RL),marker='.', s=0.1, color='aqua')
    plt.scatter(x_cords_4,y_cords_4,marker='.', s=0.5, color='aqua')
    x_cords_3, y_cords_3 = zip(*void_buffer_diag_LR)
    plt.scatter(*zip(*void_buffer_diag_LR),marker='.', s=0.1, color='green')
    plt.scatter(x_cords_3, y_cords_3, marker='.', s=0.5, color='green')
    x_cords_2, y_cords_2 = zip(*void_buffer_lat)
    plt.scatter(*zip(*void_buffer_lat),marker='.', s=0.1, color='pink')
    plt.scatter(x_cords_2,y_cords_2,marker='.', s=0.5, color='pink')
    x_cords, y_cords = zip(*void_buffer_vert)
    plt.scatter(*zip(*void_buffer_vert),marker='.', s=0.1, color='red')
    plt.scatter(x_cords,y_cords,marker='.', s=0.5, color='red')
    plt.gca().invert_yaxis()
    plt.legend()
    img = Image.fromarray(numpydata, 'RGB')
    img.save('my.png')
    plt.imshow(img)
    plt.show()

edges_combined = reduced_edges_prio_1 + reduced_edges_prio_2 + reduced_edges_prio_3 + remaining_edges_prio_1 + remaining_edges_prio_2 + remaining_edges_prio_3

#secondary_edge_reduction(edges_combined)

list_of_edge_prios = [edges_prio_1, edges_prio_2, edges_prio_3]

generate_lines(numpydata, edges_prio_1, edges_prio_2, edges_prio_3)


