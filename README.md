DEADEYE SHOOTER

Welcome to DEADEYE SHOOTER, a gesture-controlled shooting game powered by real-time computer vision and image processing. Use your hand gestures to control the game and achieve the highest score!

Game Setup
	1.	Ensure your default camera is set correctly (e.g., cv2.VideoCapture(0) for OpenCV).
	2.	Place your hand inside the green rectangle at the start and press ‘C’ to calibrate the system to your skin tone.
	3.	Important:
	•	Sit close to the screen to ensure the camera can clearly capture your hand.
	•	Make sure your hand is in front of your body to avoid confusion with the background.

Game Objective

The objective is to shoot as many moving balls as possible while using special gestures to enhance your gameplay.

Controls and Gestures
	•	Gun Gesture (Thumb and Index Finger Extended): Shoot a bullet in the direction of the moving balls.
	•	Open Palm Gesture: Pause or resume the game.
	•	Peace Gesture (Two Fingers): Freeze the balls for 10 seconds.
	•	Three-Finger Gesture: Multiply your points by 3 for 10 seconds.

Gesture Tips:
	•	Keep your hand steady and clearly visible to the camera.
	•	Stay within 1-2 feet of the camera for optimal recognition.
	•	Always position your hand against your body for a clean contrast against the background.
	•	Avoid overlapping fingers or moving too quickly, as it may interfere with accurate gesture detection.

Game Mechanics
	1.	Moving Balls: Balls appear on the screen and move dynamically. Aim and shoot to hit them.
	2.	Score Multiplier: Activate the three-finger gesture to temporarily triple your points.
	3.	Frozen Targets: Use the peace gesture to stop all balls for easier targeting.
	4.	Pause/Resume: Need a break? Open your palm to pause or resume the game.

How to Exit

To quit the game, press ‘Q’ at any time.

Installation and Requirements
	1.	Clone the repository to your local machine.
	2.	Install the required Python libraries using:

pip install -r requirements.txt


	3.	Run the game:

python main.py

Dependencies

The game relies on the following libraries:
	•	OpenCV (for video capture and image processing)
	•	NumPy (for numerical computations)
	•	PyGame (for graphical enhancements and sound effects)

Calibration Process
	1.	During calibration, place your hand in the green rectangle.
	2.	Press ‘C’ to capture your skin tone range for accurate gesture recognition.
	3.	The system uses HSV and YCrCb color spaces for robust skin segmentation under various lighting conditions.
	4.	Ensure the following during calibration:
	•	Your hand is clearly visible and positioned in front of your chest or torso.
	•	You are seated close to the screen (about 1 feet away) for better accuracy.

Troubleshooting
	•	Game doesn’t start:
	•	Ensure your camera is connected and accessible (cv2.VideoCapture(0)).
	•	Gestures not recognized:
	•	Check the lighting conditions and ensure your hand is within the camera’s view.
	•	Ensure your hand is in front of your body and not blending into the background.
	•	Recalibrate using the ‘C’ key.
	•	Balls are not freezing/multiplying points:
	•	Ensure the gestures are performed clearly and distinguishably.
	•	Stay close to the camera and maintain steady hand movements.

Enjoy your gesture-controlled gaming experience with DEADEYE SHOOTER!