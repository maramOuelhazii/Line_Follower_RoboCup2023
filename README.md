# Line_Follower_RoboCup_2023

The robot is designed to autonomously follow a black line on a white surface, detect green markers, and execute actions based on competition rules.

The system is divided into two main parts:

# Arduino Control (main_line.ino & arduino_com.ino)
The Arduino code handles all low-level hardware control:

Sensors: Reads data from an array of IR reflectance sensors to detect the position of the line.

PID Control: Implements a PID (Proportional–Integral–Derivative) controller to adjust motor speeds smoothly and keep the robot centered on the track.

Motor Control: Uses an L298N motor driver to control two DC motors for movement.

Serial Communication: Exchanges commands with the Raspberry Pi to synchronize line following with vision-based decisions.

Green Marker Handling: When the Pi sends a detection signal, the Arduino can slow down, stop, or perform specific maneuvers.

# Raspberry Pi Vision (circles.py & green_RC.py)
The Raspberry Pi runs Python scripts for image processing:

OpenCV-based Detection:

Captures frames from a Pi Camera.

Converts images to HSV color space for better color segmentation.

Detects green circular markers on the field using cv2.HoughCircles() and contour filtering.

Decision Making:
Once a marker is detected, sends a signal to the Arduino via serial communication.
Triggers specific robot behaviors depending on marker position (e.g., turns, stops, speed changes).


*You can consult the detailed cahier des charges [here](RCJRescueLine2023Rules.pdf).*
