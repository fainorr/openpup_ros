#!/usr/bin/env python

# VOICE RECOGNITION FINITE STATE MACINE NODE

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from std_msgs.msg import *
from numpy import *
import time

import inverse_kinematics
import servo_angles
# import voice recognition stuff

class Voice_FSM():
	def __init__(self):

		self.dT = 0.005
		self.timenow = time.time()
		self.oldtime = self.timenow

		self.timenow = rospy.Time.now()

		# set up your publishers with appropriate topics

		self.FSM_action = rospy.Publisher('/action', String, self.actioncallback)
		self.FSM_direction = rospy.Publusher('/direction', String, self.directioncallback)
		# insert needed voice recognition stuff

		#creat loop
		rospy.Timer(rospy.Duration(self.dT), self.loop, oneshot=False)

		self.action = 'stand'
		self.direction = 'left'

		self.Ready = 1
		self.Dance = 0
		self.Sit = 0

		self.A = 0
		self.B = 0
		self.C = 0
		self.D = 0
		self.E = 0
		self.F = 0
		self.G = 0
		self.H = 0
		self.I = 0


	def loop(self, event):

		# Block 1

		# Block 2

		self.A = self.Ready and not # any of the commands
		self.B = self.Ready and # command for Dance
		self.C = self.Ready and # command for Sit
		self.D = self.Dance and not # any of the commands
		self.E = self.Dance and # command for Stop
		self.F = self.Dance and # command for Sit
		self.G = self.Sit and not # any of the commands
		self.H = self.Sit and # command for Dance
		self.I = self.Sit and # command for Stop

		# Block 3

		self.Ready = self.A or self.E or self.I
		self.Dance = self.B or self.D or self.H
		self.Sit = self.C or self.F or self.G

		# Block 4

		if self.Ready:
			self.action = "stand"

		if self.Dance:
			self.action = "swivel"

		if self.Sit:
			self.action = "down"

		self.FSM_action.publish(self.action)
		self.FSM_direction.publish(self.direction)

	def actioncallback(self,data):

		self.action = data.data

	def directioncallback(self,data):

		self.direction = data.data


# main function

def main(args):
	rospy.init_node('openpup_Voice_FSM', anonymous=True)
	myNode = Voice_FSM()

	try:
		rospy.sping()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	main(sys.argv)