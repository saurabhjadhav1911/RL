from __future__ import print_function

try:
    import __builtin__
except ImportError:
    # Python 3
    import builtins as __builtin__

def print(color,*args, **kwargs):
    __builtin__.print(color,color)
    return __builtin__.print(color,*args, **kwargs)

from colorama import Fore, Back, Style
import colorama
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#from matplotlib import style
import numpy as np
import cv2
#import gym
import multiprocessing 
from collections import deque
import time

color=Fore.MAGENTA

class Plot():
    """docstring for Plotter"""
    def __init__(self,size=None,font_color=None):
        global color
        color= font_color or color
        self.size=[700,1300] or size
        self.mem=deque(maxlen=self.size[1])
        #self.mem=deque(maxlen=self.size[1])
        self.interval = 1.0/60.0
        #self.fig = plt.gcf()
        #self.fig.show()
        #self.fig.canvas.draw
        last_time=time.clock()

        
    def render_cv(self):
        #mm=np.array(mem)
        n=0
        img=255*np.ones((self.size),dtype=np.uint8)
        for e in self.mem:
            y=np.clip(int(self.size[0]-e),0,self.size[0]-1)
            img[y,n]=0
            n+=1
        cv2.imshow('window',img)
        cv2.waitKey(1)
        #plt.imshow(img)

    def render_matplot(self):
        #mm=np.array(mem)
        n=0
        for e in self.mem:
            y=np.clip(int(self.size[0]-e),0,self.size[0]-1)
            img[y,n]=0
            n+=1
        #cv2.imshow('window',img)
        cv2.waitKey(1)
        #plt.imshow(img)
    def render_gym(self,y):
        n=0
        img=255*np.ones((self.size),dtype=np.uint8)
        y=(y-125)*0.008159981
        cv2.circle(img,(int(300+200*np.sin(y)),int(300+200*np.cos(y))),20,(0),-1)
        cv2.imshow('window',img)
        cv2.waitKey(1)

    def render_sim(self,y,yt):
        img=255*np.ones((self.size),dtype=np.uint8)
        y=(y-125)*np.pi/180
        yt=(yt-125)*np.pi/180#*0.008159981
        cv2.circle(img,(int(300+200*np.sin(y)),int(300+200*np.cos(y))),20,(0),-1)
        cv2.circle(img,(int(800+200*np.sin(yt)),int(300+200*np.cos(yt))),20,(0),-1)
        cv2.imshow('window',img)
        cv2.waitKey(1)

    def draw(self,q):
        previousTime = time.clock()
        #plt.ion()
        last_time=time.clock()
        nt=0
        pn=0
        y=0.0
        while(True):
            while (q.empty() or ((time.clock()- previousTime) > self.interval))  is False:
                y=q.get()
                self.mem.append(y)
                nt+=1

            #self.render_gym()
            #self.render_matplot()
            #self.render_cv()
            self.render_sim(y,y)
            
            fps=1.0/(time.clock()-last_time)
            print(color,"loop running on {} fps with {} recieve speed".format(fps,(nt-pn)*fps))
            pn=nt
            last_time=time.clock()
            previousTime = time.clock()
        cv2.destroAllWindows()

if __name__ == '__main__':
	plot=Plot()
	r=0.98
	for i in range(720):
		plot.input_memory.append(r**(i))
	
