#!/usr/bin/env python

#import rospy and msg libraries
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import String
from std_msgs.msg import Float64
global inter, num3, res, op,p,q
inter = 0
num3 = 0
res=0
op = 0
p=0
q=0
def operator_fn(msg):			# callback function for the subscriber of the topic operator
	global op			#based on the message variable op are given values of 0,1,2,3 for addition, subtraction, multiplication and division respectively
	if msg.data=="add":
		op=0
	elif msg.data=="sub":
		op=1
	elif msg.data=="mul":
		op=2
	elif msg.data=="div":
		op=3

def assign_inter(temp):	# callback function for the subscriber of the topic result_inter
        global inter
        inter = temp.data
	# intermediate result is stored in variable inter_result_int

def assign_num3(temp):		#callback function for the subscriber of the topic number3
        global num3 
        num3 = temp.data
	#number3 is stored in the variable num3

rospy.init_node("node3")	#Initialisation of NODE3

rospy.Subscriber("result_inter",Int32, assign_inter)
#Initialisation of Subscriber for the topic result_inter   #data-type integer
rospy.Subscriber("number3",Int32, assign_num3)
#Initialisation of Subscriber for the topic number3 #data-type integer
rospy.Subscriber("operator",String, operator_fn)
#Initiatlisation of Subscriber for the topic operator #data-type string
pub_final_result = rospy.Publisher('result', Float64, queue_size=10)
#Initialisation of publisher for the topic result(final result)  #data-type float

rate=rospy.Rate(1) #Set the rate for message reception

while not rospy.is_shutdown(): #iterate until rospy is not shutdonw
        
        #Since we were getting two outputs we caliberated the function acccording to the values to provide stable output
        #p and q have been used for the same purpose        
        if inter==(2*num3 -3):
        	if op==0:		#apply operations 
             		res=inter+num3	
		
		elif op==1:
			res=inter-num3	
		
		elif op==2:
	     		res=inter*num3	

		elif op==3:
	     		res=float(inter)/float(num3)
        else:
             p=num3
             q=inter+2
             if op==0:		#apply operations 
             		res=q+p	
		
             elif op==1:
			res=q-p	
		
	     elif op==2:
	     		res=q*p

	     elif op==3:
	     		res=float(q)/float(p)	
        
        
        pub_final_result.publish(res)
	#pulishing the final result over the topic result (pub_res is the object name here)
        rate.sleep()		#do nothing for specified delay in rate.
