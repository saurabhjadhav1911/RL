#!/usr/bin/env python

#Copyright (c) 2015,2016 Joseph D. Steinmeyer (jodalyst), Jacob White, Nick Arango
#Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal 
#  in the Software without restriction, including without limitation the rights to use, 
#  copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the 
#  Software, and to permit persons to whom the Software is furnished to do so, subject 
#  to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies 
# or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE 
# OR OTHER DEALINGS IN THE SOFTWARE.

#Version 9 of 6.302x Software
#questions? email me at jodalyst@mit.edu
#feel free to mod this code however you want.  If you do some cool stuff, let me know...I'd like to see how far this approach can go before it hits limits


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
#async_mode = 'threading'
#async_mode = 'eventlet'
async_mode = None
if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()


import time
from threading import Thread, Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room,close_room, rooms, disconnect
import sys
import glob
import serial
import json
import struct


import csv

#Version 2.7 or Above?
if sys.version_info[0] >2:
    version3 = True
    kwargs = {'newline':''}
else:
    version3 = False 
    kwargs = {}



##import logging
##log = logging.getLogger('werkzeug')
##log.setLevel(logging.ERROR)



serialConnected = False #global flag for whether or not the serial port should be connected
serialPort =0  # (init value is 3...junk) contains serial port object when in use...touching protected by serialLock below
serialLock = Lock() #serial permission lock (protects shared resource of serial port)
print (serialLock)

#Taken from here on StackExchange: http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
#Want to give credit where credit is due!
def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in list(range(256))]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            #print("checking port "+port)
            s = serial.Serial(port)
            #print("closing port "+port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
#-------------------

#serial variables:

serialselection = ''
baudselection = 115200

mcuMessage = []


'''system_parameters (dictionary where keys are user-variable parameters and entry is list consisting of current value (index 0 and single-character comm term for conveying value back to micro...for example you could have system_parameters['K_d']=[1.4,'D']
'''
system_parameters = {} 
#params_and_values an ordered list of the names of paramters, headroom, and values to be plotted
#Used in generating CSV header list in order
params_and_values = []
#A list pointing to parameter values for quick plotting (rather than list comprehend this every time
param_vals = []

command_terms = ['HIHI']

#expected_length...how long each full message from Micro should be
expected_length = 0
#function that will be stored for chopping up message into appropriate signed/unsignedness/float, etc... makes this processing arbitrarily expandable as needed...must obviously agree with encoding scheme on micro
parseFunction = lambda x: [0]
'''Kp = 0.0
Kd = 0.0
Ki = 0.0
direct = 0.0
desired = 0.0
alternate = 0.0 # global flag of whether or not we're alternating...
'''


#ALTERNATING DATA STRUCTURE:
#   timer and state are used for storing/remembering the switching action
#   period is how often to switch (in seconds)
#   param is the user input that is switched (determined during initialization)
alt_data = {'timer': time.time(), 'state':-1.0, 'period': 5, 'param': None} #data struture used to implement alternating behavior

