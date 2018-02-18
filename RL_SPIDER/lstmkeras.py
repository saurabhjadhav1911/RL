#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL\RL_SPIDER
#https://github.com/saurabhjadhav1911/RL.git
#C:\Users\Public\RL\ABC\ABC
#C:\Users\vaibhav\Documents\Python\RL\RL_SPIDER

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import matplotlib.pyplot as plt
from threading import Thread
import threading
import tensorflow as tf
import time


class ThreadLSTM():
    """docstring for ThreadLSTM"""

    def __init__(self):

        ################################### generate train ,test data #####################################
        self.x = np.array([i for i in range(0, 100)])
        self.data = np.zeros((1, 100, 1))
        self.data[0, 30:, 0] = 1.0
        self.target = np.zeros((1, 100, 1))

        for i in range(100):
            self.target[0, i, 0] = self.data[0, i, 0] * ((
                1 - np.exp(-(i - 30) / 5.0)))

        self.x_test = np.zeros((1, 100, 1))
        self.x_test[0, 50:, 0] = 1.0
        self.y_test = np.zeros((1, 100, 1))
        self.graph_lock = threading.Lock()

        for i in range(100):
            self.y_test[0, i, 0] = self.x_test[0, i, 0] * ((
                1 - np.exp(-(i - 50) / 5.0)))

        ################################### LSTM model #####################################
        self.model = self.create_model()
        self.load_model()
        self.default_graph = tf.get_default_graph()
        ################################### Plotting #####################################
        self.fig = plt.gcf()
        self.fig.canvas.draw()

    def generate_test_data(self):
        val = int(np.random.rand() * 100)
        self.x_test = np.zeros((1, 100, 1))
        self.x_test[0, val:, 0] = 1.0
        self.y_test = np.zeros((1, 100, 1))

        for i in range(100):
            self.y_test[0, i, 0] = self.x_test[0, i, 0] * ((
                1 - np.exp(-(i - val) / 5.0)))

        return self.x_test, self.y_test

    def plot_data(self, x, data):

        plt.gcf().clear()
        #plt.plot(data[0,0,:])

        for target in data:
            plt.plot(x, target[0, :100, 0])

        self.fig.canvas.draw()
        plt.pause(0.001)

    def create_model(self):
        model = Sequential()
        model.add(LSTM(6, return_sequences=True, input_shape=(None, 1)))
        model.add(LSTM(6, return_sequences=True))
        model.add(Dense(1))
        model.compile(loss='mse', optimizer='rmsprop', metrics=['accuracy'])
        model._make_predict_function()
        return model

    def load_model(self):
        try:
            self.model.load_weights("lstmmin_size_corrected2.model")
            print('weights loaded ')
        except:
            print('weights not loaded ')

    def save_model(self):
        self.model.save_weights("lstmmin_size_corrected2.model")
        print('weights saved')

    def train(self, default_graph):
        n = 0
        for i in range(101):
            with default_graph.as_default():
                with self.graph_lock:

                    self.model.fit(
                        self.data,
                        self.target,
                        epochs=1,
                        batch_size=1,
                        verbose=2,
                        validation_data=(self.x_test, self.y_test))
                    n += 1
                    #predict = self.model.predict(self.x_test)
                    #predict = self.model.predict(self.data)
                    #self.plot_data(self.x,[predict,self.target])
            if n is 50:
                self.save_model()
                n = 0

    def check_predict(self, inp, exp_out, default_graph):

        inp = inp.reshape((1, 100, 1))
        exp_out = exp_out.reshape((1, 100, 1))
        with default_graph.as_default():
            with self.graph_lock:
                predict = self.model.predict(inp)
        self.plot_data(self.x, [inp, predict, exp_out])

    def test(self, default_graph):
        while True:
            self.generate_test_data()
            self.check_predict(self.x_test, self.y_test, default_graph)
            time.sleep(1)

    def run(self):
        train_process = Thread(target=self.train, args=(self.default_graph, ))
        #test_process = Thread(target=self.train)
        train_process.start()
        self.test(self.default_graph)
        train_process.join()


def main():
    lstm = ThreadLSTM()
    lstm.run()
    #lstm.save_model()


if __name__ == '__main__':
    main()
