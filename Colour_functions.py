

def pixel_comparison_t(current_pixel, previous_pixel, individual_threshold = 50, group_threshold = 110):
    comparison1 = abs(int(current_pixel[0]) - int(previous_pixel[0]))
    comparison2 = abs(int(current_pixel[1]) - int(previous_pixel[1]))
    comparison3 = abs(int(current_pixel[2]) - int(previous_pixel[2]))
    if any(compar > individual_threshold for compar in [comparison1, comparison2, comparison3] ):
        return True
    if (comparison1 + comparison2 + comparison3) > group_threshold:
        return True
    return False

def pixel_comparison(p1, p2):
    comparison1 = abs(int(p1[0]) - int(p2[0]))
    comparison2 = abs(int(p1[1]) - int(p2[1]))
    comparison3 = abs(int(p1[2]) - int(p2[2]))
    comparison = (comparison1 + comparison2 + comparison3)
    return comparison

def weighted_colour_match(numpydata, xy_1, xy_2, weighting_base_cm = 200):
    pixel_1 = numpydata[xy_1[1]][xy_1[0]]
    pixel_2 = numpydata[xy_2[1]][xy_2[0]]
    comparison1 = abs(int(pixel_1[0]) - int(pixel_2[0]))
    comparison2 = abs(int(pixel_1[1]) - int(pixel_2[1]))
    comparison3 = abs(int(pixel_1[2]) - int(pixel_2[2]))
    comparison = comparison1 + comparison2 + comparison3
    weight = int(max( weighting_base_cm - comparison, 0))
    return weight

# works with XYRGB inputs
def weighted_colour_match_v(xyrgb_1, xyrgb_2, weighting_base = 200, weighting_division_coefficient = 2):
    delta_rgb = pixel_comparison(xyrgb_1[2:4], xyrgb_2[2:4])
    weight = int(max( weighting_base - delta_rgb / weighting_division_coefficient, 0))
    return weight

def weighted_left_colour_match(numpydata, circular_pattern, back_xy, forward_xy, previous_direction_index, proposed_direction_index, weighting_base = 200,
                               weighting_division_coefficient = 2):
    # generate adjustment to find pixel to the left of the back pixel
    previous_perpendicular_coordinate_adjustment_left_index = ( previous_direction_index - 2 ) % 8
    previous_perpendicular_coordinate_adjustment_left = circular_pattern[previous_perpendicular_coordinate_adjustment_left_index]
    previous_left_xy = [back_xy[0] + previous_perpendicular_coordinate_adjustment_left[0], back_xy[1] + previous_perpendicular_coordinate_adjustment_left[1]]
    previous_left_rgb = numpydata[previous_left_xy[1]][previous_left_xy[0]]
    proposed_perpendicular_coordinate_adjustment_left_index = ( proposed_direction_index - 2 ) % 8
    proposed_perpendicular_coordinate_adjustment_left = circular_pattern[proposed_perpendicular_coordinate_adjustment_left_index]
    proposed_left_xy = [forward_xy[0] + proposed_perpendicular_coordinate_adjustment_left[0], forward_xy[1] + proposed_perpendicular_coordinate_adjustment_left[1]]
    proposed_left_rgb = numpydata[proposed_left_xy[1]][proposed_left_xy[0]]
    delta_left_rgb = pixel_comparison(previous_left_rgb, proposed_left_rgb)
    weighting_l = int(max( weighting_base - delta_left_rgb / weighting_division_coefficient, 0))
    return weighting_l

