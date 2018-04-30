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
#from keras.models import Sequential
#from keras.layers import Dense
#from keras.layers import LSTM
#import tensorflow as tf
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import socket
import sys
import traceback
import random
from copy import deepcopy
import Crawler


color = Fore.MAGENTA
colorama.init()

N=0
E=1
S=2
W=3
exit=1
dir=['N','E','S','W']


class RL_Crawler():
    """


    """
    def __init__(self,config,height=None,width=None,goal=None,nogoal=None,start=None,obstacles=None):
        
        #initialise cordinates and maze parameters
        self.config = config
        self.height=height or 10
        self.width= width or 10
        self.obstacles=obstacles or [[self.height+1,self.width+1]]
        self.start=[0,0]
        self.pos=self.start

        self.crawler = Crawler.Crawler(config=self.config)
        self.prev_pos=None
        self.actions=[0,1,2,3]
        self.neighbours=[[-1,0],[0,1],[1,0],[0,-1]]
        #self.move=np.array([[0,0,1],[1,0,0],[0,1,1],[1,1,0],[1,1,2],[2,1,1],[1,2,2],[2,2,1],[2,2,3],[3,2,2],[2,3,3],[3,3,2],[3,3,0],[0,3,3],[3,0,0],[0,0,3]])
        #learning parameters
        self.movement_cost=-1
        self.alpha=0.8
        self.gamma=0.9
        self.epsilon=0.1
        self.last_reward=0
        e=5
        
        #learning variables
        self.policy=""
        self.maxpolicy=""
        self.total_reward=-100
        self.iteration=1
        self.best=[""]
        self.epoch_num=1
        self.move_reward=0
        self.exit=1
        self.reached=np.zeros([self.height,self.width])
        self.Q=np.zeros((self.height,self.width,len(self.actions)),dtype=np.float32)
        self.load_Q()
        self.last_reward

        self.action_min_limit = np.array(
            self.config['Agent_config']['action_min_limit'])
        self.action_max_limit = np.array(
            self.config['Agent_config']['action_max_limit'])
        self.angle_min_limit = np.array(
            self.config['Agent_config']['action_min_limit'])
        self.angle_max_limit = np.array(
            self.config['Agent_config']['action_max_limit'])
        
        self.maxr=self.config['Agent_config']['Q_max_reward']
        self.num_states_per_angle = 10
        self.angle=0
        #image parameters
        self.pixelpercell=80
        self.pause=10
        self.img = np.zeros([self.pixelpercell*self.height,self.pixelpercell*self.width,3], np.uint8)
        self.img=self.generate_background()

    def load_Q(self):
        try:
            Q = np.load("Models/Crawler_Q_Agent_isolated_" + str(
                self.config['Agent_config']['saved_Q_index']) + ".npy")
            self.Q = Q
            print(color, 'Q values loaded ')
        except Exception as e:
            print(color, 'Q values not loaded due to {}'.format(e))

    def save_Q(self):
        np.save("Models/Crawler_Q_Agent_isolated_" +
                str(self.config['Agent_config']['saved_Q_index']) + ".npy",
                self.Q)
        print(color, 'Q values saved')

    def generate_background(self):
        self.img[:,:,:]=255
        c=self.img.shape[0]
        
        for i in range(1,self.height):
            a=int(c*i/self.height)
            cv2.line(self.img,(0,a),(self.img.shape[1],a),[0,0,0],2)
        c=self.img.shape[1]
        for i in range(1,self.width):
            a=int(c*i/self.width)
            cv2.line(self.img,(a,0),(a,self.img.shape[0]),[0,0,0],2)

        cv2.imshow('Environment',self.img)
        return self.img

    def getQ(self,state,action):
        return self.Q[state[0],state[1],action]

    def putQ(self,state,action,q):
        self.Q[state[0],state[1],action]=q

    def action(self, state):
        if random.random() < self.epsilon:
            action = random.choice(self.actions)
            #print("randomaction",action)
        else:
            q = [self.getQ(state, a) for a in self.actions]
            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(self.actions)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)

            action = self.actions[i]
            #print("best action",action)
        return action

    def render(self):
        self.env=self.generate_background()
        a=self.pixelpercell*self.pos[0]
        c=self.pixelpercell*(self.pos[0]+1)
        b=self.pixelpercell*self.pos[1]
        d=self.pixelpercell*(self.pos[1]+1)
        cv2.rectangle(self.env,(b+20,a+20),(d-20,c-20),[255,255,0], thickness=-1)
        for i in range(self.height):
            for j in range(self.width):
                c=self.pixelpercell*(i+0.54)
                d=self.pixelpercell*(j+0.28)
                for ac in self.actions:
                    a=c+self.pixelpercell*0.225*self.neighbours[ac][0]
                    b=d+self.pixelpercell*0.225*self.neighbours[ac][1]
                    cv2.putText( self.env,str(int(10000*self.Q[i][j][ac])/100.0)[0:-1],(int(b),int(a)),   cv2.FONT_HERSHEY_PLAIN, 0.8,(0, 0, 0), 1 )

        cv2.imshow('Environment',self.env)
        #cv2.imwrite("{}E{},jpg".format(self.epoch_num,self.cycle_num),self.env)
        cv2.waitKey(self.pause)

    def state_to_angle(self,val):
        #print("state_to_angle",val,self.action_min_limit)
        return (np.array(val)*20)+self.action_min_limit

    def angle_to_state(self,val):
        #print("angle_to_state",val,self.action_min_limit)
        return list(map(int,(val-self.action_min_limit+10)/20))

    def MoveDir(self,state,action):

        act=np.clip(np.array(state)+np.array(self.neighbours[action]),0,9)
        action_angles=self.state_to_angle(act)
        angles,reward=self.crawler.isolated_step(action_angles)
        #self.angle+=1
        #angles,reward=self.crawler.isolated_step([self.angle,self.angle])
        #print(self.angle)
        state=self.angle_to_state(angles)
        move_reward=(reward-self.last_reward+self.movement_cost)
        #print("reward",reward,self.last_reward,move_reward)
        self.last_reward=reward
        return exit,state,move_reward

    def Movec(self,state,act):
        c=""
        exit,state,move_reward=self.MoveDir(state,act)
        c+=str(dir[act])
        self.policy+=c
        self.policy+='|'
        return exit,state,move_reward


    def learn(self):
        ne=0
        while(1):
            self.Epoch()
            self.render()
            ne+=1
            #print("total reward",self.total_reward)
            self.epoch_num+=1
            if ((self.total_reward) >= self.maxr):
                self.maxr=self.total_reward
                self.save_Q()
                self.config['Agent_config']['Q_max_reward']=self.maxr
                save_config(self.config, 'config_crawler_isolated.json')
                print("Epoch {} with max rewdrd={} and policy = {}".format(self.epoch_num,maxr,self.policy))

    def Epoch(self):
        self.reset()
        self.exit=1
        n=0
        self.policy=""
        self.cycle_num=0
        while(self.exit==1):
            self.prev_pos=deepcopy(self.pos)
            n+=1
            act=self.action(self.pos)
            Q=self.getQ([self.prev_pos[0],self.prev_pos[1]],act)
            self.exit,pos,self.move_reward=self.Movec(self.pos,act)
            self.total_reward+=self.move_reward
            self.render()
            q = [self.getQ(pos, a) for a in self.actions]
            maxQ = max(q)
            #print(maxQ)
            Q=Q+self.alpha*(self.move_reward+(self.gamma*maxQ)-Q)
            self.putQ([self.prev_pos[0],self.prev_pos[1]],act,Q)
            self.pos=pos
            self.cycle_num+=1
            if n>200:
                self.exit=0
        #print("total reward",self.total_reward)
        return self.exit

    def reset(self):
        self.total_reward=0
        #print(self.pos)
        self.pos=[self.start[0],self.start[1]]
        action_angles=self.state_to_angle(self.pos)
        angles,reward=self.crawler.isolated_reset(action_angles)
        state=self.angle_to_state(angles)
        #print(self.policy)
        self.render()
        print("reset")
        self.reached=np.zeros([self.height,self.width])
        self.exit=1

########   Simple Default Maze  ########
def main3():
    config = read_config('config_crawler_isolated.json')
    config['GUI_config']['render_flag']=True
    config = arg_parser(config)
    save_config(config, 'config_crawler_isolated.json')
    rl=RL_Crawler(config)

    ########   Custom Maze  ########
    #rl=RLMaze(height=6,width=8,goal=[0,7],nogoal=[1,7],start=[5,0],obstacles=[[1,1],[2,3],[4,5]])
    #print(rl.state_to_angle([5,5]))
    #print(rl.angle_to_state([90,-90]))
    rl.learn()

if __name__ == '__main__':
    main3()
