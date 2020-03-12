#!/usr/bin/env python

# LIDAR ANALYSIS NODE

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from std_msgs.msg import *
from sensor_msgs.msg import *
from numpy import *
import time

import lidar_compare


class lidar_quad():

	def __init__(self):

		self.dT = 1.0;
		self.timenow = time.time()
		self.oldtime = self.timenow

		self.obst_size = 5;         # number of consecutive dots
		self.safe_range = 1.5;      # search ranges for obstacles

		self.distances = zeros(360)
		self.angles = zeros(360)

		self.analyze = lidar_compare.lidar_compare()

		# subscribe to rplidar node
		self.lidar_subscriber = rospy.Subscriber('/scan', LaserScan, self.scancallback)

		# publish array of booleans if an obstacle exists in each quadrant
		self.FSM_action = rospy.Publisher('/action', String, queue_size=1)
		self.FSM_direction = rospy.Publisher('/direction', String, queue_size=1)

		# create loop
		rospy.Timer(rospy.Duration(self.dT), self.loop, oneshot=False)


	def loop(self, event):

		self.timenow = time.time()
		self.oldtime = self.timenow

		self.action,self.direction = self.analyze.lidar_compare(self.distances, self.angles, self.obst_size, self.safe_range)

		self.FSM_action.publish(self.action)
		self.FSM_direction.publish(self.direction)


	def scancallback(self,data):

		self.distances = array(data.ranges)
		self.angles = arange(data.angle_min, data.angle_max, data.angle_increment)


# main function

def main(args):
	rospy.init_node('lidar_quad_node', anonymous=True)
	myNode = lidar_quad()

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	main(sys.argv)
