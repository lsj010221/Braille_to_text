import cv2
import numpy as np
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)  # led pin right line, 3rd from bottom
GPIO.setup(20, GPIO.IN)   # led pin right line, 2nd from bottom
GPIO.setup(21, GPIO.IN)   # led pin right line, 1st from bottom

cam = cv2.VideoCapture(0)

flag_power = False





def img_processing(img = np.zeros((480,640,3),np.uint8)) :
    cv2.imwrite('output/00_frame.jpg',img)
    
    img = cv2.Canny(img,50,170)
    cv2.imwrite('output/01_canny.jpg',img)

    contours, hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    img = np.zeros((480,640),np.uint8)
    cv2.drawContours(img,contours,-1,(255),2)
    cv2.imwrite('output/02_contours.jpg',img)





print("start")

try:
    while 1:
        if GPIO.input(21):
            while GPIO.input(21) : pass
            flag_power = not flag_power
            print("power state :",flag_power)
            cam = cv2.VideoCapture(0)
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if flag_power:
            GPIO.output(16,1)
            ret, frame = cam.read()
            if GPIO.input(20):
                print("capture")
                img_processing(frame)
                while(GPIO.input(20)) : pass
        else :
            GPIO.output(16,0)
            cam.release()
            if GPIO.input(20) :
                break
finally:
    print("cleanup")
    cam.release()
    GPIO.cleanup()

print("end")