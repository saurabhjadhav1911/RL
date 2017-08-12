#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git
import json
def save():
	config={}
	config['Serial_config']={
		'baud':115200,
		'port':"COM6"
	}
	config['Reward_config']={
		'ip':"192.168.0.103"
	}

	s=json.dumps(config)
	with open("config.json","w") as f:
		f.write(s)

def read_config():
	with open("config.json","r") as f:
		s=f.read()
		config=json.loads(s)
	return config
if __name__=='__main__':
	config=read()
	print(config['Serial_config']['baud'])