
import matplotlib.pyplot as plt
import numpy as np
from Colour_functions import *
from PIL import Image
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'white'

def image_edge_detection(image_as_numpyarray, RGB_tolerance = 120, singular_RGB_trigger = 50):
    numpydata = image_as_numpyarray
    
    img_width = int(np.size(numpydata,1))
    img_height = int(len(numpydata))
    edges_lat = []
    edges_vert = []
    edges_diag_LR = []
    edges_diag_RL = []
    pending_edges = []
    pending_r_signs = []
    pending_g_signs = []
    pending_b_signs = []

    # Lateral scan (Left ro right)
    print('checkmark1 lat scan')
    for y in range(img_height):
        pending_edges_active = False
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
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, RGB_tolerance)
            
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
                
    print('checkmark2 vert scan')
    # Vertical scan (Top to bottom)
    pending_edges = []
    for x in range(img_width):
        previous_check_different_colour = False
        for y in range(img_height):
            if y == 0:
                current_pixel = list(numpydata[y][x])
                current_xy = [x, y]
                continue
            previous_pixel = current_pixel
            previous_xy = current_xy
            current_xy = [x, y]
            current_pixel = list(numpydata[y][x])
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, RGB_tolerance)
            
            if different_colour:
                if not previous_check_different_colour:
                    pending_edges.append([previous_xy[0], previous_xy[1], previous_pixel[0], previous_pixel[1], previous_pixel[2]])
                pending_edges.append([x, y, current_pixel[0], current_pixel[1], current_pixel[2]])
                previous_check_different_colour = True
            else:
                if previous_check_different_colour:
                    if len(pending_edges) > 1:
                        returned_edges = edge_variance(pending_edges, singular_RGB_trigger, numpydata)
                        for xy in returned_edges:
                            edges_vert.append(xy)
                    elif len(pending_edges) == 1:
                        xy = [pending_edges[0][0], pending_edges[0][1]]
                        edges_vert.append(xy)
                    
                    pending_edges = []
                previous_check_different_colour = False

    print('checkmark3 L-R scan')
    # Diagonal scan L-R
    pending_edges = []
    for x_start in range(img_width):
        previous_check_different_colour = False
        for x in range(x_start, img_width):
            if x == x_start:
                y = 0
                current_pixel = list(numpydata[y][x])
                current_xy = [x, y]
                continue

            previous_pixel = current_pixel
            previous_xy = current_xy
            current_xy = [x, y]
            y = y + 1
            if y > img_height - 1:
                continue

            current_pixel = list(numpydata[y][x])
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, RGB_tolerance)
            if different_colour:
                if not previous_check_different_colour:
                    pending_edges.append([previous_xy[0], previous_xy[1], previous_pixel[0], previous_pixel[1], previous_pixel[2]])
                pending_edges.append([x, y, current_pixel[0], current_pixel[1], current_pixel[2]])
                previous_check_different_colour = True
            else:
                if previous_check_different_colour:
                    if len(pending_edges) > 1:
                        returned_edges = edge_variance(pending_edges, singular_RGB_trigger, numpydata)
                        for xy in returned_edges:
                            edges_diag_LR.append(xy)
                    elif len(pending_edges) == 1:
                        xy = [pending_edges[0][0], pending_edges[0][1]]
                        edges_diag_LR.append(xy)
                    
                    pending_edges = []
                previous_check_different_colour = False

    print('checkmark4 L-R scan pt 2')
    # Diagonal scan L-R
    pending_edges = []
    for y_start in range(img_height):
        previous_check_different_colour = False
        for y in range(y_start, img_width):
            if y == y_start:
                x = 0
                current_pixel = list(numpydata[y][x])
                current_xy = [x, y]
                continue

            previous_pixel = current_pixel
            previous_xy = current_xy
            current_xy = [x, y]
            x = x + 1
            if x > img_width - 1 or y > img_height - 1:
                continue

            current_pixel = list(numpydata[y][x])
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, RGB_tolerance)
            if different_colour:
                if not previous_check_different_colour:
                    pending_edges.append([previous_xy[0], previous_xy[1], previous_pixel[0], previous_pixel[1], previous_pixel[2]])
                pending_edges.append([x, y, current_pixel[0], current_pixel[1], current_pixel[2]])
                previous_check_different_colour = True
            else:
                if previous_check_different_colour:
                    if len(pending_edges) > 1:
                        returned_edges = edge_variance(pending_edges, singular_RGB_trigger, numpydata)
                        for xy in returned_edges:
                            edges_diag_LR.append(xy)
                    elif len(pending_edges) == 1:
                        xy = [pending_edges[0][0], pending_edges[0][1]]
                        edges_diag_LR.append(xy)
                    
                    pending_edges = []
                previous_check_different_colour = False

    print('checkmark5 R-L scan')
    # Diagonal scan R-L
    pending_edges = []
    for x_start in range(img_width - 1, 0, -1):
        previous_check_different_colour = False
        for x in range(x_start - 1, 0, -1):
            if x == x_start - 1:
                y = 0
                current_pixel = list(numpydata[y][x])
                current_xy = [x, y]
                continue

            previous_pixel = current_pixel
            previous_xy = current_xy
            current_xy = [x, y]
            y = y + 1
            if y > img_height - 1:
                continue

            current_pixel = list(numpydata[y][x])
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, RGB_tolerance)
            if different_colour:
                if not previous_check_different_colour:
                    pending_edges.append([previous_xy[0], previous_xy[1], previous_pixel[0], previous_pixel[1], previous_pixel[2]])
                pending_edges.append([x, y, current_pixel[0], current_pixel[1], current_pixel[2]])
                previous_check_different_colour = True
            else:
                if previous_check_different_colour:
                    if len(pending_edges) > 1:
                        returned_edges = edge_variance(pending_edges, singular_RGB_trigger, numpydata)
                        for xy in returned_edges:
                            edges_diag_RL.append(xy)
                    elif len(pending_edges) == 1:
                        xy = [pending_edges[0][0], pending_edges[0][1]]
                        edges_diag_RL.append(xy)
                    pending_edges = []
                previous_check_different_colour = False

    print('checkmark6 R-L scan pt 2')
    # Diagonal scan R-L
    pending_edges = []
    for y_start in range(img_height - 1, 0, -1):
        previous_check_different_colour = False
        for y in range(y_start, img_height):
            if y == y_start:
                x = img_width - 1
                current_pixel = list(numpydata[y][x])
                current_xy = [x, y]
                continue

            previous_pixel = current_pixel
            previous_xy = current_xy
            current_xy = [x, y]
            x = x - 1
            if x > img_width - 1 or y > img_height - 1:
                continue

            current_pixel = list(numpydata[y][x])
            different_colour = pixel_comparison_t(current_pixel, previous_pixel, RGB_tolerance)
            if different_colour:
                if not previous_check_different_colour:
                    pending_edges.append([previous_xy[0], previous_xy[1], previous_pixel[0], previous_pixel[1], previous_pixel[2]])
                pending_edges.append([x, y, current_pixel[0], current_pixel[1], current_pixel[2]])
                previous_check_different_colour = True
            else:
                if previous_check_different_colour:
                    if len(pending_edges) > 1:
                        returned_edges = edge_variance(pending_edges, singular_RGB_trigger, numpydata)
                        for xy in returned_edges:
                            edges_diag_RL.append(xy)
                    elif len(pending_edges) == 1:
                        xy = [pending_edges[0][0], pending_edges[0][1]]
                        edges_diag_RL.append(xy)
                    
                    pending_edges = []
                previous_check_different_colour = False

    if 20 == 2:
        
        x_cords_3, y_cords_3 = zip(*edges_lat)
        plt.scatter(*zip(*edges_lat),marker='.', s=0.1, color='green')
        plt.scatter(x_cords_3, y_cords_3, marker='.', s=0.5, color='green')
        plt.gca().invert_yaxis()
        plt.legend()
        img = Image.fromarray(numpydata, 'RGB')
        img.save('my.png')
        plt.imshow(img)
        plt.show()
        
        x_cords_2, y_cords_2 = zip(*edges_vert)
        plt.scatter(*zip(*edges_vert),marker='.', s=0.1, color='blue')
        plt.scatter(x_cords_2,y_cords_2,marker='.', s=0.5, color='blue')
        plt.gca().invert_yaxis()
        plt.legend()
        plt.imshow(img)
        plt.show()
        
        x_cords_3, y_cords_3 = zip(*edges_lat)
        plt.scatter(*zip(*edges_lat),marker='.', s=0.1, color='green')
        plt.scatter(x_cords_3, y_cords_3, marker='.', s=0.5, color='green')
        x_cords_2, y_cords_2 = zip(*edges_vert)
        plt.scatter(*zip(*edges_vert),marker='.', s=0.1, color='blue')
        plt.scatter(x_cords_2,y_cords_2,marker='.', s=0.5, color='blue')
        plt.gca().invert_yaxis()
        plt.legend()
        plt.imshow(img)
        plt.show()
        
        x_cords, y_cords = zip(*edges_diag_RL)
        plt.scatter(*zip(*edges_diag_RL),marker='.', s=0.1, color='red')
        plt.scatter(x_cords,y_cords,marker='.', s=0.5, color='red')
        plt.gca().invert_yaxis()
        plt.legend()
        plt.imshow(img)
        plt.show()
        
        x_cords_4, y_cords_4 = zip(*edges_diag_RL)
        plt.scatter(*zip(*edges_diag_LR),marker='.', s=0.1, color='grey')
        plt.scatter(x_cords_4, y_cords_4, marker='.', s=0.5, color='grey')
        plt.gca().invert_yaxis()
        plt.legend()
        plt.imshow(img)
        plt.show()

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
    
    edges_prio_1.sort()
    edges_prio_2.sort()
    edges_prio_3.sort()

    #plot of edges

    x_cords_3, y_cords_3 = zip(*edges_prio_3)
    plt.scatter(*zip(*edges_prio_3),marker='.', s=0.1, color='green')
    plt.scatter(x_cords_3, y_cords_3, marker='.', s=0.5, color='green')
    x_cords_2, y_cords_2 = zip(*edges_prio_2)
    plt.scatter(*zip(*edges_prio_2),marker='.', s=0.1, color='blue')
    plt.scatter(x_cords_2,y_cords_2,marker='.', s=0.5, color='blue')
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