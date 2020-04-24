#!/usr/bin/env python

from numpy import *

# -----------------------
# INVERSE KINEMATICS: ARM
# -----------------------

class arm_IK():

	def __init__(self):

		# arm dimensions

		self.L1 = 16.0 	# piece connected to base, inches
		self.L2 = 20.0 	# middle piece, inches
		self.L3 = 5.0 	# end/tip, inches

		self.time_constant = 2.5 # in seconds

		# end-effector start location
		self.x_start = self.L3+self.L2-self.L1
		self.y_start = 0.0
		self.z_start = 0.0

		self.find_xyz('rest', [self.x_start, self.y_start, self.z_start], 0)


	# sets desired xyz of the pointer based on requested arm action (rest, press)
	def find_xyz(self, action, button_xyz, time):

		self.t = time

		# button location
		self.x_final = button_xyz[0]
		self.y_final = button_xyz[1]
		self.z_final = button_xyz[2]

		if (action == "rest"):

			# end-effector start location
			self.x = self.x_start
			self.y = self.y_start
			self.z = self.z_start

		if (action == "press"):

			# the first motion aligns the arm in the same plane as the button by
			# rotating the base and moving the end-effector to the final z-position
			if self.t < self.time_constant:
				self.x = self.x_start + self.x_start*cos(arctan(self.y_final/self.x_final))-self.x_start
				self.y = self.y_start + self.x_start*sin(arctan(self.y_final/self.x_final))-self.y_start
				self.z = self.z_final

			# the second motion, now aligned to the button, moves only the wrist
			# and elbow joints to approach the button parallel with the floor
			if self.t >= self.time_constant:
				self.x = self.x_final
				self.y = self.y_final
				self.z = self.z_final


	def joint_angles(self, action, button_xyz, time):

		self.find_xyz(action, button_xyz, time)

		self.A1, self.A2, self.A3, self.A4 = self.getJointAng(self.x, self.y, self.z)

		return [self.A1, self.A2, self.A3, self.A4]


	def getJointAng(self, x, y, z):

		d_xy = sqrt(x**2 + y**2)
		xp = d_xy

		if (x>0):
			Ad = arctan(z/(xp-self.L3))
		else:
			Ad = pi + arctan(z/(xp-self.L3))

		d_xz = sqrt((xp-self.L3)**2 + z**2)

		# base angle
		A1 = arcsin(y/d_xy)

		# shoulder angle
		A2 = Ad + arccos((self.L1**2 + d_xz**2 - self.L2**2)/(2*self.L1*d_xz))

		# elbow angle
		A3 = arccos((self.L1**2 + self.L2**2 - d_xz**2)/(2*self.L1*self.L2))

		# wrist angle (constrained so the end link is parallel with the ground)
		A4 = 2*pi - A2 - A3

		return A1, A2, A3, A4
