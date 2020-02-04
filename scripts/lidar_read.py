#!/usr/bin/env python

# LIDAR READ

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from std_msgs.msg import *
from sensor_msgs.msg import *
from numpy import *
import time


class lidar():

	def __init__(self):

		self.dT = 1.0;
		self.timenow = time.time()
		self.oldtime = self.timenow

		# subscribe to rplidar node
		self.lidar_raw = rospy.Subscriber('/scan', LaserScan, self.scancallback)

        # create loop
        rospy.Timer(rospy.Duration(self.dT), self.loop, oneshot=False)

    def loop(self, event):

		self.timenow = time.time()
		self.oldtime = self.timenow

		self.angles = linspace(0,359,num=360)
        self.ranges = self.lidar_raw.ranges*100.0

        print(self.ranges)


	def scancallback(self,data):

		self.lidar_raw = data.data


# main function

def main(args):
	rospy.init_node('lidar_read', anonymous=True)
	myNode = lidar()

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	main(sys.argv)
