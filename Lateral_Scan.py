
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt
import numpy as np
import itertools

img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
numpydata = asarray(img)

img_width = int(np.size(numpydata,1))
img_height = int(len(numpydata))
edges = []
tolerance = 30

for y in range(img_height):
    previous_added = 0
    for x in range(img_width):
        if x == 0:
            current_pixel = numpydata[y][x]
            continue
        previous_pixel = current_pixel
        current_pixel = numpydata[y][x]
        comparison1 = abs(int(current_pixel[0]) - int(previous_pixel[0])) < tolerance
        comparison2 = abs(int(current_pixel[1]) - int(previous_pixel[1])) < tolerance
        comparison3 = abs(int(current_pixel[2]) - int(previous_pixel[2])) < tolerance
        comparison = [comparison1,comparison2,comparison3]
        equal_arrays = all(comparison)
        if not equal_arrays and previous_added == 0:
            edges.append([x, y])
            previous_added = 2
        elif previous_added > 0:
            previous_added = previous_added - 1

for x in range(img_width):
    previous_added = 0
    for y in range(img_height):
        if y == 0:
            current_pixel = numpydata[y][x]
            continue
        previous_pixel = current_pixel
        current_pixel = numpydata[y][x]
        comparison1 = abs(int(current_pixel[0]) - int(previous_pixel[0])) < tolerance
        comparison2 = abs(int(current_pixel[1]) - int(previous_pixel[1])) < tolerance
        comparison3 = abs(int(current_pixel[2]) - int(previous_pixel[2])) < tolerance
        comparison = [comparison1,comparison2,comparison3]
        equal_arrays = all(comparison)
        if not equal_arrays and previous_added == 0:
            prior_pixel = [x,y-1]
            ahead_pixel = [x,y+1]
            if prior_pixel and ahead_pixel not in edges:
                edges.append([x, y])
            previous_added = 2
        elif previous_added > 0:
            previous_added = previous_added - 1

edges.sort()
edges_unique = list(edges for edges,_ in itertools.groupby(edges))

x_cords, y_cords = zip(*edges)
# plt.scatter(*zip(*edges),marker='.', s=0.1)
#plt.scatter(x_cords,y_cords,marker='.', s=0.5)
#plt.gca().invert_yaxis()
# plt.show()
shapes = []
used = []

shape_no = 0
for xy in edges:
    if xy not in used:
        new_shape = False
        circular_pattern = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]
        prev_dirct_index = 0
        for dirct in circular_pattern:
            xy_n = [xy[0] + dirct[0], xy[1] + dirct[1]]
            if xy_n in edges:
                current_shape = []
                #current_shape_ordered = []
                shape_no = shape_no + 1
                current_shape.append([xy[0],xy[1]])
                current_shape.append([xy_n[0],xy_n[1]])
                #i = 0
                #current_shape_ordered.append([i,xy[0],xy[1]])
                #i = i + 1
                #current_shape_ordered.append([i,xy_n[0],xy_n[1]])
                used.append([xy[0],xy[1]])
                used.append([xy_n[0],xy_n[1]])
                prev_dirct = dirct
                new_shape = True
                break
            else:
                prev_dirct_index = prev_dirct_index + 1

        if new_shape:
            possibilities = 6
            while possibilities > 1:
                possibilities = possibilities - 1
                xy = xy_n
                index_rotation = [0,1,-1,2,-2,3,-3]
                index_cap = len(index_rotation)
                for index_adj in index_rotation:
                    test_index = ( prev_dirct_index + index_adj ) % index_cap
                    new_dirct = circular_pattern[test_index]
                    xy_n = [xy[0] + new_dirct[0], xy[1] + new_dirct[1]]
                    if xy_n in edges and xy_n not in current_shape:
                        used.append([xy_n[0],xy_n[1]])
                        current_shape.append([xy_n[0],xy_n[1]])
                        #i = i + 1
                        #current_shape_ordered.append([i,xy_n[0],xy_n[1]])
                        prev_dirct_index = test_index
                        possibilities = 6
                        break
            shapes.append([shape_no, current_shape])

#print(shapes)

for shape in shapes:
    print(shape[1])
    x, y = map(list, zip(*shape[1]))
    plt.plot(x, y, label = "line {}".format(shape[0]) )
plt.show()