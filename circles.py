import cv2
import serial
import os
# Run the lsusb command and store the output in a variable
port = os.popen("ls /dev | grep ACM").read().rstrip()

if port=="":
    print("error no arduino port")
    exit()
port="/dev/"+port
print(port)

# Create a VideoCapture object to read the video stream
cap = cv2.VideoCapture(2)

# Set the camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Create a named window to display the video
cv2.namedWindow('Video')

ser = serial.Serial(port, 9600, timeout=1)
ser.reset_input_buffer()

        
# Loop until the user presses the 'q' key
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Blur the image to reduce noise
    gray_blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through detected contours and process each one
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)

        # Filter out small or large areas (adjust these thresholds)
        min_area = 100
        max_area = 2000
        if min_area < area < max_area:
            # Get the bounding rectangle of the contour
            x, y, w, h = cv2.boundingRect(contour)
            
            print("x=",x,"y=",y,"w=",w,"h=",h)
            ser.write(str(str(x)+"-"+str(y)+"-"+str(w)+"-"+str(h)"\n").encode())
            
            # Draw the bounding rectangle on the original frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            ser.write("0-0-0".encode())    
            
       # Display the resulting frame
    cv2.imshow('Video', frame)
    
    # Check for user input
    if cv2.waitKey(1) == ord('q'):
        break

# Release the VideoCapture object
cap.release()
