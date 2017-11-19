#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL\RL_SPIDER
#https://github.com/saurabhjadhav1911/RL.git
#C:\Users\Public\RL\ABC\ABC
#C:\Users\vaibhav\Documents\Python\RL\RL_SPIDER


import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import matplotlib.pyplot as plt


fig=plt.gcf()
fig.canvas.draw()


x=np.array([i for i in range(0,100)])
data = np.zeros((1,100, 1))
data[0,30:,0]=1.0
target= np.zeros((1,100,1))
for i in range(100):
	target[0,i,0] = data[0,i,0]*((1-np.exp(-(i-30)/5.0)))


plt.gcf().clear()
#plt.plot(data[0,0,:])
plt.plot(target[0,:100,0])
plt.plot(data[0,:100,0])
fig.canvas.draw()
plt.pause(0.001)


x_test = np.zeros((1,100,1))
x_test[0,50:,0]=1.0
y_test = np.zeros((1,100,1))

for i in range(100):
	y_test[0,i,0] = x_test[0,i,0]*((1-np.exp(-(i-50)/5.0)))


model = Sequential()  
model.add(LSTM(6, return_sequences=True, input_shape=(None, 1)))
model.add(LSTM(6,return_sequences=True))
model.add(Dense(1))
model.compile(loss='mse', optimizer='rmsprop',metrics=['accuracy'])

try:
	model.load_weights("lstmmin_size_corrected.model")
	print('weights loaded ')
except:
	print('weights not loaded ')

for i in range(10):

	model.fit(data, target, epochs=10, batch_size=1, verbose=2,validation_data=(x_test, y_test))
	predict = model.predict(x_test)
	plt.gcf().clear()
	predict = model.predict(data)
	plt.plot(x,predict[0,:,0])
	plt.plot(x,target[0,:,0])
	fig.canvas.draw()
	plt.pause(0.01)
#plt.sho

def check_predict(inp,exp_out):

	inp=inp.reshape((1,100,1))
	exp_out=exp_out.reshape((1,100,1))
	predict = model.predict(inp)
	plt.gcf().clear()
	plt.plot(x,predict[0,:,0])
	plt.plot(x,inp[0,:,0])
	plt.plot(x,exp_out[0,:,0])
	plt.pause(5)

x_test = np.zeros((1,100,1))
x_test[0,10:,0]=1.0
y_test = np.zeros((1,100,1))
for i in range(100):
	y_test[0,i,0] = x_test[0,i,0]*((1-np.exp(-(i-10)/5.0)))

check_predict(x_test,y_test)

model.save_weights("lstmmin_size_corrected.model")
print('weights saved')
