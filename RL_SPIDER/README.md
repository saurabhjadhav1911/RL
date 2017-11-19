# RL on Robot Spider

### Dependancies

	numpy
	pyserial
	keras
	theano/tensorflow


## Hardware Environment

	#class Env in env.py file
	env=Env() 

**Reset** 

	#resets the environment and pull back the robot at starting position
	state=env.reset() 

**Step**
	
	state,reward,done=env.step(action)

**state**

sensor readings from 12 servos , 6 mpu , 4 pressure sensor and their derivatives

Serial Communication from Arduino

**reward** 

(proportional to distance calculated by image processing module , recieved by wifi from mobile)

wifi communication from android

**done** 
(end of the trial)

## Mathematical Simulator
## Agent


### Configuration

*config.json*

- formats and sizes of return variables ,functions  of of all modules
- serial configurations of communications with arduino
- ip and webpage info of commnicatuions via wifi


	#reads the configuarations
	
	from misc import *
	
	config=read_config()
	
### Multiprocessing

- Each block in algorithm ie. **Env, Agent, Simulator** is running as differant process using **python multiprocessing library**
- Other supporting componenets ie. **GUI , Plot , ROS display of mathematical simulator** are also seperate processes
- All processes communicate with each others using **multiprocessing Queue**
- **main.py** file run as **parent process** and has all function definations of target functions of child processes
- these function has target functions as **process_name_target** in main.py 


	def Env_process_target(recieve_que,send_que,config):
