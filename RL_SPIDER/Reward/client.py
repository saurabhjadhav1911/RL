#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL\RL_SPIDER\Reward
#https://github.com/saurabhjadhav1911/RL.git
import socket
import sys
sys.path.append("..")
import misc

print(sys.path)
def Main():
	host =misc.get_ip()
	port =5000

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
	print(dt)

