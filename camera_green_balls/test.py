import cv2
import numpy as np
import serial
import time
import os
port = os.popen("ls /dev | grep ACM").read().rstrip()

vid = cv2.VideoCapture(0)   

if port=="":
    print("error no arduino port")
    exit()
port="/dev/"+port
print(port)
arduino = serial.Serial(port,baudrate=9600,timeout=0.01)
time.sleep(2)

command = ""

gray_balls = False
gray_balls_red = False
Exit = False

def ball_part(img):
        global command
        global reverse
        global gray_balls 
        global gray_balls_red 
        global Exit 
        if not Exit:
            frame_hsv = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2HSV)

            frame_gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
            _, mask = detect_black_for_balls(frame_hsv)

            if not gray_balls_red:
                circles = cv2.HoughCircles(frame_gray.copy(), cv2.HOUGH_GRADIENT, dp=2.2, minDist=120)
            else:
                circles = cv2.HoughCircles(img.copy(), cv2.HOUGH_GRADIENT, dp=2.2, minDist=120)
            max_r = 0 
            max_x = 0
            max_y = 0
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                counter1,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                if counter1:
                    for (x, y, r) in circles:
                        if r > 100:
                            break
                        if max_r < r:
                            max_r = r
                            max_x = x
                            max_y = y
                    if max_r > 80:
                        verif(max_x)
                    else:
                        verif_dir(max_x)
                else:
                    command = "Z"
            else:
                command = "Z"

            try:
                if arduino.in_waiting > 0:
                    data = arduino.readline(arduino.in_waiting)
                    if data == b'P\x00':
                        gray_balls = True
                        print("received from arduino ball part")
            except:
                pass
            if gray_balls:
                result = detect_green_for_balls(frame_hsv)
                print(result[0])
                if result[0] == 'green detected':
                    dropBalls(result[1], result[2])
                else:
                    command = "Z"
            elif gray_balls_red:
                result = detect_red_for_balls(frame_hsv, frame)
                print(result[0])
                if result[0] == 'red detected':
                    dropBalls(result[1], result[2])
                else:
                    command = "Z"
            try:
                if arduino.in_waiting > 0:
                    data = arduino.readline(arduino.in_waiting)
                
                    if data == b'P\x00':
                        gray_balls = True
                        print("greeeeeeeeeeeeeeeeeeeeeeen")
            except:
                pass

            if command == "S" or command == "D":
                if command == "D":
                    if gray_balls_red == True:
                        gray_balls_red = False
                        Exit = True
                    else: gray_balls_red = True
                    gray_balls = False
                arduino.write((command + "\n").encode())
                print("getting the ball")
                counter = 0
                while counter<500000:
                    counter+=1
                    print(counter)
            else:
                arduino.write((command+"\n").encode())
                counter = 0
                print("sending without s","\t",command)
            command = "Z"
        else:
            frame_hsv = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2HSV)
            frame_gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
            _, mask = detect_black_for_balls(frame_gray)
            try:
                if arduino.in_waiting > 0:
                    data = arduino.readline(arduino.in_waiting)
                
                    if data == b'P\x00':
                        gray_balls = True
                        print("received from arduino ball part")
            except:
                pass
            if gray_balls:
                result = detect_green_for_balls(frame_hsv, frame)
                print(result[0])
                if result[0] == 'green detected':
                    Exiit(result[1], result[2])
                else:
                    command = "Z"
            
            if command == "E":
                reverse = True
                arduino.write((command + "\n").encode())
                print("getting the ball")
                counter = 0
                while counter<300:
                    counter+=1
                    print(counter)
                    _,frame = cap.read()
            else:
                arduino.write((command + "\n").encode())
                counter = 0
                arduino.flush()
                print("sending without s")
            command = "Z"

def dropBalls(x, y):
    global command
    test = x - 320
    if y > 450:
        command = "D"
    else:
        if test < -30:
            command = "L"
        elif test > 30:
            command = "R"
        elif test < 30 and test > -30:
            command = "F"
        else:
            command = "Z"

def Exiit(x, y):
    global command
    test = x - 320
    if y > 450:
        command = "E"
    else:
        if test < -30:
            command = "L"
        elif test > 30:
            command = "R"
        elif test < 30 and test > -30:
            command = "F"
        else:
            command = "Z"

def detect_black_for_balls(image):
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
            return True, mask_black
        else:
            return False, mask_black
    else:
        return False, False

def verif(x):
    global command
    test = x - 320
    if test < 20 and test > -20 :
        command = "S"
    else:
        if test < 0:
            command = "L"
        elif test > 0:
            command = "R"
        else:
            command = "Z"


def verif_dir(x):
    global command
    test = x - 320
    if test < 30 and test > -30:
        command = "F"
    else:
        if test < 0:
            command = "L"
        elif test > 0:
            command = "R"
        else:
            command = "Z"

def detect_red_for_balls(image,cap):

    lower_red = np.array([0, 50, 0])
    upper_red = np.array([175, 255, 200])
    mask_red = cv2.inRange(image, lower_red, upper_red)
    kernel = np.ones((3, 3), np.uint8)
    mask_red = cv2.erode(mask_red, kernel)
    mask_red = cv2.erode(mask_red, kernel)
    mask_red = cv2.erode(mask_red, kernel)
    mask_red = cv2.erode(mask_red, kernel)
    mask_red = cv2.dilate(mask_red, kernel)
    mask_red = cv2.dilate(mask_red, kernel)
    mask_red = cv2.dilate(mask_red, kernel)
    mask_red = cv2.dilate(mask_red, kernel)
    if not cv2.countNonZero(mask_red):
        return 'no red', False
    if image is not None:
        contours, ret = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 100:
                cv2.rectangle(cap, (x, y), (x + w, y + h), (255, 0, 0), 2)
                return 'red detected', x + (w / 2), y + h, cap
        else:
            return 'problem', False

    else:
        return 'problem', False

