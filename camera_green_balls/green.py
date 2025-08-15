import cv2
import numpy as np
import os
import serial
import time

# arduino = serial.Serial(port='/dev/ttyACM0',baudrate=9600,timeout=0.01)
time.sleep(2)

def carp_part(image,x,y):
    return image[y:y+20,x:x+20,:]


def detect_black(image):
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([179, 255, 85])#30-->50

    
    if image is not None and image.shape[1] == 20 and image.shape[0] == 20:
        mask_black = cv2.inRange(image, lower_black, upper_black)
        # print(image[0,0,:])#,'---',image[,240,:])
        if np.mean(mask_black) > 150:
            return True
        else: return False
    else: return False

def detect_green(image):
    lower_green = np.array([35, 40, 50])
    upper_green = np.array([90, 255, 200])

    # print(image[240,320,:])#,'---',image[,240,:])


    # print(image[320,240,:])
    mask_green = cv2.inRange(image, lower_green, upper_green) 
    kernel = np.ones((2, 2), np.uint8)  
    mask_green = cv2.erode(mask_green, kernel) 
    mask_green = cv2.dilate(mask_green, kernel)
    if not cv2.countNonZero(mask_green):
        return 'no green',False
    if image is not None:
        contours, ret = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        counter = 0
        for contour in contours:
            _, _, w, _ = cv2.boundingRect(contour)
            if w>30:
                counter+=1

        # if ret.shape[1] == 2:
        #     return 'stop',False
        if ret.shape[1]:
            
            x_pos, y_pos,w,h = cv2.boundingRect(contours[0])
            # if(w>90):
                # print(image[240,320,:])#,'---',image[,240,:])

            # Black bounding box

            if counter >1:
                return 'stop',False
            elif w>50 and y_pos>50 and y_pos<350:
                return 'green detected',x_pos,y_pos,w,h
            else: return 'problem',False
        else: return 'problem',False

    else: return 'problem',False

def robot_decision(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    image = cv2.resize(image,(640,480))
    localisation_result = detect_green(image)

    result = ''
    if localisation_result[0] == 'no green':
        result = '-'
    elif localisation_result[0] == 'stop':
        result ='s'
    elif localisation_result[0] == 'problem':
        result ='-'
    else:
        _,x, y,w,h = localisation_result
        x_right = x+w+5 
        y_right = y+(h//2)-10
        x_up = x
        y_up = y-25
        if image is not None:
            if not detect_black(carp_part(image.copy(),x_up,y_up)):

                result = 'f'
            elif detect_black(carp_part(image.copy(),x_right,y_right)):
                result = 'l'
            else: result = 'r'
        else: result = '-'
    return result



# for filename in os.listdir():
#     if filename.endswith('.png'):
#         print(filename)
#         cap = cv2.resize(cv2.imread(filename),(640,480))
#         if(detect_green(cv2.cvtColor(cap.copy(),cv2.COLOR_BGR2HSV))[0] == 'green detected'):
#             _,x,y,w,h = detect_green(cv2.cvtColor(cap.copy(),cv2.COLOR_BGR2HSV))
#             cv2.rectangle(cap, (x, y), (x + w, y + h), (255, 0, 0), 2)

#         # cv2.putText(cap, robot_decision(cap), (30,30), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 2)

#         cv2.imshow('Green Detection', cap)
#         cv2.waitKey(0)
# cv2.destroyAllWindows()

prevtest = "hello"
vid = cv2.VideoCapture(2)
while True:
    ret,frame = vid.read()
    cap = cv2.resize(frame,(640,480))
    cap_hsv = cv2.cvtColor(cap.copy(),cv2.COLOR_BGR2HSV)
    if(detect_green(cap_hsv)[0] == 'green detected'):
        _,x,y,w,h = detect_green(cap_hsv)
        cv2.rectangle(cap, (x, y), (x + w, y + h), (255, 0, 0), 2)
    # print(cap_hsv[240,320,:])
    cv2.circle(cap, (320, 240), 2, (0,0,255), 1)
    test = robot_decision(cap)
    
    if test != '-' and prevtest != test:
        print(test)
        # arduino.write(test.encode('utf-8'))
        prevtest = test
        # arduino.flush()




    # if arduino.in_waiting > 0:
    #     # Read the incoming data
    #     data = arduino.readline(arduino.in_waiting)
    #     print(data)
        
    #     # Check if the received message is "ok"
    #     if data == b'o\x00':
    #         print("good")
    #         arduino.write(prevtest.encode())

        
        



    # a = arduino.readline().decode().strip()
    # print(a)
    # prevtest = "aaa"
    # if a == b'ok\r':
    #     # print('abdou')
    #     arduino.write(prevtest.encode('utf-8'))
    


    # cv2.putText(cap, robot_decision(cap), (30,30), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 2)
    # print(detect_black(cv2.cvtColor(cap.copy(),cv2.COLOR_BGR2HSV)))
    cv2.imshow('Green Detection', cap)
    if cv2.waitKey(1) == 27:
        break
# arduino.close()
cap.release()
cv2.destroyAllWindows()
