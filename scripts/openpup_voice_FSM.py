#!/usr/bin/env python

# VOICE RECOGNITION FINITE STATE MACINE NODE

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from std_msgs.msg import *
from numpy import *
import time

import inverse_kinematics

class voice_FSM():
	def __init__(self):

		self.dT = 0.005
		self.timenow = time.time()
		self.oldtime = self.timenow

		self.timenow = rospy.Time.now()

		# set up your publishers with appropriate topics

		self.micsub = rospy.Subscriber("/mic_output", String, self.mic_callback)

		self.FSM_action = rospy.Publisher('/action', String, queue_size=1)
		self.FSM_direction = rospy.Publisher('/direction', String, queue_size=1)

		#creat loop
		rospy.Timer(rospy.Duration(self.dT), self.loop, oneshot=False)

		self.mic_string = 'stop'

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

		# returns booleans if one of the key words is heard

		self.dance_command = ('swivel' in self.mic_string) or \
		 				     ('dance' in self.mic_string) or \
					 		 ('little' in self.mic_string)

		self.down_command = ('down' in self.mic_string) or \
							('sit' in self.mic_string) or \
					 		('say it' in self.mic_string)

		self.stop_command = ('stop' in self.mic_string) or \
							('ready' in self.mic_string) or \
					 		('stand' in self.mic_string) or \
					 		('not' in self.mic_string)

		# Block 2

		self.A = self.Ready and not (self.dance_command or self.down_command)
		self.B = self.Ready and self.dance_command
		self.C = self.Ready and self.down_command
		self.D = self.Dance and not (self.stop_command or self.down_command)
		self.E = self.Dance and self.stop_command
		self.F = self.Dance and self.down_command
		self.G = self.Sit and not (self.stop_command or self.dance_command)
		self.H = self.Sit and self.dance_command
		self.I = self.Sit and self.stop_command

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

	def mic_callback(self,data):

		self.mic_string = data.data


# main function

def main(args):
	rospy.init_node('openpup_voice_FSM', anonymous=True)
	myNode = voice_FSM()

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	main(sys.argv)
