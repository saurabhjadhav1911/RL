import cv2
import numpy as np
cap = cv2.VideoCapture(0)

while True:
    if cap.grab():
        flag, frame = cap.retrieve()
        lower = np.array([50,50,175])
        upper= np.array([150,150,255])

        mask = cv2.inRange(frame, lower, upper)

        res = cv2.bitwise_and(frame,frame, mask= mask)

        if not flag:
            continue
        else:
            cv2.imshow('video', res)
    if cv2.waitKey(10) == 27:
        break
cv2.destroyAllWindows()
