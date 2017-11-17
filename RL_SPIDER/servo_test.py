
#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git

def Main():
    config=read_config()
    q=multiprocessing.Queue()
    parent_conn, child_conn = Pipe()
    env=Env.Env(config=config)
    sim=Plot.Plot()

    env_process=Process(target=Env.run,args=(child_conn,))
    sim_process=Process(target=Plot.run,args=(parent_conn,))

    env_process.start()
    sim_process.start()

    env_process.join()
    sim_process.join()

    print("done")

if __name__ == '__main__':
    from misc import *
    import Env
    import Sim
    import Agent
    import Plot
    from multiprocessing import Pool,Process,Pipe
    import multiprocessing  
    multiprocessing.freeze_support()
    Main()

    try:
        pass

    except Exception as e:
        print(e)
        logname=__file__.replace('.py','')
        logname+='.log'
        print("error see file {}".format(logname))
        with open(logname,"w") as f:
                f.write(str(e))


'''

from drawnow import *
import numpy as np
values = []
serialArduino = serial.Serial('com3', 115200)  
while True:
    while (serialArduino.inWaiting()==0):
        valueRead = serialArduino.readline()
  
'''
