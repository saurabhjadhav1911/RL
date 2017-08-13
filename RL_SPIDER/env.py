#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git
from misc import *
import serial
class Env():
	"""docstring for Env"""
	def __init__(self,config):
		print('Env created')
		self.config=config
		#self.serial=get_Serial()
		self.default_action=config['Env_config']['default_action']

	def get_Serial(self):
		return serial.Serial(self.config['Serial_config']['port'],baudrate=self.config['Serial_config']['baud'],timeout=self.config['Serial_config']['timeout'])

	def reset(self):
		self.action(self.default_action)
		return self.read_state()

	def action(self,act):
		line="G "+" ".join(map(str,act))
		print(line)
		#self.serial.write(line)
	def read_state(self):
		return 34*[0]
	def run(self):
		pass
env=Env(read_config())
print(env.reset())