#!/usr/bin/env python

# ULTRASONIC

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from std_msgs.msg import *
from numpy import *
import time


import RPi.GPIO as GPIO


class ultrasonic_sensor():

	def __init__(self):

		self.dT = 0.005;
		self.timenow = time.time()
		self.oldtime = self.timenow

		self.timenow = rospy.Time.now()

		self.dist = rospy.Publisher('/ultrasonic_dist', Int32, queue_size=1)

		self.trigger = 18
		self.echo = 24

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.trigger, GPIO.OUT)
		GPIO.setup(self.echo, GPIO.IN)

		# create loop
		rospy.Timer(rospy.Duration(self.dT), self.loop, oneshot=False)


	def find_distance(self):
		# set Trigger to HIGH
		GPIO.output(self.trigger, True)

		# set Trigger after 0.01ms to LOW
		time.sleep(0.00001)
		GPIO.output(self.trigger, False)

		StartTime = time.time()
		StopTime = time.time()

		# save StartTime
		while GPIO.input(self.echo) == 0:
			StartTime = time.time()

		# save time of arrival
		while GPIO.input(self.echo) == 1:
			StopTime = time.time()

		# time difference between start and arrival
		TimeElapsed = StopTime - StartTime

		# multiply with the sonic speed (34300 cm/s)
		# and divide by 2, because there and back
		# (distance in cm)
		distance = (TimeElapsed * 34300) / 2

		return distance


	def loop(self, event):

		self.timenow = time.time()
		self.oldtime = self.timenow

		self.dist_now = self.find_distance()
		self.dist.publish(self.dist_now)


# main function

def main(args):
	rospy.init_node('ultrasonic_node', anonymous=True)
	myNode = ultrasonic_sensor()

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	main(sys.argv)
