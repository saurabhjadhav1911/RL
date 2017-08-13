#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git

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
def Main():
	p1=Process(target=hi)
	p2=Process(target=hello)
	p1.start()
	p2.start()
	p1.join()
	p2.join()
	print("done")
def hi():
	for _ in xrange(100000):
		print("Hi")

def hello():
	for _ in xrange(100000):
		print("Hello")

try:
	import json
	import serial
	from multiprocessing import Pool,Process
	Main()
except Exception as e:
	print(e)
	logname=__file__.replace('.py','')
	logname+='.log'
	print("error see file {}".format(logname))
	with open(logname,"w") as f:
			f.write(str(e))


#if __name__=='__main__':
	