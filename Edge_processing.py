
import matplotlib.pyplot as plt
from PIL import Image
from Colour_functions import *
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'white'

# Lateral scan reduction (Left ro right)
def lat_edge_processing(numpydata, edges_lat, singular_RGB_trigger, RGB_tolerance, width_threshold):
    reduced_lat_edges = []
    remaining_lat_edges = []
    first = True
    skip_next = False
    for xy in edges_lat:
        if first:
            current_xy = xy
            first = False
        else:
            previous_xy = current_xy
            current_xy = xy
            current_x = current_xy[0]
            previous_x = previous_xy[0]
            if not skip_next:
                if current_xy[1] == previous_xy[1]:
                    current_pixel = list(numpydata[current_xy[1]][current_xy[0]])
                    previous_pixel = list(numpydata[previous_xy[1]][previous_xy[0]])
                    different_colour = pixel_comparison_t(current_pixel, previous_pixel, singular_RGB_trigger, RGB_tolerance)
                    
                    if not different_colour:
                        width = int (current_x - previous_x)
                        
                        mid_x = previous_x + width / 2
                        mid_xy = [mid_x, current_xy[1]]
                        
                        if width == 1:
                            reduced_lat_edges.append(mid_xy)
                            skip_next = True
                            continue
                        
                        if width < width_threshold:

                            # even width
                            if width % 2 == 0:
                                mid_x = int( previous_x + width / 2)
                                mid_xy = [mid_x, current_xy[1]]
                                middle_pixel = list(numpydata[mid_xy[1]][mid_xy[0]])
                                different_colour = pixel_comparison_t(current_pixel, middle_pixel, singular_RGB_trigger, RGB_tolerance)
                                
                            # odd width   
                            else:                     
                                mid_x1 = int( previous_x + 0.5 + width / 2)
                                mid_x2 = int( previous_x - 0.5 + width / 2)
                                mid_xy1 = [mid_x1, current_xy[1]]
                                mid_xy2 = [mid_x2, current_xy[1]]
                                middle_pixel1 = list(numpydata[mid_xy1[1]][mid_xy1[0]])
                                middle_pixel2 = list(numpydata[mid_xy2[1]][mid_xy2[0]])
                                different_colour1 = pixel_comparison_t(current_pixel, middle_pixel1, singular_RGB_trigger, RGB_tolerance)
                                different_colour2 = pixel_comparison_t(current_pixel, middle_pixel2, singular_RGB_trigger, RGB_tolerance)
                                different_colour = any([different_colour1, different_colour2])
                            
                            if not different_colour:
                                reduced_lat_edges.append(mid_xy)
                                skip_next = True
                                continue                                                  
                            
                        else:
                            remaining_lat_edges.append(previous_xy)
                            continue

                    else:
                        remaining_lat_edges.append(previous_xy)
                        continue
                else:
                    remaining_lat_edges.append(previous_xy)
            else:
                skip_next = False
    
    if 20 == 2:
        x_cords_3, y_cords_3 = zip(*reduced_lat_edges)
        plt.scatter(*zip(*reduced_lat_edges),marker='.', s=0.1, color='green')
        plt.scatter(x_cords_3, y_cords_3, marker='.', s=0.5, color='green')
        plt.gca().invert_yaxis()
        plt.legend()
        img = Image.fromarray(numpydata, 'RGB')
        img.save('my.png')
        plt.imshow(img)
        plt.show()
    
    return reduced_lat_edges, remaining_lat_edges

