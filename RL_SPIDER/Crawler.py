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

    def __init__(self, config, l1=None, l2=None, b=None, h=None, que=None):
        self.config = config
        self.env_cycle_delay=self.config['Env_config']['env_cycle_delay']
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
        self.number_of_states = 2

        self.centre_pivot = [100, 400]
        self.offset = [700, 0]
        self.angle_offset_1 = 0
        self.angle_offset_2 = 0
        self.reward_k = 1
        self.l1 = 150
        self.l2 = 150
        self.que = que or Queue()

    def render(self,img):
        cv2.imshow('window', img)
        cv2.waitKey(1)

    def step(self, action):
        self.val = action

    def run(self):
        while True:
            self.que.put(self.get_line())
            time.sleep(0.01)
        cv2.destroyAllWindows()
    def kinematics(self, val):
        for s in range(self.number_of_states):
            self.av[s] += (self.K * (val[s] - self.av[s]))

        theta1 = self.av[0]
        theta2 = self.av[1]

        self.dx = ((self.l1 * np.cos(theta1)) +
                   (self.l2 * np.cos(theta1 + theta2)))
        self.dy = ((self.l1 * np.sin(theta1)) +
                   (self.l2 * np.sin(theta1 + theta2)))
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

        return theta1, theta2, self.p, self.x

    def get_line(self):
        line = ""
        t1, t2, p, x = self.kinematics(
            [self.val[0] * np.pi / 180, self.val[1] * np.pi / 180])

        img = 255 * np.ones((900, 1400), dtype=np.uint8)
        #self.draw_leg(img, t1, t2, x, p)
        #self.render(img)

        for s in range(self.number_of_states):

            line += str(int(self.val[s]))
            line += ' '

        for s in range(self.number_of_states):        
            line += str(int(self.av[s] * 180 / np.pi))
            line += ' '

        line += str(int(self.p))
        line += ' '
        line += str(int(self.x))
        line += '|'
        if (self.config['Env_config']['show_obs']):
            print(color, "line_from_crawler", line)
        return line

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
                    10, (128 * col), -1)
        ##################################### second rod end point ################################################


def main():
    sim = Crawler()
    p, x = 0, 0

    for j in range(90):
        img = 255 * np.ones((900, 1400), dtype=np.uint8)
        t1, t2, p, x = sim.kinematics([1, 0])
        sim.draw_leg(img, t1, t2, x, p)
        #sim.circle(img,(0,j),20,0,-1)
        cv2.imshow('window', img)
        cv2.waitKey(100)
    for j in range(90):
        img = 255 * np.ones((900, 1400), dtype=np.uint8)
        t1, t2, p, x = sim.kinematics([-1, 0])
        sim.draw_leg(img, t1, t2, x, p)
        #sim.circle(img,(0,j),20,0,-1)
        cv2.imshow('window', img)
        cv2.waitKey(100)
    '''for j in range(8):
        for i in range(0, 30):
            img = 255 * np.ones((900, 1400), dtype=np.uint8)
            p, x = sim.kinematics((np.pi / 2) + ((60-i) * np.pi / 180), 0)
            sim.draw_leg(img, np.pi / 2 + ((60-i) * np.pi / 180), 0, x, p)
            cv2.imshow('window', img)
            cv2.waitKey(10)
        for i in range(0, 80):
            img = 255 * np.ones((900, 1400), dtype=np.uint8)
            p, x = sim.kinematics(np.pi / 2 + np.pi / 6, (-i * np.pi / 180))
            sim.draw_leg(img, np.pi / 2 + np.pi / 6, (-i * np.pi / 180), x, p)
            cv2.imshow('window', img)
            cv2.waitKey(10)
        for i in range(30, 60):
            img = 255 * np.ones((900, 1400), dtype=np.uint8)
            p, x = sim.kinematics((np.pi / 2) + (i * np.pi / 180), 0)
            sim.draw_leg(img, np.pi / 2 + (i * np.pi / 180), (-80 * np.pi / 180),
                         x, p)
            cv2.imshow('window', img)
            cv2.waitKey(10)
        for i in range(0, 80):
            img = 255 * np.ones((900, 1400), dtype=np.uint8)
            p, x = sim.kinematics(np.pi / 2 + np.pi / 6, ((80-i) * np.pi / 180))
            sim.draw_leg(img, np.pi / 2 + (60 * np.pi / 180), ((80-i) * np.pi / 180),
                         x, p)
            cv2.imshow('window', img)
            cv2.waitKey(10)
    '''
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
