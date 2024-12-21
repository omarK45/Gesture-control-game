import math

def calculate_angle(cog, point):
    """
    Calculate the angle between the CoG and a given point, rounded to the nearest 15 degrees.

    Args:
        cog (tuple): Coordinates of the center of gravity (x_CoG, y_CoG).
        point (tuple): Coordinates of the other point (x_point, y_point).

    Returns:
        int: The angle in degrees, rounded to the nearest 15 degrees.
    """
    # Calculate vector components
    vector = (point[0] - cog[0], point[1] - cog[1])
    
    # Calculate angle in radians
    angle_radians = math.atan2(vector[1], vector[0])
    
    # Convert angle to degrees
    angle_degrees = math.degrees(angle_radians)
    
    # Ensure angle is in the range [0, 360)
    angle_degrees = angle_degrees % 360

    # Round to the nearest multiple of 15
    rounded_angle = round(angle_degrees / 15) * 15
    
    return rounded_angle

# Example usage
cog = (250, 250)  # Center of gravity
fingertip = (350, 200)  # Fingertip coordinates

angle = calculate_angle(cog, fingertip)
print(f"Rounded Angle: {angle} degrees")
