from threading import Thread
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
import sys
import traceback

color=Fore.YELLOW


class TrainManeger(object):
	"""docstring for TrainManeger"""

	def __init__(self, arg):
		
		self.arg = arg
		
		self.models=[]


if __name__ == '__main__':
    try:

        main()

    except Exception as e:
        exc_traceback = traceback.format_exc()
        print(exc_traceback)
        logname = __file__.replace('.py', '.log')
        print("error see file {}".format(logname))
        with open(logname, "w") as f:
            f.write(str(exc_traceback))
