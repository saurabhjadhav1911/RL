import multiprocessing
import numpy as np
from misc import *
import serial
import time
import Plot
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import multiprocessing 
from collections import deque
class Consumer():
    def __init__(self):
        pass
    def consumer(self,q):
        while True:
            while q.empty() is False:
                print(q.get())
            time.sleep(0.017)


def read_state(q,ser):

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

def producer(q,config):
    ser=serial.Serial(config['Serial_config']['port'],baudrate=config['Serial_config']['baud'],timeout=config['Serial_config']['timeout'])
    time.sleep(5)
    while True:
        read_state(q,ser)
def get_value(q):
    q.put(np.random.uniform(-1,0,1000))



def run_plot(q):
    fig =plt.figure()
    ax1=fig.add_subplot(1,1,1)
    input_memory=deque(maxlen=2000)
    plt.ion()
    fig.show()
    while True:
        while q.empty() is False:
            input_memory.append(q.get())
        arr = np.random.uniform(size=(50, 50))
        plt.imshow(arr)
        plt.show()
        time.sleep(0.017)

def Main():
    qu=multiprocessing.Queue()
    qu.put(9)
    config=read_config()
    c=Consumer()
    con=multiprocessing.Process(target=run_plot,args=(qu,))
    prod=multiprocessing.Process(target=producer,args=(qu,config))
    prod.start()
    con.start()
    con.join()
    prod.join()
if __name__ == '__main__':
    Main()
