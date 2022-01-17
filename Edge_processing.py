
import matplotlib.pyplot as plt
from PIL import Image
from Colour_functions import *
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'white'

# Lateral scan reduction (Left ro right)
def lat_edge_processing(numpydata, edges_lat, singular_RGB_trigger, RGB_tolerance):
    reduced_edges = []
    previous_xy = 0
    for xy in edges_lat:
        if previous_xy == 0:
            current_xy = xy
        else:
            previous_xy = current_xy
            current_xy = xy
            current_x = current_xy[0]
            previous_x = previous_xy[0]
            if current_x == previous_x:
                current_pixel = list(numpydata[current_xy[1]][current_xy[0]])
                previous_pixel = list(numpydata[previous_xy[1]][previous_xy[0]])
                different_colour = pixel_comparison_t(current_pixel, previous_pixel, singular_RGB_trigger, RGB_tolerance)
                
                if not different_colour:
                    width = current_x - previous_x
                    mid_x = previous_x + width / 2
                    mid_xy = [mid_x, current_xy[1]]
                    
                    if width == 1:
                        reduced_edges.append(mid_xy)
                        continue
                    
                    middle_pixel = list(numpydata[mid_xy[1]][mid_xy[0]])
                    different_colour = pixel_comparison_t(current_pixel, middle_pixel, singular_RGB_trigger, RGB_tolerance)
                    
                    if not different_colour:
                        reduced_edges.append(mid_xy)
                        continue
                    
                    else:
                        reduced_edges.append(previous_xy)
                        continue

                else:
                    reduced_edges.append(previous_xy)
                    continue
                
            else:
                reduced_edges.append(previous_xy)
                
    x_cords_3, y_cords_3 = zip(*reduced_edges)
    plt.scatter(*zip(*reduced_edges),marker='.', s=0.1, color='green')
    plt.scatter(x_cords_3, y_cords_3, marker='.', s=0.5, color='green')
    plt.gca().invert_yaxis()
    plt.legend()
    img = Image.fromarray(numpydata, 'RGB')
    img.save('my.png')
    plt.imshow(img)
    plt.show()