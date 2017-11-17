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

def Env_process_target(recieve_que,send_que,config):
    print('Env process start')
    env=Env.Env(config)
    env.run(recieve_que,send_que)

class Process_Maneger():
    
    def __init__(self,PLOT=True,ROS=False):
        
        config=read_config()

        #initialise communicatoions between processes
        send_que=multiprocessing.Queue()
        recieve_que=multiprocessing.Queue()

        #process initialisation
        self.plot_process=multiprocessing.Process(target=plot_process_target,args=(recieve_que,send_que,config))
        self.env_process=multiprocessing.Process(target=Env_process_target,args=(recieve_que,send_que,config))


    def Main(self):

        self.env_process.start()
        self.plot_process.start()
        #con.start()
        print(self.plot_process.pid)
        print(self.env_process.pid)
        
        #prod.join()

        self.plot_process.join()
        self.env_process.join()

    def kill_all(self):
        p=multiprocessing.active_children()
        for i in p:
            print(i)
            i.terminate()
        '''
        if(self.plot_process.is_alive()):
            try:
                self.plot_process.join()
            except:
                self.plot_process.terminate()

        if(self.env_process.is_alive()):
            try:
                self.env_process.join()
            except:
                self.env_process.terminate()
        '''
        

try:
    process_maneger=Process_Maneger()
    process_maneger.Main()
    #process_maneger.kill_all()

except Exception as e:
    #process_maneger.kill_all()
    exc_traceback=traceback.format_exc()
    print(exc_traceback)
    logname=__file__.replace('.py','')
    logname+='.log'
    print("error see file {}".format(logname))
    with open(logname,"w") as f:
            f.write(str(exc_traceback))


