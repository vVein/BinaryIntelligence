
import matplotlib.pyplot as plt
from Colour_functions import *
from Edge_detection import *

lines = []
used = []
index_rotation = [0, 1, -1, 2, -2, 3, -3]
circular_pattern = [[0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1]]
direction_weighting = [70, 50, 50, 35, 35, 20, 20]
edges_prio_1_weighting = 125
edges_prio_2_weighting = 60
edges_prio_3_weighting = 30
weighting_threshold = 140
index_cap = len(index_rotation) + 1
shape_no = 0
current_shape = []

# Polyline functions:
def generate_lines(numpydata, edges_prio_1, edges_prio_2, edges_prio_3):

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
                
                weighted_perpendicular_colour_match_value = weighted_perpendicular_colour_match(numpydata, circular_pattern, xy, adjacent_pixel, 
                                                                                prev_dirct_index, applied_index)
                
                if adjacent_pixel == start_point and len(current_shape) > 12:
                    pixel_weight = edges_prio_1_weighting + weighted_colour_match(numpydata, xy, adjacent_pixel) + directional_weighting + 5 + weighted_perpendicular_colour_match_value
                    surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                    continue
                            
                if adjacent_pixel in used:
                    continue

                directional_weighting = direction_weighting[n]
                    
                if adjacent_pixel in edges_prio_1:
                    pixel_weight = edges_prio_1_weighting + weighted_colour_match(numpydata, xy, adjacent_pixel) + directional_weighting + weighted_perpendicular_colour_match_value
                    surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                elif adjacent_pixel in edges_prio_2:
                    pixel_weight = edges_prio_1_weighting + weighted_colour_match(numpydata, xy, adjacent_pixel) + directional_weighting + weighted_perpendicular_colour_match_value
                    surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                elif adjacent_pixel in edges_prio_3:
                    pixel_weight = edges_prio_1_weighting + weighted_colour_match(numpydata, xy, adjacent_pixel) + directional_weighting + weighted_perpendicular_colour_match_value
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
                surrounding_pixel_xys = []
                for direction in circular_pattern:
                    adjacent_pixel = [xy[0] + direction[0], xy[1] + direction[1]]
                    surrounding_pixel_xys.append([adjacent_pixel[0], adjacent_pixel[1]])
                
                # build list of suitable surrounding points and select best match       
                surrounding_pixels_weighted = []
                for adjacent_pixel in surrounding_pixel_xys:
                    if adjacent_pixel in used:
                        surrounding_pixel_in_used = True
                        break
                    if adjacent_pixel in edges_prio_1:
                        pixel_weight = edges_prio_1_weighting + weighted_colour_match(numpydata, xy, adjacent_pixel)
                        surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                    elif adjacent_pixel in edges_prio_2:
                        pixel_weight = edges_prio_1_weighting + weighted_colour_match(numpydata, xy, adjacent_pixel)
                        surrounding_pixels_weighted.append([adjacent_pixel[0], adjacent_pixel[1], pixel_weight])
                    elif adjacent_pixel in edges_prio_3:
                        pixel_weight = edges_prio_1_weighting + weighted_colour_match(numpydata, xy, adjacent_pixel)
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
                
    print('checkmark12 polyline')

    start_new_polylines()

    print('checkmark14 polylines generated')

    if 20 == 2:
        # exclude 1 & 2 point lines
        for line in lines:
            if len(line[1]) > 6:
                x, y = map(list, zip(*line[1]))
                plt.plot(x, y, label = "line {}".format(line[0]) )
        plt.gca().invert_yaxis()
        #img = Image.fromarray(numpydata, 'RGB')
        #img.save('my.png')
        #plt.imshow(img)
        plt.show()
