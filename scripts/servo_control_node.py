#!/usr/bin/env python

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from std_msgs.msg import *
from numpy import *
import time

import inverse_kinematics
import servo_angles

# ------------------
# SERVO CONTROL NODE
# ------------------

# this node receives the action and direction from the finite state machine,
# calls the IK functions to find the joint angles, and then sends them to the
# servo control board to move the pup


class servoPublisher():

	def __init__(self):

		rospy.logwarn("started servo controller")

		self.dT = 0.005;
		self.timenow = time.time()
		self.oldtime = self.timenow

		self.IK = inverse_kinematics.inverse_kinematics()
		self.servoAng = servo_angles.servo_angles()

		# subscribe to FSM
		self.FSM_action = rospy.Subscriber('/action', String, self.actioncallback)
		self.FSM_direction = rospy.Subscriber('/direction', String, self.directioncallback)

		# create loop
		rospy.Timer(rospy.Duration(self.dT), self.loop, oneshot=False)

		self.action = 'stand'
		self.direction = 'left'


	def loop(self, event):

		self.timenow = time.time()
		self.oldtime = self.timenow

		# find joint angles using the functions in inverse_kinematics.py
		myAngles = self.IK.JointAng(self.action, self.direction, self.timenow)

		# send joint angles to servo_angles.py for control
		self.servoAng.getServoAng(myAngles)


	def actioncallback(self,data):

		self.action = data.data

	def directioncallback(self,data):

		self.direction = data.data


# main function

def main(args):
	rospy.init_node('servo_control_node', anonymous=True)
	myNode = servoPublisher()

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	main(sys.argv)
