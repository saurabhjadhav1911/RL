#Test Result : +ve 

import cv2
import numpy as np
import math

img = cv2.imread('threshImage_output.png',cv2.IMREAD_COLOR)
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(imgray, (11, 11), 0)
mask = cv2.erode(blurred, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)

_, contours,_ = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
result = cv2.drawContours(img.copy(), contours, -1, (255,0,0), 3)

cOne = contours[0]
cTwo = contours[1]

momentOne = cv2.moments(cOne)
momentTwo = cv2.moments(cTwo)

cxOne = int(momentOne['m10']/momentOne['m00'])
cyOne = int(momentOne['m01']/momentOne['m00'])

cxTwo = int(momentTwo['m10']/momentTwo['m00'])
cyTwo = int(momentTwo['m01']/momentTwo['m00'])

cv2.circle(result, (cxOne, cyOne), 7, (255, 255, 255), -1)
cv2.circle(result, (cxTwo, cyTwo), 7, (255, 255, 255), -1)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(result,str(cxOne),(39,169), font, 2,(255,255,255),2, lineType =cv2.LINE_AA)
cv2.imshow('redImage',result)
cv2.imshow('original',img)
cv2.imshow('image',imgray)
cv2.waitKey(0)
cv2.destroyAllWindows()

euclidian = math.sqrt((cxTwo - cxOne)**2 + (cyTwo - cyOne)**2)
print euclidian