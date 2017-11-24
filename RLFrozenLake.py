#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#sj
import numpy as np
import random
from copy import deepcopy
import cv2
import gym

Left=0
Down=1
Right=2
Up=3

class RLFrozenLake():
    """docstring for RLFrozenLake"""
    def __init__(self):
        self.env= gym.make('FrozenLake-v0')
        self.actions=[Left,Down,Right,Up]
        self.action_name=['Left','Down','Right','Up']

        self.alpha=0.8
        self.gamma=0.9
        self.epsilon=0.1
        
        #(self.env.action_space.n)
        self.total_reward=0
        self.Q=np.zeros((self.env.observation_space.n,self.env.action_space.n))
        #self.maze_size=env.reset()
        self.pos=0

    def generate_background(self):
        self.img[:,:,:]=255
        c=self.img.shape[0]
        
        for i in xrange(1,self.maze.shape[0]):
            a=c*i/self.maze.shape[0]
            cv2.line(self.img,(0,a),(self.img.shape[1],a),[0,0,0],2)
        c=self.img.shape[1]
        for i in xrange(1,self.maze.shape[1]):
            a=c*i/self.maze.shape[1]
            cv2.line(self.img,(a,0),(a,self.img.shape[0]),[0,0,0],2)
        for i in xrange(self.maze.shape[0]):
            for j in xrange(self.maze.shape[1]):
                spl=False
                if [i,j]==self.goal:
                    color=[0,255,0]
                    spl=True
                elif [i,j]==self.nogoal:
                    color=[0,0,255]
                    spl=True
                if [i,j] in self.obstacles:
                    color=[255,0,0]
                    spl=True
                if spl:
                    a=self.pixelpercell*i
                    c=self.pixelpercell*(i+1)
                    b=self.pixelpercell*j
                    d=self.pixelpercell*(j+1)
                    cv2.rectangle(self.img,(b,a),(d,c),color, thickness=-1)
                    #print(a,b,c,d)

        cv2.imshow('Environment',self.img)
        return self.img

    def choose_action(self, state):

        if random.random() < self.epsilon:
            action = random.choice(self.actions)
            #print("randomaction",action)
        else:
            q = [self.Q[state, a] for a in self.actions]
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

    def Epoch(self):

        self.env.reset()
        #self.env.render()
        self.policy=""
        done=False
        self.total_reward=0
        while(done is False):

            self.prev_pos=deepcopy(self.pos)
            act=self.choose_action(self.pos)

            observation, reward, done, info = self.env.step(act)
            #self.env.render()
            self.beter_render()
            if reward<0:
                print('reward gone negative{}'.format(reward))
            Q=self.Q[self.prev_pos,act]
            q = [self.Q[observation, a] for a in self.actions]
            maxQ = max(q)
            Q=Q+self.alpha*(reward+(self.gamma*maxQ)-Q)
            self.Q[self.prev_pos,act]=Q

            self.pos=observation
            self.total_reward+=reward
            self.policy+=self.action_name[act]
            self.policy+='|'

        return exit

    def Run(self):
        maxr=self.total_reward
        while(1):
            self.Epoch()
            self.generateImg()
            #print("total reward",self.total_reward)
            if ((self.total_reward) >= maxr):
                maxr=self.total_reward
                print("maxr",maxr)
                print("success with max rewdrd and policy",self.policy)

def main():
    FL=RLFrozenLake()
    FL.Run()

if __name__ == '__main__':
    main()
