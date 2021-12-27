
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt
import numpy as np
import itertools
from Colour_functions import *

def image_edge_detection(image_as_numpyarray, RGB_tolerance):
    numpydata = image_as_numpyarray
    
    img_width = int(np.size(numpydata,1))
    img_height = int(len(numpydata))
    edges_lat = []
    edges_rev_lat = []
    edges_diag = []
    pending_edges = []
        
    # Lateral scan (Left ro right)
    for y in range(img_height):
        previous_check_different = False
        for x in range(img_width):
            if x == 0:
                current_pixel = list(numpydata[y][x])
                continue
            previous_pixel = current_pixel
            current_pixel = list(numpydata[y][x])
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, RGB_tolerance)
            
            if different_colour:
                pending_edges.append([x, y, current_pixel[0], current_pixel[1], current_pixel[2]])
                previous_check_different = True
            else:
                if previous_check_different:
                    returned_edges = edge_variance(pending_edges)
                    for edge in returned_edges:
                        edges_lat.append([edge[0], edge[1]])
                    pending_edges = []
                previous_check_different = False
                
    print('checkmark1')
    # Lateral scan (Top to bottom)
    for x in range(img_width):
        for y in range(img_height):
            if y == 0:
                current_pixel = list(numpydata[y][x])
                continue
            previous_pixel = current_pixel
            current_pixel = list(numpydata[y][x])
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, RGB_tolerance)
            if different_colour:
                edges_lat.append([x, y])

    print('checkmark2')
    # Reverse Lateral scan (Right to left)
    for y in range(img_height):
        for x in range(img_width - 1, 0, -1):
            if x == img_width - 1:
                current_pixel = list(numpydata[y][x])
                continue
            previous_pixel = current_pixel
            current_pixel = list(numpydata[y][x])
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, RGB_tolerance)
            if different_colour:
                edges_rev_lat.append([x, y])

    print('checkmark3')
    # Reverse Lateral scan (Bottom to top)
    for x in range(img_width):
        for y in range(img_height - 1, 0, -1):
            if y == img_height - 1:
                current_pixel = list(numpydata[y][x])
                continue
            previous_pixel = current_pixel
            current_pixel = list(numpydata[y][x])
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, RGB_tolerance)
            if different_colour:
                edges_rev_lat.append([x, y])

    print('checkmark4')
    # Diagonal scan
    for x_start in range(img_width):
        for x in range(x_start, img_width):
            if x == x_start:
                y = 0
                current_pixel = list(numpydata[y][x])
                continue

            previous_pixel = current_pixel
            y = y + 1
            if y > img_height - 1:
                continue

            current_pixel = list(numpydata[y][x])
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, RGB_tolerance)
            if different_colour:
                edges_diag.append([x, y])

    print('checkmark5')
    # Diagonal scan
    for y_start in range(img_height):
        for y in range(y_start, img_width):
            if y == y_start:
                x = 0
                current_pixel = list(numpydata[y][x])
                continue

            previous_pixel = current_pixel
            x = x + 1
            if x > img_width - 1 or y > img_height - 1:
                continue

            current_pixel = list(numpydata[y][x])
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, RGB_tolerance)
            if different_colour:
                edges_diag.append([x, y])

    print('checkmark6')
    # Diagonal scan
    for x_start in range(img_width-1, 0, -1):
        for x in range(x_start - 1, 0, -1):
            if x == x_start - 1:
                y = 0
                current_pixel = list(numpydata[y][x])
                continue

            previous_pixel = current_pixel
            y = y + 1
            if y > img_height - 1:
                continue

            current_pixel = list(numpydata[y][x])
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, RGB_tolerance)
            if different_colour:
                edges_diag.append([x, y])

    print('checkmark7')
    # Diagonal scan
    for y_start in range(img_height - 1, 0, -1):
        for y in range(y_start, img_height):
            if y == y_start:
                x = img_width - 1
                current_pixel = list(numpydata[y][x])
                continue

            previous_pixel = current_pixel
            x = x - 1
            if x > img_width - 1 or y > img_height - 1:
                continue

            current_pixel = list(numpydata[y][x])
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, RGB_tolerance)
            if different_colour:
                edges_diag.append([x, y])

    print('checkmark8')
    edges_prio_1 = []
    edges_prio_2 = []
    edges_prio_3 = []

    #Combine and compile list of cross matches 
    for edge in edges_lat:
        if edge in edges_diag and edge in edges_rev_lat:
            edges_prio_1.append(edge)
        elif edge in edges_diag or edge in edges_rev_lat:
            edges_prio_2.append(edge)
        else:
            edges_prio_3.append(edge)
    print('checkmark9')
    for edge in edges_diag:
        if edge in edges_lat and edge in edges_rev_lat:
            continue
        elif edge in edges_lat or edge in edges_rev_lat:
            edges_prio_2.append(edge)
        else:
            edges_prio_3.append(edge)

    for edge in edges_rev_lat:
        if edge not in edges_prio_1 and edge not in edges_prio_2:
            edges_prio_3.append(edge)
    print('checkmark10')
    edges_prio_1.sort()
    edges_prio_2.sort()
    edges_prio_3.sort()

    #plot of edges
    edges_unique_1 = list(edges_prio_1 for edges_prio_1,_ in itertools.groupby(edges_prio_1))
    edges_unique_2 = list(edges_prio_2 for edges_prio_2,_ in itertools.groupby(edges_prio_2))
    edges_unique_3 = list(edges_prio_3 for edges_prio_3,_ in itertools.groupby(edges_prio_3))

    x_cords_3, y_cords_3 = zip(*edges_prio_3)
    plt.scatter(*zip(*edges_prio_3),marker='.', s=0.1, color='green')
    plt.scatter(x_cords_3, y_cords_3, marker='.', s=0.5, color='green')
    x_cords_2, y_cords_2 = zip(*edges_prio_2)
    plt.scatter(*zip(*edges_prio_2),marker='.', s=0.1, color='blue')
    plt.scatter(x_cords_2,y_cords_2,marker='.', s=0.5, color='blue')
    x_cords, y_cords = zip(*edges_prio_1)
    plt.scatter(*zip(*edges_prio_1),marker='.', s=0.1, color='red')
    plt.scatter(x_cords,y_cords,marker='.', s=0.5, color='red')
    plt.gca().invert_yaxis()
    plt.legend()
    plt.show()
    print('checkmark11')

    return edges_prio_1, edges_prio_2, edges_prio_3