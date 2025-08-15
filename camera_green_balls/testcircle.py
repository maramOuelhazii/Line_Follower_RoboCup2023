import cv2
import numpy as np
import serial
import os
import time

port = os.popen("ls /dev | grep ACM").read().rstrip()

if port=="":
    print("error no arduino port")
    exit()
port="/dev/"+port
print(port)
ser = serial.Serial(port, baudrate=115200 , timeout=0.1)
cap = cv2.VideoCapture(2)
command = ""
counter = 0
state = False
time.sleep(2)
ball_counter = 0

def detect_green(image,cap):
    lower_green = np.array([35, 40, 50])
    upper_green = np.array([100, 255, 200])
    mask_green = cv2.inRange(image, lower_green, upper_green) 
    kernel = np.ones((5, 5), np.uint8)  
    mask_green = cv2.erode(mask_green, kernel) 
    mask_green = cv2.erode(mask_green, kernel) 
    mask_green = cv2.erode(mask_green, kernel) 
    mask_green = cv2.erode(mask_green, kernel) 
    mask_green = cv2.dilate(mask_green, kernel)
    mask_green = cv2.dilate(mask_green, kernel)
    mask_green = cv2.dilate(mask_green, kernel)
    mask_green = cv2.dilate(mask_green, kernel)
    if not cv2.countNonZero(mask_green):
        return 'no green detected',False
    if image is not None:
        contours, ret = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        counter = 0
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w>100:
                cv2.rectangle(cap, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            #if counter >=4:
            # return 'stop',False
                return 'green detected',x+(w/2),y+h,cap
        else: return 'problem',False
    else: return 'problem',False
def detect_gray(image):
    lower_gray = np.array([35, 35, 35])
    upper_gray = np.array([80, 90, 100])
    mask_gray = cv2.inRange(image, lower_gray, upper_gray) 
    kernel = np.ones((2, 2), np.uint8)  
    mask_gray = cv2.erode(mask_gray, kernel) 
    mask_gray = cv2.dilate(mask_gray, kernel)
    if not cv2.countNonZero(mask_gray):
        return 'no gray',False
    if image is not None:
        contours, ret = cv2.findContours(mask_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        counter = 0
        for contour in contours:
            _, _, w, _ = cv2.boundingRect(contour)
            if w>30:
                counter+=1
        if ret.shape[1]:        
            x_pos, y_pos,w,h = cv2.boundingRect(contours[0])
            if counter >1:
                return 'stop',False
            elif w>50 and y_pos>50 and y_pos<350:
                return 'gray detected',x_pos,y_pos,w,h
            else: return 'problem',False
        else: return 'problem',False

    else: return 'problem',False
def detect_red(image):
    lower_red = np.array([0, 0, 100])
    upper_red = np.array([40, 40, 255])
    mask_red = cv2.inRange(image, lower_red, upper_red) 
    kernel = np.ones((2, 2), np.uint8)  
    mask_red = cv2.erode(mask_red, kernel) 
    mask_red = cv2.dilate(mask_red, kernel)
    if not cv2.countNonZero(mask_red):
        return 'no red',False
    if image is not None:
        contours, ret = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        counter = 0
        for contour in contours:
            _, _, w, _ = cv2.boundingRect(contour)
            if w>30:
                counter+=1
        if ret.shape[1]:        
            x_pos, y_pos,w,h = cv2.boundingRect(contours[0])
            if counter >1:
                return 'stop',False
            elif w>50 and y_pos>50 and y_pos<350:
                return 'red detected',x_pos,y_pos,w,h
            else: return 'problem',False
        else: return 'problem',False

    else: return 'problem',False
def detect_blue(image):
    lower_blue = np.array([100, 35, 35])
    upper_blue = np.array([255, 90, 80])
    mask_gray = cv2.inRange(image, lower_blue, upper_blue) 
    kernel = np.ones((2, 2), np.uint8)  
    mask_blue = cv2.erode(mask_blue, kernel) 
    mask_blue = cv2.dilate(mask_blue, kernel)
    if not cv2.countNonZero(mask_blue):
        return 'no blue',False
    if image is not None:
        contours, ret = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        counter = 0
        for contour in contours:
            _, _, w, _ = cv2.boundingRect(contour)
            if w>30:
                counter+=1
        if ret.shape[1]:        
            x_pos, y_pos,w,h = cv2.boundingRect(contours[0])
            if counter >1:
                return 'stop',False
            elif w>50 and y_pos>50 and y_pos<350:
                return 'blue detected',x_pos,y_pos,w,h
            else: return 'problem',False
        else: return 'problem',False

    else: return 'problem',False
def verif(x): 
    global command
    test = x-320
    if test<20 and test>-20:
        command = "S"
    else:
        if test<0:
            command = "L"
        elif test>0:
            command = "R"
        else:
            command = "Z"
def verif_dir(x):
    global command
    test = x-320
    if test<30 and test>-30:
        command = "F"
    else:
        if test<0:
            command = "L"
        elif test>0:
            command = "R"
        else:
            command = "Z"
def detect_black(image):
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([179, 255, 85])  # 30-->50
    if image is not None:
        mask_black = cv2.inRange(image, lower_black, upper_black)
        kernel = np.ones((2, 2), np.uint8)
        mask_black = cv2.erode(mask_black, kernel)
        mask_black = cv2.erode(mask_black, kernel)
        mask_black = cv2.erode(mask_black, kernel)
        mask_black = cv2.dilate(mask_black, kernel)
        mask_black = cv2.dilate(mask_black, kernel)
        mask_black = cv2.dilate(mask_black, kernel)
        if np.mean(mask_black) > 150:
            return True,mask_black
        else:
            return False,mask_black
    else:
        return False,False
def dropBalls(x,y): 
    global command
    test = x-320
    if y>400:
        command = "D"
    else:
        if test<-30:
            command = "L"
        elif test>30:
            command = "R"
        elif test<30 and test>-30:
            command = "F"
        else:
            command = "Z"



    



while True:
    if True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame,(640,480))
        frame_hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)
        frame_hsv1 = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
        state, mask = detect_black(frame_hsv)
        circles = cv2.HoughCircles(frame_hsv1.copy(), cv2.HOUGH_GRADIENT, dp=2.2, minDist=120)
        max_r=0
        max_x=0
        max_y=0
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                if r> 100:
                    break
                if (max_r<r):
                    max_r=r
                    max_x=x
                    max_y=y 
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            cv2.circle(frame, (max_x, max_y), max_r, (0, 0, 255), 4)
            if (max_r>80):
                verif(max_x)
            else:
                verif_dir(max_x)    
        else:
            command = "Z"
    if ball_counter == 4:
        result = detect_green(frame_hsv,frame)
        if result[0] =='green detected':
            dropBalls(result[1],result[2])
            frame = result[3]
        else:
            command = "Z"
            ser.write((command+"\n").encode())
            print(command)
    if command == "D":
        ser.write((command+"\n").encode())
        ball_counter == 0
        command == "Z"
        print(command)
    else:
        print(command)
        if command == "S"  and state==False and counter == 0:
            state = True
            ser.write((command+"\n").encode())
            print("getting the ball")
            ball_counter+=1
            while(counter<2600000):
                counter+=1
            
        else:
            ser.write((command+"\n").encode())
            counter = 0
            state = False
            ser.flush()
        print(ball_counter)
        cv2.imshow('Video', frame) 
        if cv2.waitKey(1) == 27:
            break
ser.close()
cap.release()
cv2.destroyAllWindows()