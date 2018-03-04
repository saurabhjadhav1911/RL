#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL\RL_SPIDER
#https://github.com/saurabhjadhav1911/RL.git
#C:\Users\Public\RL\ABC\ABC
#C:\Users\vaibhav\Documents\Python\RL\RL_SPIDER

import multiprocessing
from colorama import Fore, Back, Style
import colorama
colorama.init()
import numpy as np
from misc import *
import serial
import time
import cv2
from collections import deque
#import gym
import DummyEnvAgent as Env
import Plot
import Sim
import Agent
import sys
import os
import traceback

#sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
color = Fore.WHITE


def plot_process_target(recieve_que, send_que, config):
    print(Fore.MAGENTA, 'Plot process start')
    plot = Plot.Plot(size=config['GUI_config']['plot_size'])
    plot.draw(recieve_que)
    print(config['GUI_config']['plot_size'])


def reward_process_target(recieve_que, send_que, config):
    print('Reward process start')
    '''plot = Plot.Plot(size=config['GUI_config']['plot_size'])
    print(config['GUI_config']['plot_size'])'''


def Sim_process_target(recieve_que, send_que, config, agent_obs_que,
                       agent_reward_que, agent_action_que):
    print(Fore.YELLOW, 'Sim process start')
    sim = Sim.Sim(config)
    sim.run(recieve_que, send_que, agent_obs_que, agent_reward_que,
            agent_action_que)
    #sim.generate_step(recieve_que, send_que)


def Env_process_target(recieve_que, send_que, config, agent_obs_que,
                       agent_reward_que, agent_action_que):
    print(Fore.GREEN, 'Env process start')
    env = Env.Env(config)
    env.run(recieve_que, send_que, agent_obs_que, agent_reward_que,
            agent_action_que)


def Agent_process_target(agent_obs_que, agent_reward_que, agent_action_que,config):
    print(Fore.BLUE, 'Agent process start')
    agent = Agent.Agent(agent_obs_que, agent_reward_que, agent_action_que,config)
    agent.run()


def Test_process_target(recieve_que, send_que, config):
    print('Test process start')
    generate_step(recieve_que, send_que, config)


def main():
    multiprocessing.freeze_support()

    config = read_config('config_crawler.json')
    config['Env_config']['env_cycle_delay']=0.001
    config = arg_parser(config)
    save_config(config, 'config_crawler.json')

    #initialise communicatoions between processes
    send_que = multiprocessing.Queue()
    recieve_que = multiprocessing.Queue()

    agent_obs_que = multiprocessing.Queue()
    agent_reward_que = multiprocessing.Queue()
    agent_action_que = multiprocessing.Queue()

    #process initialisation
    #plot_process = multiprocessing.Process(
    #    target=plot_process_target, args=(recieve_que, send_que, config))
    env_process = multiprocessing.Process(
        target=Env_process_target,
        args=(recieve_que, send_que, config, agent_obs_que, agent_reward_que,
              agent_action_que))
    sim_process = multiprocessing.Process(
        target=Sim_process_target,
        args=(recieve_que, send_que, config, agent_obs_que, agent_reward_que,
              agent_action_que))
    agent_process = multiprocessing.Process(target=Agent_process_target,args=(agent_obs_que, agent_reward_que, agent_action_que,config))
    #test_process = multiprocessing.Process(
    #    target=Test_process_target, args=(recieve_que, send_que, config))

    env_process.start()
    agent_process.start()
    #plot_process.start()
    sim_process.start()

    sim_process.join()
    agent_process.join()
    env_process.join()
    #test_process.join()


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
