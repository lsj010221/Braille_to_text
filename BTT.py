"""

read meeeeeeee!!!!!!!!!!!!!
read meeeeeeee!!!!!!!!!!!!!
read meeeeeeee!!!!!!!!!!!!!
read meeeeeeee!!!!!!!!!!!!!
read meeeeeeee!!!!!!!!!!!!!

RPI.GPIO needs admin permission
and sudo python3, python3 do not share PYTHONPATH (??? why)
so you have to install all packages to import with admin permission
its dangerous command(??) so do not test this program on your personal computer
  => sudo python3 -m pip install numpy
  => sudo python3 -m pip install opencv-python-headless (or just opencv-python)
  => sudo python3 -m pip install RPI.GPIO

also, you have to run this program with admin permission
  => sudo python3 BTT.py

do not kill this program forcibly
it cause problems with returning gpio and camera permissions

to quit this program safely
press led button while camera off

< ## debug ## > means you can delete the line
block one of them, press ctrl+shift+l, press ctrl+/
you can change mode between debugging and optimizing mode

"""

import cv2
import numpy as np
import RPi.GPIO as GPIO
from unicode import join_jamos
from braille_dict import braille_dict

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)  # led pin, connect to right line 3rd from bottom
GPIO.setup(20, GPIO.IN)   # shutter button pin, connect to right line 2nd from bottom
GPIO.setup(21, GPIO.IN)   # power control pin, connect to right line 1st from bottom

# cam = cv2.VideoCapture(0)

flag_power = False





def img_to_braille(frame = np.zeros((480,640,3),np.uint8)) :
    cv2.imwrite('output/00_frame.jpg',frame) ##debug##
    
    img = cv2.Canny(frame,50,170)
    cv2.imwrite('output/01_canny.jpg',img) ##debug##

    contours, hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    img = np.zeros((480,640),np.uint8)
    cv2.drawContours(img,contours,-1,(255),2)
    cv2.imwrite('output/02_contours.jpg',img) ##debug##

    contours, hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    dots = np.zeros((480,640),np.uint8)
    dot_list = []

    for contour in contours :
        x,y,w,h = cv2.boundingRect(contour)
        if 9<w<25 and 9<h<25:
            x = int(w*0.5+x)
            y = int(h*0.5+y)
            frame = cv2.circle(frame,(x,y),5,(0,0,255),-1) ##debug##
            dots = cv2.circle(dots,(x,y),5,(255),-1)
            dot_list.append((x,y))
    cv2.imwrite('output/03_select.jpg',frame) ##debug##

    if len(dot_list) == 0 :
        print("dot not detected") ##debug##
        return [0]
    degree = cv2.minAreaRect(np.array(dot_list))[2]
    if degree>80 :
        degree = degree-90
        dots = cv2.warpAffine(dots,cv2.getRotationMatrix2D((240,320),degree,1),(640,480))
    elif degree<10 :
        dots = cv2.warpAffine(dots,cv2.getRotationMatrix2D((240,320),degree,1),(640,480))

    flag = False
    row_pos = []
    for i in range(480) :
        if not flag and dots[i].sum() :
            j = i
            flag = True
        elif flag and dots[i].sum() == 0:
            row_pos.append(int((i+j)*0.5))
            flag = False
    flag = False
    column_pos = []
    for i in range(640) :
        if not flag and dots[:,i].sum() :
            j = i
            flag = True
        elif flag and dots[:,i].sum() == 0:
            column_pos.append(int((i+j)*0.5))
            flag = False

    if len(row_pos)==0 or len(row_pos)%3!=0 :
        print("braille maybe cropped on the border") ##debug##
        return [0]
    unit = (row_pos[2]-row_pos[0])*0.5
    column_dist = [0]*len(column_pos)
    for i in range(1,len(column_dist)) :
        column_dist[i] = (column_pos[i]-column_pos[i-1])/unit

    # left -> 0   right -> 1  / find out by backtracking
    column = [-1]*len(column_pos)
    i = 0
    while 0 <= i < len(column) :
        if column[i] < 1 :
            column[i] += 1
            if i==0 :
                i += 1
                continue
            elif column[i-1] == column[i] :
                if 2.3<column_dist[i]<=3.3 or 5.1<column_dist[i]<=6.1 or 7<column_dist[i] :
                    i += 1
                    continue
            elif not column[i] :
                if 1.4<column_dist[i]<=2.3 or 4.2<column_dist[i]<=5.1 or 7<column_dist[i] :
                    i += 1
                    continue
            elif column[i] :
                if column_dist[i]<=1.4 or 3.3<column_dist[i]<=4.2 or 6.1<column_dist[i] :
                    i += 1
                    continue
            else :
                column[i] = -1
                i -= 1
        else :
            column[i] = -1
            i -= 1
    if i == -1 :
        print("backtracking failed") ##debug##
        return [0]

    dots_line = np.zeros((480,640,3),np.uint8) ##debug##
    dots_line[row_pos,:,:] = 255 ##debug##
    dots_line[:,column_pos,:] = 255 ##debug##
    for i, x in enumerate(column_pos) : ##debug##
        if column[i] : color = (255,0,0) ##debug##
        else : color = (0,255,0) ##debug##
        for y in row_pos :  ##debug##
            if dots[y][x] : dots_line = cv2.circle(dots_line,(x,y),5,color,-1) ##debug##
    cv2.imwrite('output/04_dots.jpg',dots_line) ##debug##

    braille = []
    while len(row_pos) > 0 :
        i = 0
        while i < len(column) :
            if column_dist[i] > 4.2 : braille.append(0)
            temp = 0
            for j in range(3) :
                temp = temp * 2 + (dots[row_pos[j]][column_pos[i]]>0)
            if not column[i] and i+1 < len(column):
                if column[i+1] and column_dist[i+1]<=1.4 :
                    i += 1
                    for j in range(3) :
                        temp = temp * 2 + (dots[row_pos[j]][column_pos[i]]>0)
                else : temp *= 8
            elif not column[i] :
                temp *= 8
            i += 1
            braille.append(temp)
        braille.append(0)
        del row_pos[:3]
    
    return braille





