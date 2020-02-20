#!/usr/bin/env python

# LIDAR FINITE STATE MACHINE NODE

# check the publishers and subscribers to make sure they are okay

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from sensor_msgs.msg import Joy
from std_msgs.msg import *
from numpy import *
import time

import inverse_kinematics
import servo_angles
import lidar_quad_node

class LIDAR_FSM():
	def __init__(self):

		self.dT = 0.005
		self.timenow = time.time()
		self.oldtime = self.timenow

		self.timenow = rospy.Time.now()

		# set up your publishers with appropriate topics

		self.joy = rospy.Subscriber("/joy", Joy, self.wiimotecallback)
		self.lidar_obstacles = rospy.Subscriber("/lidar_obstacles", lidar_obstacles, self.lidarcallback)

		self.FSM_aciton = rospy.Publisher('/action', String, self.actioncallback)
		self.FSM_direction = rospy.Publisher('/direction', String, self.directioncallback)

		#create loop
		rospy.Timer(rospy.Duration(self.dT), self.loop, oneshot=False)

		self.joy = [0,0,   0,0,0,0,0]
		#          [A,B,home,+,-,1,2]

		self.lidar_obstacles = [    0,     0,    0,    0]
		#                      [Front, Right, Back, Left]

		self.action = 'stand'
		self.direction = 'left'

		self.Ready = 1
		self.Wait = 0
		self.Explore = 0
		self.Control = 0
		self.Stop = 0

		self.T0_EN = 0
		self.T0 = 0

		self.wait_time = 1
		self.timing_time = 0

		self.A_time = 0
		self.B_time = 0
		self.C_time = 0
		self.D_time = 0

		self.delta_t = 0
		self.Start_time = 0

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
		self.O = 0

		self.Straight = 0
		self.TL = 0
		self.TR = 0
		self.Ex_Stop = 0

		self.AE = 0
		self.BE = 0
		self.CE = 0
		self.DE = 0
		self.EE = 0
		self.FE = 0
		self.GE = 0
		self.HE = 0
		self.IE = 0
		self.JE = 0
		self.KE = 0
		self.LE = 0
		self.ME = 0
		self.NE = 0
		self.OE = 0
		self.OP = 0


	def loop(self, event):

		#Block 1

		self.T0_EN = self.Wait

		#--------------------TIMER_0-------------------------
		self.A_time = self.wait_time and self.T0_EN
		self.B_time = self.wait_time and not self.T0_EN
		self.C_time = self.timing_time and not self.T0_EN
		self.D_time = self.timing_time and self.T0_EN

		self.wait_time = self.B_time or self.C_time
		self.timing_time  =self.A_time or self.D_time

		if(self.A_time):
			self.Start_time = time.time()

		if(self.timing_time):
			self.delta_t = time.time() - self.Start_time

		else:
			self.delta_t = 0

		self.T0 = self.delta_t > 3
		#----------------------------------------------------

		# Block 2

		self.A = self.Ready and not (self.B or self.E or self.F)
		self.B = self.Ready and (self.joy[0] == 1)
		self.C = self.Stop and (self.joy[1] == 1)
		self.D = self.Control and (self.joy[2] == 1)
		self.E = self.Ready and (self.joy[5] == 1)
		self.F = self.Ready and (self.joy[3] == 1)
		self.G = self.Wait and not (self.H or self.T0)
		self.H = self.Wait and (self.joy[0] == 1)
		self.I = self.Wait and self.T0
		self.J = self.Explore and not (self.K or self.L)
		self.K = self.Explore and (self.joy[0] == 1)
		self.L = self.Explore and (self.joy[5] == 1)
		self.M = self.Control and (self.joy[3] == 1)
		self.N = self.Control and not (self.M or self.D)
		self.O = self.Stop and not (self.joy[1] == 1)

		# Block 3

		self.Ready = self.A or self.C or self.D
		self.Wait = self.F or self.G
		self.Explore = self.I or self.J or self.M
		self.Control = self.E or self.L or self.N
		self.Stop = self.B or self.H or self.K or self.O 

		# Block 4

		if self.Explore:

			# Block 2

			self.AE = self.Straight and (self.lidar_obstacles[0] == 0)
			self.BE = self.Straight and (self.lidar_obstacles[0] == 1) and (self.lidar_obstacles[1] == 1)
			self.CE = self.TL and (self.lidar_obstacles[0] == 1) and (self.lidar_obstacles[1] == 1)
			self.DE = self.TL and (self.lidar_obstacles[0] == 0)
			self.EE = self.Straight and (self.lidar_obstacles[0] == 1) and (self.lidar_obstacles[3] == 1)
			self.FE = self.TR and (self.lidar_obstacles[0] == 1) and (self.lidar_obstacles[3] == 1)
			self.GE = self.TR and (self.lidar_obstacles[0] == 0)
			self.HE = self.Straight and (self.lidar_obstacles[0] == 1) and (self.lidar_obstacles[1] == 1) and (self.lidar_obstacles[2] == 1) and (self.lidar_obstacles[3] == 1)
			self.IE = self.Ex_Stop and (self.lidar_obstacles[0] == 0)
			self.JE = self.Explore and (self.lidar_obstacles[3] == 0)
			self.KE = self.TL and (self.lidar_obstacles[0] == 1) and (self.lidar_obstacles[1] == 1) and (self.lidar_obstacles[2] == 1) and (self.lidar_obstacles[3] == 1)
			self.LE = self.Ex_Stop and (self.lidar_obstacles[1] == 0)
			self.ME = self.TR and (self.lidar_obstacles[0] == 1) and (self.lidar_obstacles[1] == 1) and (self.lidar_obstacles[2] == 1) and (self.lidar_obstacles[3] == 1)
			self.NE = self.Ex_Stop and (self.lidar_obstacles[0] == 1) and (self.lidar_obstacles[1] == 1) and (self.lidar_obstacles[2] == 1) and (self.lidar_obstacles[3] == 1)
			self.OE = self.TL and (self.lidar_obstacles[0] == 1) and (self.lidar_obstacles[3] == 1) and (self.lidar_obstacles[1] == 0)
			self.PE = self.TR and (self.lidar_obstacles[0] == 1) and (self.lidar_obstacles[1] == 1) and (self.lidar_obstacles[3] == 0)

			# Block 3

			self.Straight = self.AE or self.CE or self.FE or self.IE
			self.TL = self.BE or self.DE
			self.TR = self.EE or self.GE
			self.Ex_Stop = self.HE or self.JE

			# Block 4

			if self.Straight:
				self.action = "forward"

			if self.TL:
				self.action = "turn"
				self.direction = "left"

			if self.TR:
				self.action = "turn"
				self.direction = "right"

			if self.Ex_Stop:
				self.action = "stand"

			self.FSM_action.publish(self.action)
			self.FSM_direction.publish(self.direction)

		if self.Wait:
			self.action = "stand"

		if self.Stop:
			self.action = "stand"

		if self.Control:
			#insert code here that would transition to Wii remote FSM where we have complete control

		if self.Ready:
			self.action = "stand"

		self.FSM_action.publish(self.action)
		self.FSM_direction.publish(self.direction)


	def wiimotecallback(self,data):

		self.joy = data.buttons

	def lidarcallback(self,data):

		self.LIDAR = data.data

	def actioncallback(self,data):

		self.action = data.data

	def directioncallback(self,data):

		self.direction = data.data


# main function

def main(args):
	rospy.init_node('openpup_LIDAR_FSM', anonymous=True)
	myNode = LIDAR_FSM()

	try:
		rospy.sping()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	main(sys.argv)