detected_state_gray = False
detected_state_red = False 
def detect_red_for_green(image):
    global detected_state_red
    global detected_state_gray
    lower_red = np.array([0, 50, 0])
    upper_red = np.array([175, 255, 200])
    if image is not None:
        mask_gray = cv2.inRange(image, lower_red, upper_red)
        kernel = np.ones((2, 2), np.uint8)
        mask_red = cv2.erode(mask_gray, kernel)
        mask_red = cv2.erode(mask_gray, kernel)
        mask_red = cv2.erode(mask_gray, kernel)
        mask_red = cv2.dilate(mask_gray, kernel)
        mask_red = cv2.dilate(mask_gray, kernel)
        mask_red = cv2.dilate(mask_gray, kernel)
        contours, ret = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w>200:
                detected_state_red = True
    
def detect_green_for_balls(image):
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
        return 'no green detected', False
    if image is not None:
        contours, ret = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #counter = 0
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 100:

                # if counter >1:
                #     return 'stop',False
                return 'green detected', x + (w / 2), y + h
        else:
            return 'problem', False
    else:
        return 'problem', False
    
def detect_black_for_green(image):
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([179, 255, 85])  # 30-->50
    if image is not None and image.shape[1] > 15 and image.shape[0] > 15:
        mask_black = cv2.inRange(image, lower_black, upper_black)
        kernel = np.ones((2, 2), np.uint8)
        mask_black = cv2.erode(mask_black, kernel)
        mask_black = cv2.dilate(mask_black, kernel)
        if np.mean(mask_black) > 40:
            return True
        else:
            return False
    else:
        return False

def FindUpOrLeft_for_green(image, x, y):
    image1 = image[y - 25:y - 5, x+20:x + 40, :]
    image2 = image[y+20:y+40, x-25:x-5, :]
    return detect_black_for_green(image1), detect_black_for_green(image2)

def robot_decision_for_green(cap,image):
    lower_green = np.array([35, 40, 50])
    upper_green = np.array([110, 255, 200])
    mask_green = cv2.inRange(image.copy(), lower_green, upper_green)

    kernel = np.ones((2, 2), np.uint8)
    mask_green = cv2.erode(mask_green, kernel)
    mask_green = cv2.dilate(mask_green, kernel)

    cv2.rectangle(cap, (50, 50), (590, 430), (0, 0, 255), 2)
    if cv2.countNonZero(mask_green):
        contours, ret = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        new_contours = []
        for contour in contours:
            x,y,w,l = cv2.boundingRect(contour)
            if w > 95 and l>95  and y<590:
                dimensions = cv2.boundingRect(contour)
                new_contours.append(dimensions)
                x,y,w,h = dimensions
                cv2.rectangle(cap, (x, y), (x + w, y + h), (255, 0, 0), 2)
        up_left = []
        for contour in new_contours:
            x, y, _, _ = contour
            up_left.append(FindUpOrLeft_for_green(image, x, y))
        counter = 0
        for i in up_left:
            up,_ = i
            if up == 1:
                counter+=1
        if counter == 2:
            return "T",cap
        elif counter == 0 and up_left :
            return "F",cap
        else:
            for i in up_left:
                up, left = i
                if up == 1:
                    if left == 1:
                        return "R",cap
                    else: return "L",cap
    return "X",cap
reverse = False
prevdecision = "new"
t_time = time.time()
turn_counter = 0
turn_state = False
def green_part():
    global turn_state
    global turn_counter
    global t_time
    global prevdecision
    global reverse
    global detect_red_for_balls
    decision,cap = robot_decision_for_green(cap_hsv,cap_hsv)
    # print(decision)
    if decision != "X":
        prevdecision = decision
        t_time = time.time() 
    if decision == "T":
        turn_state = True
    if turn_state:
        turn_counter+=1
        prevdecision = "T"
    if turn_counter >20:
        turn_counter = 0
        turn_state = False
    
    try:
        if arduino.in_waiting > 0:
        data = arduino.readline(arduino.in_waiting)
            print(data)
            if data == b'o\x00':
    
                if detect_red_for_balls:
                    arduino.write("E".encode())
                    print("finish")
                print("received from green part")
                if time.time()-t_time>2.7:
                    arduino.write(decision.encode())
                    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                else:
                    arduino.write(prevdecision.encode())
                    print("send.................................",prevdecision)
            elif data == b'z\x00':
                    reverse = True
                    print("send.................................balls")
    except:
        pass


while True:
    
    ret, frame = vid.read()
    if not ret:
        break
    cap = cv2.resize(frame, (640, 480))
    cap_hsv = cv2.cvtColor(cap.copy(), cv2.COLOR_BGR2HSV)
    detect_red_for_green(cap_hsv)
    detected_state_gray = False
    if reverse:#not reverse
        green_part()
    else:
         ball_part(cap)

    if cv2.waitKey(1) == 27:
        break
try:
    arduino.close()
except:
    pass
vid.release()
cv2.destroyAllWindows()

