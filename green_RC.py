import cv2
import serial
import os
port="COM6"
#Initialize the camera and grab a reference to the raw camera capture
camera = cv2.VideoCapture(0)

ser = serial.Serial(port, 9600, timeout=1)
ser.reset_input_buffer()

while True:
    # Grab a frame
    (grabbed, frame) = camera.read()

    # Check if the frame was grabbed correctly
    if not grabbed:
        break

    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of colors to detect
    lower_green = (40, 100, 20)
    upper_green = (80, 255, 255)

    # Create a mask for the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Bitwise-AND the mask and the original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    #divide ethe frame into four parts

    height, width = frame.shape[:2]

    top_left = frame[:height//2, :width//2]
    top_right = frame[:height//2, width//2:]
    bottom_left = frame[height//2:, :width//2]
    bottom_right = frame[height//2:, width//2:]

    # Apply the mask to each part
    top_left_masked = mask[:height//2, :width//2]
    top_right_masked = mask[:height//2, width//2:]
    bottom_left_masked = mask[height//2:, :width//2]
    bottom_right_masked = mask[height//2:, width//2:]

    # Check if any green pixels were detected in the right half
    if cv2.countNonZero(top_right_masked) >= 400:
        print("Green detected on top_right_masked!")
        a=1
    else:
        a=0    

    # Check if any green pixels were detected in the right half
    if cv2.countNonZero(bottom_right_masked) >= 400:
        print("Green detected on bottom_right_masked!")
        b=1
    else:
        b=0    

    # Check if any green pixels were detected in the leftt half
    if cv2.countNonZero(top_left_masked) >= 400:
        print("Green detected on top_left_masked!")
        c=1
    else:
        c=0        

    # Check if any green pixels were detected in the right half
    if cv2.countNonZero(bottom_left_masked) >= 400:
        print("Green detected on bottom_left_masked!")
        d=1
    else:
        d=0  
    ch=str(a)+str(b)+str(c)+str(d)
    #ser.write(ch.encode())

    # Show the frame and the mask
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", res)

    # Check if the user pressed 'q' to quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

#ser.write(str(str(a)+"-"+str(b)+"-"+str(c)+"-"+str(d)"\n").encode())
# Clean up
camera.release()
cv2.destroyAllWindows()
