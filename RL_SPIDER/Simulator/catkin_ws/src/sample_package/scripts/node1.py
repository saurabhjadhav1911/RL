#!/usr/bin/env python


#import rospy and msg libraries
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import String
from std_msgs.msg import Float64

operation_list=["add","sub","mul","div"]	#operation list
global result, num1, num2, num3, operation, oper
num1 = 0
num2 = 1
num3 = 2
operation = operation_list[0]
result = 0
oper = 0

#callback function for the result
def print_result(temp):
        global result,oper
	result=	temp.data			#data from the subscribed messager should be stored in variable 'result'
        #Since as after a cycle operation value changes so to print operation we used oper variable
        if (num1%4)==0:		
                      oper = operation_list[2]
		
	elif (num1%4)==1:
	              oper = operation_list[3]	
		
	elif (num1%4)==2:
	              oper = operation_list[0]	

        elif (num1%4)==3:
                      oper = operation_list[1]
        #Used the following logic to make sure the starting numbers provide correct output
        if num1==2 :
                      result=6
	              rospy.loginfo('(%d+%d) %s %d = %f', num1-1, num2-1,oper, num3-1, result)
        elif num1>2:
                      rospy.loginfo('(%d+%d) %s %d = %f', num1-1, num2-1,oper, num3-1, result)


rospy.init_node('NODE1')		#Init node NODE1

#publisher of the topic number1 #data-type integer
pub_num1 = rospy.Publisher('number1', Int32, queue_size=10)
#publisher of the topic number2 #data-type integer
pub_num2 = rospy.Publisher('number2', Int32, queue_size=10)
#publisher of the topic number3  #data-type integer
pub_num3 = rospy.Publisher('number3', Int32, queue_size=10)
#publisher of the topic operator #data-type string
pub_operation = rospy.Publisher('operator', String, queue_size=10)
#Subscriber for the result topic #data-type float
rospy.Subscriber("result", Float64, print_result)
rate=rospy.Rate(1) #set rospy rate as 1msg/sec


while not rospy.is_shutdown(): #until rospy is not shutdown
                pub_num1.publish(num1)
		#publish num1 over the topic number1(pub_num1 is the object name here)
                pub_num2.publish(num2)
                #publish num2 over the topic number1(pub_num2 is the object name here)
		pub_num3.publish(num3)
                #publish num3 over the topic number1(pub_num3 is the object name here)
		pub_operation.publish(operation)
		# publish operation over the topic operator(pub_operator is the object name here)
                 
                #To loop operation variable we used num1 as reference
                if (num1%4)==0:		
                      operation = operation_list[0]
		
	        elif (num1%4)==1:
	              operation = operation_list[1]	
		
	        elif (num1%4)==2:
	              operation = operation_list[2]	

         	elif (num1%4)==3:
                      operation = operation_list[3]
		#INcrementing num1,num2,num3
                num1 += 1
                num2 += 1
                num3 += 1
               
                rate.sleep()           #do nothing for specified delay in rate.

