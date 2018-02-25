#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git
from colorama import Fore, Back, Style
import colorama
colorama.init()
from misc import *
import serial
import multiprocessing
import time
import traceback
import Crawler
from threading import Thread
value = 0
lav = 0
nf = 0
color = Fore.GREEN


class Env():
    """docstring for DummyEnv"""

    def __init__(self, config):
        print(color + 'Env created')
        self.config = config
        self.default_action = config['Env_config']['default_action']
        self.data = ""
        self.crawler = Crawler.Crawler()

    def run(self, q, r, agent_obs_que, agent_reward_que, agent_action_que):
        #ser=serial.Serial(config['Serial_config']['port'],baudrate=config['Serial_config']['baud'],timeout=config['Serial_config']['timeout'])

        crawler_thread = Thread(target=self.crawler.run)
        crawler_thread.start()

        print(color, "Dummy Env started")

        while True:
            self.read_write_state(q, r)

        crawler_thread.join()

    def read_write_state(self, q, r):
        global value, lav
        flag = False
        while r.empty() is False:
            flag = True
            arr = r.get()
            self.crawler.step(arr)
            if (self.config['Env_config']['show_obs']):
                print(color,"dummy env write", self.config['Env_config']['show_obs'], arr)
            #self.ser.write(arr.encode())
        if not self.crawler.que.empty():
            self.data = self.crawler.que.get()
            self.data = self.data.replace('|', '')
            if self.config['Env_config']['Env_vector_size'] > 1:
                value = list(map(int, self.data.split()))
            else:
                value = int(self.data)

            q.put(value)
            if (self.config['Env_config']['show_obs']):
                print(color,"dummy env read", self.config['Env_config']['show_obs'], self.data)

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
