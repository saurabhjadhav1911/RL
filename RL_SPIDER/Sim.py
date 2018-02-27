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

color = Fore.YELLOW

#host = get_sock_ip()
#host =misc.get_ip_mac()

#print(color, "host:{}".format(host))


def sprint(color, msg):
    port = 5000
    s = socket.socket()
    s.connect((host, port))
    s.send(msg)
    s.close()


def send_angles(data):
    st = ""
    for i in data:
        st += str(i)
        st += " "
    sprint(color, st)


'''
if __name__ == '__main__':
    while True:
        ip = input(">>")
        v = str(ip)
        send_angles([v, v, v, v, v, v, v, v, v, v, v, v])
'''
last_error = None


class Sim():
    """docstring for Env"""

    def __init__(self, config, font_color=None):
        global color
        color = font_color or color
        self.config = config
        self.lock = False
        self.seq_size = self.config['Sim_config']['sequence_size']
        self.vect_size = self.config['Sim_config']['obs_vector_size']
        self.batch_size = self.config['Sim_config']['batch_size']
        self.img_size = [900, 1600]
        self.output_mem = deque(maxlen=self.seq_size)
        self.input_mem = deque(maxlen=self.seq_size)
        self.t = np.array([i for i in range(0, self.seq_size)])
        self.x_train = np.zeros((1, self.seq_size, self.vect_size))
        self.y_train = np.zeros((1, self.seq_size, self.vect_size))
        #print(color,self.x_train[0].shape,self.y_train[0].shape)
        self.interval = 1.0 / 60.0
        self.val = np.zeros((self.vect_size))
        print(color, self.val)
        self.last_batch = -1

        self.min_y = [1023, 1023]
        self.max_y = [0, 0]
        #self.model._make_predict_function()
        #self.model=self.create_generalised_model(config['Sim_config']['Model_recurrent_sizes'],config['Sim_config']['Model_fully_connected_sizes'])
        self.model = self.create_model()
        self.default_graph = tf.get_default_graph()
        #self.default_graph.finalize()

        self.graph_lock = threading.Lock()
        self.load_model()

        self.fig = plt.gcf()
        self.ax = self.fig.gca(projection='3d')
        self.ax.set_xlim3d([0.0, 0.6])
        self.ax.set_ylim3d([0.0, 200.0])
        self.ax.set_zlim3d([0.0, 1.0])

        self.centre_pivot = [300, 400]
        self.offset = [700, 0]
        self.angle_offset_1 = 0
        self.angle_offset_2 = 0
        self.reward_k = 1
        self.l1 = 150
        self.l2 = 150
        #self.fig.canvas.draw()

        print(color, 'Sim created')

    def load_model(self):
        try:
            self.model.load_weights("Models/Crawler_Math_Sim_Model_" + str(
                self.config['Sim_config']['saved_model_index']) + ".model")
            print(color, 'Math Simulator weights loaded ')
        except Exception as e:
            print(color,
                  'Math Simulator weights not loaded due to {}'.format(e))

    def save_model(self):
        self.model.save_weights("Models/Crawler_Math_Sim_Model_" + str(
            self.config['Sim_config']['saved_model_index']) + ".model")
        print(color, 'weights saved')

    def create_generalised_model(self, rec_size, fc_size):
        model = Sequential()
        model.add(
            LSTM(
                rec_size[1],
                return_sequences=True,
                input_shape=(None, rec_size[0])))

        for l in range(2, len(rec_size)):  #reccurent layer sizes#
            model.add(LSTM(rec_size[l], return_sequences=True))

        for l in range(len(fc_size)):  #fully connected layer sizes#
            model.add(Dense(fc_size[l]))

        model.compile(loss='mse', optimizer='rmsprop', metrics=['accuracy'])
        return model

    def create_model(self):
        model = Sequential()
        model.add(
            LSTM(
                10, return_sequences=True, input_shape=(None, self.vect_size)))
        model.add(LSTM(10, return_sequences=True))
        model.add(Dense(10))
        model.add(Dense(self.vect_size))
        model.compile(loss='mse', optimizer='rmsprop', metrics=['accuracy'])
        model._make_predict_function()
        return model

    def plot_data(self, x, data):

        self.ax.clear()
        #plt.plot(data[0,0,:])

        for i, target in enumerate(data):
            #plt.plot(x, target.reshape((self.seq_size)))
            plt.plot(
                x,
                target.reshape((self.seq_size)),
                zs=i / 10,
                zdir='y',
                label='curve in (z,y)')

        self.ax.set_xlim3d([0.0, 200.0])
        self.ax.set_ylim3d([0.0, 0.6])
        self.ax.set_zlim3d([0.0, 1.0])
        self.fig.canvas.draw()
        plt.pause(0.001)

    def save_env_data(self):
        x_batch, y_batch = np.array(self.input_mem) / 180.0, np.array(
            self.output_mem) / 180.0
        #print(color, 'shape', y_batch.shape)
        if y_batch.shape[0] == self.seq_size:
            self.x_train, self.y_train = x_batch.reshape(
                (1, self.seq_size, self.vect_size)), y_batch.reshape(
                    (1, self.seq_size, self.vect_size))
            #print(color,'train min max',np.max(self.x_train),np.max(self.y_train))
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

    def train(self, default_graph):
        global last_error
        n = 0
        while True:
            try:
                with default_graph.as_default():
                    with self.graph_lock:
                        #print(color, "train start")
                        self.model.fit(
                            self.x_train,
                            self.y_train,
                            epochs=1,
                            batch_size=1,
                            verbose=2,
                            validation_data=(self.x_train, self.y_train))
                        #print(color, "train end")
                        n += 1
                        #self.model.set_weights(self.train_model.get_weights())
                #model.fit(data, target, epochs=10, batch_size=1, verbose=2,validation_data=(x_test, y_test))

            except Exception as e:
                if last_error is None:
                    exc_traceback = traceback.format_exc()
                    print(color, exc_traceback)
                    #print(color,e)
                    print(color, self.x_train.shape, self.y_train.shape)
                last_error = e
            if n is 20:
                self.save_model()
                n = 0
            time.sleep(0.1)
        #self.model.fit(x_train, y_train, epochs=10, batch_size=1, verbose=2,validation_data=(x_test, y_test))

    def predict_output_mem(self, x, default_graph):
        with default_graph.as_default():
            with self.graph_lock:
                yt = self.model.predict(x)
        return yt

    def render_sim(self, y, yt):
        img = 255 * np.ones((self.img_size), dtype=np.uint8)
        #print(color, 'img render', y, yt)
        y = (y) * np.pi / 180
        yt = (yt) * np.pi / 180  #*0.008159981

        self.draw_leg(img,y[0], y[1], 100, y[2])
        self.draw_leg(img,yt[0], yt[1], -100 + self.offset[0],yt[2])  #(self.reward_k * yt[3])
        cv2.imshow('window', img)
        cv2.waitKey(1)

    def circle(self, img, jt, r, c, f):
        cv2.circle(
            img, (self.centre_pivot[0] + jt[0], self.centre_pivot[1] - jt[1]),
            r, c, f)

    def draw_leg(self, img, theta1, theta2, distance, col):
        ##################################### base center point ################################################
        self.circle(img, (int(distance), 0), 20, (0), -1)
        ##################################### base center point ################################################

        ##################################### first rod end point ################################################
        self.circle(
            img,
            (int(distance + self.l1 * np.cos(theta1 + self.angle_offset_1)),
             int((self.l1 * np.sin(theta1 + self.angle_offset_1)))), 15, (0),
            -1)
        ##################################### first rod end point ################################################

        ##################################### second rod end point ################################################
        self.circle(img, (
            int(distance + self.l1 * np.cos(theta1 + self.angle_offset_1) +
                self.l2 * np.cos(theta2 + self.angle_offset_2 + theta1 + self.
                                 angle_offset_1)),
            int(self.l1 * np.sin(theta1) + self.l2 * np.sin(
                theta2 + self.angle_offset_2 + theta1 + self.angle_offset_1))),
                    10, int(128 * col), -1)
        ##################################### second rod end point ################################################

    def generate_step(self, send_que):
        while True:
            self.val[0] = 180 - self.val[0]
            send_que.put(self.val)
            print(color, self.val)
            time.sleep(1)
            self.val[1] = 180 - self.val[1]
            send_que.put(self.val)
            print(color, self.val)
            time.sleep(1)

    def run(self, recieve_que, send_que, agent_obs_que, agent_reward_que,
            agent_action_que):

        Thread(target=self.generate_step, args=(send_que, )).start()
        train_process = Thread(target=self.train, args=(self.default_graph, ))
        train_process.start()

        self.store_obs_from_env(recieve_que, self.default_graph)
        train_process.join()
        cv2.destroyAllWindows()

    def store_obs_from_env(self, recieve_que, default_graph):
        previousTime = time.clock()
        #plt.ion()
        last_time = time.clock()
        nt = 0
        pn = 0
        yt = 0
        while (True):
            while (
                    recieve_que.empty() is False
            ):  # or ((time.clock()- previousTime) > self.interval))  is False:
                y = recieve_que.get()
                #print(color,y)
                try:
                    self.min_y[0], self.max_y[0] = min(
                        [y[1], self.min_y[0]]), max([y[1], self.max_y[0]])
                    y[1] = (180.0 * (y[1] - self.min_y[0]) /
                            (self.max_y[0] - self.min_y[0]))
                    self.min_y[1], self.max_y[1] = min(
                        [y[3], self.min_y[1]]), max([y[3], self.max_y[1]])
                    y[3] = (180.0 * (y[3] - self.min_y[1]) /
                            (self.max_y[1] - self.min_y[1]))
                    self.output_mem.append([y[1], y[3], 0, 0])
                    self.input_mem.append([y[0], y[2], 0, 0])
                except Exception as e:
                    print(e)
                nt += 1
            self.save_env_data()
            ytt = np.array(self.input_mem) / 180.0
            yy = np.array(self.output_mem) / 180.0
            if (ytt.shape[0] == self.seq_size):  # and self.lock is False:
                yp = self.predict_output_mem(
                    ytt.reshape((1, self.seq_size, self.vect_size)),
                    default_graph)
                yt = yp[0][199] * 180.0
                y = yy[199] * 180.0
                #self.plot_data(self.t, [ytt, yy, yp])
                self.plot_data(self.t, [
                    self.x_train[0, :, 0], self.y_train[0, :, 0], yp[0, :, 0],
                    self.x_train[0, :, 1], self.y_train[0, :, 1], yp[0, :, 1]
                ])
                self.render_sim(y, yt)
                print(color,"y yt", y, yt)

            fps = 1.0 / (time.clock() - previousTime)
            #print(color,"loop running on {} fps with {} recieve speed".format(fps,(nt-pn)*fps))
            pn = nt
            previousTime = time.clock()


def main():
    config = read_config('config_crawler.json')
    sim = Sim(config)
    img = 255 * np.ones((900, 1400), dtype=np.uint8)
    sim.draw_leg(img, np.pi / 2 + 0, 0, 20, 0)
    cv2.imshow('window', img)
    cv2.waitKey(0)
    img = 255 * np.ones((900, 1400), dtype=np.uint8)
    sim.draw_leg(img, np.pi / 2 + np.pi / 4, 0, 40, 0)
    cv2.imshow('window', img)
    cv2.waitKey(0)
    img = 255 * np.ones((900, 1400), dtype=np.uint8)
    sim.draw_leg(img, np.pi / 2 + np.pi / 2, np.pi / 2, 60, 1)
    cv2.imshow('window', img)
    cv2.waitKey(0)
    img = 255 * np.ones((900, 1400), dtype=np.uint8)
    sim.draw_leg(img, np.pi / 2 + 0, np.pi / 2, 80, 1)
    cv2.imshow('window', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