def vert_edge_processing(numpydata, edges_vert, singular_RGB_trigger, RGB_tolerance, height_threshold):
    reduced_vert_edges = []
    remaining_vert_edges = []
    first = True
    skip_next = False
    for xy in edges_vert:
        if first:
            current_xy = xy
            first = False
        else:
            previous_xy = current_xy
            current_xy = xy
            current_y = current_xy[1]
            previous_y = previous_xy[1]
            if not skip_next:
                if current_xy[0] == previous_xy[0]:
                    current_pixel = list(numpydata[current_xy[1]][current_xy[0]])
                    previous_pixel = list(numpydata[previous_xy[1]][previous_xy[0]])
                    different_colour = pixel_comparison_t(current_pixel, previous_pixel, singular_RGB_trigger, RGB_tolerance)
                    
                    if not different_colour:
                        height = int (current_y - previous_y)
                        
                        mid_y = previous_y + height / 2
                        mid_xy = [current_xy[0], mid_y]
                        
                        if height == 1:
                            reduced_vert_edges.append(mid_xy)
                            skip_next = True
                            continue
                        
                        if height < height_threshold:

                            # even height
                            if height % 2 == 0:
                                mid_y = int( previous_y + height / 2)
                                mid_xy = [current_xy[0], mid_y]
                                middle_pixel = list(numpydata[mid_xy[1]][mid_xy[0]])
                                different_colour = pixel_comparison_t(current_pixel, middle_pixel, singular_RGB_trigger, RGB_tolerance)
                                
                            # odd height   
                            else:                     
                                mid_y1 = int( previous_y + 0.5 + height / 2)
                                mid_y2 = int( previous_y - 0.5 + height / 2)
                                mid_xy1 = [current_xy[0], mid_y1]
                                mid_xy2 = [current_xy[0], mid_y2]
                                middle_pixel1 = list(numpydata[mid_xy1[1]][mid_xy1[0]])
                                middle_pixel2 = list(numpydata[mid_xy2[1]][mid_xy2[0]])
                                different_colour1 = pixel_comparison_t(current_pixel, middle_pixel1, singular_RGB_trigger, RGB_tolerance)
                                different_colour2 = pixel_comparison_t(current_pixel, middle_pixel2, singular_RGB_trigger, RGB_tolerance)
                                different_colour = any([different_colour1, different_colour2])
                            
                            if not different_colour:
                                reduced_vert_edges.append(mid_xy)
                                skip_next = True
                                continue
                            
                        else:
                            remaining_vert_edges.append(previous_xy)
                            continue

                    else:
                        remaining_vert_edges.append(previous_xy)
                        continue
                else:
                    remaining_vert_edges.append(previous_xy)
            else:
                skip_next = False
    
    if 20 == 2:
        x_cords_2, y_cords_2 = zip(*reduced_vert_edges)
        plt.scatter(*zip(*reduced_vert_edges),marker='.', s=0.1, color='green')
        plt.scatter(x_cords_2, y_cords_2, marker='.', s=0.5, color='green')
        x_cords_1, y_cords_1 = zip(*remaining_vert_edges)
        plt.scatter(*zip(*remaining_vert_edges),marker='.', s=0.1, color='blue')
        plt.scatter(x_cords_1, y_cords_1, marker='.', s=0.5, color='blue')
        plt.gca().invert_yaxis()
        plt.legend()
        img = Image.fromarray(numpydata, 'RGB')
        img.save('my.png')
        plt.imshow(img)
        plt.show()
    
    return reduced_vert_edges, remaining_vert_edges

def diag_LR_edge_processing(numpydata, edges_diag_LR, singular_RGB_trigger, RGB_tolerance, height_threshold):
    reduced_diag_LR_edges = []
    remaining_diag_LR_edges = []
    first = True
    skip_next = False
    
    # Potential flaw here: if order is not preserved then xy will not be served in the correct order and the iterator will either
    # have to search each diagonal manually for subsequent edges or inline the processing
    for xy in edges_diag_LR:
        if first:
            current_xy = xy
            first = False
        else:
            previous_xy = current_xy
            current_xy = xy
            current_x = current_xy[0]
            current_y = current_xy[1]
            previous_x = previous_xy[0]
            previous_y = previous_xy[1]
            width = int (current_x - previous_x)
            height = int (current_y - previous_y)
            
            if not skip_next:
                if width == height:
                    current_pixel = list(numpydata[current_y][current_x])
                    previous_pixel = list(numpydata[previous_y][previous_x])
                    different_colour = pixel_comparison_t(current_pixel, previous_pixel, singular_RGB_trigger, RGB_tolerance)
                    
                    if not different_colour:
                        
                        mid_x = previous_x + width / 2
                        mid_y = previous_y + height / 2
                        mid_xy = [mid_x, mid_y]
                        
                        if height == 1:
                            reduced_diag_LR_edges.append(mid_xy)
                            skip_next = True
                            continue
                        
                        if height < height_threshold:

                            # even height; single middle point
                            if height % 2 == 0:
                                mid_x = int( previous_x + width / 2)
                                mid_y = int( previous_y + height / 2)
                                mid_xy = [mid_x, mid_y]
                                middle_pixel = list(numpydata[mid_xy[1]][mid_xy[0]])
                                different_colour = pixel_comparison_t(current_pixel, middle_pixel, singular_RGB_trigger, RGB_tolerance)
                                
                            # odd height; 2 middle points
                            else:                     
                                mid_x1 = int( previous_x + 0.5 + width / 2)
                                mid_x2 = int( previous_x - 0.5 + width / 2)
                                mid_y1 = int( previous_y + 0.5 + height / 2)
                                mid_y2 = int( previous_y - 0.5 + height / 2)
                                mid_xy1 = [mid_x1, mid_y1]
                                mid_xy2 = [mid_x2, mid_y2]
                                middle_pixel1 = list(numpydata[mid_xy1[1]][mid_xy1[0]])
                                middle_pixel2 = list(numpydata[mid_xy2[1]][mid_xy2[0]])
                                different_colour1 = pixel_comparison_t(current_pixel, middle_pixel1, singular_RGB_trigger, RGB_tolerance)
                                different_colour2 = pixel_comparison_t(current_pixel, middle_pixel2, singular_RGB_trigger, RGB_tolerance)
                                different_colour = any([different_colour1, different_colour2])
                            
                            if not different_colour:
                                reduced_diag_LR_edges.append(mid_xy)
                                skip_next = True
                                continue
                            
                        else:
                            remaining_diag_LR_edges.append(previous_xy)
                            continue

                    else:
                        remaining_diag_LR_edges.append(previous_xy)
                        continue
                else:
                    remaining_diag_LR_edges.append(previous_xy)
            else:
                skip_next = False
    
    if 20 == 2:
        x_cords_2, y_cords_2 = zip(*reduced_diag_LR_edges)
        plt.scatter(*zip(*reduced_diag_LR_edges),marker='.', s=0.1, color='green')
        plt.scatter(x_cords_2, y_cords_2, marker='.', s=0.5, color='green')
        x_cords_1, y_cords_1 = zip(*remaining_diag_LR_edges)
        plt.scatter(*zip(*remaining_diag_LR_edges),marker='.', s=0.1, color='orange')
        plt.scatter(x_cords_1, y_cords_1, marker='.', s=0.5, color='orange')
        plt.gca().invert_yaxis()
        plt.legend()
        img = Image.fromarray(numpydata, 'RGB')
        img.save('my.png')
        plt.imshow(img)
        plt.show()
    
    return reduced_diag_LR_edges, remaining_diag_LR_edges

