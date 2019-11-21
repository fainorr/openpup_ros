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

		self.T0_EN = 0
		self.T0 = 0
		self.T1_EN = 0
		self.T1 = 0

		self.wait_time0 = 1
		self.timing_time0 = 0
		self.A_time0 = 0
		self.B_time0 = 0
		self.C_time0 = 0
		self.D_time0 = 0
		self.delta_t0 = 0
		self.Start_time0 = 0

		self.wait_time1 = 1
		self.timing_time1 = 0
		self.A_time1 = 0
		self.B_time1 = 0
		self.C_time1 = 0
		self.D_time1 = 0
		self.delta_t1 = 0
		self.Start_time1 = 0

		self.A = 0
		self.B = 0
		self.C = 0
		self.D = 0
		self.E = 0
		self.F = 0
		self.G = 0
		self.H = 0
		self.I = 0
		self.J = 0
		self.K = 0
		self.L = 0
		self.M = 0
		self.N = 0


	def loop(self, event):

		# Block 1

		self.T0_EN = self.Wait or self.Back or self.TRight or self.SLeft
		self.T1_EN = self.Forward or self.TLeft or self.SRight

		# --------------------TIMER_0--------------------
		self.A_time0 = self.wait_time0 and self.T0_EN
		self.B_time0 = self.wait_time0 and not self.T0_EN
		self.C_time0 = self.timing_time0 and not self.T0_EN
		self.D_time0 = self.timing_time0 and self.T0_EN

		self.wait_time0 = self.B_time0 or self.C_time0
		self.timing_time0 = self.A_time0 or self.D_time0

		if (self.A_time0):
			self.Start_time0 = time.time()

		if(self.timing_time0):
			self.delta_t0 = time.time() - self.Start_time0

		else:
			self.delta_t0 = 0

		self.T0 = self.delta_t0 > 5
		#-----------------------------------------------

		#--------------------TIMER_1--------------------
		self.A_time1 = self.wait_time1 and self.T1_EN
		self.B_time1 = self.wait_time1 and not self.T1_EN
		self.C_time1 = self.timing_time1 and not self.T1_EN
		self.D_time1 = self.timing_time1 and self.T1_EN

		self.wait_time1 = self.B_time1 or self.C_time1
		self.timing_time1 = self.A_time1 or self.D_time1

		if (self.A_time1):
			self.Start_time1 = time.time()

		if(self.timing_time1):
			self.delta_t1 = time.time() - self.Start_time1

		else:
			self.delta_t1 = 0

		self.T1 = self.delta_t1 > 5
		#-----------------------------------------------

		# Block 2

		self.A = self.Wait and not self.T0
		self.B = self.Wait and self.T0
		self.C = self.Forward and not self.T1
		self.D = self.Forward and self.T1
		self.E = self.Back and not self.T0
		self.F = self.Back and self.T0
		self.G = self.TLeft and not self.T1
		self.H = self.TLeft and self.T1
		self.I = self.TRight and not self.T0
		self.J = self.TRight and self.T0
		self.K = self.SRight and not self.T1
		self.L = self.SRight and self.T1
		self.M = self.SLeft and not self.T0
		self.N = self.SLeft and self.T0

		# Block 3

		self.Wait = self.A or self.N
		self.Forward = self.B or self.C
		self.Back = self.D or self.E
		self.TLeft = self.F or self.G
		self.TRight = self.H or self.I
		self.SRight = self.J or self.K
		self.SLeft = self.L or self.M

		# Block 4

		if self.Forward:
			self.action = "forward"

		if self.Back:
			self.action = "backward"

		if self.SLeft:
			self.action = "sideways"
			self.direction = "left"

		if self.SRight:
			self.action = "sideways"
			self.direction = "right"

		if self.TLeft:
			self.action = "turn"
			self.direction = "left"

		if self.TRight:
			self.action = "turn"
			self.direction = "right"

		if self.Wait:
			self.action = "stand"

		self.action.publish(self.action)
		self.direction.publish(self.direction)


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

	
 