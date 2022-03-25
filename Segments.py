
from operator import ne
import matplotlib.pyplot as plt
from PIL import Image
from Colour_functions import *
from Segments_functions import *
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'white'

# Lateral scan reduction (Left ro right)
def segment_creation(numpydata, outlines, ratification_length, segment_length):
    bearing_delta_threshold = 8
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

    if 20 == 2:
        for outline in ratified_outlines:
            x, y = map(list, zip(*outline))
            plt.plot(x, y, label = "line {}".format(outline[0]) )
        plt.gca().invert_yaxis()
        img = Image.fromarray(numpydata, 'RGB')
        img.save('my.png')
        plt.imshow(img)
        plt.show()
    
    # vertex detection
    back_xy = []
    forward_bearing = 0
    line_segments = []
    for r_outline in ratified_outlines:
        first = True
        second = True
        bearing_deltas = []
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
            bearing_delta = bearing_delta_function(previous_bearing, forward_bearing)
            bearing_deltas.append(bearing_delta)
            back_xy = xy
        
        active_streak = False
        start_number = 0
        end_number = 0
        line_numbers = []
        for number, bearing_delta in enumerate(bearing_deltas):
            if bearing_delta <= bearing_delta_threshold:
                
                if not active_streak:
                    start_number = number
                    active_streak = True
                
                continue
            
            # bearing_delta > bearing_delta_threshold:
            if active_streak:                
                end_number = number -1
                if end_number - start_number > 1:
                    line_numbers.append([start_number, end_number])
            
            # any active streak ends
            active_streak = False
            
        for line_number_sf in line_numbers:
            start_number = line_number_sf[0]
            end_number = line_number_sf[1]
            start_xy = r_outline[start_number]
            end_xy = r_outline[end_number]
            line_segments.append([start_xy, end_xy])
            
    print(line_segments)
    if 2 == 2:
        for line_segment in line_segments:
            x, y = map(list, zip(*line_segment))
            plt.plot(x, y, label = "line {}".format(outline[0]) )
        plt.gca().invert_yaxis()
        img = Image.fromarray(numpydata, 'RGB')
        img.save('my.png')
        plt.imshow(img)
        plt.show()
        