
from operator import ne
import matplotlib.pyplot as plt
from PIL import Image
from Colour_functions import *
from Segments_functions import *
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'white'

# Lateral scan reduction (Left ro right)
def segment_creation(numpydata, outlines, ratification_length, segment_length):

    print('checkmark 15 segment creation initiated')
    ratified_outlines = []
    
    for outline in outlines:
        ratified_outline = []
        outline_xys = outline[1]
        
        if len(outline_xys) < segment_length:
            continue
        
        streak = 0
        cumulative_x = 0
        cumulative_y = 0
        
        for index in range(len(outline_xys)):
            
            if streak > (ratification_length - 1):
                new_x = cumulative_x / ratification_length
                new_y = cumulative_y / ratification_length
                ratified_outline.append([new_x,new_y])
                cumulative_x = 0
                cumulative_y = 0
                streak = 0
            
            next_xy = outline_xys[index]
            cumulative_x = cumulative_x + next_xy[0]
            cumulative_y = cumulative_y + next_xy[1]
            
            streak += 1
            
            if index == (len(outline_xys) - 1):
                new_x = cumulative_x / streak
                new_y = cumulative_y / streak
                ratified_outline.append([new_x,new_y])
                ratified_outlines.append(ratified_outline)

    if 2 == 2:
        for outline in ratified_outlines:
            x, y = map(list, zip(*outline))
            plt.plot(x, y, label = "line {}".format(outline[0]) )
        plt.gca().invert_yaxis()
        img = Image.fromarray(numpydata, 'RGB')
        img.save('my.png')
        plt.imshow(img)
        plt.show()
    
    # vertex detection
    
    forward_bearing = 0
    line_segments = []
    curve_segments = []
    bearing_delta_straight_line_threshold = 6
    bearing_delta_curve_threshold = 8
    
    for r_outline in ratified_outlines:
        first = True
        second = True
        start_xy = [] 
        back_xy = []
        current_curve = []
        active_curve = False
        active_line = False
        first_curve_bearing_delta = 0
        first_sign = 0

        for xy in r_outline:
            
            if first:
                back_xy = xy
                first = False
                continue
            
            if second:
                forward_bearing = bearing(back_xy, xy)
                back_xy = xy
                second = False
                continue
            
            previous_bearing = forward_bearing
            forward_bearing = bearing(back_xy, xy)
            absolute_bearing_delta, true_bearing_delta = bearing_delta_function(previous_bearing, forward_bearing)
            
            prev_xy = back_xy
            back_xy = xy
            
            # enter this if block for lines
            if absolute_bearing_delta <= bearing_delta_straight_line_threshold:
                
                # end active curve if it was previously started
                if active_curve:
                    curve_segments.append(current_curve)
                    current_curve = []
                    active_curve = False 
                
                # start a new line if one isn't active
                if not active_line:
                    start_xy = prev_xy
                    active_line = True
             
                # Check if it is the last list entry
                if xy == r_outline[-1]:
                    line_segments.append([start_xy, prev_xy])
                    active_line = False
                    continue   
                
                continue 
            
            elif active_curve:
                
                if active_line:
                    line_segments.append([start_xy, prev_xy])
                    active_line = False
                
                variance = abs(true_bearing_delta - first_curve_bearing_delta)
                sign = +1
                if true_bearing_delta < 0:
                    sign = -1
                
                if variance < bearing_delta_curve_threshold and sign == first_sign:
                    current_curve.append(xy)
                    
                    # Check if it is the last list entry
                    if xy == r_outline[-1]:
                        curve_segments.append(current_curve)
                        current_curve = []
                        active_curve = False 
                    
                    continue
                else:
                    curve_segments.append(current_curve)
                    current_curve = []
                    active_curve = False
                    continue
            
            # start a curve 
            elif not active_curve and not active_line:
                    first_curve_bearing_delta = true_bearing_delta
                    start_xy = prev_xy
                    current_curve.append(start_xy)
                    active_curve = True
                    first_sign = +1
                    if true_bearing_delta < 0:
                        first_sign = -1
                    
                    continue          
            
            # enter this block to terminate an acitve line
            else:
                if active_line:
                    line_segments.append([start_xy, prev_xy])
                    active_line = False
                    continue
            
    print(curve_segments)
    if 2 == 2:
        for line_segment in line_segments:
            x, y = map(list, zip(*line_segment))
            plt.plot(x, y, label = "line {}".format(outline[0]) )
        plt.gca().invert_yaxis()
        img = Image.fromarray(numpydata, 'RGB')
        img.save('my.png')
        plt.imshow(img)
        plt.show()

    if 2 == 2:
        for curve_segment in curve_segments:
            x, y = map(list, zip(*curve_segment))
            plt.plot(x, y, label = "line {}".format(outline[0]) )
        plt.gca().invert_yaxis()
        img = Image.fromarray(numpydata, 'RGB')
        img.save('my.png')
        plt.imshow(img)
        plt.show()
        