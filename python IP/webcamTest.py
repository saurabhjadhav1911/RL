#Test Result : +ve
#Tutorial Link : https://thecodacus.com/ip-webcam-opencv-wireless-camera/#.WlMrsnWWY8o

import urllib
import cv2
import numpy as np

#remmeber to remove garbage from the end of link.

url='http://192.168.0.100:8080/shot.jpg'

while True:
    imgResp=urllib.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)

    # all the opencv processing is done here
    
    cv2.imshow('test',img)
    if ord('q')==cv2.waitKey(10):
        exit(0)
