
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

#Compine and compile list of cross matches 
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


lines = []
used = []
index_rotation = [0, 1, -1, 2, -2, 3, -3]
circular_pattern = [[0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1]]
index_cap = len(index_rotation) + 1
shape_no = 0
current_shape = []

# Polyline functions:

def generate_polyline(start_point, prev_dirct_index, last_stored_xy):
    possibilities = index_cap
    completed_loop = False
    while possibilities >= 1 and not completed_loop:
        possibilities = possibilities - 1
        xy = last_stored_xy
        for index_adj in index_rotation:
            test_index = ( prev_dirct_index + index_adj ) % index_cap
            new_dirct = circular_pattern[test_index]
            xy_n = [xy[0] + new_dirct[0], xy[1] + new_dirct[1]]

            if xy_n == start_point and len(current_shape) > 8:
                current_shape.append(xy_n)
                possibilities = 0
                completed_loop = True
                break
            
            colour_match_bool = colour_match(numpydata, xy, xy_n, 140)
            if xy_n in edges_prio_1 and colour_match_bool and xy_n not in used :
                used.append(xy_n)
                current_shape.append(xy_n)
                last_stored_xy = xy_n
                prev_dirct_index = test_index
                possibilities = index_cap
                break
        
        # exhausted higher priority matches, search for weaker matches
        weak_match_found = False
        
        if not completed_loop and possibilities == 1:
            
            for edges_prio_n in list_of_edge_prios:
                xy = last_stored_xy                        
                
                if weak_match_found:
                    break
                
                for index_adj in index_rotation:
                    test_index = ( prev_dirct_index + index_adj ) % index_cap
                    new_dirct = circular_pattern[test_index]
                    xy_n = [xy[0] + new_dirct[0], xy[1] + new_dirct[1]]

                    if xy_n == start_point and len(current_shape) > 8:
                        current_shape.append(xy_n)
                        possibilities = 0
                        completed_loop = True
                        break

                    elif xy_n in edges_prio_n and xy_n not in used:
                        used.append(xy_n)
                        current_shape.append(xy_n)
                        prev_dirct_index = test_index
                        possibilities = index_cap
                        weak_match_found = True
                        break

def start_new_polylines():
    global shape_no
    for xy in edges_prio_1:

        if xy not in used:
            new_shape = False

            prev_dirct_index = 0
            start_point = xy
            
            # test all directions for a close match
            directional_possibilities_remaining = len(circular_pattern)
            for dirct_index, dirct in enumerate(circular_pattern):
                directional_possibilities_remaining = directional_possibilities_remaining - 1
                xy_n = [xy[0] + dirct[0], xy[1] + dirct[1]]
                colour_match_bool = colour_match(numpydata, xy, xy_n, 140)
                if xy_n in edges_prio_1 and colour_match_bool and xy_n not in used:
                    current_shape = []
                    shape_no = shape_no + 1
                    current_shape.append([xy[0], xy[1]])
                    current_shape.append([xy_n[0], xy_n[1]])
                    used.append([xy[0], xy[1]])
                    used.append([xy_n[0], xy_n[1]])
                    initial_xy = xy
                    new_shape = True  
                    prev_dirct_index = dirct_index
                    initial_directionional_index = dirct_index
                    last_stored_xy = xy_n
                    break
                
            # if no clean match found, test for weaker matches
            if not new_shape:
                directional_possibilities_remaining = len(circular_pattern)
                for dirct_index, dirct in enumerate(circular_pattern):
                    directional_possibilities_remaining = directional_possibilities_remaining - 1
                    xy_n = [xy[0] + dirct[0], xy[1] + dirct[1]]
                    if ( xy_n in edges_prio_1 or xy_n in edges_prio_2 ) and xy_n not in used:
                        current_shape = []
                        shape_no = shape_no + 1
                        current_shape.append(xy)
                        current_shape.append(xy_n)
                        used.append(xy)
                        used.append(xy_n)
                        initial_xy = xy
                        new_shape = True  
                        prev_dirct_index = dirct_index
                        initial_directionional_index = dirct_index
                        last_stored_xy = xy_n
                        break
            
            # Add to new polyline            
            if new_shape:
                generate_polyline(start_point, prev_dirct_index, last_stored_xy)
                
            if directional_possibilities_remaining != 0:
                # new starting direction, opposite of initial starting direction from origin
                reverse_initial_direction_index = ( initial_directionional_index + index_cap / 2 ) % index_cap
                xy = initial_xy

                for index_adj in index_rotation:
                    if directional_possibilities_remaining != 0:
                        directional_possibilities_remaining = directional_possibilities_remaining - 1
                        test_index = int( ( reverse_initial_direction_index + index_adj ) % index_cap )
                        new_dirct = circular_pattern[test_index]
                        xy_n = [xy[0] + new_dirct[0], xy[1] + new_dirct[1]]

                        colour_match_bool = colour_match(numpydata, xy, xy_n, 140)
                        if xy_n in edges_prio_1 and colour_match_bool and xy_n not in used :
                            used.append(xy_n)
                            current_shape.append(xy_n)
                            last_stored_xy = xy_n
                            prev_dirct_index = test_index
                            
                            generate_polyline(start_point, prev_dirct_index, last_stored_xy)
                            
                            directional_possibilities_remaining = 0
                            break
                
            lines.append([shape_no, current_shape])
                
