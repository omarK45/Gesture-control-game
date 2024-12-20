import cv2
import numpy as np

import math



def find_hand_contour(contours, frame):

    
    # Initialize the first contour as the hand_contour
    hand_contour = contours[0]

    for contour in contours:
        # Ignore contours with an area smaller than 500 (filter out small contours)
        if cv2.contourArea(contour) < 500:
            continue
       
        # Get the x and y coordinates of the contour points
        contour_points = contour[:, 0]  # Get the array of points, since each contour is an array of tuples

        # Get the minimum and maximum x and y values from the contour points to define the bounding box
        Xmin, Xmax = contour_points[:, 0].min(), contour_points[:, 0].max()  # Min and max x-coordinates
        Ymin, Ymax = contour_points[:, 1].min(), contour_points[:, 1].max()  # Min and max y-coordinates
        
        # Calculate the width and height of the bounding box
        width = Xmax - Xmin
        height = Ymax - Ymin
        
        # Calculate the aspect ratio of the bounding box
        aspect_ratio = float(width) / height

        # Skip contours that are close to a square (aspect ratio between 0.8 and 1.2)
        # This helps in ignoring oval or circular contours
        if 0.8 < aspect_ratio < 1.2:
            continue
        
        # Apply further conditions to identify the hand contour
        # Aspect ratio should be between 0.5 and 2.0 for a valid hand contour
        if aspect_ratio > 0.5 and aspect_ratio < 2.0:
            hand_contour = contour
            break  # Stop after finding a valid hand contour

    return hand_contour  # Return the identified hand contour


def point_to_line_distance(point, line_start, line_end):
    """
    Calculate the perpendicular distance from a point to a line segment.
    """
    px, py = point
    x1, y1 = line_start
    x2, y2 = line_end

    # Line segment length squared
    line_length_sq = (x2 - x1)**2 + (y2 - y1)**2
    if line_length_sq == 0:
        return math.sqrt((px - x1)**2 + (py - y1)**2)  # Point is on the start of the line

    # Project point onto the line segment
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / line_length_sq))
    projection_x = x1 + t * (x2 - x1)
    projection_y = y1 + t * (y2 - y1)

    # Distance from the point to the projection
    return math.sqrt((px - projection_x)**2 + (py - projection_y)**2)

def compute_convexity_defects(contour, hull_indices):

    defects = []
    contour_points = [(p[0][0], p[0][1]) if isinstance(p[0], np.ndarray) else tuple(p[0]) for p in contour]

    # Iterate over hull points
    for i in range(len(hull_indices)):
        pt_start = hull_indices[i]
        pt_end = hull_indices[(i + 1) % len(hull_indices)]

        # Check if hull points are in the contour
        if pt_start in contour_points and pt_end in contour_points:
            index_start = contour_points.index(pt_start)
            index_end = contour_points.index(pt_end)

            max_distance = 0
            defect_point_index = None  

           
            for idx in range(index_start + 1, index_end):
                point_in_range = contour_points[idx]
                distance_from_hull = point_to_line_distance(
                    point_in_range,
                    contour_points[index_start],
                    contour_points[index_end]
                )

                if max_distance < distance_from_hull:
                    max_distance = distance_from_hull
                    defect_point_index = idx

            if defect_point_index is not None and max_distance>15:
               
                start_point = contour_points[index_start]
                end_point = contour_points[index_end]
                deepest_point = contour_points[defect_point_index]

                defects.append((start_point, end_point, deepest_point, max_distance))

    return defects


def draw_convexity_defects(image, contour, defects):
  
    for defect in defects:
        start_point, end_point, deepest_point, depth = defect

        # Draw lines for start to end
        cv2.line(image, start_point, end_point, (0, 255, 0), 2)

        # Draw a line from the deepest point to the line segment
        cv2.line(image, deepest_point, start_point, (255, 0, 0), 2)
        cv2.line(image, deepest_point, end_point, (255, 0, 0), 2)

     

      

    return image




