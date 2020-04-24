#!/usr/bin/env python

# ARM CONTROL NODE

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from std_msgs.msg import *
from numpy import *
import time

import arm_IK
import arm_angles


class arm_controller():

	def __init__(self):

		rospy.logwarn("started arm controller")

		self.dT = 0.005;
		self.timenow = time.time()    # current time
		self.starttime = time.time()  # start time of arm movement after recognizing button
		self.time_elapsed = 0.0

		self.IK = arm_IK.arm_IK()
		self.arm_angles = arm_angles.convert_angles()

		# subscribe to action and button location
		self.action_subscriber = rospy.Subscriber('/arm_action', String, self.actioncallback)
		self.button_subscriber = rospy.Subscriber('/button_xyz', Float32MultiArray, self.buttoncallback)

		# publish angles in radians to position controllers
		self.joint1_angle = rospy.Publisher('/openArm/joint1_position_controller/command', Float64, queue_size=1)
		self.joint2_angle = rospy.Publisher('/openArm/joint2_position_controller/command', Float64, queue_size=1)
		self.joint3_angle = rospy.Publisher('/openArm/joint3_position_controller/command', Float64, queue_size=1)
		self.joint4_angle = rospy.Publisher('/openArm/joint4_position_controller/command', Float64, queue_size=1)

		self.arm_action = 'rest'
		self.button_xyz = [0.0,0.0,0.0]

		# create loop
		rospy.Timer(rospy.Duration(self.dT), self.loop, oneshot=False)


	def loop(self, event):

		# initialize publish variables
		self.arm_ang1 = Float64()
		self.arm_ang2 = Float64()
		self.arm_ang3 = Float64()
		self.arm_ang4 = Float64()

		self.timenow = time.time()
		self.time_elapsed = self.timenow - self.starttime

		# find angles based on IK coordinate frame

		IK_angles = self.IK.joint_angles(self.arm_action, self.button_xyz, self.time_elapsed)

		# convert angles to arm controller coordinate frame
		self.arm_ang1, self.arm_ang2, self.arm_ang3, self.arm_ang4 = self.arm_angles.get_arm_angles(IK_angles)

		# publish angles to controllers
		self.joint1_angle.publish(self.arm_ang1)
		self.joint2_angle.publish(self.arm_ang2)
		self.joint3_angle.publish(self.arm_ang3)
		self.joint4_angle.publish(self.arm_ang4)


	def actioncallback(self,data):

		self.arm_action = data.data
		self.starttime = time.time()

	def buttoncallback(self,data):

		self.button_xyz = data.data


# main function

def main(args):
	rospy.init_node('arm_control_node', anonymous=True)
	myNode = arm_controller()

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	main(sys.argv)
