#!/usr/bin/env python

# MICROPHONE READ NODE

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from std_msgs.msg import *
from sensor_msgs.msg import *
from numpy import *
import time

class microphone():

	def __init__(self):

		self.dT = 1.0;
		self.timenow = time.time()
		self.oldtime = self.timenow

		self.mic_text = '';

		# subscribe to rplidar node
		self.HOORAY = rospy.Subscriber("/output", String, self.mic_callback)

		# create loop
		rospy.Timer(rospy.Duration(self.dT), self.loop, oneshot=False)


	def loop(self, event):

		self.timenow = time.time()
		self.oldtime = self.timenow

		# Read output

        rospy.logwarn(self.mic_text)


	def mic_callback(self,data):

		self.mic_text = data.data


# main function

def main(args):
	rospy.init_node('mic_node', anonymous=True)
	myNode = microphone()

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	main(sys.argv)
