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
from keras.models import Sequential, Model
from keras.layers import Dense, LSTM, Input
from keras.optimizers import SGD
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
        [self.angle_vect_size, self.pressure_vect_size,
         self.reward_vect_size] = self.config['Sim_config']['obs_vector_space']
        print(color, 'obs vect space', self.angle_vect_size,
              self.pressure_vect_size, self.reward_vect_size)
        self.vect_size = self.angle_vect_size + self.pressure_vect_size + self.reward_vect_size
        self.action_space_size = self.angle_vect_size
        self.batch_size = self.config['Sim_config']['batch_size']
        self.img_size = [900, 1600]

        self.output_mem_angles = deque(maxlen=self.seq_size)
        self.output_mem_pressure = deque(maxlen=self.seq_size)
        self.output_mem_reward = deque(maxlen=self.seq_size)
        self.input_mem = deque(maxlen=self.seq_size)

        self.t = np.array([i for i in range(0, self.seq_size)])
        self.x_train = np.zeros((1, self.seq_size, self.action_space_size))
        self.y_train = [
            np.zeros((1, self.seq_size, self.angle_vect_size)),
            np.zeros((1, self.seq_size, self.pressure_vect_size)),
            np.zeros((1, self.seq_size, self.reward_vect_size))
        ]
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
        self.angle_values = 2
        self.reward_k = 1
        self.k_reward = 1000

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
        input_layer = Input(shape=(None, self.action_space_size))
        lstm_layer_1 = LSTM(10, return_sequences=True)(input_layer)
        lstm_layer_2 = LSTM(10, return_sequences=True)(lstm_layer_1)

        sub_last_layer = Dense(10)(lstm_layer_2)

        ### splitting last layer
        output_angles = Dense(self.angle_vect_size)(
            sub_last_layer)  #analog output
        output_pressure = Dense(
            self.pressure_vect_size,
            activation='sigmoid')(sub_last_layer)  #binary output
        output_reward = Dense(self.reward_vect_size)(
            sub_last_layer)  #analog output

        model = Model(
            inputs=input_layer,
            outputs=[output_angles, output_pressure, output_reward])
        model.compile(
            optimizer=SGD(lr=0.00001),
            loss=['mse', 'binary_crossentropy', 'mse'],
            metrics=['accuracy'],
            loss_weights=[0.10, 0.06, 0.04])

        model._make_predict_function()
        return model
    def create_model_2(self):
        rec_model = Sequential()
        rec_model.add(LSTM(10, return_sequences=True, input_shape=(None, self.action_space_size)))
        rec_model.add(LSTM(10, return_sequences=True))
        rec_model.add(Dense(10))
        
        model.compile(loss='mse', optimizer='rmsprop', metrics=['accuracy'])
        model._make_predict_function()
        input_layer = Input(shape=(None, self.action_space_size))
        
        sub_last_layer = Dense(10)(lstm_layer_2)

        ### splitting last layer
        output_angles = Dense(self.angle_vect_size)(
            sub_last_layer)  #analog output
        output_pressure = Dense(
            self.pressure_vect_size,
            activation='sigmoid')(sub_last_layer)  #binary output
        output_reward = Dense(self.reward_vect_size)(
            sub_last_layer)  #analog output

        model = Model(
            inputs=input_layer,
            outputs=[output_angles, output_pressure, output_reward])
        model.compile(
            optimizer=SGD(lr=0.00001),
            loss=['mse', 'binary_crossentropy', 'mse'],
            metrics=['accuracy'],
            loss_weights=[0.10, 0.06, 0.04])

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
        self.ax.set_ylim3d([0.0, 1])
        self.ax.set_zlim3d([-1.0, 1.2])
        self.fig.canvas.draw()
        plt.pause(0.001)

    def save_env_data(self):
        x_batch, y_batch = np.array(self.input_mem), [
            np.array(self.output_mem_angles),
            np.array(self.output_mem_pressure),
            np.array(self.output_mem_reward)
        ]
        #print(color, 'shape', x_batch.shape)
        if x_batch.shape[0] == self.seq_size:
            self.x_train, self.y_train = x_batch.reshape(
                (1, self.seq_size, self.action_space_size)), [
                    y_batch[0].reshape(
                        (1, self.seq_size,
                         self.angle_vect_size)), y_batch[1].reshape(
                             (1, self.seq_size, self.pressure_vect_size)),
                    y_batch[2].reshape((1, self.seq_size,
                                        self.reward_vect_size))
                ]
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
                            verbose=0,
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
                    print(color, self.x_train.shape, self.y_train[0].shape,
                          self.y_train[1].shape, self.y_train[2].shape)
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

        obs_angles, obs_pressure, obs_reward = y
        predicted_obs_angles, predicted_obs_pressure, predicted_obs_reward = yt

        #  require angles in radians
        img = 255 * np.ones((self.img_size), dtype=np.uint8)
        #print(color, 'img render', y, yt)

        obs_angles = (obs_angles) * np.pi / 180  ## radians
        predicted_obs_angles = (predicted_obs_angles) * np.pi / 180  ## radians
        #obs_reward = obs_reward / self.k_reward
        #predicted_obs_reward = predicted_obs_reward / self.k_reward ##pixels

        self.draw_leg(img, obs_angles[0], obs_angles[1], 100, obs_pressure)
        self.draw_leg(img, predicted_obs_angles[0], predicted_obs_angles[1],
                      100 + self.offset[0],
                      predicted_obs_reward)  #(self.reward_k * yt[3])
        cv2.imshow('window', img)
        cv2.waitKey(1)

    def circle(self, img, jt, r, c, f):
        cv2.circle(
            img, (self.centre_pivot[0] + jt[0], self.centre_pivot[1] - jt[1]),
            r, c, f)

    def draw_leg(self, img, theta1, theta2, distance, col):
        #  require angles in radians
        ##################################### base center point ################################################
        self.circle(img, (int(distance), 0), 20, (0), -1)
        ##################################### base center point ################################################
        #print(color,distance,self.l1,np.cos(theta1 + self.angle_offset_1),self.angle_offset_1)
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

        #Thread(target=self.generate_step, args=(send_que, )).start()
        train_process = Thread(target=self.train, args=(self.default_graph, ))
        #train_process.start()

        self.store_obs_from_env(recieve_que, self.default_graph)
        #train_process.join()
        cv2.destroyAllWindows()

    def denormalise(self, x, mn, mx):
        return 180.0 * (x - mn) / (mx - mn)

    def normalise(self, x, mn, mx):
        return (x - mn) / (mx - mn)

    def store_obs_from_env(self, recieve_que, default_graph):
        previousTime = time.clock()
        #plt.ion()
        last_time = time.clock()
        nt = 0
        pn = 0
        last_action_input = 0
        while (True):
            while (
                    recieve_que.empty() is False
            ):  # or ((time.clock()- previousTime) > self.interval))  is False:
                obs = recieve_que.get()  # recieve angles in degrees

                #print(color, "y", obs)
                try:
                    ## normalise betwwen limits 180 and 0 degrees
                    '''
                    self.min_y = [
                        min(a, b) for a, b in
                        zip(obs[self.angle_vect_size:2 * self.angle_vect_size],
                            self.min_y[self.angle_vect_size:
                                       2 * self.angle_vect_size])
                    ]
                    self.max_y = [
                        max(a, b) for a, b in
                        zip(obs[self.angle_vect_size:2 * self.angle_vect_size],
                            self.max_y[self.angle_vect_size:
                                       2 * self.angle_vect_size])
                    ]
                    obs[:2 * self.angle_vect_size] = [
                        self.denormalise(x, mn, mx) for x, mn, mx in zip(
                            obs[self.angle_vect_size:2 * self.angle_vect_size],
                            self.min_y[self.angle_vect_size:
                                       2 * self.angle_vect_size], self.max_y[
                                           self.angle_vect_size:
                                           2 * self.angle_vect_size])
                    ]
                    '''
                    #store degrees values for lstm

                    self.input_mem.append(obs[0:self.angle_vect_size])
                    self.output_mem_angles.append(
                        obs[self.angle_vect_size:(2 * self.angle_vect_size)])
                    self.output_mem_pressure.append(obs[(
                        2 * self.angle_vect_size
                    ):(2 * self.angle_vect_size + self.pressure_vect_size)])
                    self.output_mem_reward.append(obs[-self.reward_vect_size:])
                    '''
                    self.input_mem.append(obs[0:self.angle_vect_size])

                    self.output_mem_angles.append(
                        obs[2:4])
                    self.output_mem_pressure.append(obs[4:5])

                    self.output_mem_reward.append(obs[-self.reward_vect_size:])
                    '''

                    #print(color, "action_input_y", obs[0:2])
                    #print(color, "obs_y", obs[2:4], obs[4:5],obs[-self.reward_vect_size:])
                except Exception as e:
                    exc_traceback = traceback.format_exc()
                    print(color, exc_traceback)
                nt += 1

            self.save_env_data()

            action_input = np.array(self.input_mem)  ## degrees
            obs_angles = np.array(self.output_mem_angles)  ## degrees
            obs_pressure = np.array(self.output_mem_pressure)  ##binary
            obs_reward = np.array(self.output_mem_reward)  ## pixels

            #print(color, "action_input", action_input.shape)
            #print(color, "obs", obs_angles.shape, obs_pressure.shape,obs_reward.shape)

            try:
                obs_angles = obs_angles / 180.0  ## normalised angles
                action_input = action_input / 180.0  ## normalised angles
                obs_reward = obs_reward / self.k_reward  ## normalised reward

                # normalize angles to feed lstm
                if (action_input.shape[0] == self.seq_size
                    ):  # and self.lock is False:
                    predicted_obs_angles, predicted_obs_pressure, predicted_obs_reward = self.predict_output_mem(
                        action_input.reshape((1, self.seq_size,
                                              self.action_space_size)),
                        default_graph)

                    predicted_obs_pressure[:,:,:]=0
                    ## normalised predicted output by the math simulator
                    #print(color,'p pred',predicted_obs_reward)
                    last_predicted_obs_angles, last_predicted_obs_pressure, last_predicted_obs_reward = predicted_obs_angles[
                        0][199], predicted_obs_pressure[0][
                            199], predicted_obs_reward[0][199]
                    last_obs_angles, last_obs_pressure, last_obs_reward = obs_angles[
                        199], obs_pressure[199], obs_reward[199]
                    last_action_input = action_input[199]

                    self.plot_data(self.t, [
                        action_input[:, 0], obs_angles[:, 0],
                        predicted_obs_angles[0, :, 0], action_input[:, 1],
                        obs_angles[:, 1], predicted_obs_angles[0, :, 1],
                        obs_pressure[:, 0], predicted_obs_pressure[0, :, 0],
                        obs_reward[:, 0], predicted_obs_reward[0, :, 0]
                    ])

                    ## render with actuaal degrres and pixel values
                    '''
                    self.render_sim([
                        last_obs_angles * 180.0, last_obs_pressure,
                        last_obs_reward * self.k_reward
                    ], [
                        last_predicted_obs_angles * 180.0,
                        last_predicted_obs_pressure,
                        last_predicted_obs_reward * self.k_reward
                    ])'''
                    #print(color, "y yt", last_predicted_obs_angles,last_action_input)

            except Exception as e:
                exc_traceback = traceback.format_exc()
                print(color, exc_traceback)

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
