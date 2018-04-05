
import socket
import sys
import os
import misc
import math

def Listen():
    host=misc.get_sock_ip()
    port =5000
    s=socket.socket()
    s.bind((host,port))
    print("##################### server started on ip {} ######################".format(host))
    flag=True
    start=True
    while flag:
        s.listen(2)
        c,addr=s.accept()
        data=c.recv(1024)
        if not data:
            pass
        else:
            print(">>{}".format(data))
            

        if "END" in data:
            flag=False

        
    c.close()
    
if __name__=='__main__':
    Listen()
