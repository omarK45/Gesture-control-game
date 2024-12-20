import cv2
import numpy as np

def calibrate_skin_tone(frame, tolerance_hsv=40, tolerance_ycrcb=20):
    
    h, w, _ = frame.shape
    x1, y1, x2, y2 = w // 2 - 50, h // 2 - 50, w // 2 + 50, h // 2 + 50
    roi = frame[y1:y2, x1:x2]

    
    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    hsv_mean = np.mean(roi_hsv, axis=(0, 1))
    hsv_min = np.clip(hsv_mean - tolerance_hsv, 0, 255).astype(np.uint8)
    hsv_max = np.clip(hsv_mean + tolerance_hsv, 0, 255).astype(np.uint8)

   
    roi_ycrcb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCrCb)
    ycrcb_mean = np.mean(roi_ycrcb, axis=(0, 1))
    ycrcb_min = np.clip(ycrcb_mean - tolerance_ycrcb, 0, 255).astype(np.uint8)
    ycrcb_max = np.clip(ycrcb_mean + tolerance_ycrcb, 0, 255).astype(np.uint8)

    print("Calibrated HSV Min:", hsv_min, "HSV Max:", hsv_max)
    print("Calibrated YCrCb Min:", ycrcb_min, "YCrCb Max:", ycrcb_max)

    return (tuple(hsv_min), tuple(hsv_max)), (tuple(ycrcb_min), tuple(ycrcb_max))

def skin_segmentation(frame, hsv_min, hsv_max):
   
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

    # Create masks for HSV and YCrCb
    mask_hsv = cv2.inRange(hsv, np.array(hsv_min, dtype=np.uint8), np.array(hsv_max, dtype=np.uint8))
    #mask_ycrcb = cv2.inRange(ycrcb, np.array(ycrcb_min, dtype=np.uint8), np.array(ycrcb_max, dtype=np.uint8))

   
    #mask_combined = cv2.bitwise_and(mask_hsv, mask_ycrcb)

  
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    #mask_combined = cv2.morphologyEx(mask_combined, cv2.MORPH_OPEN, kernel, iterations=2)
    #mask_combined = cv2.morphologyEx(mask_combined, cv2.MORPH_CLOSE, kernel, iterations=2)

    return mask_hsv
