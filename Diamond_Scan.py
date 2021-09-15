
# Import the necessary libraries
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt
import numpy as np
import itertools
  
def starting_centre_point (img_array):
      first_y = int(len(img_array) / 2)
      first_x = int(np.size(img_array,1)/2)
      return first_x, first_y

def colour_inspection_shape (size, img_array, centre_x_1, centre_y_1 ):
     # rows, cols = (1, 2)
     # inspection_colours = [[0 for i in range(cols)] for j in range(rows)]
     # print(centre_x_1, centre_y_1)
      inspection_colours = []
      for i in range(-size,size+1):
            for j in range (-(size-abs(i)),size+1-abs(i)):
                 # print(i,j)
                  x_ordinate = centre_x_1 + j
                  if x_ordinate < 0 or x_ordinate >= img_width:
                        continue
                  y_ordinate = centre_y_1 + i
                  if y_ordinate < 0 or y_ordinate >= img_height:
                        continue
                  # print (x_ordinate, y_ordinate)
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
shape_size = 4
img_width = int(np.size(numpydata,1))
img_height = int(len(numpydata))

centre_x = shape_size
centre_y = shape_size

minimum_match_ratio = 0.7
edges= []

def circular_sweep (centre_x, centre_y):
      # circular_pattern = [[0,2],[1,1],[2,0],[1,-1],[0,-2],[-1,-1],[-2,0],[-1,1]]
      circular_pattern = [[0,1],[1,0],[0,-1],[-1,0]]
      for i in range(len(circular_pattern)):
            next_x = centre_x + shape_size * circular_pattern[i][0]
            if next_x < 0 or next_x >= img_width:
                  continue
            next_y = centre_y + shape_size * circular_pattern[i][1]
            if next_y < 0 or next_y >= img_height:
                  continue
            pattern_B = colour_inspection_shape(shape_size,numpydata,next_x,next_y)
            if len(pattern_B[0]) == 0 or len(pattern_A[0]) == 0 :
                  continue
           # print(pattern_A,pattern_B)
            match_ratio = pattern_match(pattern_A,pattern_B)
            if match_ratio < minimum_match_ratio:
                 # print(pattern_A,pattern_B)
                  x_ordinate = min(centre_x, next_x) + abs(centre_x - next_x)
                  y_ordinate = min(centre_y, next_y) + abs(centre_y - next_y)
                  edges.append([x_ordinate, y_ordinate])

pattern_A = colour_inspection_shape(shape_size,numpydata,centre_x,centre_y)
#print(pattern_A)
circular_sweep(centre_x,centre_y)

x_spacing = 1
y_spacing = 1
no_x_adjustments = int((img_width / x_spacing) - 4)
no_y_adjustments = int((img_height / y_spacing) - 4)

for i in range(no_y_adjustments):
      centre_y = centre_y + y_spacing
      centre_x = shape_size
      for j in range(no_x_adjustments):
            centre_x = centre_x + x_spacing
            pattern_A = colour_inspection_shape(shape_size,numpydata,centre_x,centre_y)
            circular_sweep(centre_x,centre_y)
edges.sort()
list(edges for edges,_ in itertools.groupby(edges))
print(edges)

plt.scatter(*zip(*edges))
plt.gca().invert_yaxis()
plt.show()

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
