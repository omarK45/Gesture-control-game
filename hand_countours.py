import cv2
import numpy as np

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
