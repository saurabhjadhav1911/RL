#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git
def Main():
	
	config=read_config()
	env=Env.Env(config=config)
	sim=Sim.Sim()
	agent=Agent.Agent()

	env_process=Process(target=env.run)
	sim_process=Process(target=sim.run)
	agent_process=Process(target=agent.run)

	env_process.start()
	sim_process.start()
	agent_process.start()

	env_process.join()
	sim_process.join()
	agent_process.join()

	print("done")

try:
	from misc import *
	import Env
	import Sim
	import Agent
	from multiprocessing import Pool,Process
	Main()

except Exception as e:
	print(e)
	logname=__file__.replace('.py','')
	logname+='.log'
	print("error see file {}".format(logname))
	with open(logname,"w") as f:
			f.write(str(e))
