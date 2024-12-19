import cv2
import numpy as np

def calibrate_skin_tone(frame, tolerance=40):

    h, w, _ = frame.shape
    x1, y1, x2, y2 = w // 2 - 50, h // 2 - 50, w // 2 + 50, h // 2 + 50
    roi = frame[y1:y2, x1:x2]

    # Convert the ROI to HSV
    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    hsv_mean = np.mean(roi_hsv, axis=(0, 1))

    # Set HSV thresholds based on tolerance
    hsv_min = np.clip(hsv_mean - tolerance, 0, 255).astype(np.uint8)
    hsv_max = np.clip(hsv_mean + tolerance, 0, 255).astype(np.uint8)

    print("Calibrated HSV Min:", hsv_min, "HSV Max:", hsv_max)
    return tuple(hsv_min), tuple(hsv_max)


def skin_segmentation(frame, hsv_min, hsv_max):
    # Convert to HSV and YCrCb
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

    # Create HSV mask
    mask_hsv = cv2.inRange(hsv, np.array(hsv_min, dtype=np.uint8), np.array(hsv_max, dtype=np.uint8))

    # Create YCrCb mask
    ycrcb_min = np.array([0, 133, 77], dtype=np.uint8)
    ycrcb_max = np.array([255, 173, 127], dtype=np.uint8)
    mask_ycrcb = cv2.inRange(ycrcb, ycrcb_min, ycrcb_max)

    # Combine masks
    mask_combined = cv2.bitwise_or(mask_hsv, mask_ycrcb)

    # Morphological operations to clean noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask_combined = cv2.morphologyEx(mask_combined, cv2.MORPH_OPEN, kernel, iterations=2)
    mask_combined = cv2.morphologyEx(mask_combined, cv2.MORPH_CLOSE, kernel, iterations=2)

    return mask_combined,mask_hsv,mask_ycrcb

