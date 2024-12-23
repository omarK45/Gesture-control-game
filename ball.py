import time
import cv2
import numpy as np

BALL_COLOR = (255, 255, 0)  # Yellow ball
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
from random import randint
from random import choice

class Ball:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.is_shrinking = False
        self.shrink_frames = 10  # Number of frames for shrinking animation

    def move(self):
        self.y += self.speed  # Move the ball downwards

    def draw(self, frame):
        cv2.circle(frame, (self.x, self.y), self.radius, BALL_COLOR, -1)  # Draw the ball on the frame

    def shrink(self):
        if self.is_shrinking and self.shrink_frames > 0:
            self.radius -= max(self.radius // self.shrink_frames, 1)  # Reduce radius by at least 1
            self.shrink_frames -= 1
            if self.shrink_frames == 0:
                self.radius = 0  # Completely shrink

    def update_and_draw(frame, balls, bullet_position, bullet_angle, ball_radius, ball_speed, score,last_ball_spawn_time, ball_spawn_interval, paused,multiplier,pauseballs):
        # Update and draw balls only if not paused
        if not paused and not pauseballs:
            for ball in balls:
                ball.move()  # Move the ball only if the game is not paused
                ball.draw(frame)
                # Reset ball to the top if it falls out of the screen
                if ball.y - ball.radius > SCREEN_HEIGHT:
                    ball.y = randint(-200, -50)
                    ball.x = choice([ball_radius + 20, SCREEN_WIDTH - (ball_radius + 20)])

                # Check for collision with the bullet
                if bullet_position and detect_collision(bullet_position, ball):
                    balls.remove(ball)  # Remove the ball on collision
                    bullet_position = None  # Reset the bullet position
                    bullet_angle = None
                    score += multiplier  # Increase score by 10
                    # Spawn new balls periodically even if the game is paused
            if time.time() - last_ball_spawn_time > ball_spawn_interval:
                side = choice([0, 1])
                if side == 0:
                    x_pos = ball_radius + 10
                else:
                    x_pos = SCREEN_WIDTH - ball_radius
                y_pos = randint(-200, -50)
                balls.append(Ball(x_pos, y_pos, ball_radius, ball_speed))
                last_ball_spawn_time = time.time()
        elif (paused==True):
         for ball in balls:
                ball.draw(frame)
                # Reset ball to the top if it falls out of the screen
                if ball.y - ball.radius > SCREEN_HEIGHT:
                    ball.y = randint(-200, -50)
                    ball.x = choice([ball_radius + 20, SCREEN_WIDTH - (ball_radius + 20)])
       
       
       #for peace sign
        elif(pauseballs==True):
            for ball in balls:
                ball.draw(frame)
                # Reset ball to the top if it falls out of the screen
                if ball.y - ball.radius > SCREEN_HEIGHT:
                    ball.y = randint(-200, -50)
                    ball.x = choice([ball_radius + 20, SCREEN_WIDTH - (ball_radius + 20)])

        # Check for collision with the bullet
                if bullet_position and detect_collision(bullet_position, ball):
                    balls.remove(ball)  # Remove the ball on collision
                    bullet_position = None  # Reset the bullet position
                    bullet_angle = None
                    score += multiplier  # Increase score by 10
        

        # Display the score
        cv2.putText(frame, f"Score: {score}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return bullet_position, bullet_angle, score, last_ball_spawn_time

def detect_collision(bullet_pos, ball):
    distance = np.sqrt((bullet_pos[0] - ball.x) ** 2 + (bullet_pos[1] - ball.y) ** 2)
    return distance <= ball.radius