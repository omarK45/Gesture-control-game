import cv2
import numpy as np
import pygame
import gui
from Background_subtract import BackgroundSubtractor
from skin_segment import calibrate_skin_tone, skin_segmentation
from hand_countours import *
from convex_hull import *
from Dataset_Creation import *
from CoG import *
from Classification import *
from convexity_defects import *
from Angle_detection import *
from bullet import *
from random import randint
from random import choice
from ball import Ball
import time
from extras import *
from skin_segment_dnn import *


BALL_COLOR = (255, 255, 0)  # Yellow ball
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
# Ball class to represent the falling balls



import pickle
                        
def main():
    
       # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,max_num_hands=2,min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils
    
    gesture_change=False
    majority_element=None
    gesture_count=0
    gesture_array=[]
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open camera.")
        return
    bg_subtractor = BackgroundSubtractor(alpha=0.005)
    calibrated = False
    hsv_min, hsv_max = None, None
    # Create balls
    balls = []
    ball_radius = 30
    ball_speed = 15

    # Add initial balls to the list (randomly from left or right)
    for _ in range(2):
        side = choice([0, 1])  # Randomly choose left (0) or right (1)
        if side == 0:
            x_pos = ball_radius + 10
        else:
            x_pos = SCREEN_WIDTH - ball_radius
        y_pos = randint(-200, -50)  # Start above the screen
        balls.append(Ball(x_pos, y_pos, ball_radius, ball_speed))
    print("Place your hand in the rectangle and press 'c' to calibrate.")
    ycrcb_min, ycrcb_max = None, None
    bullet_position=None
    
    bullet_angle=None
    score = 0
    ball_spawn_interval = 5    # Time in seconds between spawning new balls
    last_ball_spawn_time = time.time()  # Track the last spawn time
    paused = False  # Initialize the pause state
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)  # Flip to correct orientation
        if not calibrated:
            h, w, _ = frame.shape
            cv2.rectangle(frame, (w // 2 - 50, h // 2 - 50), (w // 2 + 50, h // 2 + 50), (0, 255, 0), 2)
            cv2.putText(frame, 'Press c to calibrate...', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('Calibration', frame)

            if cv2.waitKey(1) & 0xFF == ord('c'):
                (hsv_min, hsv_max), (ycrcb_min, ycrcb_max) = calibrate_skin_tone(frame)
                calibrated = True
                cv2.destroyWindow('Calibration')
                print("Calibration Complete!")
            continue
   
        
        #Pausingggggggggg Balls 
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Pressed 'q' to quit.")
            gui.quit_game()
            break
        elif key ==ord('p'):
            paused = not paused
            print("Pause isssss")
            print(paused)

        if  (majority_element == "open palm") and gesture_change:
            paused=not paused
            gesture_change=False

        # if  cv2.waitKey(1) & 0xFF == ord('p'):  # Press 'p' to toggle pause

           
        bullet_position, bullet_angle, score, last_ball_spawn_time = Ball.update_and_draw(frame, balls, bullet_position, bullet_angle, ball_radius, ball_speed, score, last_ball_spawn_time, ball_spawn_interval,paused)
        height=frame.shape[0]
        left_quarter_x = frame.shape[1] // 6
        right_corner_x = left_quarter_x*5
        middle_frame = frame[:, left_quarter_x:right_corner_x]
        # Add lines to the frame
        # color = (128, 128, 128)
        # thickness = 2  # Thickness of the lines
        # cv2.line(frame, (left_quarter_x, 0), (left_quarter_x, height), color, thickness)  # Left quarter line
        # cv2.line(frame, (right_corner_x, 0), (right_corner_x, height), color, thickness)  # Right corner line

        # Background subtraction and skin segmentation
        bg_mask = bg_subtractor.apply(frame)
        
        #cv2.bitwise_not(mask_ycrcb)
        #combined_mask=cv2.bitwise_and(mask_hsv,bg_mask)
        #combined_mask=cv2.bitwise_and(mask_hsv,bg_mask)
        #segmented_output = cv2.bitwise_and(frame, frame, mask=skin_mask)
        mask_hsv= skin_segmentation(frame, hsv_min, hsv_max)
       
        
        # Find contours from the HSV mask
        contours, hierarchy = cv2.findContours(mask_hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours)==0:
           continue
        # Sort contours by area
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Use the function to find the hand contour
        
        hand_contour,aspect_ratio= find_hand_contour(sorted_contours, frame)

        # Draw the detected hand contour
        if hand_contour is not None:
            cv2.drawContours(frame, [hand_contour], -1, (0, 255, 0), 7)  # Green contour

            hull = convex_hull(hand_contour)  # normal
            hull_contour = np.array(hull, dtype=np.int32).reshape((-1, 1, 2))  # motkhalef
            cv2.drawContours(frame, [hull_contour], -1, (0, 0, 255), 7)

        points = [(p[0][0], p[0][1]) if isinstance(p[0], np.ndarray) else tuple(p[0]) for p in hand_contour]
        centroid = calculate_centroid(points)
        centroid = (int(centroid[0]), int(centroid[1]))
        cv2.circle(frame, centroid, 5, (255, 0, 0), -1)

        defects = compute_convexity_defects(hand_contour, hull)
        frame = draw_convexity_defects(frame, hand_contour, defects)

        
        cv2.imshow("Original Frame", frame)
        #cv2.imshow("bg mask", bg_mask)
        #cv2.imshow("combined mask",combined_mask)
        cv2.imshow("HSV Mask", mask_hsv)
        #cv2.imshow("dnn Mask", mask_dnn)
        
        
        
        with open("datasets/svm_model.pkl", "rb") as model_file:
            svm = pickle.load(model_file)
        with open("datasets/scaler.pkl", "rb") as scaler_file:
            scaler = pickle.load(scaler_file)

        
        
        convex_hull_area = cv2.contourArea(np.array(hull, dtype=np.int32))
        contour_area = cv2.contourArea(hand_contour)
        contour_hull_ratio = contour_area / convex_hull_area
        
        perimeter = cv2.arcLength(hand_contour, True)
        circularity = (4 * np.pi * contour_area) / (perimeter ** 2)
        
        frame_features = np.array([len(defects), contour_hull_ratio, aspect_ratio, circularity]).reshape(1, -1)
        features_scaled = scaler.transform(frame_features)
        # print(frame.shape)
        # Predict gesture
        prediction = svm.predict(features_scaled)
        predictiondnn=predict_gesture_from_frame(frame,hands,mp_drawing)
        print("Prediction:", prediction[0])
        print("Prediction: using dnn", predictiondnn)
        cv2.putText(frame, f"Gesture: {prediction[0]}", (1000, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Gesture: {predictiondnn}", (1000, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        gesture_array.append(prediction[0])
        gesture_count+=1
        if gesture_count==30:
            
            majority_element = find_majority_element(gesture_array)
            if majority_element=="open palm":
                gesture_change=True
            gesture_count=0
            gesture_array=[]
    
        #________________________________________Bullet_____________________________________
        if majority_element=="gun":
            rounded_angle, furthest_point = calculate_angle(centroid,hull)
            if(bullet_position==None):
                bullet_position=furthest_point
                bullet_angle=rounded_angle
                
        
            if not paused:
                bullet_position = move_bullet(frame, bullet_position, bullet_angle, speed=25)

        # Check if the bullet is out of frame
            if (bullet_position[0] < 0 or bullet_position[0] >= frame.shape[1] or
                bullet_position[1] < 0 or bullet_position[1] >= frame.shape[0]):
                bullet_position=None
                bullet_angle=None

    # Display the frame
        cv2.imshow("Bullet Animation", frame)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    gui.main_menu()