#C:\Users\vaibhav\Documents\Python\RL\RL_SPIDER

import numpy as np


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import matplotlib.pyplot as plt

fig=plt.gcf()
fig.canvas.draw()
fig.show()

x=np.array([i for i in range(0,100)])
data = np.zeros((80, 1, 100))
data[0,0,50:]=1.0
target = np.zeros((80, 1, 100))
for t in range(80):
	for i in range(100):
		target[t,0,i] = data[t,0,i]*((1-np.exp(-(i-t)/5.0)))


plt.gcf().clear()

#plt.plot(data[0,0,:])
plt.plot(x,target[0,0,:])
fig.canvas.draw()


def main():


	#plt.pause(5)

	x_test = np.zeros((1, 1, 100))
	x_test[0,0,30:]=1.0
	y_test = np.zeros((1, 1, 100))
	for i in range(100):
		y_test[0,0,i] = x_test[0,0,i]*((1-np.exp(-(i-30)/5.0)))



	model = Sequential()  
	model.add(LSTM(100, input_shape=(1, 100),return_sequences=True))
	model.add(Dense(100))
	model.compile(loss='mean_absolute_error', optimizer='adam',metrics=['accuracy'])
	try:
		model.load_weights("lstm.model")
		print('weights loaded ')
	except:
		print('weights not loaded ')

	for i in range(10):

		model.fit(data, target, nb_epoch=10, batch_size=1, verbose=2,validation_data=(x_test, y_test))
		predict = model.predict(x_test)
		plt.gcf().clear()
		plt.plot(x,predict[0,0,:])
		plt.plot(x,y_test[0,0,:])
		predict = model.predict(data)
		plt.plot(x,predict[0,0,:])
		plt.plot(x,target[0,0,:])
		fig.canvas.draw()
		#plt.show()
	model.save_weights("lstm.model")
main()
plt.pause(10)
