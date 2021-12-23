
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt
import numpy as np
import itertools
from Colour_functions import *

img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
numpydata = asarray(img)

img_width = int(np.size(numpydata,1))
img_height = int(len(numpydata))
edges_lat = []
edges_rev_lat = []
edges_diag = []

# Lateral scan (Left ro right)
for y in range(img_height):
    for x in range(img_width):
        if x == 0:
            current_pixel = numpydata[y][x]
            continue
        previous_pixel = current_pixel
        current_pixel = numpydata[y][x]
        different_colour = pixel_comparison(current_pixel, previous_pixel)
        if different_colour:
            edges_lat.append([x, y])

# Lateral scan (Top to bottom)
for x in range(img_width):
    for y in range(img_height):
        if y == 0:
            current_pixel = numpydata[y][x]
            continue
        previous_pixel = current_pixel
        current_pixel = numpydata[y][x]
        different_colour = pixel_comparison(current_pixel, previous_pixel)
        if different_colour:
            edges_lat.append([x, y])

# Reverse Lateral scan (Right to left)
for y in range(img_height):
    for x in range(img_width - 1, 0, -1):
        if x == img_width - 1:
            current_pixel = numpydata[y][x]
            continue
        previous_pixel = current_pixel
        current_pixel = numpydata[y][x]
        different_colour = pixel_comparison(current_pixel, previous_pixel)
        if different_colour:
            edges_rev_lat.append([x, y])

# Reverse Lateral scan (Bottom to top)
for x in range(img_width):
    for y in range(img_height - 1, 0, -1):
        if y == img_height - 1:
            current_pixel = numpydata[y][x]
            continue
        previous_pixel = current_pixel
        current_pixel = numpydata[y][x]
        different_colour = pixel_comparison(current_pixel, previous_pixel)
        if different_colour:
            edges_rev_lat.append([x, y])

# Diagonal scan
for x_start in range(img_width):
    for x in range(x_start, img_width):
        if x == x_start:
            y = 0
            current_pixel = numpydata[y][x]
            continue

        previous_pixel = current_pixel
        y = y + 1
        if y > img_height - 1:
            continue

        current_pixel = numpydata[y][x]
        different_colour = pixel_comparison(current_pixel, previous_pixel)
        if different_colour:
            edges_diag.append([x, y])

# Diagonal scan
for y_start in range(img_height):
    for y in range(y_start, img_width):
        if y == y_start:
            x = 0
            current_pixel = numpydata[y][x]
            continue

        previous_pixel = current_pixel
        x = x + 1
        if x > img_width - 1 or y > img_height - 1:
            continue

        current_pixel = numpydata[y][x]
        different_colour = pixel_comparison(current_pixel, previous_pixel)
        if different_colour:
            edges_diag.append([x, y])

# Diagonal scan
for x_start in range(img_width-1, 0, -1):
    for x in range(x_start - 1, 0, -1):
        if x == x_start - 1:
            y = 0
            current_pixel = numpydata[y][x]
            continue

        previous_pixel = current_pixel
        y = y + 1
        if y > img_height - 1:
            continue

        current_pixel = numpydata[y][x]
        different_colour = pixel_comparison(current_pixel, previous_pixel)
        if different_colour:
            edges_diag.append([x, y])

# Diagonal scan
for y_start in range(img_height - 1, 0, -1):
    for y in range(y_start, img_height):
        if y == y_start:
            x = img_width - 1
            current_pixel = numpydata[y][x]
            continue

        previous_pixel = current_pixel
        x = x - 1
        if x > img_width - 1 or y > img_height - 1:
            continue

        current_pixel = numpydata[y][x]
        different_colour = pixel_comparison(current_pixel, previous_pixel)
        if different_colour:
            edges_diag.append([x, y])

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

edges_prio_1.sort()
edges_prio_2.sort()
edges_prio_3.sort()
list_of_edge_prios = [edges_prio_1, edges_prio_2, edges_prio_3]

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

lines = []
used = []
index_rotation = [0, 1, -1, 2, -2, 3, -3]
circular_pattern = [[0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1]]
direction_weighting = [110, 80, 80, 50, 50, 30, 30]
edges_prio_1_weighting = 100
edges_prio_2_weighting = 60
edges_prio_3_weighting = 30
weighting_threshold = 120
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

terminus_points = []

