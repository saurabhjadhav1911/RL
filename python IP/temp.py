import cv2
import numpy as np 

def cal_COM(i):
	moment = cv2.moments(i)
	x = int(moment['m10']/moment['m00'])
	y = int(moment['m01']/moment['m00'])
	return (x,y)

cap = cv2.VideoCapture('testVideo.mp4')
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)
lower_red = np.array([0,0,150])
upper_red = np.array([100,100,250])
for i in xrange(0,length):
	_, img = cap.read()

	redThresh = cv2.inRange(img,lower_red,upper_red)
	redResult = cv2.bitwise_and(img,img, mask = redThresh)
	redResult_gray = cv2.cvtColor(redResult, cv2.COLOR_BGR2GRAY)

	blurred = cv2.GaussianBlur(redResult_gray, (11, 11), 0)
	mask = cv2.erode(blurred, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	_, contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	result = cv2.drawContours(redResult, contours, -1, (255,0,0), 3)
	#print len(contours)
	l = len(contours)
	if l>0:
		sumx = 0
		sumy = 0

		for j in xrange(0,l):
			temp = contours[j]
			[i,j] = cal_COM(temp)
			sumx = sumx+i
			sumy = sumy+j
		Cx = sumx//l
		Cy = sumy//l
		print(Cy,Cx)

	cv2.imshow('original',img)
	#cv2.imshow('RED',redThresh)
	cv2.imshow('RED - 2',redResult)
	#cv2.imshow('RED - mask',mask)
	cv2.imshow('Contours', result)

	if ord('q')==cv2.waitKey(10):
		break

cap.release()
cv2.destroyAllWindows()