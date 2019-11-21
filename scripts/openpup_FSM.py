#!/usr/bin/env python

# FINITE STATE MACHINE NODE

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from std_msgs.msg import *
from numpy import *
import time


import inverse_kinematics
import servo_angles


class FSM():
	def __init__(self):
		
		self.dT = 0.005;
		self.timenow = time.time()
		self.oldtime = self.timenow

		self.timenow = rospy.Time.now()
		
		# set up your publishers with appropriate topic types

		self.FSM_action = rospy.Publisher('/action', String, self.actioncallback)
		self.FSM_direction = rospy.Publisher('/direction', String, self.directioncallback)

		# create loop
		rospy.Timer(rospy.Duration(self.dT), self.loop, oneshot=False)

		self.action = 'stand'
		self.direction = 'left'

		self.Wait = 1
		self.Back = 0
		self.TRight = 0
		self.SLeft = 0
		self.Forward = 0
		self.TLeft = 0
		self.SRight = 0


	def loop(self, event):

		# Block 1

		T0_EN = self.Wait or self.Back or self.TRight or self.SLeft
		T1_EN = self.Forward or self.TLeft or self.SRight

		# --------------------TIMER_0--------------------
		A_time0 = wait_time0 and T0_EN
		B_time0 = wait_time0 and not T0_EN
		C_time0 = timing_time0 and not T0_EN
		D_time0 = timing_time0 and T0_EN

		wait_time0 = B_time0 or C_time0
		timingt_time0 = A_time0 or D_time0

		if (A_time0):
			Start_time0 = time.time()

		if(timing_time):
			delta_t0 = time.time() - Start_time0

		else:
			delta_t0 = 0

		T0 = delta_t0 > 5
		#-----------------------------------------------

		#--------------------TIMER_1--------------------
		A_time1 = wait_time1 and T1_EN
		B_time1 = wait_time1 and not T1_EN
		C_time1 = timing_time1 and not T1_EN
		D_time1 = timing_time1 and T1_EN

		wait_time1 = B_time1 or C_time1
		timingt_time1 = A_time1 or D_time1

		if (A_time1):
			Start_time1 = time.time()

		if(timing_time):
			delta_t1 = time.time() - Start_time1

		else:
			delta_t1 = 0

		T1 = delta_t1 > 5
		#-----------------------------------------------

		# Block 2

		A = self.Wait and not T0
		B = self.Wait and T0
		C = self.Forward and not T1
		D = self.Forward and T1
		E = self.Back and not T0
		F = self.Back and T0
		G = self.TLeft and not T1
		H = self.TLeft and T1
		I = self.TRight and not T0
		J = self.TRight and T0
		K = self.SRight and not T1
		L = self.SRight and T1
		M = self.SLeft and not T0
		N = self.Sleft and T0

		# Block 3

		self.Wait = A or N
		self.Forward = B or C
		self.Back = D or E
		self.TLeft = F or G
		self.TRight = H or I
		self.SRight = J or K
		self.SLeft = L or M

		# Block 4

		if self.Forward:
			action = "forward"

		if self.Back:
			action = "backward"

		if self.SLeft:
			action = "sideways"
			direction = "left"

		if self.SRight:
			action = "sideways"
			direction = "right"

		if self.TLeft:
			action = "turn"
			direction = "left"

		if self.TRight:
			action = "turn"
			direction = "right"

		if self.Wait:
			action = "stand"

		self.action.publish(action)
		self.direction.publish(direction)


	def actioncallback(self,data):

		self.action = data.data

	def directioncallback(self,data):

		self.direction = data.data


# main function

def main(args):
	rospy.init_node('openpup_FSM', anonymous=True)
	myNode = FSM()

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	main(sys.argv)

	
 