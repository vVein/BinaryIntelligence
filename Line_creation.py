
import matplotlib.pyplot as plt
from Colour_functions import *
from Edge_detection import *

lines = []
used = []
index_rotation = [0, 1, -1, 2, -2, 3, -3]
circular_pattern = [[0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1]]
direction_weighting = [50, 40, 40, 30, 30, 20, 20]
edges_prio_1_weighting = 125
edges_prio_2_weighting = 60
edges_prio_3_weighting = 30
weighting_threshold = 300
index_cap = len(index_rotation) + 1
shape_no = 0
current_shape = []

# Polyline functions:
def generate_outlines(numpydata, edges_prio_1, edges_prio_2, edges_prio_3, direction_weighting = [50, 40, 40, 30, 30, 20, 20], 
                      edges_prio_1_weighting = 125, edges_prio_2_weighting = 60, edges_prio_3_weighting = 30, weighting_threshold = 300, 
                      weighting_base = 200, weighting_division_coefficient = 2, rgb_delta_limit = 30, centre_weighting_division_coefficient = 3,
                      weighting_base_cm = 200, colour_match_limit = 20, start_point_return_weighting = 5):

    def generate_polyline(start_point, prev_dirct_index, last_stored_xy):
        global current_shape
        completed_loop = False
        suitable_matches = True
        while suitable_matches and not completed_loop:
            
            xy = last_stored_xy
            
            # build list of suitable surrounding points and select best match  
            surrounding_pixels_weighted = []
            for n, index_adj in enumerate(index_rotation):
                applied_index = ( prev_dirct_index + index_adj ) % index_cap
                direction = circular_pattern[applied_index]
                adjacent_pixel = [xy[0] + direction[0], xy[1] + direction[1]]
                
                left_colour_match_weighting = weighted_left_colour_match(numpydata, circular_pattern, xy, adjacent_pixel, prev_dirct_index, 
                                                                         applied_index, weighting_base, weighting_division_coefficient)
                right_colour_match_weighting = weighted_right_colour_match(numpydata, circular_pattern, xy, adjacent_pixel, prev_dirct_index,
                                                                           applied_index, weighting_base, weighting_division_coefficient)
                
                left_right_center_colour_match_weighting = left_right_center_colour_match(numpydata, circular_pattern, adjacent_pixel, 
                                                                                        applied_index, rgb_delta_limit, centre_weighting_division_coefficient)
                if left_right_center_colour_match_weighting < 0:
                    continue
                
                colour_match_weighting = weighted_colour_match(numpydata, xy, adjacent_pixel, weighting_base_cm)
                
                if colour_match_weighting < colour_match_limit:
                    continue
                
                weighted_perpendicular_colour_match_value = left_colour_match_weighting + right_colour_match_weighting
                
                if adjacent_pixel == start_point and len(current_shape) > 12:
                    pixel_weight = edges_prio_1_weighting + colour_match_weighting + directional_weighting + start_point_return_weighting + weighted_perpendicular_colour_match_value
                    surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                    continue
                            
                if adjacent_pixel in used:
                    continue

                directional_weighting = direction_weighting[n]
                
                partial_pixel_weight = left_right_center_colour_match_weighting + directional_weighting + weighted_perpendicular_colour_match_value + colour_match_weighting
                    
                if adjacent_pixel in edges_prio_1:
                    pixel_weight = edges_prio_1_weighting + partial_pixel_weight
                    surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                elif adjacent_pixel in edges_prio_2:
                    pixel_weight = edges_prio_2_weighting + partial_pixel_weight
                    surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                elif adjacent_pixel in edges_prio_3:
                    pixel_weight = edges_prio_3_weighting + partial_pixel_weight
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

    def start_new_polylines():
        global shape_no, current_shape
        for xy in edges_prio_1:
            
            new_shape = False
            surrounding_pixel_in_used = False
                    
            if xy not in used:

                prev_dirct_index = 0
                start_point = xy
                            
                # find best first point          
                # build list of suitable surrounding points and select best match 
                   
                surrounding_pixels_weighted = []
                for index in range(len(circular_pattern)):
                    direction = circular_pattern[index]
                    adjacent_pixel = [xy[0] + direction[0], xy[1] + direction[1]]
                
                    if adjacent_pixel in used:
                        surrounding_pixel_in_used = True
                        break
                    
                    left_colour_match_weighting = weighted_left_colour_match(numpydata, circular_pattern, xy, adjacent_pixel, index, index,
                                                                             weighting_base, weighting_division_coefficient)
                    right_colour_match_weighting = weighted_right_colour_match(numpydata, circular_pattern, xy, adjacent_pixel, index, index,
                                                                               weighting_base, weighting_division_coefficient)  
                    
                    left_right_center_colour_match_weighting = left_right_center_colour_match(numpydata, circular_pattern, adjacent_pixel, index,
                                                                                              rgb_delta_limit, centre_weighting_division_coefficient)
                    if left_right_center_colour_match_weighting < 0:
                        continue
                                       
                    weighted_perpendicular_colour_match_value = left_colour_match_weighting + right_colour_match_weighting
                    
                    colour_match_weighting = weighted_colour_match(numpydata, xy, adjacent_pixel, weighting_base_cm)
                
                    if colour_match_weighting < colour_match_limit:
                        continue
                    
                    directional_weighting = direction_weighting[0]
                    
                    partial_pixel_weight = left_right_center_colour_match_weighting + directional_weighting + weighted_perpendicular_colour_match_value + colour_match_weighting
                    
                    if adjacent_pixel in edges_prio_1:
                        pixel_weight = edges_prio_1_weighting + partial_pixel_weight
                        surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                    elif adjacent_pixel in edges_prio_2:
                        pixel_weight = edges_prio_2_weighting + partial_pixel_weight
                        surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                    elif adjacent_pixel in edges_prio_3:
                        pixel_weight = edges_prio_3_weighting + partial_pixel_weight
                        surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                
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
                    dirct_index = [indx for indx, dirct in enumerate(circular_pattern) if dirct == delta]
                    prev_dirct_index = dirct_index[0]
                    last_stored_xy = xy_n

            # Add to new polyline            
            if new_shape:
                generate_polyline(start_point, prev_dirct_index, last_stored_xy)
                
                lines.append([shape_no, current_shape])
                
    print('checkmark12 outlines')

    start_new_polylines()

    print('checkmark14 outlines generated')

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
