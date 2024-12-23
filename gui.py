import cv2
import numpy as np
import pygame
from main import main



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
