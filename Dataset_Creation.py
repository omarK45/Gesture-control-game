import cv2
import os

def collect_gesture_data(gesture_name, save_path="dataset"):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open camera.")
        return

    save_dir = os.path.join(save_path, gesture_name)
    os.makedirs(save_dir, exist_ok=True)

    print(f"Collecting data for gesture: {gesture_name}")
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame.")
            break

        frame = cv2.flip(frame, 1)  # Flip horizontally
        cv2.imshow("Gesture Capture", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # Press 's' to save a frame
            filename = os.path.join(save_dir, f"frame_{frame_count}.png")
            cv2.imwrite(filename, frame)
            print(f"Saved {filename}")
            frame_count += 1
        elif key == ord('q'):  # Press 'q' to quit
            print("Exiting...")
            break

    cap.release()
    cv2.destroyAllWindows()

