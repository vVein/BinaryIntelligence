
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt
import numpy as np
import itertools
from Colour_functions import *
from Edge_detection import *

img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
numpydata = asarray(img)

edges_prio_1, edges_prio_2, edges_prio_3 = image_edge_detection(numpydata, 200)

list_of_edge_prios = [edges_prio_1, edges_prio_2, edges_prio_3]

lines = []
used = []
index_rotation = [0, 1, -1, 2, -2, 3, -3]
circular_pattern = [[0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1]]
direction_weighting = [90, 70, 70, 55, 55, 40, 40]
edges_prio_1_weighting = 125
edges_prio_2_weighting = 60
edges_prio_3_weighting = 30
weighting_threshold = 140
index_cap = len(index_rotation) + 1
shape_no = 0
current_shape = []

# Polyline functions:

def generate_polyline(start_point, prev_dirct_index, last_stored_xy):
    global current_shape
    completed_loop = False
    suitable_matches = True
    while suitable_matches and not completed_loop:
        
        xy = last_stored_xy
              
        # build list of suitable surrounding points and select best match  
        surrounding_pixels_weighted = []
        for n, index_adj in enumerate(index_rotation):
            applied_index = ( prev_dirct_index + index_adj ) % index_cap
            direction = circular_pattern[applied_index]
            adjacent_pixel = [xy[0] + direction[0], xy[1] + direction[1]]
            
            if adjacent_pixel == start_point and len(current_shape) > 12:
                pixel_weight = edges_prio_1_weighting * 10
                surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                continue
                        
            if adjacent_pixel in used:
                continue

            directional_weighting = direction_weighting[n]
                
            if adjacent_pixel in edges_prio_1:
                pixel_weight = edges_prio_1_weighting + weighted_colour_match(numpydata, xy, adjacent_pixel) + directional_weighting
                surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
            elif adjacent_pixel in edges_prio_2:
                pixel_weight = edges_prio_1_weighting + weighted_colour_match(numpydata, xy, adjacent_pixel) + directional_weighting
                surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
            elif adjacent_pixel in edges_prio_3:
                pixel_weight = edges_prio_1_weighting + weighted_colour_match(numpydata, xy, adjacent_pixel) + directional_weighting
                surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])       
        
        if len(surrounding_pixels_weighted) == 0:
            suitable_matches = False
            break
        
        surrounding_pixels_weighted.sort(key = lambda surrounding_pixels_weighted : surrounding_pixels_weighted[2], reverse = True)
        xy_n = [surrounding_pixels_weighted[0][0], surrounding_pixels_weighted[0][1]]
        xy_n_weight = surrounding_pixels_weighted[0][2]
            
        if xy_n == start_point and len(current_shape) > 12:
            current_shape.append(xy_n)
            completed_loop = True
            break
        
        if xy_n_weight >= weighting_threshold:
            used.append(xy_n)
            current_shape.append(xy_n)
            last_stored_xy = xy_n
            delta = [xy_n[0]-xy[0],xy_n[1]-xy[1]]
            dirct_index = [indx for indx, dirct in enumerate(circular_pattern) if dirct == delta]
            prev_dirct_index = dirct_index[0]

        if xy_n_weight < weighting_threshold:
            suitable_matches = False

def start_new_polylines():
    global shape_no, current_shape
    for xy in edges_prio_1:
        
        new_shape = False
        surrounding_pixel_in_used = False
                
        if xy not in used:

            prev_dirct_index = 0
            start_point = xy
                        
            # find best first point             
            surrounding_pixel_xys = []
            for direction in circular_pattern:
                adjacent_pixel = [xy[0] + direction[0], xy[1] + direction[1]]
                surrounding_pixel_xys.append([adjacent_pixel[0], adjacent_pixel[1]])
            
            # build list of suitable surrounding points and select best match       
            surrounding_pixels_weighted = []
            for adjacent_pixel in surrounding_pixel_xys:
                if adjacent_pixel in used:
                    surrounding_pixel_in_used = True
                    break
                if adjacent_pixel in edges_prio_1:
                    pixel_weight = edges_prio_1_weighting + weighted_colour_match(numpydata, xy, adjacent_pixel)
                    surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                elif adjacent_pixel in edges_prio_2:
                    pixel_weight = edges_prio_1_weighting + weighted_colour_match(numpydata, xy, adjacent_pixel)
                    surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                elif adjacent_pixel in edges_prio_3:
                    pixel_weight = edges_prio_1_weighting + weighted_colour_match(numpydata, xy, adjacent_pixel)
                    surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
            
            if surrounding_pixel_in_used:
                continue
                 
            if len(surrounding_pixels_weighted) == 0:
                continue
                    
            surrounding_pixels_weighted.sort(key = lambda surrounding_pixels_weighted : surrounding_pixels_weighted[2], reverse = True)
            xy_n = [surrounding_pixels_weighted[0][0], surrounding_pixels_weighted[0][1]]
            xy_n_weight = surrounding_pixels_weighted[0][2]
            
            if xy_n_weight >= weighting_threshold:
                current_shape = []
                shape_no = shape_no + 1
                current_shape.append([xy[0], xy[1]])
                current_shape.append([xy_n[0], xy_n[1]])
                used.append([xy[0], xy[1]])
                used.append([xy_n[0], xy_n[1]])
                initial_xy = xy
                new_shape = True
                delta = [xy_n[0]-xy[0],xy_n[1]-xy[1]]
                dirct_index = [indx for indx, dirct in enumerate(circular_pattern) if dirct == delta]
                prev_dirct_index = dirct_index[0]
                initial_directionional_index = dirct_index[0]
                last_stored_xy = xy_n

        # Add to new polyline            
        if new_shape:
            generate_polyline(start_point, prev_dirct_index, last_stored_xy)
        
            # check a second direction    
            #reverse_initial_direction_index = ( initial_directionional_index + index_cap / 2 ) % index_cap
       
            #generate_polyline(initial_xy, reverse_initial_direction_index, initial_xy)

            lines.append([shape_no, current_shape])
                
start_new_polylines()

# exclude 1 & 2 point lines
for line in lines:
    if len(line[1]) > 6:
        x, y = map(list, zip(*line[1]))
        plt.plot(x, y, label = "line {}".format(line[0]) )
plt.gca().invert_yaxis()
plt.show()
