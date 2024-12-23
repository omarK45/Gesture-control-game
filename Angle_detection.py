import math
import numpy as np

def calculate_angle(cog, hull):
    max_distance = 0
    furthest_point = None

    for point in hull:
        x, y = point # Hull points are stored as [[x, y]]
        # Calculate Euclidean distance
        distance = np.sqrt((x - cog[0])**2 + (y - cog[1])**2)
        if distance > max_distance:
            max_distance = distance
            furthest_point = (x, y)

    
    # Calculate vector components
    vector = (furthest_point[0] - cog[0], furthest_point[1] - cog[1])
    
    # Calculate angle in radians
    angle_radians = math.atan2(vector[1], vector[0])
    
    # Convert angle to degrees
    angle_degrees = math.degrees(angle_radians)
    
    # Ensure angle is in the range [0, 360)
    angle_degrees = angle_degrees % 360

    # Round to the nearest multiple of 15
    rounded_angle = round(angle_degrees / 15) * 15
    
    return rounded_angle, furthest_point

# Example usage

# Example usage
cog = (250, 250)  # Center of gravity
fingertip = [(300, 249)]  # Fingertip coordinates

angle ,_= calculate_angle(cog, fingertip)
#print(f"Rounded Angle: {angle} degrees")

#fo2 90
#shemal 180
#taht 270
#yemeen 0/360
