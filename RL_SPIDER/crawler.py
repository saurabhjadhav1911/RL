import numpy as np
import cv2
import time
from multiprocessing import Queue
from colorama import Fore, Back, Style
import colorama
colorama.init()
color = Fore.GREEN

class Crawler():
    """docstring for Crawler"""

    def __init__(self, l1=None, l2=None, b=None, h=None, que=None):
        self.l1 = l1 or 150.0
        self.l2 = l2 or 150.0
        self.K = 0.1
        self.av = [0, 0]
        self.pav = 0
        self.val = [0, 0]
        self.data = ""
        self.mn = 1024
        self.mx = 0
        self.angle = 0
        self.l = 0.0
        self.state = 0
        self.p = 0
        self.last_p = 0
        self.saved_x = 0
        self.saved_dx = 0
        self.saved_y = 0
        self.saved_dy = 0
        self.dx = 0
        self.dy = 0
        self.x = 0
        self.y = 0
        self.number_of_states=2

        self.que = que or Queue()

    def render(self):
        pass

    def step(self, action):
        self.val =action

    def run(self):
        while True:
            self.que.put(self.get_line())
            time.sleep(0.01)

    def kinematics(self, theta1, theta2):
        self.dx = ((self.l1 * np.sin(theta1)) +
                   (self.l2 * np.sin(theta1 + theta2)))
        self.dy = ((self.l1 * np.cos(theta1)) +
                   (self.l2 * np.cos(theta1 + theta2)))
        if self.dy > 0:
            self.p = 0
        else:
            self.p = 1

        if self.p == 1 and self.last_p == 0:
            # rising edge p
            self.saved_x = self.x
            self.saved_dx = self.dx
            #saved_y = y
            #saved_dy = dy
        if self.p == 1:
            self.x = self.saved_x + self.saved_dx - self.dx
        #last_dx = dx
        #last_x = x
        #last_dy = dy
        #last_y = y
        self.last_p = self.p

        return self.p, self.x

    def get_line(self):
        line = ""
        for s in range(self.number_of_states):
            self.av[s] += (self.K * (self.val[s] - self.av[s]))
            line += str(int(self.val[s]))
            line += ' '
            line += str(int(self.av[s]))
            line += ' '
        p, x = self.kinematics(self.av[0] * 3.14159 / 180, self.av[1] * 3.14159 / 180)
        line += str(int(self.p))
        line += ' '
        line += str(int(self.x))
        line += '|'
        print(color,"line_from_crawler",line)
        return line
