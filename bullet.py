import cv2
import numpy as np

import cv2
import numpy as np

def move_bullet(frame, start_point, angle_degrees, speed=14):
    """
    Animates a bullet moving from the start point at the given angle.

    Parameters:
        frame (numpy.ndarray): The frame to draw on.
        start_point (tuple): (x, y) coordinates of the starting point.
        angle_degrees (float): Angle of movement in degrees (0° is right, 90° is up, 180° is left, 270° is down).
        speed (int): Number of pixels the bullet moves per frame.

    Returns:
        tuple: The new position of the bullet (x, y).
    """
    # Convert degrees to radians and adjust for OpenCV's coordinate system
    angle_radians = np.radians(angle_degrees)

    # Calculate the direction vector from the angle
    dx = speed * np.cos(angle_radians)
    dy = speed * np.sin(angle_radians)

    # Update the bullet's position
    new_x = int(start_point[0] + dx)
    new_y = int(start_point[1] + dy)

    # Draw the bullet on the frame
    cv2.circle(frame, (new_x, new_y), 20, (0, 255, 0), -1)  # Bullet as a red circle

    return new_x, new_y


# # Example usage
# frame_width, frame_height = 1280, 720
# frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

# # Initialize the bullet's starting position and angle
# start_point = (640, 360)  # Starting position (x, y)
# end_point = (600, 360)    # Example second point
# angle = 180

# # Run the animation
# bullet_position = start_point
# while True:
#     # Clear the frame
#     frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

#     # Move the bullet
#     bullet_position = move_bullet(frame, bullet_position, angle, speed=10)

#     # Check if the bullet is out of frame
#     if (bullet_position[0] < 0 or bullet_position[0] >= frame_width or
#         bullet_position[1] < 0 or bullet_position[1] >= frame_height):
#         print("Bullet exited the frame.")
#         break

#     # Display the frame
#     cv2.imshow("Bullet Animation", frame)
#     if cv2.waitKey(10) & 0xFF == ord('q'):  # Press 'q' to quit
#         break

# cv2.destroyAllWindows()
# #90 

