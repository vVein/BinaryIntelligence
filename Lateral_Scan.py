
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
plt.scatter(x_cords,y_cords,marker='.', s=0.5)
plt.gca().invert_yaxis()
plt.show()