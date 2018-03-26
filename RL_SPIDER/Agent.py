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
import random
from copy import deepcopy

color = Fore.MAGENTA
colorama.init()


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
        self.angle_min_limit = np.array(
            self.config['Agent_config']['action_min_limit'])
        self.angle_max_limit = np.array(
            self.config['Agent_config']['action_max_limit'])
        self.responce_dict = {}

        self.learning_rate = 0.001
        self.epsilon_decay = 0.995
        self.tau = .125
        self.default_action = np.array(
            self.config['Env_config']['default_action'])
        self.movement_cost = -5.0
        self.total_movement_cost = 0
        self.alpha = 0.8
        self.gamma = 0.9
        self.epsilon_min = 0.1
        self.epsilon = 0.1
        self.sim_cycle_id = 0
        self.cycle_id = 0
        self.reset_id = 0
        self.steps_per_episode = self.config['Agent_config'][
            'steps_per_episode']
        self.sim_step = 0
        self.episode_num = 0
        self.val = [0, 0]
        self.memory_length = self.config['Agent_config']['memory_length']
        print(color, "mem len", self.memory_length)

        self.agent_action_memory = np.zeros((self.memory_length))
        self.agent_env_memory = np.zeros(
            (self.memory_length,
             (3 * self.angle_vect_size + self.pressure_vect_size +
              self.reward_vect_size))
        )  ## actions,angles,der-angles,pressure,prev-angles,prev-der-angles,prev-pressure,reward
        self.agent_env_memory = np.zeros(
            (self.memory_length,
             (5 * self.angle_vect_size + 2 * self.pressure_vect_size +
              self.reward_vect_size))
        )  ## actions,angles,der-angles,pressure,prev-angles,prev-der-angles,prev-pressure,reward
        #print(color, self.agent_env_memory.shape)

        self.num_actions = 4
        self.actions = np.zeros((self.num_actions, self.action_space_size))
        for i in range(self.num_actions):
            self.actions[i] = [
                int(np.cos(2 * i * np.pi / self.num_actions) / 0.6),
                int(np.sin(2 * i * np.pi / self.num_actions) / 0.6)
            ]

        self.diag_actions = np.zeros((self.num_actions,
                                      self.action_space_size))
        for i in range(self.num_actions):
            self.diag_actions[i] = [
                int(np.cos(2 * (i + 0.5) * np.pi / self.num_actions) / 0.6),
                int(np.sin(2 * (i + 0.5) * np.pi / self.num_actions) / 0.6)
            ]
        print(color, "actions", self.actions)
        print(color, "diag actions", self.diag_actions)
        self.num_states_per_angle = 10
        self.num_states_per_pressure = 2
        self.Q = np.zeros(
            (self.num_states_per_angle, self.num_states_per_angle,
             self.num_states_per_pressure, self.num_actions),
            dtype=np.float)

        self.load_Q()
        '''
        self.actor_state_input,self.actor_model = self.create_actor_model()
        _,self.target_actor_model = self.create_actor_model()

        self.critic_state_input,self.critic_action_input,self.critic_model = self.create_critic_model()
        _,_,self.target_critic_model = self.create_critic_model()

        self.default_graph = tf.get_default_graph()'''
        self.pixelpercell = 80
        self.pause = 25
        self.img = np.zeros([
            self.pixelpercell * self.num_states_per_angle,
            2 * self.pixelpercell * self.num_states_per_angle, 3
        ], np.uint8)
        self.img = self.generate_background()
        self.fig = plt.gcf()
        self.ax = self.fig.gca(projection='3d')

    def run(self):
        #self.consumer_test()
        #train_process = Thread(target=self.train, args=(self.default_graph, ))
        #train_process.start()

        #self.env_reset()
        self.get_obs_action()

        #train_process.join()

    def consumer_test(self):
        Thread(target=self.generate_step).start()
        while True:
            while self.agent_obs_que.empty() is False:
                responce_obs = self.agent_obs_que.get()
                responce_reward = self.agent_reward_que.get()
                print(color, "agent recieved this", responce_obs,
                      responce_reward)
            #self.episode()

    def generate_background(self):
        self.img[:, :, :] = 255
        c = self.img.shape[0]

        for i in range(1, self.num_states_per_angle):
            a = int(c * i / self.num_states_per_angle)
            cv2.line(self.img, (0, a), (self.img.shape[1], a), [0, 0, 0], 2)
        c = self.img.shape[1]
        for i in range(1, self.num_states_per_angle):
            a = int(c * i / self.num_states_per_angle)
            cv2.line(self.img, (a, 0), (a, self.img.shape[0]), [0, 0, 0], 2)

        cv2.imshow('Environment', self.img)
        #cv2.waitKey(0)
        return self.img

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

    def render(self, pos):
        self.env = self.generate_background()
        a = int(self.pixelpercell * pos[0])
        c = int(self.pixelpercell * (pos[0] + 1))
        b = int(self.pixelpercell * (2 * pos[1] + pos[2]))
        d = int(self.pixelpercell * (2 * pos[1] + 1 + pos[2]))
        cv2.rectangle(
            self.env, (b + 20, a + 20), (d - 20, c - 20), [255, 255, 0],
            thickness=-1)
        maxq=np.max(self.Q)
        minq=np.min(self.Q)
        #print(maxq,minq)
        #print(self.Q.shape)
        for i in range(self.num_states_per_angle):
            for j in range(self.num_states_per_angle):
                c = self.pixelpercell * (i + 0.54)
                d = self.pixelpercell * (2 * j + 0.28 + 1)

                for ac in range(self.num_actions):
                    a = c + self.pixelpercell * 0.225 * self.actions[ac][0]
                    b = d + self.pixelpercell * 0.225 * self.actions[ac][1]
                    try:
                        h=int(255*((self.Q[i,j,1,ac]-minq)/(maxq-minq)))
                    except:
                        h=0
                    #print(self.Q[i,j,1,ac])
                    rgb=cv2.cvtColor(np.array([[[h,255,255]]],np.uint8),cv2.COLOR_HSV2BGR)[0,0]
                    rgb=[int(rgb[0]),int(rgb[1]),int(rgb[2])]
                    cv2.putText(
                        self.env,
                        str(int(self.Q[i][j][0][ac]) / 100.0)[0:5],
                        #str(ac),
                        (int(b), int(a)), cv2.FONT_HERSHEY_PLAIN, 0.8,
                        (0, 0, 0), 1)
                    center = (int(self.pixelpercell * (2 * j + 1.5)),
                              int(self.pixelpercell * (i + 0.5)))
                    
                    '''
                    cv2.circle(
                        self.env,
                        (center[0] +
                         int(self.diag_actions[ac % self.num_actions, 0] * self.pixelpercell / 2),
                         center[1] +
                         int(-self.diag_actions[ac % self.num_actions, 1] * self.pixelpercell / 2)),
                        10, [255, 0, 0], -1)
                    cv2.circle(
                        self.env,
                        (center[0] +
                         int(self.diag_actions[(ac - 1) % self.num_actions, 0] *
                             self.pixelpercell / 2), center[1] +
                         int(-self.diag_actions[(ac - 1) % self.num_actions, 1] *
                             self.pixelpercell / 2)), 15, [0, 0, 255], -1)
                    cv2.fillPoly(self.env, [np.array([[
                        int(center[0]),
                        int(center[1])
                    ], [
                        center[0] +
                        int(self.diag_actions[ac % self.num_actions, 0] * self.pixelpercell / 2),
                        center[1] +
                        int(-self.diag_actions[ac % self.num_actions, 1] * self.pixelpercell / 2)
                    ], [
                        center[0] +
                        int(self.diag_actions[(ac - 1) % self.num_actions, 0] *
                            self.pixelpercell / 2),
                        center[1] + int(-self.diag_actions[(
                            ac - 1) % self.num_actions, 1] * self.pixelpercell / 2)
                    ]],np.int32)],rgb) 
                    cv2.circle(self.env, center, 10, [0, 255, 255], -1)'''
                c = self.pixelpercell * (i + 0.54)
                d = self.pixelpercell * (2 * j + 0.28)
                for ac in range(self.num_actions):
                    a = c + self.pixelpercell * 0.225 * self.actions[ac][0]
                    b = d + self.pixelpercell * 0.225 * self.actions[ac][1]
                    cv2.putText(
                        self.env,
                        str(int(100.00 * self.Q[i][j][1][ac]) / 100.0)[0:-1],
                        #str(ac),
                        (int(b), int(a)), cv2.FONT_HERSHEY_PLAIN, 0.8,
                        (0, 0, 0), 1)
                    center = (int(self.pixelpercell * (2 * j + 0.5)),
                              int(self.pixelpercell * (i + 0.5)))
                    '''
                    cv2.circle(
                        self.env,
                        (center[0] +
                         int(self.diag_actions[ac % self.num_actions, 0] * self.pixelpercell / 2),
                         center[1] +
                         int(-self.diag_actions[ac % self.num_actions, 1] * self.pixelpercell / 2)),
                        10, [255, 0, 0], -1)
                    cv2.circle(
                        self.env,
                        (center[0] +
                         int(self.diag_actions[(ac - 1) % self.num_actions, 0] *
                             self.pixelpercell / 2), center[1] +
                         int(-self.diag_actions[(ac - 1) % self.num_actions, 1] *
                             self.pixelpercell / 2)), 15, [0, 0, 255], -1)
                    cv2.fillPoly(self.env, [np.array([[
                        int(center[0]),
                        int(center[1])
                    ], [
                        center[0] +
                        int(self.diag_actions[ac % self.num_actions, 0] * self.pixelpercell / 2),
                        center[1] +
                        int(-self.diag_actions[ac % self.num_actions, 1] * self.pixelpercell / 2)
                    ], [
                        center[0] +
                        int(self.diag_actions[(ac - 1) % self.num_actions, 0] *
                            self.pixelpercell / 2),
                        center[1] + int(-self.diag_actions[(
                            ac - 1) % self.num_actions, 1] * self.pixelpercell / 2)
                    ]],np.int32)],(255,255,0)) 
                    cv2.circle(self.env, center, 10, [0, 255, 255], -1)
                    '''
        #center = (int(self.pixelpercell * (2 * pos[1] + 0.5)),int(self.pixelpercell * (pos[0] + 0.5)))
        #cv2.circle(self.env, center, 10, [0, 0, 255], -1)

        cv2.imshow('Environment', self.env)
        #cv2.imwrite("{}E{},jpg".format(self.epoch_num,self.cycle_num),self.env)
        cv2.waitKey(self.pause)

    def load_Q(self):
        try:
            Q = np.load("Models/Crawler_Q_Agent_" + str(
                self.config['Agent_config']['saved_Q_index']) + ".npy")
            self.Q = Q
            print(color, 'Q values loaded ')
        except Exception as e:
            print(color, 'Q values not loaded due to {}'.format(e))

    def save_Q(self):
        np.save("Models/Crawler_Q_Agent_" +
                str(self.config['Agent_config']['saved_Q_index']) + ".npy",
                self.Q)
        print(color, 'Q values saved')

    def update_Q(self, mem_id):
        action = deepcopy(self.agent_env_memory[mem_id, :self.angle_vect_size])
        state = deepcopy(
            self.agent_env_memory[mem_id, self.angle_vect_size:3 * self.
                                  angle_vect_size + self.pressure_vect_size])
        prev_state = deepcopy(
            self.agent_env_memory[mem_id, 3 * self.angle_vect_size + self.
                                  pressure_vect_size:-self.reward_vect_size])
        reward = deepcopy(
            self.agent_env_memory[mem_id, -self.reward_vect_size:])

        action[0:self.angle_vect_size] = self.num_states_per_angle * (
            action[0:self.angle_vect_size] - self.angle_min_limit) / (
                self.angle_max_limit - self.angle_min_limit)
        state[0:self.angle_vect_size] = self.num_states_per_angle * (
            state[0:self.angle_vect_size] - self.angle_min_limit) / (
                self.angle_max_limit - self.angle_min_limit)
        prev_state[0:self.angle_vect_size] = self.num_states_per_angle * (
            prev_state[0:self.angle_vect_size] - self.angle_min_limit) / (
                self.angle_max_limit - self.angle_min_limit)

        action = action.astype(int)
        state = state.astype(int)
        prev_state = prev_state.astype(int)
        action = np.clip(action, 0, self.num_states_per_angle - 1)
        state = np.clip(state, 0, self.num_states_per_angle - 1)
        prev_state = np.clip(prev_state, 0, self.num_states_per_angle - 1)
        ## actions,angles,der-angles,pressure,prev-angles,prev-der-angles,prev-pressure,reward

        Q = deepcopy(self.Q[prev_state[0], prev_state[1], prev_state[4],
                            action[0], action[1]])

        q = deepcopy(self.Q[state[0], state[1], state[4]])
        maxQ = np.amax(q)

        #print(maxQ)
        qp = Q
        Q = Q + self.alpha * (reward[0] + (self.gamma * maxQ) - Q)
        if qp is not Q:
            pass
            #print(color,
            #      "Q value at state {} and action {} updated from {} to {}".
            #      format([prev_state[0], prev_state[1], prev_state[4]],
            #             [action[0], action[1]], qp, Q))
        self.Q[prev_state[0], prev_state[1], prev_state[4], action[0], action[
            1]] = Q

    def update_Q_negh(self, mem_id):
        action = deepcopy(self.agent_action_memory[mem_id])
        state = deepcopy(
            self.agent_env_memory[mem_id, self.angle_vect_size:3 * self.
                                  angle_vect_size + self.pressure_vect_size])
        prev_state = deepcopy(
            self.agent_env_memory[mem_id, 3 * self.angle_vect_size + self.
                                  pressure_vect_size:-self.reward_vect_size])
        reward = deepcopy(
            self.agent_env_memory[mem_id, -self.reward_vect_size:])

        state[0:self.angle_vect_size] = self.num_states_per_angle * (
            state[0:self.angle_vect_size] - self.angle_min_limit) / (
                self.angle_max_limit - self.angle_min_limit)
        prev_state[0:self.angle_vect_size] = self.num_states_per_angle * (
            prev_state[0:self.angle_vect_size] - self.angle_min_limit) / (
                self.angle_max_limit - self.angle_min_limit)

        action = action.astype(int)
        state = state.astype(int)
        prev_state = prev_state.astype(int)
        state = np.clip(state, 0, self.num_states_per_angle - 1)
        prev_state = np.clip(prev_state, 0, self.num_states_per_angle - 1)
        ## actions,angles,der-angles,pressure,prev-angles,prev-der-angles,prev-pressure,reward

        Q = deepcopy(
            self.Q[prev_state[0], prev_state[1], prev_state[4], action])

        q = deepcopy(self.Q[state[0], state[1], state[4]])
        maxQ = np.amax(q)

        #print(maxQ)
        qp = Q
        Q = Q + self.alpha * (reward[0] + (self.gamma * maxQ) - Q)
        '''
        if qp is not Q:
            print(color,
                  "Q value at state {} and action {} updated from {} to {}".
                  format([prev_state[0], prev_state[1], prev_state[4]], action,
                         qp, Q))
        '''
        self.Q[prev_state[0], prev_state[1], prev_state[4], action] = Q

    def take_immediate_action(self, rec_state):
        state = deepcopy(rec_state)
        if ((self.cycle_id + self.memory_length - self.reset_id) %
                self.memory_length) >= self.steps_per_episode:
            cycle_id = self.cycle_id
            self.env_reset()
            #print(color, "cycle_id", self.cycle_id)
            print(color, "episode {} finished with total reward {}".format(
                self.episode_num,
                self.agent_env_memory[cycle_id, -self.reward_vect_size:]))
            self.episode_num += 1
            self.save_Q()
        else:
            self.cycle_id = (self.cycle_id + 1) % self.memory_length

            #print(color, "state_in_obs", state)
            #self.epsilon = max(self.epsilon_min,self.epsilon * self.epsilon_decay)

            if random.random() < self.epsilon:
                action = (self.num_states_per_angle * np.random.rand(
                    self.angle_vect_size))
                action = action.astype(int)
                #print(color,"random_action_1",action)
            else:
                state[0:self.angle_vect_size] = self.num_states_per_angle * (
                    state[0:self.angle_vect_size] - self.angle_min_limit) / (
                        self.angle_max_limit - self.angle_min_limit)
                state = state.astype(int)
                state = np.clip(state, 0, self.num_states_per_angle - 1)
                q = self.Q[state[0], state[1], state[4]]
                maxQ = np.amax(q)
                count = (q == maxQ).sum()
                if count > 1:
                    best = np.argwhere(q == maxQ)
                    i = random.choice(best)
                else:
                    i = np.argwhere(q == maxQ)

                action = i
                #print("best action",action)
                action = action.astype(int)
                action = action.reshape((self.action_space_size))
                #print(color,"Q_action_2",action)
            ######## actor network predict #########

            action_angles = ((action / self.num_states_per_angle) *
                             (self.action_max_limit - self.action_min_limit
                              )) + self.action_min_limit
            #print(color,"action_angles",action_angles)
            self.act(action_angles)

    def take_immediate_action_negh(self, rec_state):
        state = deepcopy(rec_state)
        state[0:self.angle_vect_size] = self.num_states_per_angle * (
            state[0:self.angle_vect_size] - self.angle_min_limit) / (
                self.angle_max_limit - self.angle_min_limit)
        state = state.astype(int)
        state = np.clip(state, 0, self.num_states_per_angle - 1)
        if ((self.cycle_id + self.memory_length - self.reset_id) %
                self.memory_length) >= self.steps_per_episode:
            cycle_id = self.cycle_id
            self.env_reset()
            #print(color, "cycle_id", self.cycle_id)
            print(color, "episode {} finished with total reward {}".format(
                self.episode_num,
                self.agent_env_memory[cycle_id, -self.reward_vect_size:]))
            self.episode_num += 1
            self.save_Q()
        else:
            self.cycle_id = (self.cycle_id + 1) % self.memory_length

            #print(color, "state_in_obs", state)
            #self.epsilon = max(self.epsilon_min,self.epsilon * self.epsilon_decay)

            if random.random() < self.epsilon:
                i = random.choice(range(self.num_actions))
                daction = self.actions[i]

                daction = daction.astype(int)
                action = state[:self.action_space_size] + daction
                self.agent_action_memory[self.cycle_id] = i
                #print(color, "random_action_1", action)
            else:
                q = self.Q[state[0], state[1], state[4]]
                maxQ = np.amax(q)
                count = (q == maxQ).sum()
                #print(color, "q", q, count)
                if count > 1:
                    best = np.argwhere(q == maxQ)
                    i = random.choice(best)
                    #print(color, "more q max vlas", i, best)
                else:
                    i = np.argwhere(q == maxQ)
                    #print(color, "q max", i)

                daction = self.actions[i]
                daction = daction.astype(int)

                self.agent_action_memory[self.cycle_id] = i
                action = state[:self.action_space_size] + daction
                action = action.reshape((self.action_space_size))
                #print(color, "Q_action_2", action)
            ######## actor network predict #########

            action_angles = ((action / self.num_states_per_angle) *
                             (self.action_max_limit - self.action_min_limit
                              )) + self.action_min_limit
            #print(color,"action_angles",action_angles)
            self.act(action_angles)
            self.render([state[0], state[1], state[4]])

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
                         pressure))
                    #print(color, "recieved obs", actions, angle, pressure)
                    ################ take_immediate_action although reward is pending #################
                    self.take_immediate_action_negh(state)
                    prev_state = self.agent_env_memory[
                        ((obs_id - 1) % self.memory_length
                         ), self.angle_vect_size:
                        3 * self.angle_vect_size + self.pressure_vect_size]
                    ## actions,angles,der-angles,pressure,prev-angles,prev-der-angles,prev-pressure,reward
                    #print(color, "state pre", prev_state)
                    descrete_action = (actions - self.angle_min_limit) / (
                        self.angle_max_limit - self.angle_min_limit)
                    prev_descrete_action = (
                        self.agent_env_memory[(
                            obs_id - 1 + self.memory_length
                        ) % self.memory_length, 0:self.angle_vect_size] -
                        self.angle_min_limit) / (
                            self.angle_max_limit - self.angle_min_limit)
                    if descrete_action is not prev_descrete_action:
                        self.total_movement_cost += self.movement_cost
                    self.agent_env_memory[obs_id] = np.concatenate(
                        (actions, state, prev_state,
                         [self.total_movement_cost]))  #
                    #print(color, "saved in mem", (actions, state, prev_state,[self.total_movement_cost]))
                    #new_state=np.concatenate((angle,angle-self.last_angles))

                while self.agent_reward_que.empty() is False:
                    responce_reward, reward_id = self.agent_reward_que.get()
                    self.agent_env_memory[reward_id,
                                          -self.reward_vect_size:] += np.array(
                                              responce_reward)
                    self.update_Q_negh(reward_id)
                #print(color, "saved in agent memory",self.agent_env_memory[reward_id])
                #if obs_id is not reward_id:
                #    print(color,"obs reward out of sync")

            except Exception as e:
                exc_traceback = traceback.format_exc()
                print(color, exc_traceback)
                print(color, self.agent_env_memory.shape)

        return state, reward, done

    def env_reset(self):
        self.cycle_id = (self.cycle_id + 1) % self.memory_length
        self.reset_id = self.cycle_id
        self.total_movement_cost = 0
        self.cycle_id = -self.cycle_id
        self.act(self.default_action)
        self.cycle_id = -self.cycle_id

    def act(self, action):
        self.agent_action_que.put([action, self.cycle_id])

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


