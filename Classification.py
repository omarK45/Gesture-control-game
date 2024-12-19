import cv2
import numpy as np

# Function to calculate convexity defects and classify fingers
def classify_fingers(contour, hull, cog, frame):
    # Calculate convexity defects
    hull_indices = cv2.convexHull(contour, returnPoints=False)
    defects = cv2.convexityDefects(contour, hull_indices)
    
    if defects is None:
        return [], frame

    finger_points = []  # To store finger tips

    for i in range(defects.shape[0]):
        start_idx, end_idx, far_idx, depth = defects[i, 0]

        # Extract points
        start_point = tuple(contour[start_idx][0])
        end_point = tuple(contour[end_idx][0])
        far_point = tuple(contour[far_idx][0])
        depth_value = depth / 256.0  # Depth is scaled by 256 in OpenCV

        # Filter defects based on geometry and depth
        if depth_value > 10 and far_point[1] < cog[1]:  # Above the CoG and deep enough
            finger_points.append(start_point)
            
            # Visualize the points on the frame
            cv2.circle(frame, start_point, 5, (0, 255, 0), -1)  # Start points in green
            cv2.circle(frame, far_point, 5, (0, 0, 255), -1)    # Far points in red
            cv2.circle(frame, end_point, 5, (255, 0, 0), -1)    # End points in blue
            
            # Draw lines connecting points
            cv2.line(frame, start_point, end_point, (255, 255, 0), 2)
            cv2.line(frame, start_point, far_point, (0, 255, 255), 1)
            cv2.line(frame, end_point, far_point, (0, 255, 255), 1)

    # Return the classified finger points and the annotated frame
    return finger_points, frame