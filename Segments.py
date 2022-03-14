
from operator import ne
import matplotlib.pyplot as plt
from PIL import Image
from Colour_functions import *
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'white'

# Lateral scan reduction (Left ro right)
def segment_creation(numpydata, outlines, segment_length):
    
    print('checkmark 15 segment creation initiated')
    width_tolerance = 1
    segments = []
    ratified_outlines = []
    
    ratification_length = 3
    
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
                print(ratified_outline)
                ratified_outlines.append(ratified_outline)
    print(ratified_outlines)
    if 2 == 2:
        for outline in ratified_outlines:
            x, y = map(list, zip(*outline))
            plt.plot(x, y, label = "line {}".format(outline[0]) )
        plt.gca().invert_yaxis()
        img = Image.fromarray(numpydata, 'RGB')
        img.save('my.png')
        plt.imshow(img)
        plt.show()
            
    # intermediate point test

    # 1. start point
    # 2. determine direction
    # 3. move along polyline segment length
    # 4. determine midpoint
    # 5. determine if mid point is located along the tangent
    # 6. if so then likely a line segment; else possible curve or non segment; shorten segment
    
    # exclude short lines
    for outline in outlines:
        outline_xys = outline[1]
        
        if len(outline_xys) < segment_length:
            continue
        
        starting_index = 0
        starting_xy = outline_xys[starting_index]
        forward_index = segment_length
        forward_xy = outline_xys[forward_index]
        
        delta_x = forward_xy[0] - starting_xy[0]
        delta_y = forward_xy[1] - starting_xy[1]
        
        
        midpoint_index = int((forward_index - starting_index) / 2 )
        midpoint_xy = outline_xys[midpoint_index]
        
        print(starting_xy)
    