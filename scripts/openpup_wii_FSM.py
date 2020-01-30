#!/usr/bin/env python

# FINITE STATE MACHINE NODE

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from sensor_msgs.msg import Joy
from std_msgs.msg import *
from numpy import *
from random import randint
import time


import inverse_kinematics
import servo_angles


class wii_FSM():
	def __init__(self):

		self.dT = 0.005;
		self.timenow = time.time()
		self.oldtime = self.timenow

		self.timenow = rospy.Time.now()

		# set up your publishers with appropriate topic types

		self.joy = rospy.Subscriber("/joy", Joy, self.wiimotecallback)

		self.FSM_action = rospy.Publisher('/action', String, queue_size=1)
		self.FSM_direction = rospy.Publisher('/direction', String, queue_size=1)

		# create loop
		rospy.Timer(rospy.Duration(self.dT), self.loop, oneshot=False)

		self.joy = [0,0,   0,0,0,0,0]
		#		   [A,B,home,+,-,1,2]

		self.action = 'stand'
		self.direction = 'left'

		self.Wait = 1
		self.Swivel = 0
		self.Down = 0
		self.Forward = 0
		self.TRight = 0
		self.SRight = 0
		self.TLeft = 0
		self.SLeft = 0

		self.A = 0
		self.B = 0
		self.C = 0
		self.D = 0
		self.E = 0
		self.F = 0
		self.G = 0
		self.H = 0


	def loop(self, event):

		# button A
		self.A = (self.Wait or self.Swivel or self.Down or self.Forward or self.TRight or self.SRight or self.TLeft or self.SLeft) \
					and (self.joy[0] == 1) and (self.joy[5] == 0) and (self.joy[6] == 0) and (self.joy[1] == 0)

		# buttons A and 2
		self.B = (self.Wait or self.Swivel or self.Down or self.Forward or self.TRight or self.SRight or self.TLeft or self.SLeft) \
					and (self.joy[0] == 1) and (self.joy[5] == 0) and (self.joy[6] == 1)

		# button 2 only
		self.C = (self.Wait or self.Swivel or self.Down or self.Forward or self.TRight or self.SRight or self.TLeft or self.SLeft) \
					and (self.joy[0] == 0) and (self.joy[5] == 0) and (self.joy[6] == 1)

		# buttons A and 1
		self.D = (self.Wait or self.Swivel or self.Down or self.Forward or self.TRight or self.SRight or self.TLeft or self.SLeft) \
					and (self.joy[0] == 1) and (self.joy[5] == 1) and (self.joy[6] == 0)

		# button 1 only
		self.E = (self.Wait or self.Swivel or self.Down or self.Forward or self.TRight or self.SRight or self.TLeft or self.SLeft) \
					and (self.joy[0] == 0) and (self.joy[5] == 1) and (self.joy[6] == 0)

		# button B only
		self.F = (self.Wait or self.Swivel or self.Down or self.Forward or self.TRight or self.SRight or self.TLeft or self.SLeft) \
					and (self.joy[0] == 0) and (self.joy[5] == 0) and (self.joy[6] == 0) and (self.joy[1] == 1)

		# both 1 and 2 OR no buttons
		self.G = (self.Wait or self.Swivel or self.Down or self.Forward or self.TRight or self.SRight or self.TLeft or self.SLeft) \
					and (((self.joy[5] == 1) and (self.joy[6] == 1)) or \
						 ((self.joy[0] == 0) and (self.joy[5] == 0) and (self.joy[6] == 0) and (self.joy[1] == 0)))

		# buttons A and B button
		self.H = (self.Wait or self.Swivel or self.Down or self.Forward or self.TRight or self.SRight or self.TLeft or self.SLeft) \
					and (self.joy[0] == 1) and (self.joy[1] == 1)

		self.Forward = self.A
		self.SRight = self.B
		self.TRight = self.C
		self.SLeft = self.D
		self.TLeft = self.E
		self.Swivel = self.F
		self.Wait = self.G
		self.Down = self.H

		if self.Forward:
			self.action = "forward"

		if self.Swivel:
			self.action = "swivel"

		if self.Down:
			self.action = "down"

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

		# print('Wait = ', self.Wait)
		# print('Swivel = ', self.Swivel)
		# print('Forward = ', self.Forward)
		# print('TRight = ', self.TRight)
		# print('SRight = ', self.SRight)
		# print('TLeft = ', self.TLeft)
		# print('SLeft = ', self.SLeft)

		self.FSM_action.publish(self.action)
		self.FSM_direction.publish(self.direction)


	def wiimotecallback(self,data):

		self.joy = data.buttons

	def actioncallback(self,data):

		self.action = data.data

	def directioncallback(self,data):

		self.direction = data.data


# main function

def main(args):
	rospy.init_node('openpup_wii_FSM', anonymous=True)
	myNode = wii_FSM()

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	main(sys.argv)
