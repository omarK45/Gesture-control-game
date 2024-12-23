import cv2
import mediapipe as mp
import numpy as np

def detect_hand_and_get_hsv_mask(frame):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=1,
                           min_detection_confidence=0.5,
                           min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils
    
    hsv_mask = np.zeros_like(frame[:, :, 0])  # Initialize an empty mask
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get bounding box
            h, w, _ = frame.shape
            x_min = w
            y_min = h
            x_max = y_max = 0
            for lm in hand_landmarks.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x)
                y_max = max(y_max, y)

            # Expand the bounding box slightly for better mask creation
            x_min = max(x_min - 20, 0)
            y_min = max(y_min - 20, 0)
            x_max = min(x_max + 20, w)
            y_max = min(y_max + 20, h)

            # Extract hand region
            hand_region = frame[y_min:y_max, x_min:x_max]

            # Convert to HSV and create a mask
            hsv_hand = cv2.cvtColor(hand_region, cv2.COLOR_BGR2HSV)
            hsv_mean = np.mean(hsv_hand, axis=(0, 1))
            lower_hsv = np.clip(hsv_mean - 30, 0, 255).astype(np.uint8)
            upper_hsv = np.clip(hsv_mean + 30, 0, 255).astype(np.uint8)

            # Create an HSV mask for the entire frame
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hsv_mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)

            # Draw the bounding box on the frame (optional)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
    
    return frame, hsv_mask
