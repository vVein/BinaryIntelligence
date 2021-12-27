
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt
import numpy as np

tolerance = 140

def pixel_comparison_t(current_pixel, previous_pixel, tolerance = 120):
    comparison1 = abs(int(current_pixel[0]) - int(previous_pixel[0]))
    comparison2 = abs(int(current_pixel[1]) - int(previous_pixel[1]))
    comparison3 = abs(int(current_pixel[2]) - int(previous_pixel[2]))
    comparison = (comparison1 + comparison2 + comparison3) > tolerance
    return comparison

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
        

def redacted_colour_match(numpydata, xy, xy_n, dirct):
    matrix1 = np.array([[dirct[0], dirct[1]], [-dirct[0], -dirct[1]]])
    matrix2 = np.array([[0, 1], [1, 0]])
    matrix3 = np.dot(matrix1, matrix2)
    #perpendicular
    direction_1 = [matrix3[0,0],matrix3[0,1]]
    direction_2 = [matrix3[1,0],matrix3[1,1]]
    test_length = 5
    xy_pixels_1 = []
    xy_pixels_2 = []
    xy_n_pixels_1 = []
    xy_n_pixels_2 = []
    
    for pt in range(1, test_length + 1):
        xy_coordinate_1 = [xy[0] + pt * direction_1[0], xy[1] + pt * direction_1[1]]
        xy_coordinate_2 = [xy[0] + pt * direction_2[0], xy[1] + pt * direction_2[1]]
        xyn_coordinate_1 = [xy_n[0] + pt * direction_1[0], xy_n[1] + pt * direction_1[1]]
        xyn_coordinate_2 = [xy_n[0] + pt * direction_2[0], xy_n[1] + pt * direction_2[1]]
        img_width = int(np.size(numpydata,1))
        img_height = int(len(numpydata))
        
        if xy_coordinate_1[0] > img_width:
            xy_coordinate_1[0] = img_width
        if xy_coordinate_1[0] < 0:
            xy_coordinate_1[0] = 0
        if xy_coordinate_1[1] > img_height:
            xy_coordinate_1[1] = img_height
        if xy_coordinate_1[1] < 0:
            xy_coordinate_1[1] = 0
        if xy_coordinate_2[0] > img_width:
            xy_coordinate_2[0] = img_width
        if xy_coordinate_2[0] < 0:
            xy_coordinate_2[0] = 0
        if xy_coordinate_2[1] > img_height:
            xy_coordinate_2[1] = img_height
        if xy_coordinate_2[1] < 0:
            xy_coordinate_2[1] = 0
        if xyn_coordinate_1[0] > img_width:
            xyn_coordinate_1[0] = img_width
        if xyn_coordinate_1[0] < 0:
            xyn_coordinate_1[0] = 0
        if xyn_coordinate_1[1] > img_height:
            xyn_coordinate_1[1] = img_height
        if xyn_coordinate_1[1] < 0:
            xyn_coordinate_1[1] = 0
        if xyn_coordinate_2[0] > img_width:
            xyn_coordinate_2[0] = img_width
        if xyn_coordinate_2[0] < 0:
            xyn_coordinate_2[0] = 0
        if xyn_coordinate_2[1] > img_height:
            xyn_coordinate_2[1] = img_height
        if xyn_coordinate_2[1] < 0:
            xyn_coordinate_2[1] = 0
        xy_pixel_1 = numpydata[xy_coordinate_1[1]][xy_coordinate_1[0]]
        xy_pixel_2 = numpydata[xy_coordinate_2[1]][xy_coordinate_2[0]]
        xy_n_pixel_1 = numpydata[xyn_coordinate_1[1]][xyn_coordinate_1[0]]
        xy_n_pixel_2 = numpydata[xyn_coordinate_2[1]][xyn_coordinate_2[0]]
        xy_pixels_1.append(xy_pixel_1)
        xy_pixels_2.append(xy_pixel_2)
        xy_n_pixels_1.append(xy_n_pixel_1)
        xy_n_pixels_2.append(xy_n_pixel_2)
    
    delta = 0
    threshold = 800
    #compare xy pixels with xy n pixels 
    for row in range(len(xy_pixels_1)):
        for colour in range(len(xy_pixels_1[0])):
            delta = delta + abs(int(xy_pixels_1[row][colour]) - int(xy_n_pixels_1[row][colour]))
            delta = delta + abs(int(xy_pixels_2[row][colour]) - int(xy_n_pixels_2[row][colour]))
    
    return delta < threshold