import cv2
import os

# Run the lsusb command and store the output in a variable
#port = os.popen("ls /dev | grep ACM").read().rstrip()

#if port == "":
   # print("error no Arduino port")
   # exit()
#port = "/dev/" + port
#print(port)

# Create a VideoCapture object to read the video stream
cap = cv2.VideoCapture(0)

# Set the camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Create a named window to display the video
cv2.namedWindow('Video')

# Loop until the user presses the 'q' key
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur the image to reduce noise
    gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Hough Circle Transform to detect circles in the blurred image
    circles = cv2.HoughCircles(
        gray_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=30,
        param1=50, param2=30, minRadius=10, maxRadius=50
    )

    # If circles are detected, process each one
    if circles is not None:
        circles = circles.astype(int)
        for circle in circles[0, :]:
            x, y, radius = circle

            # Print circle information
            print("x=", x, "y=", y, "radius=", radius)

            # Draw the circle on the original frame
            cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Check for user input
    if cv2.waitKey(1) == ord('q'):
        break

# Release the VideoCapture object
cap.release()