# if the left and right colours match the centre; its not an edge; therefore void
def left_right_center_colour_match(numpydata, circular_pattern, forward_xy, proposed_direction_index, rgb_delta_limit = 30,
                                   centre_weighting_division_coefficient = 3):
    proposed_perpendicular_coordinate_adjustment_left_index = ( proposed_direction_index - 2 ) % 8
    proposed_perpendicular_coordinate_adjustment_left = circular_pattern[proposed_perpendicular_coordinate_adjustment_left_index]
    proposed_left_xy = [forward_xy[0] + proposed_perpendicular_coordinate_adjustment_left[0], forward_xy[1] + proposed_perpendicular_coordinate_adjustment_left[1]]
    proposed_left_rgb = numpydata[proposed_left_xy[1]][proposed_left_xy[0]]
    
    proposed_perpendicular_coordinate_adjustment_right_index = ( proposed_direction_index + 2 ) % 8
    proposed_perpendicular_coordinate_adjustment_right = circular_pattern[proposed_perpendicular_coordinate_adjustment_right_index]
    proposed_right_xy = [forward_xy[0] + proposed_perpendicular_coordinate_adjustment_right[0], forward_xy[1] + proposed_perpendicular_coordinate_adjustment_right[1]]
    proposed_right_rgb = numpydata[proposed_right_xy[1]][proposed_right_xy[0]]
    
    proposed_rgb = numpydata[forward_xy[1]][forward_xy[0]]
    
    delta_left_rgb = pixel_comparison(proposed_rgb, proposed_left_rgb)
    delta_right_rgb = pixel_comparison(proposed_rgb, proposed_right_rgb)
    
    if delta_left_rgb < rgb_delta_limit and delta_right_rgb < rgb_delta_limit:
        weighting = -300
        return weighting
    
    weighting = max(delta_left_rgb, delta_right_rgb) / centre_weighting_division_coefficient
    
    return weighting

def weighted_right_colour_match(numpydata, circular_pattern, back_xy, forward_xy, previous_direction_index, proposed_direction_index,
                                weighting_base = 200, weighting_division_coefficient = 2):
    previous_perpendicular_coordinate_adjustment_right_index = ( previous_direction_index + 2 ) % 8
    previous_perpendicular_coordinate_adjustment_right = circular_pattern[previous_perpendicular_coordinate_adjustment_right_index]
    previous_right_xy = [back_xy[0] + previous_perpendicular_coordinate_adjustment_right[0], back_xy[1] + previous_perpendicular_coordinate_adjustment_right[1]]
    previous_right_rgb = numpydata[previous_right_xy[1]][previous_right_xy[0]]
    proposed_perpendicular_coordinate_adjustment_right_index = ( proposed_direction_index + 2 ) % 8
    proposed_perpendicular_coordinate_adjustment_right = circular_pattern[proposed_perpendicular_coordinate_adjustment_right_index]
    proposed_right_xy = [forward_xy[0] + proposed_perpendicular_coordinate_adjustment_right[0], forward_xy[1] + proposed_perpendicular_coordinate_adjustment_right[1]]
    proposed_right_rgb = numpydata[proposed_right_xy[1]][proposed_right_xy[0]]
    delta_right_rgb = pixel_comparison(previous_right_rgb, proposed_right_rgb)
    weighting_r = int(max( weighting_base - delta_right_rgb / weighting_division_coefficient, 0))
    return weighting_r

def colour_match(numpydata, xy, xy_n, tolerance):
    xy_pixel = numpydata[xy[1]][xy[0]]
    xy_n_pixel = numpydata[xy_n[1]][xy_n[0]]
    return not pixel_comparison(xy_pixel, xy_n_pixel, tolerance)

def RGB_sign_delta(back_pixel, forward_pixel, delta_trigger = 50):
    
    r_delta = int(back_pixel[0]) - int(forward_pixel[0])
    g_delta = int(back_pixel[1]) - int(forward_pixel[1])
    b_delta = int(back_pixel[2]) - int(forward_pixel[2])
    r_sign = 0
    g_sign = 0
    b_sign = 0
    
    if abs(r_delta) > delta_trigger:
        if r_delta > 0:
            r_sign = 1
        elif r_delta < 0:
            r_sign = -1
        else:
            r_sign = 0
        
    if abs(g_delta) > delta_trigger:
        if g_delta > 0:
            g_sign = 1
        elif g_delta < 0:
            g_sign = -1
        else:
            g_sign = 0      

    if abs(b_delta) > delta_trigger:
        if b_delta > 0:
            b_sign = 1
        elif b_delta < 0:
            b_sign = -1
        else:
            b_sign = 0
    
    return [r_sign, g_sign, b_sign]

