#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,Activation,Dropout
from keras.optimizers import Adam
import pydot
from os.path import isfile, join
import sys
import os
import gym
import random
from collections import deque

class DQN():
    """docstring for DQN"""
    def __init__(self,env):
        self.memory=deque(maxlen=2000)
        self.epsilon=0.01
        self.epsilon_min=0.01
        self.epsilon_decay=0.995
        self.learning_rate=0.01
        self.env=env
        self.gamma=0.9
        ip=self.env.observation_space.shape[0]
        op=self.env.action_space.n
        self.model=self.create_model(ip,op)
        self.target_model=self.create_model(ip,op)

    def train_step(self,state,action,reward,new_state,done):
        batch_size=32
        if len(self.memory)<batch_size:
            return
        samples=random.sample(self.memory,batch_size)

        #model.fit()
        for sample in samples:
            state,action,reward,new_state,done=sample
            target=self.target_model.predict(state)
            #print(target)
            if done:
                target[0][action]=reward
            else:
                Q_future=self.gamma*np.max(self.target_model.predict(new_state))
                #print(Q_future)
                target[0][action]=reward+self.gamma*Q_future
            self.model.fit(state,target,epochs=1,verbose=0)


    def remember(self,state,action,reward,new_state,done):
        self.memory.append([state,action,reward,new_state,done])

    def act(self,state):
        self.epsilon*=self.epsilon_decay
        self.epsilon=max(self.epsilon,self.epsilon_min)
        r=np.random.random()
        if r<self.epsilon:
            return self.env.action_space.sample()
        else:
            return np.argmax(self.model.predict(state)[0])
    def save(self):
        self.model.save_weights("model.model")
    def load(self):
        self.model.load_weights("model.model")
        self.target_model.load_weights("model.model")
    def create_model(self,input_size,output_size):
        model=Sequential()
        model.add(Dense(24,input_shape=(input_size,)))
        model.add(Activation('relu'))
        model.add(Dropout(0.6))
        model.add(Dense(48,))
        model.add(Activation('relu'))
        model.add(Dropout(0.6))
        model.add(Dense(24,))
        model.add(Activation('relu'))
        model.add(Dropout(0.6))
        model.add(Dense(output_size,))
        model.add(Activation('softmax'))
        model.compile(optimizer=Adam(lr=self.learning_rate),
              loss='mean_squared_error')
        return model
    def  train_target(self):
        self.target_model.set_weights(self.model.get_weights())

def main():
    env = gym.make("MountainCar-v0")
    dqn=DQN(env)
    try:
        dqn.load()
        print("weights loaded")
    except Exception as e:
        print(e)
    num_trials = 20
    sim_steps = 2000
    for i in range(num_trials):
        cur_state = env.reset().reshape(1,2)
        new_state=cur_state
        score = 0
        for step in range(sim_steps):
            #env.render()
            action=env.action_space.sample()
            action=dqn.act(cur_state)
            new_state,reward,done,info= env.step(action)
            new_state=new_state.reshape(1,2)
            dqn.remember(cur_state,action,reward,new_state,done)
            dqn.train_step(cur_state,action,reward,new_state,done)
            dqn.train_target()
            cur_state=new_state
            if done:
                break
        print("trial number {} completed".format(i))
    dqn.save()
    #print(dqn.memory)

if __name__ == "__main__":
    main()
    
    print('done')