#Start up Flask server:
app = Flask(__name__, template_folder = './',static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!' #shhh don't tell anyone. Is a secret
socketio = SocketIO(app, async_mode = async_mode)
thread = None

#csv variables:
global csv_default
global csv_recent
global current
global archive
csv_st = time.time()
#variable which determines whether a csv is being generated or not.
csv_yn = False  #start out not writing csv files
csvLock = Lock()

keepRunning = True #set to True for default


#global setup variables:
#used during initialization of comms/building GUI
isSetup = False
setupString = ""
allGoodFromGUI = False


#Function run in parallel on infinite loop with 
#serves as serial listener outside of separate loop
def serialThread():
    print ("Starting serial background thread.")
    global desired
    global serialLock
    global csvLock
    global serialPort
    global system_parameters
    global params_and_values
    global expected_length
    global parseFunction
    global param_vals
    global csv_default
    global csv_recent
    global alt_data
    global alternate
    global isSetup
    global setupString
    global command_terms
    while True:
        #print (serialConnected)
        if serialConnected:
            print("serial connected!")
            print("not setup")
            writeUpdates('~',0)
            time.sleep(2.0)
            serialLock.acquire()
            try:
                new_setupString = serialPort.readline()
                serialPort.flushInput()
            except:
                print ("initi string reading issue")
            serialLock.release()
            print("before")
            print(new_setupString)
            new_setupString = strip_until_marker(new_setupString)
            print("after")
            print(new_setupString)
            temp_commands = new_setupString.split('&')
            temp_commands = temp_commands[1:-1]
            print(temp_commands)
            print(command_terms)
            if temp_commands != command_terms: #only reload the gui if the configuration setup string has changed!
                command_terms = temp_commands
                print("DETECTED DIFFERENT STARTUP STRING!")
                setupString = new_setupString
                print(setupString)
                temp = setupString.split('&',1)[1]
                temp = temp.rsplit('&',1)[0]
                setupString = temp
                print(setupString)
                try:#send up to javascript to sort its part out
                    socketio.emit('startup',setupString,broadcast =True)
                except:
                    print ("failed socket")
                #build structures based on setupString's contents and orderj
                plot_count =0 #used for tallying plots
                spaces = [] #used for determining how to chop data string (bytes per var)
                s=[] #list of sliders
                t=[] #list of temporal plots
                h = []  #contains headroom value if that is being plotted
                for x in command_terms:
                    if len(x)>0 and x[0] =='S': #is a slider
                        print("slider")
                        slider_vals = x.split('~') #chop string
                        print(slider_vals)
                        #next: add key to system_parameters dict of slider name
                        #entry is starting val (0) and one char value used for comms
                        system_parameters[slider_vals[1]]=[0,slider_vals[2]] 
                        s.append(slider_vals[1]) #add name of param to s list
                        #next is to fill in the param_vals list with the current value
                        param_vals.append(system_parameters[slider_vals[1]][0])  
                    if len(x)>0 and x[0] == 'A': #we are alternating
                        vals = x.split('~') #split substring
                        alt_data['period'] = float(vals[2]) #period unpacked
                        alt_data['param'] = vals[1] #link alternate to selected parameter
                    if len(x)>0 and x[0]=='T': #we have a temporal plot
                        print("Plot")
                        plot_vals = x.split('~') #split substring
                        t.append(plot_vals[1]) #add name to t list
                        #next line: append list: [num_bytes,signed/unsigned/float,etc..]
                        print(plot_vals)
                        spaces.append([int(plot_vals[2][1]),plot_vals[2][0]])
                        plot_count +=1 #increment plot count
                    if len(x)>0 and x[0]=='H':
                        head_vals = x.split('~')
                        h.append("Headroom")
                        plot_count +=1 #headroom isn't a "plot" but treated same
                        if head_vals[1] =='2':
                            spaces.append([2,'S']) #needed since 16bit int on Arduino
                        elif head_vals[1] =='4':
                            spaces.append([4,'F']) #needed since ARM32 Teensy
                params_and_values = t+h+s #in order plots, headroom, sliders
                print("Identified values: %r" %(params_and_values))
                expected_length = sum(x[0] for x in spaces)+2 #2 from open/closing byte
                #parse_prototype is function that will chop up incoming bytes for sending up to the GUI
                def parse_prototype(listo):
                    new_out = []
                    current_index=1 #start 1 up because of start byte
                    #print(listo)
                    for x in range(plot_count):
                        val = 0
                        if spaces[x][0] == 1:
                            if spaces[x][1] == 'S':
                                val = struct.unpack('b',listo[current_index:current_index+1])[0]
                            elif spaces[x][1] =='U':
                                val = struct.unpack('B',listo[current_index:current_index+1])[0]
                        elif spaces[x][0] == 2:
                            if spaces[x][1] == 'S':
                                val = struct.unpack('<h',listo[current_index:current_index+2])[0]
                            elif spaces[x][1] == 'U':
                                val = struct.unpack('H',listo[current_index:current_index+2])[0]
                        elif spaces[x][0] == 4:
                            if spaces[x][1] == 'F':
                                val = struct.unpack('f',listo[current_index:current_index+4])[0]
                            elif spaces[x][1] == 'S':
                                val = struct.unpack('i',listo[current_index:current_index+4])[0]
                        new_out.append(val)
                        current_index += spaces[x][0]
                    return new_out
                parseFunction = parse_prototype
                while not allGoodFromGUI:
                    print("Waiting for GUI Setup...")
                    time.sleep(1.0)
                isSetup = True
            else:
                print("SAME AS BEFORE!")
                inform_dev() #just tell device that we are good
                serialLock.acquire()
                try:
                    serialPort.flushInput()
                except:
                    print ("initi string reading issue")
                serialLock.release()
                print("updating Parameters:")
                for x in s: #reload gui and device
                    socketio.emit('setup slider',{0:x,1:str(system_parameters[x][0])}, broadcast=True)
                    print("Writing %s to be %0.4f" %(system_parameters[x][1],system_parameters[x][0]))
                    writeUpdates(system_parameters[x][1],system_parameters[x][0])
                    time.sleep(0.1)
                    writeUpdates(system_parameters[x][1],system_parameters[x][0])
                    time.sleep(0.1)
            time.sleep(1)
            print(system_parameters)
            print ("Starting to read serial subthread")

            print ('Alternating state')
            print (alternate)
            print("expected length:")
            print (expected_length)
            print (serialConnected)
            while serialConnected:
                serialLock.acquire()
                b = serialPort.read(expected_length)
                if len(b) != expected_length:
                    print("expected=%d, actual=%d\n",len(b),expected_length)
                new_data = None
                if len(b) > 0 and messageRead(b,expected_length):
                    new_data =  parseFunction(b)
                if new_data != None:
                    try:
                        socketio.emit('note',new_data,broadcast =True)
                    except:
                        print ("failed socket")
                    if csv_yn:
                        temp_time = [time.time()-csv_st] #time since recording started
                        csvLock.acquire()
                        newb_list = temp_time+new_data+[system_parameters[x][0] for x in s]
                        csv_default.writerow(newb_list)
                        csv_recent.writerow(newb_list)
                        csvLock.release()
                    #elif bytesThere > expected_length:
                    #    try:
                    #        serialPort.flushInput()
                    #    except:
                    #        print ("failure to flush input")
                serialLock.release()
                time.sleep(0.01)
                if alternate == 1:
                    if time.time()-alt_data['timer'] > alt_data['period']:
                        print ('Switch to :')
                        alt_data['timer'] = time.time() #reset timer
                        poi = alt_data['param'] #param of interest
                        print(type(system_parameters[poi][0]))
                        print(system_parameters[poi][0])
                        system_parameters[poi][0] = system_parameters[poi][0]*-1.0
                        alt_data['state'] = alt_data.get('state')*-1
                        writeUpdates(system_parameters[poi][1],system_parameters[poi][0])
                        try:
                            socketio.emit('state toggle', system_parameters[poi][0], broadcast=True) #tell the GUI that the desired has changed
                        except:
                            print('failed toggle socket')
            print ("Stopping serial read. Returning to idle state")
        time.sleep(0.01)


def strip_until_marker(input_string):
    #return only text after last non-ascii character has been found
    #should *always* work...closing byte of plot package is \xff which is non-ascii and
    #should get caught in this scheme...there are of course ways to break this but they
    #require breaking the communication contract we have setup.
    new_string = ''
    for x in range(len(input_string)):
        poss = input_string[x:x+1]
        try:
            if version3:
                if type(poss)==type("hi"):
                    poss = str.encode(poss,'ascii') #fail here possibly
            char = poss.decode('ascii')
            new_string+=char
        except:
            new_string=""
    return new_string


#runtime variables...
def messageRead(buff,exp):
    first = struct.unpack('b',buff[0:1])[0]
    last = struct.unpack('b',buff[exp-1:exp])[0]
    if first == 0 and last == -1:
        return True
    else:
        return False
    # if not version3:
    #     newb = buff
    #     buff = [ord(q) for q in newb] #converts yucky binary/string abominations of python 2.* into list of ascii numbers essentially...not issue in 3
    # mcuMessage=list(range(expected))
    # if buff[0] == 0 and buff[expected-1] == 255: #likely correct message
    #     errorF = False
    #     mcuMessage[0] = buff[0]
    #     mcuMessage[expected-1] = buff[expected-1]
    #     for i in range(1,expected-1):
    #         bufI = buff[i]
    #         if bufI ==0 or bufI == 255:
    #             errorF = True;
    #         mcuMessage[i] = bufI
    #     if not errorF:
    #         return mcuMessage
    # return None           


@app.route('/')
def index():
    global thread
    print ("A user connected")
    if thread is None:
        thread = Thread(target=serialThread)
        thread.daemon = True
        thread.start()
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print ('hey someone connected')
    ports = serial_ports() #generate list of currently connected serial ports 
    print (ports)
    newb=[]
    for p in ports:
        newb.append({"comName": p})
    print (json.dumps(newb))
    #emit('serial list display', {'data': ports}) #emit socket with serial ports in it
    emit('serial list display', newb) #emit socket with serial ports in it
    #emit('my response', {'data': 'Connected'}) 

@socketio.on('disconnect')
def test_disconnect():
    global csv_yn
    global csvLock
    emit('serial disconnect request',broadcast=True)
    csv_yn = 0
    #if current is not None and archive is not None:
    csvLock.acquire()
    try:
        current.close()
        archive.close()
    except NameError:
        pass #if didn't exist yet, don't try...
    csvLock.release()
    print('Client disconnected. Hopefully that was for the best.')
    writeUpdates('~',0)#for non-autoreset devices must tell it to enter child state again

def writeUpdates(tag,val):
    global serialPort
    global serialLock
                
    string_to_write = tag+' %0.2f\n' %(float(val))
    print(string_to_write)
    if serialConnected:
        serialLock.acquire() #claim serial resource
        if version3:
            b = bytes(string_to_write,'UTF-8')
            print(b)
            serialPort.write(bytes(string_to_write,'UTF-8'))
        else:
            serialPort.write(string_to_write.encode('utf-8'))
            #serialPort.write(string_to_write)
        serialLock.release() #release serial resource back out into big scary world
    else:
        print ("Change in %s to value %s not written since no live serial comm exists yet" %(tag,val))


# Specs
@socketio.on('serial select')
def action(port):
    global serialselection
    print ('serial port changed to %s' %(port))
    serialselection = port
    
@socketio.on('baud select')
def action(baud):
    global baudselection
    print ('baud changed to %s' %(baud))
    baudselection = baud

@socketio.on('csv state')
def csver(csv_val):
    global csv_default
    global csv_recent
    global current
    global archive
    global csv_yn
    global csvLock
    global csv_st
    if int(csv_val) == 0:
        print('closing csv files')
        csv_yn = 0
        csvLock.acquire()
        try:
            current.close()
            archive.close()
        except NameError:
            pass #did not exist yet...totes fine
        csvLock.release()
    else: #do other thing
        print('Trying opening csv files up!')
        csv_st = time.time()
        #current = open('./csv_files/current.csv',"w",encoding='utf8',newline='')
        #archive = open('./csv_files/'+str(int(time.time()))+'.csv',"w",encoding='utf8',newline='')
        try:
            current = open('./csv_files/current.csv',"w",**kwargs)
            archive = open('./csv_files/'+str(int(time.time()))+'.csv',"w",**kwargs)
            csv_default = csv.writer(archive)
            csv_recent = csv.writer(current)
            csvLock.acquire() 
            csv_default.writerow(['Time']+params_and_values)
            csv_recent.writerow(['Time']+params_and_values)

            csvLock.release()
            csv_yn = 1
            print ('CSV File Open successful')
        except:
            print("Failed to open CSV Files")
                
@socketio.on('serial connect request')
def connection(already_built):
    global serialConnected
    global serialPort
    global serialLock
    global alternate
    global isSetup
    already_built = eval(str(already_built))
    print("state of gui")
    print(already_built)
    isSetup = already_built['state'] #user this 
    print(isSetup)
    alternate = 0
    print ('Trying to connect to: ' + serialselection + ' ' + str(baudselection))
    print (serialLock)
    print (serialConnected)
    try:
        serialLock.acquire()
        print ("Lock acquired")
        serialPort = serial.Serial(serialselection, int(baudselection),timeout=4)
        print ('SerialPort')
        print ('Connected to ' + str(serialselection) + ' at ' + str(baudselection) + ' BAUD.')
        emit('serial connected', broadcast=True) #tells page to indicate connection (in button)
        serialPort.flushInput()
        #serialPort.flushOutput()
        serialLock.release()
        serialConnected = True #set global flag
    except:
        print ("Failed to connect with "+str(serialselection) + ' at ' + str(baudselection) + ' BAUD.')



@socketio.on('serial disconnect request')
def discon():
    global serialConnected
    global serialLock
    global serialPort
    print ('Trying to disconnect...')
    serialLock.acquire()
    serialPort.close()
    serialLock.release()
    serialConnected = False 
    emit('serial disconnected',broadcast=True)
    print ('Disconnected...good riddance' )

@socketio.on("disconnected")
def ending_it():
    print ("We're done")



@socketio.on('change')
def action(data):
    global system_parameters
    data = eval(str(data))
    system_parameters[data['id']][0]=float(data['val'])
    writeUpdates(system_parameters[data['id']][1],system_parameters[data['id']][0])

@socketio.on('all set from gui')
def action():
    global allGoodFromGUI
    allGoodFromGUI = True
    print("we are done from GUI Side")
    inform_dev()

def inform_dev():
    global serialPort
    global serialLock
    string_to_write = "SET\n"
    if serialConnected:
        serialLock.acquire() #claim serial resource
        if version3:
            serialPort.write(bytes(string_to_write,'UTF-8'))
        else:
            print(string_to_write)
            serialPort.write(string_to_write)
            serialPort.flushInput()
        serialLock.release() #release serial resource back out into big scary world
    else:
        print ("can't inform device since it isn't connected...what does this even mean")

@socketio.on('alternate state')
def action(alt):
    alt = int(alt)
    global alternate
    global alt_data
    if alt == 1:
        print ('%s changed to alternating at +/- %0.2f ' %(alt_data['param'],float(system_parameters[alt_data['param']][0])))
        alt_data['timer'] = time.time()
        alt_data['state'] = 1.0
        alternate = 1
    else:
        print ('%s changed to fixed at %0.2f' %(alt_data['param'],float(system_parameters[alt_data['param']][0])))
        alternate = 0
        



if __name__ == '__main__':
    socketio.run(app, port=3000, debug=True)

