
import json
try:
	import subprocess
except:
	pass
import os
import socket

def read_config():
	filename=os.path.join(os.path.dirname(__file__),'config.json')
	print(filename)
	with open(filename,"r") as f:
		s=f.read()
		config=json.loads(s)
	return config

def get_ip_mac():
	config=read_config()
	mac=config['Reward_config']['mac']

	mac=mac.replace(':','-')
	data=subprocess.check_output(['arp','-a'])
	#line=data
	data=data.split('\n')
	host=None
	for line in data:
		if mac in line:
			line=line.split()
			host=line[0]
	if host==None:
		host=get_sock_ip()

	print("my ip is {}".format(host))
	return host
	
def get_sock_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
	s.connect(("8.8.8.8", 80)) 
	host=s.getsockname()[0]
	s.close()
	return host

def sprint(data):
	#host =get_sock_ip()
	host='192.168.0.102'
	#host =get_ip_mac()
	port =5000
	s=socket.socket()
	s.connect((host,port))
	l=len(data)
	n=0
	eof=True
	while eof:
	    if l>1000:
	        q=1000
	        l-=1000
	    else:
	        q=l
	        eof=False
	    s.send(data[n:n+q])
	msg=None
	s.close()

if __name__=='__main__':
	sprint("my ip is {}".format(get_ip_mac()))


