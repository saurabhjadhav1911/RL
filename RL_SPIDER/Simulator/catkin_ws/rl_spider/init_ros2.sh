
echo "##############################################  1st ########################################################################"
source /opt/ros/indigo/setup.bash
cd ~/catkin_ws/ && catkin_make && source devel/setup.sh

roscore &
killall python
echo "################################################ 2nd #######################################################################"
rosrun rl_spider custom_joint_state_publisher &

echo "################################################ 3nd #######################################################################"
roslaunch rl_spider display.launch &


echo "################################################ 4nd #######################################################################"
python ~/catkin_ws/src/rl_spider/scripts/Math_Simulator_ROS_GUI.py


