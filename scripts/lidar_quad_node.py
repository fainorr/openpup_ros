#!/usr/bin/env python

# LIDAR ANALYSIS NODE
# breaks scan into four quadrants
# checks for obst_size (number of consecutive dots) within safe_range
# passes array of booleans (true if obstacle exists) [front, right, back, left]

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

        self.obst_size = 4;         # number of consecutive dots
        self.safe_range = 0.5;      # search ranges for obstacles

		self.distances = zeros(360)
		self.angles = zeros(360)

		# subscribe to rplidar node
		self.lidar_subscriber = rospy.Subscriber('/scan', LaserScan, self.scancallback)

        # publish array of booleans if an obstacle exists in each quadrant
        self.quad_obstacles = [0,0,0,0]
        self.lidar_publisher = rospy.Publisher('/lidar_obstacles', Array, queue_size=1)

		# create loop
		rospy.Timer(rospy.Duration(self.dT), self.loop, oneshot=False)


	def loop(self, event):

		self.timenow = time.time()
		self.oldtime = self.timenow

		# ANALYZE scan

        # concert distances to boolean array if in range
        for i in range(0,360):
            if self.distances[i] > self.safe_range: self.distances[i] = 0
            else: self.distances[i] = 1

        for quad in range(0,4):
            self.quad_check = zeros((90-self.obst_size,1))

            for j in range(90*quad, 90*(quad+1) - self.obst_size):
                scan_obst_size = 0

                for k in range(0,self.obst_size):
                    if self.distances[j+k] == 1: scan_obst_size = scan_obst_size + 1

                if scan_obst_size == self.obst_size: self.quad_check[j-90*quad] = 1

            if sum(self.quad_check >= 1): self.quad_obstacles[quad] = 1

        self.lidar_publisher.publish(self.quad_obstacles)


	def scancallback(self,data):

		self.distances = data.ranges
		self.angles = arange(data.angle_min, data.angle_max, data.angle_increment)


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
