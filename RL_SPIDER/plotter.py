import multiprocessing
import cv2
import numpy as np
import time
from misc import *
import serial

from collections import deque

class Plotter():
    """docstring for Plotter"""
    def __init__(self,size=None):
        self.size=[480,1080] or size
        self.back_image=255*np.ones((self.size),dtype=np.uint8)
        self.mem=deque(maxlen=self.size[1])


    def render(self,mem,size,back_image):
        #mm=np.array(mem)
        img=255*np.ones((self.size),dtype=np.uint8)
        n=0
        for e in mem:
            y=np.clip(int(size[0]-40-2*e),0,size[0]-1)
            img[y,n]=0
            n+=1
        cv2.imshow('window',img)
        cv2.waitKey(1)
    def add_elements(self,q,mem,back_image,size):
        previousTime = time.clock()
        interval = 1.0/60.0
        while(True):
            while (q.empty() or ((time.clock()- previousTime) > interval))  is False:
                mem.append(q.get())
            self.render(mem,size, back_image)
            previousTime = time.clock()

def get_value(q):
    while True:
        q.put(np.random.uniform(40,440))
        time.sleep(0.001)
def read_write_state(q,ser,r):
    flag=False
    while r.empty() is False:
        flag=True
        arr=str(r.get())
        arr+="\n"
        ser.write(arr.encode())

    if(ser.inWaiting()>0):
        data=ser.readline()
        try:
            data=str(data,'utf-8')
            data=data.replace("\r\n","")
            #data=data.replace("\r","")
            #data=data.split()
            
            value=int(data)
            
            q.put(value)
            #p.send(value)

        except Exception as e:
            print(e)

def producer(q,r,config):
    ser=serial.Serial(config['Serial_config']['port'],baudrate=config['Serial_config']['baud'],timeout=config['Serial_config']['timeout'])
    time.sleep(5)
    while True:
        read_write_state(q,ser,r)
def generator(r):
    val=0
    while True:
        r.put(val)
        val=180-val
        time.sleep(2)
if __name__ == '__main__':
    plot=Plotter()
    q=multiprocessing.Queue()
    r=multiprocessing.Queue()
    config=read_config()
    process=multiprocessing.Process(target= plot.add_elements,args=(q,plot.mem,plot.back_image, plot.size))
    process2 =multiprocessing.Process(target=producer,args=(q,r,config))
    process3 =multiprocessing.Process(target=generator,args=(r,))

    process.start()
    process2.start()
    process3.start()
    process.join()
    process3.join()
    process2.join()
    
    cv2.destroyAllWindows()



        
