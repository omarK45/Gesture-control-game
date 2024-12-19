import numpy as np
def calculate_centroid(points):

    
    m00 = len(points)  # Area: count of points (if all points have equal weight)
    m10 = sum(x for x, y in points)  # Sum of x-coordinates
    m01 = sum(y for x, y in points)  # Sum of y-coordinates
    
    # Ensure that m00 is not zero to avoid division by zero
    if m00 != 0:
        centroid_x = m10 / m00
        centroid_y = m01 / m00
        return (centroid_x, centroid_y)
    else:
        return None  # In case there is no valid contour area