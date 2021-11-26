import cv2
import numpy as np

img = cv2.imread("data/dots1.jpg")
result = img.copy()
canny = cv2.Canny(img,50,170)
cv2.imwrite('output/01_canny.jpg',canny)


contours, hierarchy = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img,contours,-1,(0,255,0),2)
select = np.zeros(canny.shape,np.uint8)
cv2.drawContours(select,contours,-1,(255),2)

cv2.imwrite('output/02_contours.jpg',select)

contours, hierarchy = cv2.findContours(select,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
select = np.zeros(canny.shape,np.uint8)
dots = np.zeros(canny.shape,np.uint8)

dot_list = []

for contour in contours :
    x,y,w,h = cv2.boundingRect(contour)
    if 3<w<35 and 3<h<35:
        cv2.drawContours(select,[contour],-1,(255),1)
        x = int(w*0.5+x)
        y = int(h*0.5+y)
        result = cv2.circle(result,(x,y),5,(0,0,255),-1)
        dots = cv2.circle(dots,(x,y),5,(255),-1)
        dot_list.append((x,y))

cv2.imwrite('output/03_select.jpg',select)

degree = cv2.minAreaRect(np.array(dot_list))[2]
if degree>80 :
    degree = degree-90
    print(degree)
    h,w = dots.shape
    dots = cv2.warpAffine(dots,cv2.getRotationMatrix2D((h/2,w/2),degree,1),(w,h))
    result = cv2.warpAffine(result,cv2.getRotationMatrix2D((h/2,w/2),degree,1),(w,h))
elif degree<10 :
    print(degree)
    h,w = dots.shape
    dots = cv2.warpAffine(dots,cv2.getRotationMatrix2D((h/2,w/2),degree,1),(w,h))
    result = cv2.warpAffine(result,cv2.getRotationMatrix2D((h/2,w/2),degree,1),(w,h))
else :
    print(degree)

cv2.imwrite('output/00_frame.jpg',result)

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

dots_line = dots.copy()

for i in row :
    dots_line[i,:]=255
    print('row', i)
for i in column :
    dots_line[:,i]=255
    print('col', i)

for i in range(len(row)%3) :
    r = (row[2] - row[0])*0.5


cv2.imwrite('output/04_dots.jpg',dots_line)