import serial
import numpy
import os
import time
def process(gline):
    print(gline)
    #code=gline.split('(')
    #value=int(gline)
    #arduino.write(struct.pack('>B', value))
    ser.write(gline.encode())
    nt=0
    pn=0
    last_time=time.clock()
    for i in range(2000):
        if(ser.inWaiting()>0):
            print(ser.readline())
            fps=1.0/(time.clock()-last_time)
            print("loop running on {} fps with {} recieve speed".format(fps,(nt-pn)*fps))
            pn=nt
            last_time=time.clock()
            #break            
def getfile():
    #filename=raw_input("Enter filepath of gcode")
    filename= "gcode.txt"

    global gcode
    gcode=open(filename,"r")
    print("file opened succesfully")
    return gcode
def serialconnect():
    try:
        global ser
        ser = serial.Serial("COM4", 115200)
    except serial.serialutil.SerialException:
        print("Serial port not connected .Check connection and port name")
        return 0      
while(getfile()==0):
    print("read file again")
while(serialconnect()==0):
    print("connect com port again")
time.sleep(3)
while True:
    line=gcode.readline()
    if not line: break
    process(line)
    time.sleep(2)
#print(gcode.readline())
