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

color = Fore.MAGENTA


class Agent():
    """docstring for Env"""

    def __init__(self, agent_obs_que, agent_reward_que, agent_action_que,
                 config):
        self.config = config
        [self.angle_vect_size, self.pressure_vect_size,
         self.reward_vect_size] = self.config['Sim_config']['obs_vector_space']
        print(color, 'obs vect space', self.angle_vect_size,
              self.pressure_vect_size, self.reward_vect_size)
        self.total_vect_size = (
            self.angle_vect_size
        ) + self.pressure_vect_size + self.reward_vect_size
        self.action_space_size = self.angle_vect_size

        self.agent_action_que = agent_action_que
        self.agent_obs_que = agent_obs_que
        self.agent_reward_que = agent_reward_que

        #self.sim_obs_que = agent_obs_que
        #self.sim_action_que = sim_action_que
        self.action_min_limit = np.array(
            self.config['Agent_config']['action_min_limit'])
        self.action_max_limit = np.array(
            self.config['Agent_config']['action_max_limit'])

        self.responce_dict = {}

        self.default_action = np.array(
            self.config['Env_config']['default_action'])
        self.movement_cost = 0
        self.sim_cycle_id = 0
        self.cycle_id = 0
        self.steps_per_episode = self.config['Agent_config'][
            'steps_per_episode']
        self.sim_step = 0
        self.val = [0, 0]
        self.memory_length = self.config['Agent_config']['memory_length']
        print(color,"mem len",self.memory_length)
        self.agent_env_memory = np.zeros((self.memory_length,(3*self.angle_vect_size+self.pressure_vect_size+self.reward_vect_size)))  ## actions,angles,der-angles,pressure,reward
        print(color,self.agent_env_memory)
    def run(self):
        #self.consumer_test()
        self.env_reset()
        self.get_obs_action()

    def consumer_test(self):
        Thread(target=self.generate_step).start()
        while True:
            while self.agent_obs_que.empty() is False:
                responce_obs = self.agent_obs_que.get()
                responce_reward = self.agent_reward_que.get()
                print(color, "agent recieved this", responce_obs,
                      responce_reward)
            #self.episode()

    def generate_step(self):
        while True:
            self.val[0] = 90 - self.val[0]
            self.act(self.val)
            print(color, self.val)
            self.cycle_id += 1
            time.sleep(1)
            self.val[1] = -90 - self.val[1]
            self.act(self.val)
            self.cycle_id += 1
            print(color, self.val)
            time.sleep(1)

    def get_obs_action(self):
        while True:
            try:
                while self.agent_obs_que.empty() is False:
                    responce_obs, obs_id = self.agent_obs_que.get()
                    actions, angle, pressure = np.array(
                        responce_obs[:self.angle_vect_size]), np.array(
                            responce_obs[
                                self.angle_vect_size:
                                2 * self.angle_vect_size]), np.array(
                                    responce_obs[2 * self.angle_vect_size:
                                                 2 * self.angle_vect_size +
                                                 self.pressure_vect_size])
                    state = np.concatenate(
                        (angle, angle - self.agent_env_memory[(
                            (obs_id - 1) % self.memory_length
                        ), self.angle_vect_size:2 * self.angle_vect_size],
                         pressure)) ## actions,angles,der-angles,pressure,reward

                    ################ take_immediate_action although reward is pending #################
                    self.take_immediate_action(state)

                    self.agent_env_memory[obs_id] = np.concatenate(
                        (actions, state, [self.movement_cost]))

                    #new_state=np.concatenate((angle,angle-self.last_angles))

                while self.agent_reward_que.empty() is False:
                    responce_reward, reward_id = self.agent_reward_que.get()
                    self.agent_env_memory[obs_id,
                                          -self.reward_vect_size:] += np.array(
                                              responce_reward)
                    #print(color, "saved in agent memory",self.agent_env_memory[obs_id])
                #if obs_id is not reward_id:
                #    print(color,"obs reward out of sync")

            except Exception as e:
                exc_traceback = traceback.format_exc()
                print(color, exc_traceback)
                print(color,self.agent_env_memory.shape)

        return state, reward, done

    def env_reset(self):
        self.agent_action_que.put([self.default_action, self.cycle_id])

    def act(self, action):
        self.agent_action_que.put([action, self.cycle_id])

    def take_immediate_action(self, state):
        self.cycle_id = (self.cycle_id + 1) % self.memory_length
        action = (np.random.rand(self.angle_vect_size) *
                  (self.action_max_limit - self.action_min_limit
                   )) + self.action_min_limit

        ######## actor network predict #########
        self.act(action)

    def env_step(self, action):
        #self.sim_action_que.put([action, self.sim_cycle_id])
        while True:
            try:
                state, reward, done, id = self.sim_state_que.get()
                if self.cycle_id is id:
                    break
            except Exception as e:
                print(color, e)
        return state, reward, done

    def env_train(self):
        pass

    def env_episode(self):
        sim_current_state, _, done = self.sim_reset()
        for i in range(self.steps_per_episode):
            action = self.act(sim_current_state)
            new_state, reward, done = self.sim_step(action)
            self.sim_memory.append(
                [sim_current_state, action, new_state, reward, done])
            sim_current_state = new_state
            if done:
                break

    def sim_reset(self):
        self.sim_step = 0
        self.sim_action_que.put([self.default_action, self.sim_cycle_id])
        while True:
            try:
                state, reward, done, id = self.sim_state_que.get()
                if self.sim_cycle_id is id:
                    reward = 0
                    done = False
                    break
            except Exception as e:
                print(color, e)

        return state, reward, done

    def act(self, action):
        self.agent_action_que.put([action, self.cycle_id])

    def sim_step(self, action):
        #self.sim_action_que.put([action, self.sim_cycle_id])
        while True:
            try:
                state, reward, done, id = self.sim_state_que.get()
                if self.sim_cycle_id is id:
                    break
            except Exception as e:
                print(color, e)
        return state, reward, done

    def sim_train(self):
        pass

    def sim_episode(self):
        sim_current_state, _, done = self.sim_reset()
        for i in range(self.steps_per_episode):
            action = self.act(sim_current_state)
            new_state, reward, done = self.sim_step(action)
            self.sim_memory.append(
                [sim_current_state, action, new_state, reward, done])
            sim_current_state = new_state
            if done:
                break
