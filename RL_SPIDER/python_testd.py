
import argparse
import sys
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
import matplotlib.pyplot as plt
import socket
import traceback
from functools import reduce
from misc import *

config = read_config()


def flatten(d, pref=''):
    return(reduce(
        lambda new_d, kv: \
            isinstance(kv[1], dict) and \
            {**new_d, **flatten(kv[1], pref + kv[0])} or \
            {**new_d,  kv[0]: [kv[1],pref+'|'+kv[0],]},
        d.items(),
        {}
    ))

class Reference:
    def __init__(self, val):
        self._value = val # just refers to val, no copy

    def get(self):
        return self._value

    def set(self, val):
        self._value = val

def main():
	
def add(args):
    return args.x + args.y


class PrintThread(Thread):
    """docstring for PrintThread"""

    def __init__(self, arg):
        super(PrintThread, self).__init__(target=self.run)
        self.arg = arg

    def run(self):
        for i in range(20):
            print('this is thread {}'.format(self.arg))


def main3():
    pt1 = PrintThread(1)
    pt2 = PrintThread(2)

    pt1.start()
    pt2.start()

    pt1.join()
    pt2.join()


def do_render(item):
    def wrapped_item():
        return 'a wrapped_item of {}'.format(str(item()))

    return wrapped_item


def render():
    return 'image generated'


if __name__ == '__main__':
    main()