def braille_to_text(braille = [0]) :
    i = 0
    char_pos = 3
    text = ""
    while i < len(braille) :
        cur = braille_dict.get(braille[i])
        if cur is None :
            print("cannot translate") ##debug##
            return " "

        if cur[2] == 2 and char_pos == 2 :
            cur = braille_dict.get(braille[i]*100+64)
        elif cur[2] and i+1 < len(braille):
            if braille_dict.get(braille[i]*100+braille[i+1]) is not None :
                cur = braille_dict.get(braille[i]*100+braille[i+1])
                i += 1

        if cur[1] == 1 and char_pos == 1 :
            text += 'ㅏ'
        elif cur[1] == 2 and char_pos != 1 :
            text += 'ㅇ'
        elif cur[1] == 3 and char_pos == 1 :
            text += 'ㅏ'
        elif cur[1] == 4 and char_pos == 1 :
            text += 'ㅏ'
        elif cur[1] == 5 and char_pos != 1 :
            text += 'ㅇ'
        

        text += cur[0]
        char_pos = cur[1]
        i += 1

    return join_jamos(text)





print("start")

# main
try:
    while 1:
        # button event
        if GPIO.input(21):
            if flag_power :
                cam.release()
                flag_power = False
                print("power off") ##debug##
                GPIO.output(16,0)
            else :
                cam = cv2.VideoCapture(0)
                cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                flag_power = True
                print("power on") ##debug##
                GPIO.output(16,1)
            while GPIO.input(21) : pass

        # run when power on
        if flag_power:
            GPIO.output(16,1)
            ret, frame = cam.read()
            if GPIO.input(20):
                print("capture") ##debug##
                braille = img_to_braille(frame)
                text = braille_to_text(braille)
                print(text) ##debug##
                while(GPIO.input(20)) : pass
        
        # run when power off
        elif GPIO.input(20) :
            break

# cleanup
finally:
    print("cleanup")
    if flag_power : cam.release()
    GPIO.cleanup()

print("end") 