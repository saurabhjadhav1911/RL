import numpy as np 
from scipy import interpolate 
import matplotlib.pyplot as plt
import time

def interpolateReward( timeReqAt, timeArray, rewardArray):
	interpFunction  = interpolate.interp1d(timeArray, rewardArray, kind = 'cubic')
	t = interpFunction(timeReqAt)
	return t

x = np.arange(0,4)
y = np.exp(-x/4)*x
xnew = np.array(0.3)


for i in range(0,1000):
	start = time.time()
	ynew = interpolateReward(xnew, x, y)
stop = time.time()

print(start)
print(stop)
print(stop - start)
plt.plot(x, y, 'o', xnew, ynew, '*')
plt.show()