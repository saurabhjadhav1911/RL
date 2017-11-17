import multiprocessing
import numpy as np
from misc import *
import serial
import time
value=None


class Consumer():
    def __init__(self):
        pass
    def consumer(self,q):
        while True:
            while q.empty() is False:
                print(q.get())
                

class Env():
    """docstring for Env"""
    
    def __init__(self,config):
        print('Env created')
        self.config=config
        #self.serial=self.get_Serial()
        #self.default_action=config['Env_config']['default_action']
    '''
    def get_Serial(self):
        return serial.Serial(self.config['Serial_config']['port'],baudrate=self.config['Serial_config']['baud'],timeout=self.config['Serial_config']['timeout'])
    '''
    def reset(self):
        self.action(self.default_action)
        return self.read_state()

    def action(self,act):
        line="G "+" ".join(map(str,act))
        print(line)
        #self.serial.write(line)
    def read_state(self,q):
        if(self.ser.inWaiting()>0):
            data=self.ser.readline()
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

        return value

    def run(self,q):
        ser=serial.Serial(config['Serial_config']['port'],baudrate=config['Serial_config']['baud'],timeout=config['Serial_config']['timeout'])
        while True:
            self.read_state(q)
            
    def producer(self,q):
        for i in range(100):
            self.get_value(q)
    def get_value(self,q):
        q.put(np.random.uniform(-1,0,1000))

      
def Main():
    qu=multiprocessing.Queue()
    qu.put(9)
    config=read_config()
    env=Env(config)
    C=Consumer()
    con=multiprocessing.Process(target=C.consumer,args=(qu,))
    prod=multiprocessing.Process(target=env.run,args=(qu,))
    con.start()
    prod.start()

    con.join()
    prod.join()
if __name__ == '__main__':
    Main()
