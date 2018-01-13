import math
import cv2
import numpy as np 
import urllib

##############################
#set Threshold values
#############################
greenThresh_value = np.array(100, dtype=np.uint8)
redThresh_value = np.array(100, dtype=np.uint8)


############################
#Functions
############################
def cal_distance(a1,a2):
	[x1,y1] = a1
	[x2,y2] = a2
	return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def cal_COM(i):
	moment = cv2.moments(i)
	x = int(moment['m10']/moment['m00'])
	y = int(moment['m01']/moment['m00'])
	return [x,y]

def get_threshImage(img):
	greenImage = img[:,:,2]
	redImage = img[:,:,1]
#Thresholding
	_,greenThresh = cv2.threshold(greenImage,greenThresh_value,255,cv2.THRESH_BINARY_INV)
	_,redThresh = cv2.threshold(redImage,redThresh_value,255,cv2.THRESH_BINARY_INV)
#Logical operation
	greenResult = cv2.bitwise_and(img,img, mask = greenThresh)
	redResult = cv2.bitwise_and(img,img, mask = redThresh)
	mergeResult = cv2.bitwise_xor(greenResult,redResult)

	return mergeResult

def detect_circles(img):	
	imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(imgray, (11, 11), 0)
	mask = cv2.erode(blurred, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	_, contours,_ = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	result = cv2.drawContours(img.copy(), contours, -1, (255,0,0), 3)
	##check for contour list
	euclidian =cal_distance(cal_COM(contours[0]),cal_COM(contours[1]))
	
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(result,str(euclidian),(39,169), font, 2,(255,255,255),2, lineType =cv2.LINE_AA)

	cv2.imshow('Live', result)
	return euclidian

def main():
	#remmeber to remove garbage from the end of link.

	cam = cv2.VideoCapture(1)

	while True:
		_, img = cam.read()
	
		cv2.imshow('ha',img)
		#distance  = detect_circles(img)
		if ord('q')==cv2.waitKey(10):
			break

	cv2.destroyAllWindows()
main()