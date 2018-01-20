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
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import matplotlib.pyplot as plt
import socket
import sys

host =misc.get_sock_ip()
#host =misc.get_ip_mac()

print("host:{}".format(host))
def sprint(msg):
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
    sprint(st)

if __name__=='__main__':
    while True:
        ip=input(">>")
        v=str(ip)
        send_angles([v,v,v,v,v,v,v,v,v,v,v,v])


class Sim():
    """docstring for Env"""
    def __init__(self,config):
        
        
        self.seq_size=config['Sim_config']['sequence_size']
        self.vect_size=config['Sim_config']['obs_vector_size']
        self.batch_size=config['Sim_config']['batch_size']

        self.output_mem=deque(maxlen=self.seq_size)
        self.input_mem=deque(maxlen=self.seq_size)
        self.x_train=np.array((self.batch_size,self.seq_size,self.vect_size))
        self.x_train=np.array((self.batch_size,self.seq_size,self.vect_size))
        self.interval=1.0/60.0
        self.val=0
        self.last_batch=-1

        #self.model=self.create_generalised_model(config['Sim_config']['Model_recurrent_sizes'],config['Sim_config']['Model_fully_connected_sizes'])
        self.model=self.create_model()

        try:
            model.load_weights("Models/Math_Sim_Model_"+str(config['Sim_config']['saved_model_index'])+".model")
            print('Math Simulator weights loaded ')
        except Exception as e:
            print('Math Simulator weights not loaded due to {}'.format(e))
        
        print('Sim created')

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
        x_batch,y_batch=np.array(self.input_mem),np.array(self.output_mem)
        if self.last_batch is -1:
            for b in range(self.batch_size):
                x_train[b],y_train[b]=x_batch,y_batch
            self.last_batch=0
        else:
            self.last_batch=(self.last_batch+1)%self.batch_size
            x_train[self.last_batch],y_train[self.last_batch]=np.copy(x_batch),np.copy(y_batch)

    def train(self):
        self.model.fit(self.x_train, self.y_train, epochs=10, batch_size=1, verbose=2)
        #self.model.fit(x_train, y_train, epochs=10, batch_size=1, verbose=2,validation_data=(x_test, y_test))


    def predict_mem(self):
        yt=model.predict(np.array())
        return yt

    def render_sim(self,y,yt):
        img=255*np.ones((self.size),dtype=np.uint8)
        y=(y-125)*0.008159981
        cv2.circle(img,(int(300+200*np.sin(y)),int(300+200*np.cos(y))),20,(0),-1)
        cv2.circle(img,(int(300+200*np.sin(yt)),int(800+200*np.cos(yt))),20,(0),-1)
        cv2.imshow('window',img)
        cv2.waitKey(1)

    def generate_step(self,recieve_que,send_que):
        while True:
            send_que.put(self.val)
            print(self.val)
            self.val=180-self.val
            time.sleep(2)

    def run(self,recieve_que,send_que):
        previousTime = time.clock()
        #plt.ion()
        last_time=time.clock()
        nt=0
        pn=0
        while(True):
            while (q.empty() or ((time.clock()- previousTime) > self.interval))  is False:
                self.output_mem.append(recieve_que.get())
                
                self.input_mem.append(self.val)
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
        