start_new_polylines()

# exclude 1 & 2 point lines
for line in lines:
    if len(line[1]) > 3:
        x, y = map(list, zip(*line[1]))
        plt.plot(x, y, label = "line {}".format(line[0]) )
plt.gca().invert_yaxis()
plt.show()

terminus_points = []

for line in lines:
    if len(line[1]) > 3:
        end_index = len(line[1]) - 1
        begin_point = line[1][0]
        end_point = line[1][end_index]
        # Remove complete loops, probable shapes
        if begin_point == end_point:
            continue
        # Locate other end points in close proximity
        # Should eventually locate all line points, not just end points
        terminus_points.append([line[0], begin_point])
        terminus_points.append([line[0], end_point])

lines_to_be_combined = []
flagged = []
for terminus in terminus_points:
    if terminus not in flagged:
        terminus_xy = terminus[1]
        for termini in terminus_points:
            x_delta = abs(terminus_xy[0] - termini[1][0])
            y_delta = abs(terminus_xy[1] - termini[1][1])
            if x_delta < 3 and y_delta < 3 and x_delta + y_delta != 0:
                lines_to_be_combined.append([terminus, termini])
                flagged.append(terminus)
                flagged.append(termini)

lines_to_be_removed = []
for entries in lines_to_be_combined:

    first_xy = entries[0][1]
    first_line_no = entries[0][0]
    first_line_index = first_line_no - 1
    first_line = lines[first_line_index][1]
    second_xy = entries[1][1]
    second_line_no = entries[1][0]
    second_line_index = second_line_no - 1
    second_line = lines[second_line_index][1]

    if first_line_no == second_line_no:
        continue

    if first_xy == first_line[0]:
        if second_xy == second_line[0]:
            replacement = second_line[::-1] + first_line
            lines[first_line_index][1] = replacement
            lines_to_be_removed.append(second_line_index)
        elif second_xy == second_line[-1]:
            replacement = second_line + first_line
            lines[first_line_index][1] = replacement
            lines_to_be_removed.append(second_line_index)
    elif first_xy == first_line[-1]:
        if second_xy == second_line[0]:
            replacement = first_line + second_line
            lines[first_line_index][1] = replacement
            lines_to_be_removed.append(second_line_index)
        elif second_xy == second_line[-1]:
            replacement = first_line + second_line[::-1]
            lines[first_line_index][1] = replacement
            lines_to_be_removed.append(second_line_index)

for line_index in reversed(lines_to_be_removed):
    a = lines.pop(line_index)

for line in lines:
    if len(line[1]) > 3:
        x, y = map(list, zip(*line[1]))
        plt.plot(x, y, label = "line {}".format(line[0]) )
plt.gca().invert_yaxis()
plt.show()
