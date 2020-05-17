#!/usr/bin/env python

#FINITE STATE MACHINE NODE

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from sensor_msgs.msg import Joy
from std_msgs.msg import *
from numpy import *
import time

# -------------------------
# FINITE STATE MACHINE NODE -- ultrasonic
# -------------------------

# this finite state machine controls the pup using inputs from the ultrasonic
# sensor to test its ability to detect obstacles

class ultra_FSM():
	def __init__(self):

		rospy.logwarn("started FSM")

		# set threshhold distance in centimeters to trigger obstacle avoidance
		self.threshhold_dist = 20.0
		self.ultrasonic_value = 30.0
		self.Dst = False

		self.dT = 0.005;
		self.timenow = time.time()
		self.oldtime = self.timenow

		self.timenow = rospy.Time.now()

		# subscribe to wii remote and ultrasonic sensor
		self.joy = rospy.Subscriber("/joy", Joy, self.wiimotecallback)
		self.ultra_subscriber = rospy.Subscriber('/sonar_dist', Float32, self.ultracallback)

		# publish the action and direction
		self.FSM_action = rospy.Publisher('/action', String, queue_size=1)
		self.FSM_direction = rospy.Publisher('/direction', String, queue_size=1)

		# create loop
		rospy.Timer(rospy.Duration(self.dT), self.loop, oneshot=False)

		self.joy = [0,0,   0,0,0,0,0]
		#          [A,B,home,+,-,1,2]

		self.action = 'stand'
		self.direction = 'left'

		self.Ready = 1
		self.Wait = 0
		self.Forward = 0
		self.Strafe = 0
		self.Turn = 0
		self.Stop = 0

		self.T0_EN = 0
		self.T0 = 0
		self.T1_EN = 0
		self.T1 = 0
		self.T2_EN = 0
		self.T2 = 0

		self.wait_time0 = 1
		self.timing_time0 = 0
		self.wait_time1 = 1
		self.timing_time1 = 0
		self.wait_time2 = 1
		self.timing_time2 = 0

		self.A_time0 = 0
		self.B_time0 = 0
		self.C_time0 = 0
		self.D_time0 = 0
		self.A_time1 = 0
		self.B_time1 = 0
		self.C_time1 = 0
		self.D_time1 = 0
		self.A_time2 = 0
		self.B_time2 = 0
		self.C_time2 = 0
		self.D_time2 = 0

		self.delta_t0 = 0
		self.Start_time0 = 0
		self.delta_t1 = 0
		self.Start_time1 = 0
		self.delta_t2 = 0
		self.Start_time2 = 0

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
		self.P = 0
		self.Q = 0
		self.R = 0
		self.S = 0


	def loop(self, event):

		# FSM blocks

		# --- Block 1 ---

		self.T0_EN = self.Wait
		self.T1_EN = self.Strafe
		self.T2_EN = self.Turn

		# TIMER 0
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

		self.T0 = self.delta_t0 > 1

		# TIMER 1
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

		# TIMER 2
		self.A_time2 = self.wait_time2 and self.T2_EN
		self.B_time2 = self.wait_time2 and not self.T2_EN
		self.C_time2 = self.timing_time2 and not self.T2_EN
		self.D_time2 = self.timing_time2 and self.T2_EN

		self.wait_time2 = self.B_time2 or self.C_time2
		self.timing_time2 = self.A_time2 or self.D_time2

		if (self.A_time2):
			self.Start_time2 = time.time()

		if(self.timing_time2):
			self.delta_t2 = time.time() - self.Start_time2

		else:
			self.delta_t2 = 0

		self.T2 = self.delta_t2 > 5


		# --- Block 2 ---

		self.A = self.Ready and not (self.joy[0] == 1) and not (self.joy[1] == 1)
		self.B = self.Ready and (self.joy[0] == 1)
		self.C = self.Wait and not (self.joy[1] == 1) and not self.T0
		self.D = self.Wait and self.T0 and not self.Dst
		self.E = self.Forward and not (self.joy[1] == 1) and not self.Dst
		self.F = self.Forward and self.Dst
		self.G = self.Wait and self.T0 and self.Dst
		self.H = self.Strafe and self.T1 and not self.Dst
		self.I = self.Strafe and not (self.joy[1] == 1) and not self.T1
		self.J = self.Strafe and self.Dst and self.T1
		self.K = self.Turn and not (self.joy[1] == 1) and not self.T2
		self.L = self.Turn and self.T2
		self.M = self.Turn and (self.joy[1] == 1)
		self.N = self.Wait and (self.joy[1] == 1)
		self.O = self.Forward and (self.joy[1] == 1)
		self.P = self.Strafe and (self.joy[1] == 1)
		self.Q = self.Stop and not (self.joy[2] == 1)
		self.R = self.Stop and (self.joy[2] == 1)
		self.S = self.Ready and (self.joy[1] == 1)


		# --- Block 3 ---

		self.Ready = self.A or self.R
		self.Wait = self.B or self.C or self.H or self.L
		self.Forward = self.D or self.E
		self.Strafe = self.F or self.G or self.I
		self.Turn = self.J or self.K
		self.Stop = self.M or self.N or self.O or self.P or self.Q or self.S


		# --- Block 4 ---

		if self.Forward:
			self.action = "forward"

		if self.Strafe:
			self.action = "sideways"
			self.direction = "right"

		if self.Turn:
			self.action = "turn"
			self.direction = "right"

		if self.Wait or self.Stop or self.Ready:
			self.action = "stand"

		self.FSM_action.publish(self.action)
		self.FSM_direction.publish(self.direction)

	def wiimotecallback(self,data):

		self.joy = data.buttons

	def ultracallback(self,data):

		self.ultrasonic_value = data.data
		self.Dst = (self.ultrasonic_value <= self.threshhold_dist)

# main function

def main(args):
	rospy.init_node('openpup_ultra_FSM', anonymous=True)
	myNode = ultra_FSM()

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	main(sys.argv)
