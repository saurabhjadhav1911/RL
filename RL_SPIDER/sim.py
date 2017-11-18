#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git

import multiprocessing
import numpy as np
from misc import *
import time
import cv2
from collections import deque
import sys
import os
import traceback

class Sim():
	"""docstring for Env"""
	def __init__(self,config):
		print('Sim created')
		self.output_mem=deque(maxlen=1000)

	def render_sim(self,y,yt):
        img=255*np.ones((self.size),dtype=np.uint8)
        y=(y-125)*0.008159981
        cv2.circle(img,(int(300+200*np.sin(y)),int(300+200*np.cos(y))),20,(0),-1)
        cv2.circle(img,(int(300+200*np.sin(yt)),int(800+200*np.cos(yt))),20,(0),-1)
        cv2.imshow('window',img)
        cv2.waitKey(1)

	def run(self,recieve_que,send_que):
		previousTime = time.clock()
        #plt.ion()
        last_time=time.clock()
        nt=0
        pn=0
        while(True):
            while (q.empty() or ((time.clock()- previousTime) > self.interval))  is False:
                self.output_mem.append(recieve_que.get())
                
                self.input_mem.append()
                nt+=1

            self.render_gym()
            fps=1.0/(time.clock()-previousTime)
            #print("loop running on {} fps with {} recieve speed".format(fps,(nt-pn)*fps))
            pn=nt
            previousTime = time.clock()
        cv2.destroAllWindows()

def main():
	config=read_config()
	sim=Sim(config)
	
	
if __name__ == '__main__':
	main()
		