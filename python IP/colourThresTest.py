#Test Result : +ve for image, vido not attempted
import cv2
import numpy as np

##############################
#set Threshold values
#############################
greenThresh_value = np.array(100, dtype=np.uint8)
redThresh_value = np.array(100, dtype=np.uint8)

# #############################
# #Read test Image
# ############################
img = cv2.imread('testImage.png',cv2.IMREAD_COLOR)

# ###Split image into Green and Red
greenImage = img[:,:,2]
redImage = img[:,:,1]

# #############################
# #Processing
############################

#Thresholding
ret,greenThresh = cv2.threshold(greenImage,greenThresh_value,255,cv2.THRESH_BINARY_INV)
ret,redThresh = cv2.threshold(redImage,redThresh_value,255,cv2.THRESH_BINARY_INV)

#Logical operation
greenResult = cv2.bitwise_and(img,img, mask = greenThresh)
redResult = cv2.bitwise_and(img,img, mask = redThresh)
result = cv2.bitwise_xor(greenResult,redResult)


###########################
#Display
##########################

cv2.imshow('hu',result)

cv2.waitKey(0)
cv2.destroyAllWindows()