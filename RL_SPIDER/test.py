#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git

def save():
	config={}
	config['Serial_config']={
		'baud':115200,
		'port':"COM6",
		'timeout':1
	}
	config['Reward_config']={
		'ip':"192.168.0.103"
	}
	config['Env_config']={
		'action_space_size':12,
		'default_action':12*[0]
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

dt="""
#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL\RL_SPIDER\Reward
#https://github.com/saurabhjadhav1911/RL.git
import socket

def Main():

	host ='192.168.0.102'
	port =5000

	s=socket.socket()
	s.connect((host,port))

	msg=raw_input("msg")
	
	while msg!='q':
		
		print("to server {}".format(str(msg)))		
		s.send(msg)

		data=s.recv(1024)
		print("from server {}".format(str(data)))
		msg=raw_input("msg")	
		

		s.send(data)
	s.close()


if __name__=='__main__':
	Main()

"""

try:
	import json
	import serial
	from multiprocessing import Pool,Process
	import qrcode
	import cv2
	img = qrcode.make(dt)
	print(img)
	
except Exception as e:
	print(e)
	logname=__file__.replace('.py','')
	logname+='.log'
	print("error see file {}".format(logname))
	with open(logname,"w") as f:
			f.write(str(e))


#if __name__=='__main__':