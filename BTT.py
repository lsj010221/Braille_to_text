import cv2
import numpy as np

img = cv2.imread("data/dots1.jpg")
result = img.copy()
canny = cv2.Canny(img,50,170)
cv2.imwrite('output/canny.jpg',canny)


contours, hierarchy = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img,contours,-1,(0,255,0),2)
canvas = np.zeros(canny.shape,np.uint8)
cv2.drawContours(canvas,contours,-1,(255),2)

cv2.imwrite('output/contours.jpg',img)

contours, hierarchy = cv2.findContours(canvas,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
canvas = np.zeros(canny.shape,np.uint8)
dots = np.zeros(canny.shape,np.uint8)

for contour in contours :
    x,y,w,h = cv2.boundingRect(contour)
    if 3<w<35 and 5<h<25:
        cv2.drawContours(canvas,[contour],-1,(255),1)
        x = int(w*0.5+x)
        y = int(h*0.5+y)
        result = cv2.circle(result,(x,y),5,(0,0,255),-1)
        dots = cv2.circle(dots,(x,y),5,(255),-1)

i = 0
flag = False
row = []
while i < dots.shape[0] :
    if not flag and dots[i].sum() :
        j = i
        flag = True
    elif flag and dots[i].sum() == 0:
        row.append(int((i+j)*0.5))
        flag = False
    i += 1

i = 0
flag = False
column = []
while i < dots.shape[1] :
    if not flag and dots[:,i].sum() :
        j = i
        flag = True
    elif flag and dots[:,i].sum() == 0:
        column.append(int((i+j)*0.5))
        flag = False
    i += 1

print(row)
print(column)

for i in row :
    dots[i,:]=255
    print('row', i)
for i in column :
    dots[:,i]=255
    print('col', i)                                                     

for i in range(len(row)%3) :
    r = (row[2] - row[0])*0.5

cv2.imwrite('output/canvas.jpg',canvas)
cv2.imwrite('output/result.jpg',result)
cv2.imwrite('output/dots.jpg',dots)