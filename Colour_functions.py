

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

def weighted_colour_match(numpydata, xy_1, xy_2):
    pixel_1 = numpydata[xy_1[1]][xy_1[0]]
    pixel_2 = numpydata[xy_2[1]][xy_2[0]]
    comparison1 = abs(int(pixel_1[0]) - int(pixel_2[0]))
    comparison2 = abs(int(pixel_1[1]) - int(pixel_2[1]))
    comparison3 = abs(int(pixel_1[2]) - int(pixel_2[2]))
    comparison = comparison1 + comparison2 + comparison3
    weight = int(max( 90 - comparison / 2, 0))
    return weight

def colour_match(numpydata, xy, xy_n, tolerance):
    xy_pixel = numpydata[xy[1]][xy[0]]
    xy_n_pixel = numpydata[xy_n[1]][xy_n[0]]
    return not pixel_comparison(xy_pixel, xy_n_pixel, tolerance)

def edge_variance(pending_edges, delta_trigger):
    number_of_edges = len(pending_edges)
    returned_edges = []
    
    if number_of_edges <= 1:
        edge = pending_edges[0]
        xy = [edge[0], edge[1]]
        returned_edges.append(xy)
        return returned_edges
    
    r_signs = []
    g_signs = []
    b_signs = []
    nominated_edges_indices = []
    
    for order, edge in enumerate(pending_edges):
        if order == 0:
            current_pixel = edge           
        else:
            previous_pixel = current_pixel
            current_pixel = edge
            r_delta = int(previous_pixel[2]) - int(current_pixel[2])
            g_delta = int(previous_pixel[3]) - int(current_pixel[3])
            b_delta = int(previous_pixel[4]) - int(current_pixel[4])
            
            if abs(r_delta) > delta_trigger:
                if r_delta > 0:
                    sign = 1
                elif r_delta < 0:
                    sign = -1
                else:
                    sign = 0
                r_signs.append(sign)
                
            if abs(g_delta) > delta_trigger:
                if g_delta > 0:
                    sign = 1
                elif g_delta < 0:
                    sign = -1
                else:
                    sign = 0
                g_signs.append(sign)            

            if abs(b_delta) > delta_trigger:
                if b_delta > 0:
                    sign = 1
                elif b_delta < 0:
                    sign = -1
                else:
                    sign = 0
                b_signs.append(sign)            
            
    list_of_signs = [r_signs, g_signs, b_signs]
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
                if current_sign == 0 or current_sign == +1:
                    nominated_edges_indices.append(order)
            elif previous_sign == +1:
                if current_sign == 0 or current_sign == -1:
                    nominated_edges_indices.append(order)
    
    if len(nominated_edges_indices) == 0:
        max_index = len(pending_edges) - 1
        nominated_edges_indices.append(max_index)
    
    unique_nominated_edges_indices = set(nominated_edges_indices)
    
    for order, edge in enumerate(pending_edges):
        if order in unique_nominated_edges_indices:
            xy = [edge[0], edge[1]]
            returned_edges.append(xy)
    return returned_edges
                          
def block_predominant_colour(numpydata, xy, block_size):
    colours = []
    block_width = int(block_size / 2)
    for adj_x in range(-block_width, block_width):
        for adj_y in range(-block_width, block_width):
            xy_add = [xy[0] + adj_x, xy[1] + adj_y]
            xy_pixel = numpydata[xy_add[1]][xy_add[0]]
            pixel_tupl = (xy_pixel[0], xy_pixel[1], xy_pixel[2])
            colours.append(pixel_tupl)
    most_common = max(set(colours), key = colours.count)
    return list(most_common)

def weakest_background_match(pixel_1, pixel_2, predominant_background_pixel):
    pixel_1_background_delta = pixel_comparison(pixel_1, predominant_background_pixel)
    pixel_2_background_delta = pixel_comparison(pixel_2, predominant_background_pixel)
    if pixel_1_background_delta > pixel_2_background_delta:
        return list(pixel_1)
    else:
        return list(pixel_2)
        