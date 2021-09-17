
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt
import numpy as np
import itertools

img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
numpydata = asarray(img)

img_width = int(np.size(numpydata,1))
img_height = int(len(numpydata))
edges= []

for y in range(img_height):
    for x in range(img_width):
        if x == 0:
            current_pixel = numpydata[y][x]
            continue
        previous_pixel = current_pixel
        current_pixel = numpydata[y][x]
        comparison1 = abs(int(current_pixel[0]) - int(previous_pixel[0])) < 15
        comparison2 = abs(int(current_pixel[1]) - int(previous_pixel[1])) < 15
        comparison3 = abs(int(current_pixel[2]) - int(previous_pixel[2])) < 15
        comparison = [comparison1,comparison2,comparison3]
        equal_arrays = all(comparison)
        if not equal_arrays:
            edges.append([x, y])
edges.sort()
edges_unique = list(edges for edges,_ in itertools.groupby(edges))
x_cords, y_cords = zip(*edges)
# plt.scatter(*zip(*edges),marker='.', s=0.1)
plt.scatter(x_cords,y_cords,marker='.', s=0.5)
plt.gca().invert_yaxis()
plt.show()