def edge_variance(pending_edges, delta_trigger):

    returned_edges = []
    
    r_signs = []
    g_signs = []
    b_signs = []
    flip_point_indices = []
    end_index = 0
    
    for order, edge in enumerate(pending_edges):
        
        # check pending edges for sign flip(s)
        # - build sign list
        if order == 0:
            current_pixel = edge           
        else:
            previous_pixel = current_pixel
            current_pixel = edge
            
            r_delta = int(previous_pixel[2]) - int(current_pixel[2])
            g_delta = int(previous_pixel[3]) - int(current_pixel[3])
            b_delta = int(previous_pixel[4]) - int(current_pixel[4])
            
            sign = 0
            if abs(r_delta) > delta_trigger:
                if r_delta > 0:
                    sign = 1
                elif r_delta < 0:
                    sign = -1
                else:
                    sign = 0
            r_signs.append(sign)
            
            sign = 0
            if abs(g_delta) > delta_trigger:
                if g_delta > 0:
                    sign = 1
                elif g_delta < 0:
                    sign = -1
                else:
                    sign = 0
            g_signs.append(sign)            

            sign = 0
            if abs(b_delta) > delta_trigger:
                if b_delta > 0:
                    sign = 1
                elif b_delta < 0:
                    sign = -1
                else:
                    sign = 0
            b_signs.append(sign)            
            
    list_of_signs = [r_signs, g_signs, b_signs]
       
    # check sign lists for a flip
    for x_signs in list_of_signs:
        for order, sign in enumerate(x_signs):
            if order == 0:
                current_sign = sign
                continue
            else:
                previous_sign = current_sign
                current_sign = sign
                
            if previous_sign == 0:
                continue
            elif previous_sign == current_sign:
                continue
            elif previous_sign == -1:
                if current_sign == 0:
                    end_index = order
                if current_sign == +1:
                    flip_point_indices.append(order)
            elif previous_sign == +1:
                if current_sign == 0:
                    end_index = order
                if current_sign == -1:
                    flip_point_indices.append(order)
    
    # add first boundary point:
    midway = [(pending_edges[0][0] + pending_edges[1][0]) / 2, (pending_edges[0][1] + pending_edges[1][1]) / 2, pending_edges[0][2],
              pending_edges[0][3], pending_edges[0][4]]
    returned_edges.append(midway)
    
    # add last boundary point
    # if end index was previously determined the last gradient point is not at the end of the list; otherwise it is
    if end_index == 0:
        midway = [(pending_edges[-1][0] + pending_edges[-2][0]) / 2, (pending_edges[-1][1] + pending_edges[-2][1]) / 2, pending_edges[-1][2],
              pending_edges[-1][3], pending_edges[-1][4]]
        returned_edges.append(midway)
    else:
        midway = [(pending_edges[end_index][0] + pending_edges[end_index - 1][0]) / 2, 
                  (pending_edges[end_index][1] + pending_edges[end_index - 1][1]) / 2, pending_edges[end_index][2], pending_edges[end_index][3],
                  pending_edges[end_index][4]]
        returned_edges.append(midway)
    
    # add boundaries either side of flip points;
    # in the event of a continuous streak which includes the RGB gradient flipping atleast once
    if len(flip_point_indices) > 0:
        for flip_index in flip_point_indices:
            midway = [(pending_edges[flip_index][0] + pending_edges[flip_index - 1][0]) / 2,
                       (pending_edges[flip_index][1] + pending_edges[flip_index - 1][1]) / 2, pending_edges[flip_index][2],
                       pending_edges[flip_index][3], pending_edges[flip_index][4]]
            returned_edges.append(midway)
            midway = [(pending_edges[flip_index][0] + pending_edges[flip_index + 1][0]) / 2,
                       (pending_edges[flip_index][1] + pending_edges[flip_index + 1][1]) / 2, pending_edges[flip_index][2],
                       pending_edges[flip_index][3], pending_edges[flip_index][4]]
            returned_edges.append(midway)
    
    # clean list to be added of duplicates, there is a possibility that the end could fall right after a flip and be added twice
    # and really short pending lists could also have overlapping boundaries
    returned_edges_clean = []
    for boundary in returned_edges:
        if boundary not in returned_edges_clean:
            returned_edges_clean.append(boundary)
            
    return returned_edges_clean
        