def diag_RL_edge_processing(numpydata, edges_diag_RL, singular_RGB_trigger, RGB_tolerance, height_threshold):
    reduced_diag_RL_edges = []
    remaining_diag_RL_edges = []
    first = True
    skip_next = False
    
    # Potential flaw here: if order is not preserved then xy will not be served in the correct order and the iterator will either
    # have to search each diagonal manually for subsequent edges or inline the processing
    for xy in edges_diag_RL:
        if first:
            current_xy = xy
            first = False
        else:
            previous_xy = current_xy
            current_xy = xy
            current_x = current_xy[0]
            current_y = current_xy[1]
            previous_x = previous_xy[0]
            previous_y = previous_xy[1]
            delta_x = int (current_x - previous_x)
            height = int (current_y - previous_y)
            
            if not skip_next:
                if -1 * delta_x == height:
                    current_pixel = list(numpydata[current_y][current_x])
                    previous_pixel = list(numpydata[previous_y][previous_x])
                    different_colour = pixel_comparison_t(current_pixel, previous_pixel, singular_RGB_trigger, RGB_tolerance)
                    
                    if not different_colour:
                        
                        mid_x = previous_x + delta_x / 2
                        mid_y = previous_y + height / 2
                        mid_xy = [mid_x, mid_y]
                        
                        if height == 1:
                            reduced_diag_RL_edges.append(mid_xy)
                            skip_next = True
                            continue
                        
                        if height < height_threshold:

                            # even height; single middle point
                            if height % 2 == 0:
                                mid_x = int( previous_x + delta_x / 2)
                                mid_y = int( previous_y + height / 2)
                                mid_xy = [mid_x, mid_y]
                                middle_pixel = list(numpydata[mid_xy[1]][mid_xy[0]])
                                different_colour = pixel_comparison_t(current_pixel, middle_pixel, singular_RGB_trigger, RGB_tolerance)
                                
                            # odd height; 2 middle points
                            else:                     
                                mid_x1 = int( previous_x + 0.5 + delta_x / 2)
                                mid_x2 = int( previous_x - 0.5 + delta_x / 2)
                                mid_y1 = int( previous_y - 0.5 + height / 2)
                                mid_y2 = int( previous_y + 0.5 + height / 2)
                                mid_xy1 = [mid_x1, mid_y1]
                                mid_xy2 = [mid_x2, mid_y2]
                                middle_pixel1 = list(numpydata[mid_xy1[1]][mid_xy1[0]])
                                middle_pixel2 = list(numpydata[mid_xy2[1]][mid_xy2[0]])
                                different_colour1 = pixel_comparison_t(current_pixel, middle_pixel1, singular_RGB_trigger, RGB_tolerance)
                                different_colour2 = pixel_comparison_t(current_pixel, middle_pixel2, singular_RGB_trigger, RGB_tolerance)
                                different_colour = any([different_colour1, different_colour2])
                            
                            if not different_colour:
                                reduced_diag_RL_edges.append(mid_xy)
                                skip_next = True
                                continue
                            
                        else:
                            remaining_diag_RL_edges.append(previous_xy)
                            continue

                    else:
                        remaining_diag_RL_edges.append(previous_xy)
                        continue
                else:
                    remaining_diag_RL_edges.append(previous_xy)
            else:
                skip_next = False
    
    if 20 == 2:
        x_cords_2, y_cords_2 = zip(*reduced_diag_RL_edges)
        plt.scatter(*zip(*reduced_diag_RL_edges),marker='.', s=0.1, color='green')
        plt.scatter(x_cords_2, y_cords_2, marker='.', s=0.5, color='green')
        x_cords_1, y_cords_1 = zip(*remaining_diag_RL_edges)
        plt.scatter(*zip(*remaining_diag_RL_edges),marker='.', s=0.1, color='orange')
        plt.scatter(x_cords_1, y_cords_1, marker='.', s=0.5, color='orange')
        plt.gca().invert_yaxis()
        plt.legend()
        img = Image.fromarray(numpydata, 'RGB')
        img.save('my.png')
        plt.imshow(img)
        plt.show()
    
    return reduced_diag_RL_edges, remaining_diag_RL_edges
    
