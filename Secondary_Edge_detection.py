
import matplotlib.pyplot as plt
from Colour_functions import *
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'white'

def edge_processing(numpydata, edges_lat, singular_RGB_trigger, RGB_tolerance):
    reduced_edges = edges_lat
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
                    
                    current_pixel = list(numpydata[current_xy[1]][current_xy[0]])
            


    # Lateral scan (Left ro right)
    print('checkmark1 lat scan')
    for y in range(img_height):
        pending_edges_active = False
        pending_edges = []
        pending_r_signs = []
        pending_g_signs = []
        pending_b_signs = []
        for x in range(img_width):
            if x == 0:
                current_pixel = list(numpydata[y][x])
                current_xy = [x, y]
                continue
            previous_pixel = current_pixel
            previous_xy = current_xy
            current_xy = [x, y]
            current_pixel = list(numpydata[y][x])
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, singular_RGB_trigger, RGB_tolerance)
            
            if different_colour:   
                if not pending_edges_active:
                    pending_edges.append([previous_xy[0], previous_xy[1], previous_pixel[0], previous_pixel[1], previous_pixel[2]])
                
                rgb_signs = RGB_sign_delta(previous_pixel, current_pixel)
                   
                pending_r_signs.append(rgb_signs[0])
                pending_g_signs.append(rgb_signs[1])
                pending_b_signs.append(rgb_signs[2])
                list_of_sign_lists = [pending_r_signs, pending_g_signs, pending_b_signs]
                # split if signs flip
                for sign_sublist in list_of_sign_lists:
                    if -1 in sign_sublist and +1 in sign_sublist:
                        returned_edges = edge_variance(pending_edges, singular_RGB_trigger, numpydata)
                        for xy in returned_edges:
                            edges_lat.append(xy)
                        pending_edges = []
                        pending_r_signs = []
                        pending_g_signs = []
                        pending_b_signs = []
                        pending_edges.append([previous_xy[0], previous_xy[1], previous_pixel[0], previous_pixel[1], previous_pixel[2]])
                        pending_edges.append([x, y, current_pixel[0], current_pixel[1], current_pixel[2]])
                        rgb_signs = RGB_sign_delta(previous_pixel, current_pixel)
                        pending_r_signs.append(rgb_signs[0])
                        pending_g_signs.append(rgb_signs[1])
                        pending_b_signs.append(rgb_signs[2])
                        break
                else:
                    pending_edges.append([x, y, current_pixel[0], current_pixel[1], current_pixel[2]])        
                
                pending_edges_active = True   
            else:
                if pending_edges_active:
                    if len(pending_edges) > 1:
                        returned_edges = edge_variance(pending_edges, singular_RGB_trigger, numpydata)
                        for xy in returned_edges:
                            edges_lat.append(xy)
                    elif len(pending_edges) == 1:
                        xy = [pending_edges[0][0], pending_edges[0][1]]
                        edges_lat.append(xy)
                    
                    pending_edges = []
                    pending_r_signs = []
                    pending_g_signs = []
                    pending_b_signs = []
                pending_edges_active = False
                
