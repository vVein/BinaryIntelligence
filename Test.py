from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt
import numpy as np
import itertools

# load the image and convert into
# numpy array
img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
  
# asarray() class is used to convert
# PIL images into NumPy arrays
numpydata = asarray(img)
  
# <class 'numpy.ndarray'>
#print(type(numpydata))
  
#  shape
print(numpydata.shape)

print(img.mode)

print(numpydata[331][547][2])

img = Image.fromarray(numpydata, 'RGB')
img.save('my.png')

plt.imshow(img)
plt.show()

list1 = [[15,3],[18,6],[7,82],[18,6]]
list1.sort()
stripped = list(list1 for list1,_ in itertools.groupby(list1))

circular_pattern = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]

print(list1)
print(stripped)
print(circular_pattern[3])
