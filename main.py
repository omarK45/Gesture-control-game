import cv2
import numpy as np
import pygame
from Background_subtract import BackgroundSubtractor
from skin_segment import calibrate_skin_tone, skin_segmentation
from hand_countours import *
from convex_hull import *
from CoG import *
from Classification import *

#--------------------------------GAME GUI--------------------------------#
# Initialize pygame
pygame.init()
# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# Load background image
background_image = pygame.image.load("shoot.jpg")  # Replace with your background image path
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)

# Fonts
font = pygame.font.Font("Vipnagorgialla Bd It.otf", 70)
small_font = pygame.font.Font("Vipnagorgialla Bd It.otf", 60)

# Button dimensions
BUTTON_WIDTH, BUTTON_HEIGHT = 500, 100

# Custom cursor
original_cursor = pygame.image.load("cursor.png")
custom_cursor = pygame.transform.scale(original_cursor, (60, 60))  # Resize cursor
pygame.mouse.set_visible(False)  # Hide default cursor


def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1)  # Loop indefinitely


def stop_audio():
    pygame.mixer.music.stop()


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, (x, y))


def draw_button(text, x, y, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Change color on hover
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, button_rect)
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, button_rect, border_radius=15)

    # Center text in button
    text_surface = small_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)


def start_game():
    global running_main_menu  # Use a flag to stop the main menu loop
    running_main_menu = False
    main()  # Call the main game function

def quit_game():
    stop_audio()
    cv2.destroyAllWindows()
    pygame.quit()
    exit()


def main_menu():
    play_audio("video-game-tank-metal-220562.mp3")  # Replace with your audio file path
    running_main_menu = True
    while running_main_menu:
        screen.blit(background_image, (0, 0))

        draw_text("Dead Eye Shooter", font, GREEN, SCREEN_WIDTH // 5, 100)

        # Draw buttons
        draw_button("Start Game", SCREEN_WIDTH // 2 - 200, 300, GREEN, DARK_GREEN, start_game)
        draw_button("Quit", SCREEN_WIDTH // 2 - 200, 450, RED, DARK_RED, quit_game)

        # Custom cursor
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(custom_cursor, (mouse_pos[0] - 10, mouse_pos[1] - 10))  # Adjust for better alignment

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()  # Ensure proper quitting

        # Update the display
        pygame.display.flip()


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open camera.")
        return

    bg_subtractor = BackgroundSubtractor(alpha=0.1)
    calibrated = False
    hsv_min, hsv_max = None, None

    print("Place your hand in the rectangle and press 'c' to calibrate.")
    ycrcb_min, ycrcb_max = None, None

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
        mask_hsv= skin_segmentation(middle_frame, hsv_min, hsv_max, ycrcb_min, ycrcb_max)
        #cv2.bitwise_not(mask_ycrcb)

        #segmented_output = cv2.bitwise_and(frame, frame, mask=skin_mask)
        skin_mask, mask_hsv, mask_ycrcb = skin_segmentation(frame, hsv_min, hsv_max)

        # Find contours from the HSV mask
        contours, hierarchy = cv2.findContours(mask_hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Sort contours by area
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Use the function to find the hand contour
        hand_contour = find_hand_contour(sorted_contours, frame)

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
        cv2.imshow("HSV Mask", mask_hsv)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Pressed 'q' to quit.")
            quit_game()
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main_menu()
