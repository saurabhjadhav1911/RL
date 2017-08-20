#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL\RL_SPIDER
#https://github.com/saurabhjadhav1911/RL.git
import json
import subprocess
import os

def read_config():
	filename=os.path.join(os.path.dirname(__file__),'config.json')
	print(filename)
	with open(filename,"r") as f:
		s=f.read()
		config=json.loads(s)
	return config

def get_ip():
	config=read_config()
	mac=config['Reward_config']['mac']
	mac=mac.replace(':','-')
	data=subprocess.check_output(['arp','-a'])
	#line=data
	data=data.split('\n')
	for line in data:
		if mac in line:
			line=line.split()
			return line[0]

if __name__=='__main__':
	print(get_ip())


