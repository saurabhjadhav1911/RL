import cv2
import numpy as np 
import time

def get_COM (c):
		M = cv2.moments(c)
		if not(M["m00"] == 0):
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			return cX,cY
		else:
			return None
cam = cv2.VideoCapture(0)
#fourcc = cv2.VideoWriter_fourcc(*'XVID')+
#out = cv2.VideoWriter('./EpisodeVideos/output.avi',fourcc, 10.0, (640,480))
#cam = cv2.VideoCapture('testVedio.mp4')
#l= int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
#for i in xrange(0,l):
#last_time=0
while True:

	_,img  = cam.read()
	upper_thres = np.array([95,95,250])
	lower_thresh = np.array([40,20,120])
	mask = cv2.inRange(img, lower_thresh,upper_thres)

	mask_blur = cv2.GaussianBlur(mask, (9, 9), 0)
	mask2 = cv2.erode(mask_blur, None, iterations=2)
	mask2 = cv2.dilate(mask2, None, iterations=2)

	mask_color = cv2.bitwise_and(img,img,mask = mask)

	final_gray = cv2.cvtColor(mask_color, cv2.COLOR_BGR2GRAY)

	_, contours, _ = cv2.findContours(final_gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(mask_color, contours, -1, (255,0,0), 3)

	for j in xrange(0,len(contours)):

		c = contours[j]
		t = get_COM(c)
		if not(t ==None):
			x,y = t
			cv2.circle(mask_color, (x, y), 2, (255, 255, 255), -1)

	#out.write(img)
	#print("loop running of {} fps".format(1/(time.time()-last_time)))
	#last_time=time.time()
	cv2.imshow('redMask',mask_color)
	cv2.imshow('original',img)
	#cv2.imshow('mask',mask)
	#cv2.imshow('final',final_gray)
	if cv2.waitKey(10) == 27:
		break
def getreward():

	dpos=pos-start_pos
	distance=dir_unit_vector*dpos
	return distance
def reset():
	pass

cam.release()
#out.release()
cv2.destroyAllWindows()