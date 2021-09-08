
# Import the necessary libraries
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt
import numpy as np
  
def starting_centre_point (img_array):
      first_y = int(len(img_array) / 2)
      first_x = int(np.size(img_array,1)/2)
      return first_x, first_y

def colour_inspection_shape (size, img_array, centre_x, centre_y ):
     # rows, cols = (1, 2)
     # inspection_colours = [[0 for i in range(cols)] for j in range(rows)]
      inspection_colours = []
      for i in range(-size,size+1):
            for j in range (-(size-abs(i)),size+1-abs(i)):
                 # print(i,j)
                  x_ordinate = centre_x + j
                  y_ordinate = centre_y + i
                  pixel = img_array[y_ordinate][x_ordinate]
                  inspection_colours.append([pixel[0],pixel[1],pixel[2]])
      
      # inspection_colours = np.array([centre_x, centre_y], dtype = int)
      # inspection_colours = np.append(inspection_colours, [x_ordinate,y_ordinate])
      inspection_colours = np.array(inspection_colours)
      colours, counts = np.unique(inspection_colours, axis=0, return_counts=True)
      passing = 0.3
      pattern_colours = []
      pattern_counts = []
      no = np.size(inspection_colours,0)
      counts = [count/no for count in counts]
      for k in range(len(counts)):
            if counts[k] > passing:
                  pattern_colours.append(colours[k])
                  pattern_counts.append(counts[k])
      return pattern_colours, pattern_counts
      # print(inspection_colours)

def pattern_match (p1, p2):
      sub_total_max = max (np.sum(p1[1]), np.sum(p2[1]))
      running_total = 0
      for i in range(len(p1[0])) :
            for j in range(len(p2[0])):
                  comparison = p1[0][i] == p2[0][j]
                  equal_arrays = comparison.all()
                  if equal_arrays:
                        running_total =  running_total + min(p1[1][i],p2[1][j])
      match_ratio = running_total / sub_total_max
      return match_ratio

# load the image and convert into
# numpy array
img = Image.open(r'C:\Users\Stude\OneDrive\Pictures\Image-Analysis\Shapes.jpg')
  
# asarray() class is used to convert
# PIL images into NumPy arrays
numpydata = asarray(img)
  
# <class 'numpy.ndarray'>
#print(type(numpydata))
  
#  shape
#print(numpydata.shape)

#print(img.mode)

#print(numpydata[0][0][2])
first_centre_x = int(np.size(numpydata,1)/2)
first_centre_y = int(len(numpydata) / 2)
shape_size = 5
minimum_match_ratio = 0.7
edges= []

def circular_sweep (centre_x, centre_y):
      circular_pattern = [[0,2],[1,1],[2,0],[1,-1],[0,-2],[-1,-1],[-2,0],[-1,1]]
      for i in range(len(circular_pattern)):
            next_x = centre_x + shape_size * circular_pattern[i][0]
            next_y = centre_y + shape_size * circular_pattern[i][1]
            pattern_B = colour_inspection_shape(shape_size,numpydata,next_x,next_y)
            print(next_x)
            match_ratio = pattern_match(pattern_A,pattern_B)
            if match_ratio < minimum_match_ratio:
                  x_ordinate = min(first_centre_x, next_x) + abs(first_centre_x - next_x)
                  y_ordinate = min(first_centre_y, next_y) + abs(first_centre_y - next_y)
                  edges.append([x_ordinate,y_ordinate])

pattern_A = colour_inspection_shape(shape_size,numpydata,first_centre_x,first_centre_y)
print(pattern_A)
circular_sweep(first_centre_x,first_centre_y)

print(edges)

#img = Image.fromarray(numpydata, 'RGB')
#img.save('my.png')
#plt.imshow(img)
#plt.show()

pixel1 = numpydata[0][0]
pixel2 = numpydata[0][1]
delta = pixel1[0]-pixel2[0]

for y in numpydata:
      for x in y:
            pixelx = x
#print(pixelx)
