#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git

from threading import Thread
import threading
from colorama import Fore, Back, Style
import colorama
import multiprocessing
import numpy as np
from misc import *
import time
import cv2
from collections import deque
import sys
import os
import traceback
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import tensorflow as tf
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import socket
import sys
import traceback

color = Fore.BLUE

class Agent():
    """docstring for Env"""

    def __init__(self, config, agent_obs_que, agent_reward_que,
                 agent_action_que):
        self.config = config
        self.action_space_size = self.config['Env_config']['action_space_size']
        self.state_space_size = self.config['Env_config']['Env_vector_size']
        self.sim_obs_que = agent_obs_que
        self.sim_action_que = agent_reward_que
        self.default_action = np.array(
            self.config['Env_config']['default_action'])
        self.sim_cycle_id = 0
        self.steps_per_episode=self.config['Agent_config']['steps_per_episode']
        self.sim_step=0
        self.sim_memory=deque(maxlen=self.config['Agent_config']['memory_length'])

    def run(self):

        while True:
            self.episode()

    def sim_reset(self):
    	self.sim_step=0
        self.sim_action_que.put([self.default_action, self.sim_cycle_id])
        while True:
        	try:
        		state,reward,done,id=self.sim_state_que.get()
        		if self.sim_cycle_id is id:
        			reward=0
        			done=False
        			break
        	except Exception as e:
        		print(color,e)

        return state,reward,done

    def sim_step(self,action):
        self.sim_action_que.put([action, self.sim_cycle_id])
        while True:
        	try:
        		state,reward,done,id=self.sim_state_que.get()
        		if self.sim_cycle_id is id:
        			break
        	except Exception as e:
        		print(color,e)
        return state,reward,done

    def sim_train(self):
    	pass
    def sim_episode(self):
        sim_current_state,_,done=self.sim_reset()
        for i in range(self.steps_per_episode):
        	action=self.act(sim_current_state)
        	new_state, reward, done = self.sim_step(action)
        	self.sim_memory.append([sim_current_state,action,new_state,reward,done])
        	sim_current_state=new_state
        	if done:
        		break