def edge_prioritisation(numpydata, edges_lat, edges_vert, edges_diag_LR, edges_diag_RL):
    
    print('checkmark7 prio combinations')
    edges_prio_1 = []
    edges_prio_2 = []
    edges_prio_3 = []

    #Combine and compile list of cross matches 
    for edge in edges_lat:
        if edge in edges_vert:
            if edge in edges_diag_LR or edge in edges_diag_RL:
                edges_prio_1.append(edge)
                continue
            else:
                edges_prio_2.append(edge)
                continue
        elif edge in edges_diag_LR:
            if edge in edges_diag_RL:
                edges_prio_1.append(edge)
                continue
            else:
                edges_prio_2.append(edge)
                continue
        elif edge in edges_diag_RL:
            edges_prio_2.append(edge)
            continue
        else:
            edges_prio_3.append(edge)
        
    print('checkmark9')
    
    for edge in edges_vert:
        if edge not in edges_lat:
            if edge in edges_diag_LR:
                if edge in edges_diag_RL:
                    edges_prio_1.append(edge)
                    continue
                else:
                    edges_prio_2.append(edge)
                    continue
            elif edge in edges_diag_RL:
                edges_prio_2.append(edge)
                continue
            else:
                edges_prio_3.append(edge)   
    
    for edge in edges_diag_LR:
        if edge not in edges_lat:
            if edge not in edges_vert:
                if edge in edges_diag_RL:
                    edges_prio_2.append(edge)
                    continue
                else:
                    edges_prio_3.append(edge)  

    for edge in edges_diag_RL:
        if edge not in edges_lat:
            if edge not in edges_vert:
                if edge not in edges_diag_LR:
                    edges_prio_3.append(edge)

    print('checkmark10')
    
    if 20 == 2:
        edges_prio_1.sort()
        edges_prio_2.sort()
        edges_prio_3.sort()

        #plot of edges

        x_cords_3, y_cords_3 = zip(*edges_prio_3)
        plt.scatter(*zip(*edges_prio_3),marker='.', s=0.1, color='green')
        plt.scatter(x_cords_3, y_cords_3, marker='.', s=0.5, color='green')
        x_cords_2, y_cords_2 = zip(*edges_prio_2)
        plt.scatter(*zip(*edges_prio_2),marker='.', s=0.1, color='orange')
        plt.scatter(x_cords_2,y_cords_2,marker='.', s=0.5, color='orange')
        x_cords, y_cords = zip(*edges_prio_1)
        plt.scatter(*zip(*edges_prio_1),marker='.', s=0.1, color='red')
        plt.scatter(x_cords,y_cords,marker='.', s=0.5, color='red')
        plt.gca().invert_yaxis()
        plt.legend()
        img = Image.fromarray(numpydata, 'RGB')
        img.save('my.png')
        plt.imshow(img)
        plt.show()
        print('checkmark11')

    return edges_prio_1, edges_prio_2, edges_prio_3