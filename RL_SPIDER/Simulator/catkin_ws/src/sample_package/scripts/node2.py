#!/usr/bin/env python

#import rospy and msg libraries
import rospy
from std_msgs.msg import Int32
global num1, num2, inter
num1 = 0
num2 = 0
inter = 0

def assign_num1(temp_num):       # callback function for Subscriber of topic 'number1'
        global num1 
	num1 = temp_num.data
def assign_num2(temp_num):	#call back function for Subscriber of topic 'number2'
	global num2
        num2 = temp_num.data


rospy.init_node('node2')		#Initialisation of node2

pub_inter_result = rospy.Publisher('result_inter', Int32, queue_size=10)
#publisher of the topic result_inter (intermediate result) which is gonna be used in node3 for result calculation  #data-type integer
rate=rospy.Rate(1)		# set rate of message reception
rospy.Subscriber("number1",Int32, assign_num1)
#Initialisation of a Subscriber for the topic number1 #data-type integer
rospy.Subscriber("number2",Int32, assign_num2)
#Initialisation of a Subsciber for the topic number2  #data-type integer

while not rospy.is_shutdown():		#while rospy is not shutdown
	#calulate num1+num2 and store it in result_inter
        inter=num1+num2
	#inter_result is published over the topic result_inter
        pub_inter_result.publish(inter)
        rate.sleep()		#do nothing for specified delay in rate.

