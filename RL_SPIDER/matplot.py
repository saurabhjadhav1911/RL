import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import queue
import serial
#import multiprocessing.Queue as Queue
import sys
print(sys.executable)
arduino=serial.Serial('com4',115200)
import queue


class ImprovedQueue(queue.Queue):
    def __init__(self, arg):
        super(ImprovedQueue, self).__init__()
        self.arg = arg

    def to_list(self):
        with self.mutex:
            return list(self.queue)
  

fig=plt.figure()

ax1=fig.add_subplot(1,1,1)
r=0.98
q=ImprovedQueue(10000)
for i in range(10000):
    q.put(r**(i))
mul=r*np.ones([10000])
x=np.linspace(0,99,num=10000)


def animate(k):
    global data,q
    ax1.clear()
    ax1.plot(x,q.to_list())

ani=animation.FuncAnimation(fig,animate,interval=17)


for i in range(100000):
    if(arduino.inWaiting()>0):
        dat=arduino.readline()
        try:
            dat=str(dat,'utf-8')
            dat=dat.replace("\r\n","")
            #data=data.replace("\r","")
            value=int(dat)
            v=q.get()
            q.put(value)
        except Exception as e:
            print(e)

plt.show()