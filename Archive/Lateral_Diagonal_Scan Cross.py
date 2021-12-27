
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt
import numpy as np
import itertools

img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
numpydata = asarray(img)

img_width = int(np.size(numpydata,1))
img_height = int(len(numpydata))
edges_lat = []
edges_rev_lat = []
edges_diag = []
tolerance = 140

def pixel_comparison(current_pixel, previous_pixel):
    comparison1 = abs(int(current_pixel[0]) - int(previous_pixel[0]))
    comparison2 = abs(int(current_pixel[1]) - int(previous_pixel[1]))
    comparison3 = abs(int(current_pixel[2]) - int(previous_pixel[2]))
    comparison = (comparison1 + comparison2 + comparison3 ) > tolerance
    return comparison

# Lateral scan (Left ro right)
for y in range(img_height):
    previous_added = 0
    for x in range(img_width):
        if x == 0:
            current_pixel = numpydata[y][x]
            continue
        previous_pixel = current_pixel
        current_pixel = numpydata[y][x]
        different_colour = pixel_comparison(current_pixel, previous_pixel)
        if different_colour and previous_added == 0:
            edges_lat.append([x, y])
            previous_added = 2
        elif previous_added > 0:
            previous_added = previous_added - 1

# Lateral scan (Top to bottom)
for x in range(img_width):
    previous_added = 0
    for y in range(img_height):
        if y == 0:
            current_pixel = numpydata[y][x]
            continue
        previous_pixel = current_pixel
        current_pixel = numpydata[y][x]
        different_colour = pixel_comparison(current_pixel, previous_pixel)
        if different_colour and previous_added == 0:
            edges_lat.append([x, y])
            previous_added = 2
        elif previous_added > 0:
            previous_added = previous_added - 1

# Reverse Lateral scan (Right to left)
for y in range(img_height):
    previous_added = 0
    for x in range(img_width - 1, 0, -1):
        if x == img_width - 1:
            current_pixel = numpydata[y][x]
            continue
        previous_pixel = current_pixel
        current_pixel = numpydata[y][x]
        different_colour = pixel_comparison(current_pixel, previous_pixel)
        if different_colour and previous_added == 0:
            edges_rev_lat.append([x, y])
            previous_added = 2
        elif previous_added > 0:
            previous_added = previous_added - 1

# Reverse Lateral scan (Bottom to top)
for x in range(img_width):
    previous_added = 0
    for y in range(img_height - 1, 0, -1):
        if y == img_height - 1:
            current_pixel = numpydata[y][x]
            continue
        previous_pixel = current_pixel
        current_pixel = numpydata[y][x]
        different_colour = pixel_comparison(current_pixel, previous_pixel)
        if different_colour and previous_added == 0:
            edges_rev_lat.append([x, y])
            previous_added = 2
        elif previous_added > 0:
            previous_added = previous_added - 1

# Diagonal scan
for x_start in range(img_width):
    previous_added = 0
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
        if different_colour and previous_added == 0:
            edges_diag.append([x, y])
            previous_added = 2
        elif previous_added > 0:
            previous_added = previous_added - 1

# Diagonal scan
for y_start in range(img_height):
    previous_added = 0

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
        if different_colour and previous_added == 0:
            edges_diag.append([x, y])
            previous_added = 2
        elif previous_added > 0:
            previous_added = previous_added - 1

# Diagonal scan
for x_start in range(img_width-1, 0, -1):
    previous_added = 0
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
        if different_colour and previous_added == 0:
            edges_diag.append([x, y])
            previous_added = 2
        elif previous_added > 0:
            previous_added = previous_added - 1

# Diagonal scan
for y_start in range(img_height - 1, 0, -1):
    previous_added = 0

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
        if different_colour and previous_added == 0:
            prior_pixel = [x + 1, y - 1]
            ahead_pixel = [x - 1, y + 1]
            if prior_pixel and ahead_pixel not in edges_diag:
                edges_diag.append([x, y])
        elif previous_added > 0:
            previous_added = previous_added - 1

edges_prio_1 = []
edges_prio_2 = []
edges_prio_3 = []

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
index_cap = len(index_rotation) + 1

shape_no = 0
for xy in edges_prio_1:
    if xy not in used:
        new_shape = False
        circular_pattern = [[0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1]]
        prev_dirct_index = 0
        start_point = xy
        for dirct_index, dirct in enumerate(circular_pattern):
            xy_n = [xy[0] + dirct[0], xy[1] + dirct[1]]
            if xy_n in edges_prio_1 or edges_prio_2 :
                current_shape = []
                shape_no = shape_no + 1
                current_shape.append([xy[0],xy[1]])
                current_shape.append([xy_n[0],xy_n[1]])
                used.append([xy[0],xy[1]])
                used.append([xy_n[0],xy_n[1]])
                prev_dirct = dirct
                new_shape = True  
                prev_dirct_index = dirct_index
                break

        if new_shape:
            possibilities = 14
            while possibilities > 1:
                possibilities = possibilities - 1
                xy = xy_n
                for index_adj in index_rotation:
                    test_index = ( prev_dirct_index + index_adj ) % index_cap
                    new_dirct = circular_pattern[test_index]
                    xy_n = [xy[0] + new_dirct[0], xy[1] + new_dirct[1]]

                    if xy_n == start_point:
                        current_shape.append(xy_n)
                        possibilities = 0
                        break

                    elif xy_n in edges_prio_1 and xy_n not in used:
                        used.append(xy_n)
                        current_shape.append(xy_n)
                        prev_dirct_index = test_index
                        possibilities = 14
                        break

                

            lines.append([shape_no, current_shape])

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
