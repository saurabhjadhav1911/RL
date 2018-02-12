#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git
from __future__ import print_function

try:
    import __builtin__
except ImportError:
    # Python 3
    import builtins as __builtin__
'''
def print(color,*args, **kwargs):
    __builtin__.print(color,color)
    return __builtin__.print(color,*args, **kwargs)'''
from threading import Thread
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
import matplotlib.pyplot as plt
import socket
import sys
import traceback

color=Fore.YELLOW
host =get_sock_ip()
#host =misc.get_ip_mac()

print(color,"host:{}".format(host))
def sprint(color,msg):
    port =5000
    s=socket.socket()
    s.connect((host,port))
    s.send(msg)
    s.close()

def send_angles(data):
    st=""
    for i in data:
        st+=str(i)
        st+=" "
    sprint(color,st)

if __name__=='__main__':
    while True:
        ip=input(">>")
        v=str(ip)
        send_angles([v,v,v,v,v,v,v,v,v,v,v,v])

last_error=None
class Sim():
    """docstring for Env"""
    def __init__(self,config,font_color=None):
        global color
        color= font_color or color
        self.lock=False
        self.seq_size=config['Sim_config']['sequence_size']
        self.vect_size=config['Sim_config']['obs_vector_size']
        self.batch_size=config['Sim_config']['batch_size']
        self.img_size=[700,1300]
        self.output_mem=deque(maxlen=self.seq_size)
        self.input_mem=deque(maxlen=self.seq_size)
        self.x_train=np.zeros((1,self.seq_size,self.vect_size))
        self.y_train=np.zeros((1,self.seq_size,self.vect_size))
        self.default_graph = tf.get_default_graph()
        #print(color,self.x_train[0].shape,self.y_train[0].shape)
        self.interval=1.0/60.0
        self.val=0
        self.last_batch=-1
        
        #self.model._make_predict_function()    
        #self.model=self.create_generalised_model(config['Sim_config']['Model_recurrent_sizes'],config['Sim_config']['Model_fully_connected_sizes'])
        self.model=self.create_model()
        self.model._make_predict_function()

        try:
            self.model.load_weights("Models/Math_Sim_Model_"+str(config['Sim_config']['saved_model_index'])+".model")
            print(color,'Math Simulator weights loaded ')
        except Exception as e:
            print(color,'Math Simulator weights not loaded due to {}'.format(e))
        
        print(color,'Sim created')

    def create_generalised_model(self,rec_size,fc_size):
        model = Sequential()  
        model.add(LSTM(rec_size[1], return_sequences=True, input_shape=(None, rec_size[0])))

        for l in range(2,len(rec_size)):#reccurent layer sizes#
            model.add(LSTM(rec_size[l],return_sequences=True))

        for l in range(len(fc_size)):#fully connected layer sizes#
            model.add(Dense(fc_size[l]))

        model.compile(loss='mse', optimizer='rmsprop',metrics=['accuracy'])
        return model

    def create_model(self):
        model = Sequential()
        model.add(LSTM(6, return_sequences=True, input_shape=(None, 1)))
        model.add(LSTM(6,return_sequences=True))
        model.add(Dense(1))
        model.compile(loss='mse', optimizer='rmsprop',metrics=['accuracy'])
        return model

    def save_env_data(self):
        x_batch,y_batch=np.array(self.input_mem)/180.0,np.array(self.output_mem)/180.0
        
        if y_batch.shape==self.seq_size:
            self.x_train,self.y_train=x_batch.reshape((1,self.seq_size,self.vect_size)),y_batch.reshape((1,self.seq_size,self.vect_size))
        '''    if self.last_batch is -1:
                for b in range(self.batch_size):
                    self.x_train[b],self.y_train[b]=x_batch,y_batch
                self.last_batch=0
            else:
                self.last_batch=(self.last_batch+1)%self.batch_size
                self.x_train[self.last_batch],self.y_train[self.last_batch]=x_batch,y_batch
        '''
        #print(color,x_batch.shape,y_batch.shape)
        #print(color,self.x_train[0].shape,self.y_train[0].shape)

    def train(self):
        global last_error
        while True:
            try:
                
                print(color,"train start")
                self.lock=True
                self.train_model=self.create_model()
                #self.train_model.set_weights(self.model.get_weights())
                self.train_model.fit(self.x_train, self.y_train, epochs=1, batch_size=1, verbose=2)#,validation_data=(self.x_train,self.y_train))
                
                self.model.set_weights(self.train_model.get_weights())
                print(color,"train end")
                self.lock=False
                #model.fit(data, target, epochs=10, batch_size=1, verbose=2,validation_data=(x_test, y_test))
                time.sleep(0.1)
            except Exception as e:
                if last_error is None:
                    exc_traceback = traceback.format_exc()
                    print(color,exc_traceback)
                    #print(color,e)
                    print(color,self.x_train.shape,self.y_train.shape)
                last_error=e
        #self.model.fit(x_train, y_train, epochs=10, batch_size=1, verbose=2,validation_data=(x_test, y_test))

    def predict_output_mem(self,x):
        with self.default_graph.as_default():
            yt=self.model.predict(x)
        return yt

    def render_sim(self,y,yt):
        img=255*np.ones((self.img_size),dtype=np.uint8)
        y=(y-125)*np.pi/180
        yt=(yt-125)*np.pi/180#*0.008159981
        cv2.circle(img,(int(300+200*np.sin(y)),int(300+200*np.cos(y))),20,(0),-1)
        cv2.circle(img,(int(800+200*np.sin(yt)),int(300+200*np.cos(yt))),20,(0),-1)
        cv2.imshow('window',img)
        cv2.waitKey(1)

    def generate_step(self,send_que):
        while True:
            send_que.put(self.val)
            print(color,self.val)
            self.val=180-self.val
            time.sleep(2)

    def run(self,recieve_que,send_que):

        Thread(target=self.generate_step, args=(send_que,) ).start()
        train_process = Thread(target=self.train)
        train_process.start()

        self.store_obs_from_env(recieve_que)
        train_process.join()
        cv2.destroyAllWindows()

    def store_obs_from_env(self,recieve_que):
        previousTime = time.clock()
        #plt.ion()
        last_time=time.clock()
        nt=0
        pn=0
        yt=0
        while(True):
            while (recieve_que.empty() is False):# or ((time.clock()- previousTime) > self.interval))  is False:
                y=recieve_que.get()
                self.output_mem.append(y)
                self.input_mem.append(self.val)
                nt+=1
            self.save_env_data()
            ytt=np.array(self.input_mem)/180.0
            yy=np.array(self.output_mem)/180.0
            if (ytt.shape[0]==self.seq_size):# and self.lock is False:
                yp=self.predict_output_mem(ytt.reshape((1,self.seq_size,self.vect_size)))
                yt=yp[0][199]*180.0
                y=yy[199]*180.0
                print(color,y,yt)
            self.render_sim(y,yt)
            fps=1.0/(time.clock()-previousTime)
            #print(color,"loop running on {} fps with {} recieve speed".format(fps,(nt-pn)*fps))
            pn=nt
            previousTime = time.clock()

def main():
    config=read_config()
    sim=Sim(config)
if __name__ == '__main__':
    main()
        

