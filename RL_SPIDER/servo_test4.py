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
import gym



def read_state(q,ser):

    if(ser.inWaiting()>0):
        data=ser.readline()
        try:
            data=str(data,'utf-8')
            print(data)
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




def main_render(input_memory):
    input_mem=np.array(input_memory)
    env = gym.make("Pendulum-v2")
    num_trials=10
    j=0
    sim_steps = 1000
    for i in range(num_trials):
        print('trial')
        env.reset()
        score = 0
        for step in range(sim_steps):
            env.render()
            action=0#env.action_space.sample()
            newth=input_mem[j]/100 #np.random.uniform(-3.14,3.14,1000)
            j+=1
            newthdot=0#np.random.uniform(-8,8,1000)
            new_state,reward,done,info= env.step([newth,newthdot,action])
            #new_state=new_state.reshape(dqn.ip)
            #dqn.remember(cur_state,action,[reward],new_state,done)
            if done:
                break
        print("trial number {} completed".format(i))
    #dqn.train()

def run_plot(q):
    input_memory=deque(maxlen=2000)
    for i in range(4000):
        input_memory.append(q.get())
    main_render(input_memory)

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
