
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
previous_rgbs = []

# Polyline functions:
def generate_outlines(numpydata, edges_lat, edges_vert, edges_diag_LR, edges_diag_RL, direction_weighting = [50, 40, 40, 30, 30, 20, 20], 
                      weighting_threshold = 80, weighting_base = 250, weighting_division_coefficient = 2,
                      colour_match_minimum = 20, start_point_return_weighting = 5, minimum_polyline_loop_length = 12, 
                      directional_multiplier_weighting = 35, trailing_rgb_length = 10):

    print('generate outlines')
    
    edges_combined = edges_lat + edges_vert + edges_diag_LR + edges_diag_RL

    def generate_polyline(start_point, prev_dirct_index, last_stored_xyrgb, previous_rgbs):
        
        global current_shape
        completed_loop = False
        suitable_matches = True

        while suitable_matches and not completed_loop:

            xyrgb = last_stored_xyrgb
            xy = xyrgb[0:2]
            
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
                    test_xy = [xy[0] + direction[0] * multiplier, xy[1] + direction[1] * multiplier]
                    
                    # match adjacent pixel to edge in lists if present
                    test_xyrgb = [0]
                    
                    for xyrgb_l in edges_combined:
                        if xyrgb_l[0:2] == test_xy:
                            test_xyrgb = xyrgb_l
                    
                    # test pixel is not present in the list of edges; proceed to next test
                    if test_xyrgb == [0]:
                        continue
                    
                    sum_totals = [0, 0, 0]
                    avg_rgb = [0, 0, 0]
                    
                    if len(previous_rgbs) < trailing_rgb_length:
                        # average entire list and use as base xyrgb
                        for r in range(3):
                            for previous_rgb in previous_rgbs:
                                sum_totals[r] = sum_totals[r] + previous_rgb[r]
                        for r in range(3):
                            avg_rgb[r] = int( sum_totals[r] / len(previous_rgbs) )
                        
                    else:
                        # average trailing list and use as base xyrgb
                        trailing_rgbs = previous_rgbs[-trailing_rgb_length: -1]
                        for r in range(3):
                            for previous_rgb in trailing_rgbs:
                                sum_totals[r] = sum_totals[r] + previous_rgb[r]
                        for r in range(3):
                            avg_rgb[r] = int( sum_totals[r] / len(trailing_rgbs) )
                    
                    prxy_avgrgb = xy + avg_rgb
                    colour_match_weighting = weighted_colour_match_v(prxy_avgrgb, test_xyrgb, weighting_base, weighting_division_coefficient)
                    
                    if colour_match_weighting < colour_match_minimum:
                        continue
                    
                    directional_weighting = direction_weighting[n]
                    
                    directional_multiplier_weight = 0
                    if multiplier == 0.5:
                        directional_multiplier_weight = directional_multiplier_weighting
                    
                    # close the loop prio
                    if test_xy == start_point and len(current_shape) > minimum_polyline_loop_length:
                        pixel_weight = [colour_match_weighting + directional_weighting + start_point_return_weighting + directional_multiplier_weight]
                        surrounding_pixels_weighted.append(test_xyrgb + pixel_weight)
                        continue
                    
                    # dont reuse edges
                    if test_xy in used:
                        continue
                    
                    pixel_weight = [directional_weighting + colour_match_weighting + directional_multiplier_weight]
                    
                    # build list of candidate pixels
                    surrounding_pixels_weighted.append(test_xyrgb + pixel_weight)
            
            if len(surrounding_pixels_weighted) == 0:
                suitable_matches = False
                break
            
            surrounding_pixels_weighted.sort(key = lambda surrounding_pixels_weighted : surrounding_pixels_weighted[5], reverse = True)
            xyrgb_n = surrounding_pixels_weighted[0][0:5]
            xy_n = xyrgb_n[0:2]
            xy_n_weight = surrounding_pixels_weighted[0][5]
            
            # close the shape
            if xy_n == start_point and len(current_shape) > minimum_polyline_loop_length:
                current_shape.append(xy_n)
                completed_loop = True
                break
            
            if xy_n_weight >= weighting_threshold:
                used.append(xy_n)
                current_shape.append(xy_n)
                previous_rgbs.append(xyrgb_n[2:5])
                last_stored_xyrgb = xyrgb_n
                delta = [xy_n[0]-xy[0], xy_n[1]-xy[1]]
                
                # account for half steps
                if not int(delta[0]) == delta[0] or not int(delta[1]) == delta[1] :
                    old_delta = delta
                    delta = [int(old_delta[0] * 2), int(old_delta[1] * 2)]
                
                dirct_index = [indx for indx, dirct in enumerate(circular_pattern) if dirct == delta]
                prev_dirct_index = dirct_index[0]
            
            # stop considering candidates within the shortlist that fall below the threshold
            if xy_n_weight < weighting_threshold:
                suitable_matches = False

    total = len(edges_combined)
    milestone_step = 0.05

    # this is the beginning of the routine, unfortunate positioning
    def start_new_polylines():
        global shape_no, current_shape
        next_milestone = 0.05
        for position, xyrgb in enumerate(edges_combined):
            
            if position / total > next_milestone:
                print(int(next_milestone * 100),"%")
                next_milestone = next_milestone + milestone_step
            
            new_shape = False
            surrounding_pixel_in_used = False
            xy = xyrgb[0:2]
            
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

                        test_xy = [xy[0] + direction[0] * multiplier, xy[1] + direction[1] * multiplier]
                    
                        # prevent use of pixels adjacent to used ones
                        if test_xy in used:
                            surrounding_pixel_in_used = True
                            break
                        
                        # match adjacent pixel to edge in lists if present
                        test_xyrgb = [0]
                    
                        for xyrgb_l in edges_combined:                       
                            if xyrgb_l[0:2] == test_xy:
                                test_xyrgb = xyrgb_l
                    
                        # test pixel is not present in the list of edges; proceed to next test
                        if test_xyrgb == [0]:
                            continue
                                                    
                        colour_match_weighting = weighted_colour_match_v(xyrgb, test_xyrgb, weighting_base, weighting_division_coefficient)
                        
                        directional_multiplier_weight = 0
                        if multiplier == 0.5:
                            directional_multiplier_weight = directional_multiplier_weighting
                        
                        pixel_weight = [colour_match_weighting + directional_multiplier_weight]
                        
                        if colour_match_weighting < colour_match_minimum:
                            continue

                        surrounding_pixels_weighted.append(test_xyrgb + pixel_weight)
                
                # move on to a new pixel if nearby pixel already used
                if surrounding_pixel_in_used:
                    continue
                    
                if len(surrounding_pixels_weighted) == 0:
                    continue
                        
                surrounding_pixels_weighted.sort(key = lambda surrounding_pixels_weighted : surrounding_pixels_weighted[5], reverse = True)
                xyrgb_n = surrounding_pixels_weighted[0][0:5]
                xy_n = xyrgb_n[0:2]
                xy_n_weight = surrounding_pixels_weighted[0][5]
                
                if xy_n_weight >= weighting_threshold:
                    current_shape = []
                    previous_rgbs = []
                    shape_no = shape_no + 1
                    current_shape.append([xy[0], xy[1]])
                    current_shape.append([xy_n[0], xy_n[1]])
                    used.append([xy[0], xy[1]])
                    used.append([xy_n[0], xy_n[1]])
                    previous_rgbs.append(xyrgb[2:5])
                    previous_rgbs.append(xyrgb_n[2:5])
                    new_shape = True
                    delta = [xy_n[0] - xy[0], xy_n[1] - xy[1]]
                    
                    # account for half steps
                    if not int(delta[0]) == delta[0] or not int(delta[1]) == delta[1] :
                        old_delta = delta
                        delta = [int(old_delta[0] * 2), int(old_delta[1] * 2)]

                    dirct_index = [indx for indx, dirct in enumerate(circular_pattern) if dirct == delta]
                    prev_dirct_index = dirct_index[0]
                    last_stored_xyrgb = xyrgb_n

            # Add to new polyline            
            if new_shape:
                generate_polyline(start_point, prev_dirct_index, last_stored_xyrgb, previous_rgbs)
                
                lines.append([shape_no, current_shape])

    start_new_polylines()

    print('outlines generated')

    # filter short lines
    final_lines = []
    
    for line in lines:
        if len(line[1]) > 3:
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
