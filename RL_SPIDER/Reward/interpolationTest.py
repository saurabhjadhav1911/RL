import numpy as np 
from scipy import interpolate 
import matplotlib.pyplot as plt
import time

def interpolateReward( timeReqAt, timeArray, rewardArray):
	interpFunction  = interpolate.interp1d(timeArray, rewardArray, kind = 'cubic')
	t = interpFunction(timeReqAt)
	print (t)
	return t

x = np.arange(0,10)
y = np.exp(-x/4)*x
print(y)
xnew = np.arange(0,9,.2)
ynew = interpolateReward(xnew, x, y)
plt.plot(x, y, 'o', xnew, ynew, '*')
plt.show()