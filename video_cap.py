import cv2

def capture_video():
    """
    Captures video frames from the webcam and returns the original frame.
    :return: Generator yielding video frames.
    """
    cap = cv2.VideoCapture(0)  # Default camera index
    if not cap.isOpened():
        print("Error: Cannot access the camera.")
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video.")
            break

        frame_resized = cv2.resize(frame, (640, 480))  # Resize for efficiency
        yield frame_resized  # Return the original resized frame

    cap.release()
    cv2.destroyAllWindows()
