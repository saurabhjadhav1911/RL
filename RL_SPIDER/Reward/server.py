#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL\RL_SPIDER\Reward
#https://github.com/saurabhjadhav1911/RL.git
import socket

def Main():
	host ='192.168.0.102'
	port =5000


	s=socket.socket()
	s.bind((host,port))

	s.listen(1)
	c,addr=s.accept()
	print("connection established {}".format(str(addr)))

	while True:
		data=c.recv(1024)
		if not data:
			print("no data")
			break
		print("from connection {}".format(str(data)))

		data=str(data).upper()
		
		print("to connection {}".format(str(data)))		

		c.send(data)
	c.close()


if __name__=='__main__':
	Main()

