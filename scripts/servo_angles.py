#!/usr/bin/env python

from __future__ import division
import Adafruit_PCA9685

from numpy import *
from math import *
import time

# ------------
# SERVO ANGLES
# ------------

# this function receives the IK joint angles, converts them to servo angles,
# and sends the correct pulse to the servo control board.

pwm = Adafruit_PCA9685.PCA9685()
zero = 0

class servo_angles():

	def __init__(self):

		# define offsets such that sending the servos to these offsets achieves
		# all angles of zero based on the defined coordinate frame; these are
		# relevant only to the specific orientation the servos were mounted
		# when assembling the pup and will change if the pup were re-assembled

		self.tib1_offset = 1800
		self.fem1_offset = 1720
		self.sh1_offset = 2000

		self.tib2_offset = 300
		self.fem2_offset = 400
		self.sh2_offset = 500

		self.tib3_offset = 1800
		self.fem3_offset = 1800
		self.sh3_offset = 2000

		self.tib4_offset = 300
		self.fem4_offset = 420
		self.sh4_offset = 500

		self.getServoAng([0,0,0,0,0,0,0,0,0,0,0,0])


	def getServoAng(self, myAngles):

		self.angs1 = myAngles[0]
		self.angf1 = myAngles[1]
		self.angt1 = myAngles[2]
		self.angs2 = myAngles[3]
		self.angf2 = myAngles[4]
		self.angt2 = myAngles[5]
		self.angs3 = myAngles[6]
		self.angf3 = myAngles[7]
		self.angt3 = myAngles[8]
		self.angs4 = myAngles[9]
		self.angf4 = myAngles[10]
		self.angt4 = myAngles[11]

		if self.angf1 > 0: self.angf1 = self.angf1 - 2*pi
		if self.angf3 > 0: self.angf3 = self.angf3 - 2*pi


		# convert to servo angles: for the pup's servos, there are roughly
		# 800 +- 40 counts per 90 degrees of rotation

		self.sangf1 = (840*self.angf1)/(pi/2)
		self.sangt1 = (800*self.angt1)/(pi/2)
		self.sangs1 = (760*self.angs1)/(pi/2)

		self.sangf2 = (780*self.angf2)/(pi/2)
		self.sangt2 = (760*self.angt2)/(pi/2)
		self.sangs2 = (760*self.angs2)/(pi/2)

		self.sangf3 = (800*self.angf3)/(pi/2)
		self.sangt3 = (760*self.angt3)/(pi/2)
		self.sangs3 = (760*self.angs3)/(pi/2)

		self.sangf4 = (800*self.angf4)/(pi/2)
		self.sangt4 = (760*self.angt4)/(pi/2)
		self.sangs4 = (760*self.angs4)/(pi/2)


		# send the servo angles to indivial servos via their appropriate
		# pins on the servo control board

		pwm.set_pwm(0, 0, self.tib2_offset + int(self.sangt2))		#port 0: right front tibia
		pwm.set_pwm(1, 0, self.fem2_offset + int(self.sangf2))		#port 1: right front femur
		pwm.set_pwm(2, 0, self.sh2_offset - int(self.sangs2))		#port 2: right front hip

		pwm.set_pwm(3, 0, self.tib1_offset + int(self.sangt1))		#port 3: left front tibia
		pwm.set_pwm(4, 0, self.fem1_offset + int(self.sangf1))		#port 4: left front femur
		pwm.set_pwm(5, 0, self.sh1_offset - int(self.sangs1))		#port 5: left front hip

		pwm.set_pwm(8, 0, self.fem3_offset + int(self.sangf3))		#port 8: left back femur
		pwm.set_pwm(9, 0, self.tib3_offset + int(self.sangt3))		#port 9: left back tibia
		pwm.set_pwm(10, 0, self.sh3_offset - int(self.sangs3))		#port 10: left back hip

		pwm.set_pwm(12, 0, self.fem4_offset + int(self.sangf4))		#port 12: right back femur
		pwm.set_pwm(7, 0, self.tib4_offset + int(self.sangt4))		#port 7: right back tibia
		pwm.set_pwm(13, 0, self.sh4_offset - int(self.sangs4))		#port 11: right back hip


	def set_servo_pulse(self, channel, pulse):
		pulse_length = 1000000
		pulse_length //=60
		print('{0}us per bit' .format (pulse_length))
		pulse *= 1000
		pulse //= pulse_length
		pwm.set_pwm(channel, 0, pulse)
		pwm.set_pwm_freq(100)
