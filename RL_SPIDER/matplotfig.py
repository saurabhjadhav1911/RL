import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import cv2
import multiprocessing 
from collections import deque
import time


mem=deque(maxlen=1080)
def render_matplot(self):
    #mm=np.array(mem)
    pass
    #plt.imshow(img)
def main():
    
    fig = plt.gcf()
    fig.show()
    fig.canvas.draw()
    data = [[i for i in range(100)]]
    data = np.array(data, dtype=float)/10.0

    target = deque(maxlen=100)
    for i in range(100):
        target.append(np.sin(i/10))

    data = data.reshape((1, 1, 100))
    last_time=time.clock()
    for i in range(30):
        plt.gcf().clear()
        target.append(np.sin((100+i)/10.0))
        #plt.plot(data[0,0,:],target)
        fig.canvas.draw()
        print("loop running on {} fps".format(1.0/(time.clock()-last_time)))
        last_time=time.clock()

if __name__ == '__main__':
    main()