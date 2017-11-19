#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL\RL_SPIDER
#https://github.com/saurabhjadhav1911/RL.git
#C:\Users\Public\RL\ABC\ABC
#C:\Users\vaibhav\Documents\Python\RL\RL_SPIDER

import multiprocessing
import numpy as np
from misc import *
import serial
import time
import Plot
import cv2
from collections import deque
import gym
import Env
import Plot
import Sim
import sys
import os
import traceback
#sys.path.append(os.path.join(os.path.dirname(__file__),'..'))





def plot_process_target(recieve_que,send_que,config):
    print('Plot process start')
    plot=Plot.Plot(size=config['GUI_config']['plot_size'])
    plot.draw(recieve_que)
    print(config['GUI_config']['plot_size'])

def reward_process_target(recieve_que,send_que,config):
    plot=Plot.Plot(size=config['GUI_config']['plot_size'])
    print(config['GUI_config']['plot_size'])

def Sim_process_target(recieve_que,send_que,config):
    sim=Sim.Sim(config)
    #sim.run(recieve_que,send_que)
    sim.generate_step(recieve_que,send_que)

def Env_process_target(recieve_que,send_que,config):
    print('Env process start')
    env=Env.Env(config)
    env.run(recieve_que,send_que)



def Main():
    multiprocessing.freeze_support()
    config=read_config()

    #initialise communicatoions between processes
    send_que=multiprocessing.Queue()
    recieve_que=multiprocessing.Queue()

    #process initialisation
    plot_process=multiprocessing.Process(target=plot_process_target,args=(recieve_que,send_que,config))
    env_process=multiprocessing.Process(target=Env_process_target,args=(recieve_que,send_que,config))
    sim_process=multiprocessing.Process(target=Sim_process_target,args=(recieve_que,send_que,config))

    env_process.start()
    plot_process.start()
    sim_process.start()
    #con.start()
    sim_process.join()
    plot_process.join()
    env_process.join()
    #prod.join()


try:

    Main()

except Exception as e:
    exc_traceback=traceback.format_exc()
    print(exc_traceback)
    logname=__file__.replace('.py','.log')
    print("error see file {}".format(logname))
    with open(logname,"w") as f:
            f.write(str(exc_traceback))


