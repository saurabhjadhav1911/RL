#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,Activation,Dropout
from keras.optimizers import Adam
from os.path import isfile, join
import sys
import os
import gym
import random
from collections import deque

class DQN():
    """docstring for DQN"""
    def __init__(self,env):
        self.input_memory=deque(maxlen=4000)
        self.target_memory=deque(maxlen=4000)
        self.epsilon=0.01
        self.epsilon_min=0.01
        self.epsilon_decay=0.995
        self.learning_rate=0.1
        self.env=env
        self.gamma=0.9
        self.ip=self.env.observation_space.shape[0]
        self.op=2#self.env.action_space.n
        self.model=self.create_model((self.ip+1),(self.ip+1))
        self.target_model=self.create_model(self.ip,self.op)

    def train(self):
        ip=np.array(self.input_memory)
        target=np.array(self.target_memory)
        self.model.fit(ip,target,epochs=1000)


    def remember(self,state,action,reward,new_state,done):
        self.input_memory.append(np.concatenate([state,action]))
        self.target_memory.append(np.concatenate([reward,new_state]))

    def act(self,state):
        self.epsilon*=self.epsilon_decay
        self.epsilon=max(self.epsilon,self.epsilon_min)
        r=np.random.random()
        if r<self.epsilon:
            return self.env.action_space.sample()
        else:
            return np.argmax(self.model.predict(state)[0])

    def save(self):
        self.model.save_weights("servo_math_simulator.model")

    def load(self):
        self.model.load_weights("servo_math_simulator.model")
        self.target_model.load_weights("servo_math_simulator.model")

    def create_model(self,input_size,output_size):
        model=Sequential()
        model.add(Dense(24,input_shape=(input_size,)))
        model.add(Activation('relu'))
        model.add(Dropout(0.6))
        model.add(Dense(24,))
        model.add(Activation('relu'))
        model.add(Dropout(0.6))
        model.add(Dense(output_size,))
        model.add(Activation('relu'))
        model.compile(optimizer=Adam(lr=self.learning_rate),
              loss='mean_squared_error')
        return model

    def  train_target(self):
        self.target_model.set_weights(self.model.get_weights())

def main():
    phy_env = gym.make("Pendulum-v0")
    env = gym.make("Pendulum-v2")
    dqn=DQN(env)
    num_trials = 10
    sim_steps = 1000
    for i in range(num_trials):
        print('trial')
        cur_state = env.reset().reshape(dqn.ip)
        print(cur_state.shape)
        new_state=cur_state
        score = 0
        for step in range(sim_steps):
            env.render()
            action=0#env.action_space.sample()
            newth=1.2#np.random.uniform(-3.14,3.14,1000)
            newthdot=0#np.random.uniform(-8,8,1000)
            new_state,reward,done,info= env.step([newth,newthdot,action])
            #new_state=new_state.reshape(dqn.ip)
            #dqn.remember(cur_state,action,[reward],new_state,done)
            cur_state=new_state
            if done:
                break
        print("trial number {} completed".format(i))
    #dqn.train()

if __name__ == "__main__":
    main()
    
    print('done')
