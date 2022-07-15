
import matplotlib.pyplot as plt
from Colour_functions import *
from Edge_detection import *

lines = []
used = []
index_rotation = [0, 1, -1, 2, -2, 3, -3]
circular_pattern = [[0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1]]
circular_pattern_multipliers = [0.5, 1]
direction_weighting = [50, 40, 40, 30, 30, 20, 20]
edges_prio_1_weighting = 125
edges_prio_2_weighting = 60
edges_prio_3_weighting = 30
weighting_threshold = 300
index_cap = len(index_rotation) + 1
shape_no = 0
current_shape = []

# Polyline functions:
def generate_outlines(numpydata, edges_lat, edges_vert, edges_diag_LR, edges_diag_RL, direction_weighting = [50, 40, 40, 30, 30, 20, 20], 
                      weighting_threshold = 100, weighting_base = 200, weighting_division_coefficient = 2,
                      colour_match_minimum = 20, start_point_return_weighting = 5, minimum_polyline_loop_length = 12):

    print('generate outlines')
    
    edges_combined = edges_lat + edges_vert + edges_diag_LR + edges_diag_RL

    def generate_polyline(start_point, prev_dirct_index, last_stored_xy):
        
        global current_shape
        completed_loop = False
        suitable_matches = True
        
        while suitable_matches and not completed_loop:
            
            xy = last_stored_xy
            
            # build list of suitable surrounding points and select best match 
            # empty list 
            surrounding_pixels_weighted = []
            # start with closest step spacing then work outwards
            for multiplier in circular_pattern_multipliers:
                for n, index_adj in enumerate(index_rotation):
                    # determine new directional index, starts with direction of previous stored edge
                    applied_index = ( prev_dirct_index + index_adj ) % index_cap
                    direction = circular_pattern[applied_index]
                    # next pixel to test xy
                    test_pixel = [xy[0] + direction[0] * multiplier, xy[1] + direction[1] * multiplier]
                    
                    # match adjacent pixel to edge in lists if present
                    
                    for xyrgb in edges_combined:
                        if xyrgb[0:1] == test_pixel:
                            adjacent_pixel = xyrgb
                    # 
                    colour_match_weighting = weighted_colour_match_v(numpydata, xy, adjacent_pixel, weighting_base, weighting_division_coefficient)
                    
                    if colour_match_weighting < colour_match_minimum:
                        continue
                    
                    if adjacent_pixel == start_point and len(current_shape) > minimum_polyline_loop_length:
                        pixel_weight = edges_prio_1_weighting + colour_match_weighting + directional_weighting + start_point_return_weighting
                        surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                        continue
                                
                    if adjacent_pixel in used:
                        continue

                    directional_weighting = direction_weighting[n]
                    
                    pixel_weight = directional_weighting + colour_match_weighting
                        
                    surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
   
            
            if len(surrounding_pixels_weighted) == 0:
                suitable_matches = False
                break
            
            surrounding_pixels_weighted.sort(key = lambda surrounding_pixels_weighted : surrounding_pixels_weighted[2], reverse = True)
            xy_n = [surrounding_pixels_weighted[0][0], surrounding_pixels_weighted[0][1]]
            xy_n_weight = surrounding_pixels_weighted[0][2]
                
            if xy_n == start_point and len(current_shape) > 12:
                current_shape.append(xy_n)
                completed_loop = True
                break
            
            if xy_n_weight >= weighting_threshold:
                used.append(xy_n)
                current_shape.append(xy_n)
                last_stored_xy = xy_n
                delta = [xy_n[0]-xy[0],xy_n[1]-xy[1]]
                dirct_index = [indx for indx, dirct in enumerate(circular_pattern) if dirct == delta]
                prev_dirct_index = dirct_index[0]

            if xy_n_weight < weighting_threshold:
                suitable_matches = False

    # this is the beginning of the routine, unfortunate positioning
    def start_new_polylines():
        global shape_no, current_shape
        for xy in edges_combined:
            
            new_shape = False
            surrounding_pixel_in_used = False
            
            if xy not in used:

                prev_dirct_index = 0
                start_point = xy
                            
                # find best first point          
                # build list of suitable surrounding points and select best match 
                
                surrounding_pixels_weighted = []
                
                # start with closest step spacing then work outwards
                for multiplier in circular_pattern_multipliers:
                    # surrounding pattern
                    for index in range(len(circular_pattern)):
                        
                        direction = circular_pattern[index]

                        adjacent_pixel = [xy[0] + direction[0] * multiplier, xy[1] + direction[1] * multiplier]
                    
                        # prevent use of pixels adjacent to used ones
                        if adjacent_pixel in used:
                            surrounding_pixel_in_used = True
                            break
                                                
                        colour_match_weighting = weighted_colour_match_v(numpydata, xy, adjacent_pixel, weighting_base, weighting_division_coefficient)
                    
                        if colour_match_weighting < colour_match_minimum:
                            continue
                                                
                        surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], colour_match_weighting])
                
                # move on to a new pixel if nearby pixel already used
                if surrounding_pixel_in_used:
                    continue
                    
                if len(surrounding_pixels_weighted) == 0:
                    continue
                        
                surrounding_pixels_weighted.sort(key = lambda surrounding_pixels_weighted : surrounding_pixels_weighted[2], reverse = True)
                xy_n = [surrounding_pixels_weighted[0][0], surrounding_pixels_weighted[0][1]]
                xy_n_weight = surrounding_pixels_weighted[0][2]
                
                if xy_n_weight >= weighting_threshold:
                    current_shape = []
                    shape_no = shape_no + 1
                    current_shape.append([xy[0], xy[1]])
                    current_shape.append([xy_n[0], xy_n[1]])
                    used.append([xy[0], xy[1]])
                    used.append([xy_n[0], xy_n[1]])
                    new_shape = True
                    delta = [xy_n[0] - xy[0], xy_n[1] - xy[1]]
                    
                    # account for half steps
                    if isinstance(delta[0], float):
                        old_delta = delta
                        delta = [int(old_delta[0] * 2), int(old_delta[1] * 2)]

                    dirct_index = [indx for indx, dirct in enumerate(circular_pattern) if dirct == delta]
                    prev_dirct_index = dirct_index[0]
                    last_stored_xy = xy_n

            # Add to new polyline            
            if new_shape:
                generate_polyline(start_point, prev_dirct_index, last_stored_xy)
                
                lines.append([shape_no, current_shape])

    start_new_polylines()

    print('outlines generated')

    # filter short lines
    final_lines = []
    
    for line in lines:
        if len(line[1]) > 6:
            final_lines.append(line)

    if 2 == 2:
        for line in final_lines:
            print(line)
            x, y = map(list, zip(*line[1]))
            plt.plot(x, y, label = "line {}".format(line[0]) )
        plt.gca().invert_yaxis()
        img = Image.fromarray(numpydata, 'RGB')
        img.save('my.png')
        plt.imshow(img)
        plt.show()
        
    return final_lines
