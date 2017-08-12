#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git


try:
	from misc import *
	
except Exception as e:
	print(e)
	logname=__file__.replace('.py','')
	logname+='.log'
	print(logname)
	with open(logname,"w") as f:
			f.write(str(e))
