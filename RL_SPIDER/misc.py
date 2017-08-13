#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git
import json
def read_config():
	with open("config.json","r") as f:
		s=f.read()
		config=json.loads(s)
	return config
