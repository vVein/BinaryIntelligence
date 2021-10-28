
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
tolerance = 80

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

edges = []
for edge in edges_lat:
    if edge in edges_diag and edge in edges_rev_lat:
        edges.append(edge)

edges.sort()
edges_unique = list(edges for edges,_ in itertools.groupby(edges))

x_cords, y_cords = zip(*edges)
plt.scatter(*zip(*edges),marker='.', s=0.1)
plt.scatter(x_cords,y_cords,marker='.', s=0.5)
plt.gca().invert_yaxis()
plt.show()
lines = []
used = []
index_rotation = [0,1,-1,2,-2,3,-3]
index_cap = len(index_rotation) + 1