def Agent_process_target(agent_obs_que, agent_reward_que, agent_action_que,
                         config):
    print(Fore.BLUE, 'Agent process start')
    agent = Agent(agent_obs_que, agent_reward_que, agent_action_que, config)
    agent.take_immediate_action([0, 0, 0])
    #agent.run()


def main2():

    multiprocessing.freeze_support()

    config = read_config('config_crawler.json')
    config['Env_config']['env_cycle_delay'] = 0.001
    config = arg_parser(config)
    save_config(config, 'config_crawler.json')

    agent_obs_que = multiprocessing.Queue()
    agent_reward_que = multiprocessing.Queue()
    agent_action_que = multiprocessing.Queue()

    Agent_process_target(agent_obs_que, agent_reward_que, agent_action_que,
                         config)


def main():

    multiprocessing.freeze_support()

    config = read_config('config_crawler.json')
    config['Env_config']['env_cycle_delay'] = 0.01
    config = arg_parser(config)
    save_config(config, 'config_crawler.json')

    agent_obs_que = multiprocessing.Queue()
    agent_reward_que = multiprocessing.Queue()
    agent_action_que = multiprocessing.Queue()
    agent = Agent(agent_obs_que, agent_reward_que, agent_action_que, config)
    agent.render([5, 5, 0])
    cv2.waitKey(0)
    agent.save_Q()


if __name__ == '__main__':
    main()
