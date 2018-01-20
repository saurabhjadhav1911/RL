import socket
import sys
host =misc.get_sock_ip()
#host =misc.get_ip_mac()

print("host:{}".format(host))
def sprint(msg):
	port =5000
	s=socket.socket()
	s.connect((host,port))
	s.send(msg)
	s.close()

def send_angles(data):
	st=""
	for i in data:
		st+=str(i)
		st+=" "
	sprint(st)

if __name__=='__main__':
	while True:
		ip=input(">>")
		v=str(ip)
		send_angles([v,v,v,v,v,v,v,v,v,v,v,v])

