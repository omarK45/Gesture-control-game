import cv2
import mediapipe as mp

def classify_gesture(hand_landmarks):
 
    thumb_tip = hand_landmarks[mp.solutions.hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks[mp.solutions.hands.HandLandmark.THUMB_IP]
    index_tip = hand_landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    index_mcp = hand_landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP]
    middle_tip = hand_landmarks[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_mcp = hand_landmarks[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP]
    ring_tip = hand_landmarks[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks[mp.solutions.hands.HandLandmark.PINKY_TIP]

    def is_above(p1, p2):
        #Check if a fingertip is above its base."""
        return p1.y < p2.y

    def is_spread(p1, p2, threshold):
        #Check if two landmarks are far enough apart horizontally."""
        return abs(p1.x - p2.x) > threshold

    def is_left(p1, p2):
        #Check if one landmark is to the left of another."""
        return p1.x < p2.x

    # Gun Gesture Pointing Left
    if is_above(thumb_tip, thumb_ip) and is_spread(thumb_tip, index_tip, 0.2) and \
       is_left(middle_tip, thumb_tip) and all(is_above(thumb_tip, finger_tip) for finger_tip in [index_tip, middle_tip, ring_tip, pinky_tip]):
        return "gun"

    # Gun Gesture Pointing Right
    if is_above(thumb_tip, thumb_ip) and is_spread(thumb_tip, index_tip, 0.2) and \
       not is_left(middle_tip, thumb_tip) and all(is_above(thumb_tip, finger_tip) for finger_tip in [index_tip, middle_tip, ring_tip, pinky_tip]):
        return "gun"

    # Open Palm
    if all(is_above(finger_tip, finger_mcp) for finger_tip, finger_mcp in [
        (thumb_tip, thumb_ip), (index_tip, index_mcp), (middle_tip, middle_mcp), (ring_tip, middle_mcp), (pinky_tip, middle_mcp)]) and \
       is_spread(thumb_tip, index_tip, 0.05) and is_spread(index_tip, middle_tip, 0.03):
        return "open palm"

    # Peace Sign
    if is_above(index_tip, index_mcp) and is_above(middle_tip, middle_mcp) and \
       not is_above(ring_tip, middle_mcp) and not is_above(pinky_tip, middle_mcp) and is_spread(index_tip, middle_tip, 0.1):
        return "peace"

    # Three-Finger Gesture (Index, Middle, Ring)
    if is_above(index_tip, index_mcp) and is_above(middle_tip, middle_mcp) and is_above(ring_tip, middle_mcp) and is_spread(index_tip, middle_tip, 0.05):
        return "three"

    return "Unknown Gesture"


def predict_gesture_from_frame(frame, hands, mp_drawing):

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            #mp_drawing.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
            return classify_gesture(hand_landmarks.landmark)
    return "No Hand Detected"
