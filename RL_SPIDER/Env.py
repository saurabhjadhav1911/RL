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
    return __builtin__.print(color,*args, **kwargs)
'''
from colorama import Fore, Back, Style
import colorama
colorama.init()
from misc import *
import serial
import multiprocessing
import time
import traceback

value = 0
lav = 0
nf = 0
color = Fore.GREEN


class Env():
    """docstring for Env"""

    def __init__(self, config):
        print(color + 'Env created')
        self.config = config
        self.ser = self.get_Serial()
        self.default_action = config['Env_config']['default_action']
        self.data = ""

    def get_Serial(self):
        return serial.Serial(
            self.config['Serial_config']['port'],
            baudrate=self.config['Serial_config']['baud'],
            timeout=self.config['Serial_config']['timeout'])

    def reset(self):
        self.action(self.default_action)
        return self.read_state()

    def action(self, act):
        line = "G " + " ".join(map(str, act))
        print(color, line)
        #self.serial.write(line)

    def run(self, q, r):
        #ser=serial.Serial(config['Serial_config']['port'],baudrate=config['Serial_config']['baud'],timeout=config['Serial_config']['timeout'])
        print(color, "Serial communicatoion started")
        while True:
            self.read_write_state(q, r)

    def read_write_state(self, q, r):
        global value, lav
        flag = False
        while r.empty() is False:
            flag = True
            arr = " ".join(map(str, r.get()))
            arr += "|"
            #unicode(s, "utf-8")
            if(self.config['Env_config']['show_obs']):

                print(color,self.config['Env_config']['show_obs'],arr)
            self.ser.write(arr.encode())

        if (self.ser.inWaiting() > 0):
            c = self.ser.read()
            #print(color,c)
            try:
                c = str(c, 'utf-8')
                if c is '|':
                    #dta=data
                    #nf+=1
                    lav = value

                    if self.config['Env_config']['Env_vector_size'] > 1:
                        value = list(map(int, self.data.split()))
                    else:
                        value = int(self.data)
                    #if lav is not value:
                    if(self.config['Env_config']['show_obs']):
                        print(color,self.config['Env_config']['show_obs'],self.data)
                    q.put(value)
                    #v=q.get()
                    self.data = ""
                else:
                    self.data += c
            except Exception as e:
                exc_traceback = traceback.format_exc()
                print(color, exc_traceback)
                #pass
    def test_run(self, q, r):
        #ser=serial.Serial(config['Serial_config']['port'],baudrate=config['Serial_config']['baud'],timeout=config['Serial_config']['timeout'])
        while True:
            self.read_write_state(q, r)


############################  testing  Env  ############################


def Env_process_target(recieve_que, send_que, config):
    print(color, 'Env process start')
    env = Env(config)
    env.run(recieve_que, send_que)


def Test_process_target(recieve_que, send_que, config):

    print(color, 'Test process start')
    generate_step(recieve_que, send_que, config)


def main():
    multiprocessing.freeze_support()

    config = read_config('config_crawler.json')
    config = arg_parser(config)
    save_config(config, 'config_crawler.json')
    #initialise communicatoions between processes
    send_que = multiprocessing.Queue()
    recieve_que = multiprocessing.Queue()

    #process initialisation

    env_process = multiprocessing.Process(
        target=Env_process_target, args=(recieve_que, send_que, config))
    test_process = multiprocessing.Process(
        target=Test_process_target, args=(recieve_que, send_que, config))

    env_process.start()
    test_process.start()
    #con.start()
    test_process.join()
    env_process.join()
    #prod.join()


if __name__ == '__main__':
    main()
