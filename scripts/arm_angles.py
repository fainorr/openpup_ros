#!/usr/bin/env python

from numpy import *

# -----------------------
# INVERSE KINEMATICS: ARM
# -----------------------

class convert_angles():

	def __init__(self):

		self.get_arm_angles([0, 0, 0, 0])


	# convert angles from IK reference frame to arm global coordinate system
	def get_arm_angles(self, my_angles):

		ang1 = my_angles[0]
		ang2 = my_angles[1]
		ang3 = my_angles[2]
		ang4 = my_angles[3]

		arm_ang1 = ang1
		arm_ang2 = ang2 - pi/2
		arm_ang3 = ang3 - pi
		arm_ang4 = ang4 - pi

		return arm_ang1, arm_ang2, arm_ang3, arm_ang4
