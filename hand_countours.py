import cv2
import numpy as np

import math
def find_hand_contour(contours, frame):
    eps = 1e-7  # Small epsilon to avoid division by zero
    hand_contour = None
    aspect_ratio = 0

    if not contours:
        return None, 0  # No contours found

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue

        contour_points = contour[:, 0]  # Extract x and y coordinates
        Xmin, Xmax = contour_points[:, 0].min(), contour_points[:, 0].max()
        Ymin, Ymax = contour_points[:, 1].min(), contour_points[:, 1].max()
        width = Xmax - Xmin
        height = Ymax - Ymin + eps
        aspect_ratio = float(width) / height

        if 0.5 < aspect_ratio < 2.0:  # Valid hand aspect ratio range
            hand_contour = contour
            break

    if hand_contour is None:
        hand_contour = contours[0]  # Fallback to the first contour
        contour_points = hand_contour[:, 0]
        Xmin, Xmax = contour_points[:, 0].min(), contour_points[:, 0].max()
        Ymin, Ymax = contour_points[:, 1].min(), contour_points[:, 1].max()
        width = Xmax - Xmin
        height = Ymax - Ymin + eps
        aspect_ratio = float(width) / height

    return hand_contour, aspect_ratio
