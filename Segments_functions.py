
import math

def bearing(back_xy, forward_xy):

    delta_x = forward_xy[0] - back_xy[0]
    delta_y = forward_xy[1] - back_xy[1]
    signX = 1
    signY = 1
    mew = 0
    if delta_x < 0:
        signX = -1
    if delta_y < 0:
        signY = -1

    if delta_x == 0:
        if signY == 1:
            return mew
        else:
            return 180
    if delta_y == 0:
        if signX == 1:
            return 90
        else:
            return 270
    
    # Quadrant 1
    if signX == +1 and signY == -1:
        mew = abs(math.degrees(math.atan(delta_x / delta_y)))
        return mew
    
    # Quadrant 2
    if signX == +1 and signY == +1:
        mew = abs(math.degrees(math.atan(delta_y / delta_x))) + 90
        return mew
    
    # Quadrant 3
    if signX == -1 and signY == +1:
        mew = abs(math.degrees(math.atan(delta_x / delta_y))) + 180
        return mew


    # Quadrant 4
    if signX == -1 and signY == -1:
        mew = abs(math.degrees(math.atan(delta_y / delta_x))) + 270
        return mew

    return mew

def bearing_delta_function(previous_bearing, forward_bearing):
    bearing_delta = forward_bearing - previous_bearing
    if abs(bearing_delta) > 180:
        bearing_delta = 0
        true_bearing_delta = abs(180 + bearing_delta)
    else:
        true_bearing_delta = abs(bearing_delta)
    return true_bearing_delta