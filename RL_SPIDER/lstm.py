#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL
#https://github.com/saurabhjadhav1911/RL.git

import numpy as np
import matplotlib.pyplot as plt
class LSTM():
    """docstring for LSTM"""
    def __init__(self, input_size,hidden_size,output_size,n):

        self.input_size=input_size
        self.hidden_size=hidden_size
        self.output_size=output_size
        self.n=n
        self.lr=0.001
        self.Wf=np.random.random((self.hidden_size+self.input_size+1,self.hidden_size))
        self.Wi=np.random.random((self.hidden_size+self.input_size+1,self.hidden_size))
        self.Wc=np.random.random((self.hidden_size+self.input_size+1,self.hidden_size))
        self.Wo=np.random.random((self.hidden_size+self.input_size+1,self.hidden_size))
        self.Wout=np.random.random((self.hidden_size,self.output_size))
        self.reset()

    def reset(self):
        n=self.n
        self.cell_state=np.zeros((1,self.hidden_size))
        self.hidden_state=np.zeros((1,self.hidden_size))
        self.y=np.zeros((1,self.output_size))

        self.cell_states=np.zeros((n,1,self.hidden_size))
        self.forget_gates=np.zeros((n,1,self.hidden_size))
        self.input_gates=np.zeros((n,1,self.hidden_size))
        self.cell_state_gate_temp=np.zeros((n,1,self.hidden_size))
        self.hidden_states=np.zeros((n,1,self.hidden_size))
        self.outputs=np.zeros((n,1,self.hidden_size))
        self.x_stack=np.zeros((n,1,self.input_size+self.hidden_size+1))
        self.ys=np.zeros((n,1,self.output_size))

    def forward(self,X,t):
        
        x=np.hstack((self.hidden_state,X,np.ones((1,1))))
        self.x_stack[t]=x
        forget_gate=self.sigmoid(np.dot(x,self.Wf)) 
        input_gate=self.sigmoid(np.dot(x,self.Wi))
        cell_state_gate_temp=self.tangent(np.dot(x,self.Wc))    
        self.cell_state=(forget_gate*self.cell_state)+(input_gate*cell_state_gate_temp)
        self.output=self.sigmoid(np.dot(x,self.Wo))
        self.hidden_state=self.output*self.tangent(self.cell_state)
        self.y=4*(self.sigmoid(np.dot(self.hidden_state,self.Wout))-1)

        self.cell_states[t]=self.cell_state

        self.forget_gates[t]=forget_gate
        self.input_gates[t]=input_gate
        self.cell_state_gate_temp[t]=cell_state_gate_temp
        self.hidden_states[t]=self.hidden_state
        self.outputs[t]=self.output
        self.ys[t]=self.y

        return self.y
    def check_nan(self,inp):
        if np.max(inp)>10000:
            raise('here')
        return inp
    def train_step(self,x,y):
        self.reset()
        #x=np.hstack((self.hidden_state,X,np.ones((1,1))))
        self.Derror=np.zeros_like(self.ys)
        self.Dcell_states=np.zeros_like(self.cell_states)
        self.Dforget_gates=np.zeros_like(self.forget_gates)
        self.Dinput_gates=np.zeros_like(self.input_gates)
        self.Dcell_state_gate_temp=np.zeros_like(self.cell_state_gate_temp)
        self.Dhidden_states=np.zeros_like(self.hidden_states)
        self.Doutputs=np.zeros_like(self.outputs)
        self.Dx_stack=np.zeros_like(self.x_stack)
        #self.Dys=np.zeros_like(self.ys)
        dc0=np.zeros_like(self.cell_state)
        for t in range(len(x)):
            self.forward([[x[t]]],t)
        
        for t in reversed(range(len(x))):
            self.Derror[t]=((self.ys[t]-[[y[t]]])*self.sigmoid_derivative(self.ys[t]))
            #print(t)

            self.Dhidden_states[t]+=(np.dot(self.Derror[t],self.Wout.T)*self.sigmoid_derivative(self.hidden_states[t]))
            np.clip(self.Dhidden_states,-100,100,out=self.Dhidden_states)
            self.Dcell_states[t]+=(self.outputs[t]*(1-(self.dtangent(self.cell_states[t]))**2)*self.Dhidden_states[t])
            if t>0:
                self.Dcell_states[t-1]+=self.Dcell_states[t]*self.forget_gates[t]
                self.Dforget_gates[t]=(self.cell_states[t]*self.cell_states[t-1])*self.sigmoid_derivative(self.forget_gates[t])
            else:
                self.Dcell_states[0]+=dc0
                self.Dforget_gates[t]=self.cell_states[t]*dc0

            self.Doutputs[t]=self.Dhidden_states[t]*self.tangent(self.cell_states[t])*self.sigmoid_derivative(self.outputs[t])
            self.Dinput_gates[t]=self.Dcell_states[t]*self.cell_state_gate_temp[t]*self.sigmoid_derivative(self.input_gates[t])
            self.Dcell_state_gate_temp[t]=self.cell_states[t]*self.input_gates[t]*(1-(self.cell_state_gate_temp[t]**2))

            DJDWout=np.dot(self.hidden_states[t].T,self.Derror[t])
            DJDi=np.dot(self.x_stack[t].T,self.Dinput_gates[t])
            DJDf=np.dot(self.x_stack[t].T,self.Dforget_gates[t])
            DJDc=np.dot(self.x_stack[t].T,self.Dcell_state_gate_temp[t])
            DJDo=np.dot(self.x_stack[t].T,self.Doutputs[t])

            self.Dhidden_states[t-1]+=((np.dot(self.Dinput_gates[t],self.Wi.T)+np.dot(self.Dforget_gates[t],self.Wf.T)+np.dot(self.Doutputs[t],self.Wo.T)+np.dot(self.Dcell_state_gate_temp[t],self.Wc.T))[:,:self.hidden_size])

            self.Wout-=self.lr*DJDWout
            self.Wo-=self.lr*DJDo
            self.Wi-=self.lr*DJDi
            self.Wf-=self.lr*DJDf
            self.Wc-=self.lr*DJDc

            
    def tangent(self,x):
        return np.tanh(x)

    def dtangent(self,x):
        return 1-np.tanh(x)**2

    def sigmoid(self,x):
        return 1/(1+np.exp(-x))

    def sigmoid_derivative(self,x):
        return x*(1-x)

    def dsigmoid(self,x):
        return self.sigmoid(x)*(1-self.sigmoid(x))


def main():
    lstm=LSTM(1,5,1,100)
    x=np.array(range(100))/100.0
    #print(x)
    y=np.sin(4*3.14*x)
    #print(y)
    
    plt.axis([0, 1, -5, 5])
    plt.ion()

    for i in range(1000):
        for i in range(100):
        	lstm.train_step(x,y)
        plt.pause(0.05)
        yt=np.copy(lstm.ys)
        yt=yt.reshape(x.shape)
        plt.gcf().clear()
        plt.plot(x,y)
        plt.plot(x,yt)


if __name__ == '__main__':
    main()
        
