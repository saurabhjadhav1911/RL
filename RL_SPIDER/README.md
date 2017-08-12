# RL on Robot Spider

## Hardware Environment

	#class Env
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
