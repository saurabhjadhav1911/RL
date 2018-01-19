#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git

import numpy as np
import copy
import matplotlib.pyplot as plt
		

class RNN():
	"""docstring for RNN"""
	def __init__(self):
		self.alpha=0.1
		self.input_size=1
		self.hidden_size=16
		self.output_size=1

		self.Wih=2*np.random.random((self.input_size,self.hidden_size))-1

		self.Who=2*np.random.random((self.hidden_size,self.output_size))-1

		self.Whh=2*np.random.random((self.hidden_size,self.hidden_size))-1

		self.DWih=np.zeros_like(self.Wih)
		self.DWho=np.zeros_like(self.Who)
		self.DWhh=np.zeros_like(self.Whh)

		self.hidden_value=np.zeros((1,self.hidden_size))
		self.last_hidden_value=np.zeros_like(self.hidden_value)

	def generatedata(self):
		int2binary={}
		bin_dim=8
		largest_num=pow(2,bin_dim)
		#self.binary=
		a=list()
		b=list()
		c=list()
		binary=np.unpackbits(np.array([range(largest_num)],dtype=np.uint8).T,axis=1)
		for i in range(largest_num):
			int2binary[i]=binary[i]
		for i in range(10000):
			a_int=np.random.randint(largest_num/2)
			b_int=np.random.randint(largest_num/2)
			a.append(int2binary[a_int])
			b.append(int2binary[b_int])
			c_int=a_int+b_int
			c.append(int2binary[c_int])
		return np.array(a),np.array(b),np.array(c)

	def GenerateData(self):

		x=np.array(range(10000))*3.14/1000
		y=np.array(np.cos(x))
		x=x.reshape(10000,1)
		return x,y

	def plotdata(self,x,y):
		fig=plt.figure()
		ax1=fig.add_subplot(1,1,1)
		ax1.plot(y)
		plt.show()
	
	def forwardProp(self,x,y):
		self.hidden_value_out=np.dot(x,self.Wih)+np.dot(self.last_hidden_value,self.Whh)
		self.hidden_value=self.sigmoid(self.hidden_value_out)
		self.output_out=np.dot(self.hidden_value,self.Who)
		self.output=self.sigmoid(self.output_out)

		error=y-self.output
		self.DWho=-error*self.dsigmoid(self.output_out)
		self.DJDWho=np.dot(self.hidden_value.T,self.DWho)
		self.DWih=np.dot(self.DWho,self.dsigmoid(self.hidden_value_out))*self.Wih.T
		self.DJDWih=np.dot(x.T,self.DWih)
		self.DWhh=np.dot(self.DWho,self.dsigmoid(self.hidden_values_out))*self.Whh.T
		self.DJDWhh=np.dot(self.last_hidden_value.T,self.DWhh)
		#self.DWhh=np.dot(self.DWho,self.Whh.T)
		return self.DWho.shape,self.DWih.shape
		#return x.shape,np.dot(x,self.Wih).shape,np.dot(self.last_hidden_value,self.Whh).shape

	def tangent(self,x):
		return np.tanh(x)

	def dtangent(self,x):
		return 1-np.tanh(x)**2

	def sigmoid(self,x):
		return 1/(1+np.exp(-x))

	def dsigmoid(self,x):
		return self.sigmoid(x)*(1-self.sigmoid(x))


def main():
	rnn=RNN()
	x,y=rnn.GenerateData()
	#rnn.plotdata(x,y)
	print(rnn.forwardProp(x[0],y[0]))
if __name__ == '__main__':
	main()