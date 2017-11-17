#C:\Users\vaibhav\Documents\Python\RL\RL_SPIDER

import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import matplotlib.pyplot as plt

plt.axis([0, 1, -5, 5])
plt.ion()

data = [[i for i in range(100)]]
data = np.array(data, dtype=float)/10.0

target = np.sin(data)

data = data.reshape((1, 1, 100)) 
target = target.reshape((1, 1, 100)) 




#plt.pause(5)

x_test=[i for i in range(100,200)]
x_test=np.array(x_test).reshape((1,1,100))/10.0
y_test=np.sin(x_test)


model = Sequential()  
model.add(LSTM(100, input_shape=(1, 100),return_sequences=True))
model.add(Dense(100))
model.compile(loss='mean_absolute_error', optimizer='adam',metrics=['accuracy'])

for i in range(10):

	model.fit(data, target, nb_epoch=10, batch_size=1, verbose=2,validation_data=(x_test, y_test))
	predict = model.predict(data)
	plt.gcf().clear()
	plt.plot(data[0,0,:],predict[0,0,:])
	fig.canvas.draw()
	#plt.show()


