
# # Example usage
# frame_width, frame_height = 1280, 720
# frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

# # Initialize the bullet's starting position and angle
# start_point = (640, 360)  # Starting position (x, y)
# end_point = (600, 360)    # Example second point
# angle = 180

# # Run the animation
# bullet_position = start_point
# while True:
#     # Clear the frame
#     frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

#     # Move the bullet
#     bullet_position = move_bullet(frame, bullet_position, angle, speed=10)

#     # Check if the bullet is out of frame
#     if (bullet_position[0] < 0 or bullet_position[0] >= frame_width or
#         bullet_position[1] < 0 or bullet_position[1] >= frame_height):
#         print("Bullet exited the frame.")
#         break

#     # Display the frame
#     cv2.imshow("Bullet Animation", frame)
#     if cv2.waitKey(10) & 0xFF == ord('q'):  # Press 'q' to quit
#         break

# cv2.destroyAllWindows()
# #90 

