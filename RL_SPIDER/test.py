#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git
try:
	import json
	import pyserial

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


except Exception as e:
	print(e)
	logname=__file__.replace('.py','')
	logname+='.log'
	print(logname)
	with open(logname,"w") as f:
			f.write(str(e))

#if __name__=='__main__':
	