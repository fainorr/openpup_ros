#!/usr/bin/env python

from numpy import *
# from matplotlib.pyplot import *

# -----------------------
# INVERSE KINEMATICS: 3-D
# -----------------------

class inverse_kinematics():

	def __init__(self):

		# robot dimensions

		self.lf = 2.70 # femur, inches
		self.lt = 2.60 # tibia, inches
		self.ls = 1.40 # shoulder offset, inches

		self.find_xyz('stand', 'left', 0)

	def find_xyz(self, action, direction, time):

		self.t = time

		if (action == "stand"):

			x_center = 0.5
			y_center = -1
			z_center = -4

			self.x1 = x_center
			self.y1 = y_center
			self.z1 = z_center

			self.x2 = x_center
			self.y2 = y_center
			self.z2 = z_center

			self.x3 = x_center
			self.y3 = y_center
			self.z3 = z_center

			self.x4 = x_center
			self.y4 = y_center
			self.z4 = z_center

		if (action == "forward"):
			leg_pace = 6.0 # pace of gait

			x_center = -0.2
			x_stride = 1

			y_center = -1
			y_offset = 0

			z_center = -4.5
			z_lift = 1

			leg1_offset = 0			# front left
			leg2_offset = pi		# front right
			leg3_offset = pi		# back left
			leg4_offset = 0 		# back right

			self.x1 = x_center + x_stride*sin(leg_pace*self.t - pi/2 - leg1_offset)
			self.y1 = y_center + y_offset*sin(leg_pace*self.t - pi - leg1_offset)
			self.z1 = z_center + z_lift*sin(leg_pace*self.t - leg1_offset)

			self.x2 = x_center + x_stride*sin(leg_pace*self.t - pi/2 - leg2_offset)
			self.y2 = y_center + y_offset*sin(leg_pace*self.t - pi - leg2_offset)
			self.z2 = z_center + z_lift*sin(leg_pace*self.t - leg2_offset)

			self.x3 = x_center + x_stride*sin(leg_pace*self.t - pi/2 - leg3_offset)
			self.y3 = y_center + y_offset*sin(leg_pace*self.t - pi - leg3_offset)
			self.z3 = z_center + z_lift*sin(leg_pace*self.t - leg3_offset)

			self.x4 = x_center + x_stride*sin(leg_pace*self.t - pi/2 - leg4_offset)
			self.y4 = y_center + y_offset*sin(leg_pace*self.t - pi - leg4_offset)
			self.z4 = z_center + z_lift*sin(leg_pace*self.t - leg4_offset)

			if (self.z1) < z_center: self.z1 = z_center
			if (self.z2) < z_center: self.z2 = z_center
			if (self.z3) < z_center: self.z3 = z_center
			if (self.z4) < z_center: self.z4 = z_center

		elif (action == "turn"):
			leg_pace = 8.0 # pace of gait

			x_center_front = 0.5
			x_center_back = -0.5
			x_stride = 0

			y_center = -1

			if (direction == "left"):
				y_offset = 0.5
			elif (direction == "right"):
				y_offset = -0.5

			z_center = -4
			z_lift = 1

			leg1_offset = 0			# front left
			leg2_offset = pi		# front right
			leg3_offset = pi		# back left
			leg4_offset = 0 		# back right

			self.x1 = x_center_front + x_stride*sin(leg_pace*self.t - pi/2 - leg1_offset)
			self.y1 = y_center - y_offset*sin(leg_pace*self.t - pi - leg1_offset)
			self.z1 = z_center + z_lift*sin(leg_pace*self.t - pi/2 - leg1_offset)

			self.x2 = x_center_front + x_stride*sin(leg_pace*self.t - pi/2 - leg2_offset)
			self.y2 = y_center + y_offset*sin(leg_pace*self.t - pi - leg2_offset)
			self.z2 = z_center + z_lift*sin(leg_pace*self.t - pi/2 - leg2_offset)

			self.x3 = x_center_back + x_stride*sin(leg_pace*self.t - pi/2 - leg3_offset)
			self.y3 = y_center + y_offset*sin(leg_pace*self.t - pi - leg3_offset)
			self.z3 = z_center + z_lift*sin(leg_pace*self.t - pi/2 - leg3_offset)

			self.x4 = x_center_back + x_stride*sin(leg_pace*self.t - pi/2 - leg4_offset)
			self.y4 = y_center - y_offset*sin(leg_pace*self.t - pi - leg4_offset)
			self.z4 = z_center + z_lift*sin(leg_pace*self.t - pi/2 - leg4_offset)

			if (self.z1) < z_center: self.z1 = z_center
			if (self.z2) < z_center: self.z2 = z_center
			if (self.z3) < z_center: self.z3 = z_center
			if (self.z4) < z_center: self.z4 = z_center

		elif (action == "swivel"):
			leg_pace = 5.0 # pace of gait

			x_center = 0.5
			x_stride = 1

			y_center = -0.5
			y_offset = 1

			z_center = -4
			z_lift = 0

			leg1_offset = 0			# front left
			leg2_offset = 0			# front right
			leg3_offset = 0			# back left
			leg4_offset = 0 		# back right

			self.x1 = x_center + x_stride*sin(leg_pace*self.t - pi/2 - leg1_offset)
			self.y1 = y_center - y_offset*sin(leg_pace*self.t - pi - leg1_offset)
			self.z1 = z_center + z_lift*sin(leg_pace*self.t - pi/2 - leg1_offset)

			self.x2 = x_center + x_stride*sin(leg_pace*self.t - pi/2 - leg2_offset)
			self.y2 = y_center + y_offset*sin(leg_pace*self.t - pi - leg2_offset)
			self.z2 = z_center + z_lift*sin(leg_pace*self.t - pi/2 - leg2_offset)

			self.x3 = x_center + x_stride*sin(leg_pace*self.t - pi/2 - leg3_offset)
			self.y3 = y_center + y_offset*sin(leg_pace*self.t - leg3_offset)
			self.z3 = z_center + z_lift*sin(leg_pace*self.t - pi/2 - leg3_offset)

			self.x4 = x_center + x_stride*sin(leg_pace*self.t - pi/2 -leg4_offset)
			self.y4 = y_center - y_offset*sin(leg_pace*self.t - leg4_offset)
			self.z4 = z_center + z_lift*sin(leg_pace*self.t - pi/2 - leg4_offset)

			if (self.z1) < z_center: self.z1 = z_center
			if (self.z2) < z_center: self.z2 = z_center
			if (self.z3) < z_center: self.z3 = z_center
			if (self.z4) < z_center: self.z4 = z_center

		elif (action == "sideways"):
			leg_pace = 10.0 # pace of gait

			x_center = -0.1
			x_stride = 0

			y_center = -1
			if (direction == "left"):
				y_offset = -0.5
			elif (direction == "right"):
				y_offset = 0.5

			z_center = -4.75
			z_lift = 0.75

			leg1_offset = 0			# front left
			leg2_offset = pi		# front right
			leg3_offset = pi/2		# back left
			leg4_offset = 3*pi/2 	# back right

			self.x1 = x_center + x_stride*sin(leg_pace*self.t - pi/2 - leg1_offset)
			self.y1 = y_center + y_offset*sin(leg_pace*self.t - pi - leg1_offset)
			self.z1 = z_center + z_lift*sin(leg_pace*self.t - pi/2 - leg1_offset)

			self.x2 = x_center + x_stride*sin(leg_pace*self.t - pi/2 - leg2_offset)
			self.y2 = y_center - y_offset*sin(leg_pace*self.t - pi - leg2_offset)
			self.z2 = z_center + z_lift*sin(leg_pace*self.t - pi/2 - leg2_offset)

			self.x3 = x_center + x_stride*sin(leg_pace*self.t - pi/2 - leg3_offset)
			self.y3 = y_center + y_offset*sin(leg_pace*self.t - pi - leg3_offset)
			self.z3 = z_center + z_lift*sin(leg_pace*self.t - pi/2 - leg3_offset)

			self.x4 = x_center + x_stride*sin(leg_pace*self.t - pi/2 - leg4_offset)
			self.y4 = y_center - y_offset*sin(leg_pace*self.t - pi - leg4_offset)
			self.z4 = z_center + z_lift*sin(leg_pace*self.t - pi/2 - leg4_offset)

			if (self.z1) < z_center: self.z1 = z_center
			if (self.z2) < z_center: self.z2 = z_center
			if (self.z3) < z_center: self.z3 = z_center
			if (self.z4) < z_center: self.z4 = z_center

	def JointAng(self, action, direction, time):

		self.find_xyz(action, direction, time)

		self.angs1, self.angf1, self.angt1 = self.getJointAng(self.x1, self.y1, self.z1, 1)
		self.angs2, self.angf2, self.angt2 = self.getJointAng(self.x2, self.y2, self.z2, 2)
		self.angs3, self.angf3, self.angt3 = self.getJointAng(self.x3, self.y3, self.z3, 3)
		self.angs4, self.angf4, self.angt4 = self.getJointAng(self.x4, self.y4, self.z4, 4)

		return [self.angs1, self.angf1, self.angt1, self.angs2, self.angf2, self.angt2, self.angs3, self.angf3, self.angt3, self.angs4, self.angf4, self.angt4]

	def getJointAng(self, x, y, z, leg):

		if (y<0):
			Adxy = arctan(z/y)
		else:
			Adxy = pi + arctan(z/y)

		dxy = sqrt(y**2 + z**2)
		As = Adxy - arccos(self.ls/dxy)

		if (leg == 1 or leg == 3):
			As = pi-As

			if (x<0):
				Ad = pi + arctan((z+self.ls*sin(As))/x)
			else:
				Ad = arctan((z+self.ls*sin(As))/x)

			d = sqrt(x**2 + (z+self.ls*sin(As))**2)
			Af = Ad - arccos((self.lf**2 + d**2 - self.lt**2)/(2*self.lf*d))
			At = pi - arccos((self.lf**2 + self.lt**2 - d**2)/(2*self.lf*self.lt))

			Af = pi-Af
			At = -At

		else:
			if (x<0):
				Ad = arctan((z+self.ls*sin(As))/x)
			else:
				Ad = pi + arctan((z+self.ls*sin(As))/x)

			d = sqrt(x**2 + (z+self.ls*sin(As))**2)
			Af = Ad - arccos((self.lf**2 + d**2 - self.lt**2)/(2*self.lf*d))
			At = pi - arccos((self.lf**2 + self.lt**2 - d**2)/(2*self.lf*self.lt))


		return As,Af,At
 



