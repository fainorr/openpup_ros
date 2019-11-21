
# SERVO CONTROL NODE

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from std_msgs.msg import *
from numpy import *
import Time


import inverse_kinematics
import servo_angles


class servoPublisher():

	def __init__(self):

		rospy.init_node('servo_control')

		self.dT = 0.005;
		self.timenow = rospy.Time.now()
		self.oldtime = self.timenow

		self.IK = inverse_kinematics.inverse_kinematics()
		self.servoAng = servo_angles.servo_angles()


		# subscribe to FSM
		self.FSM_action = rospy.Subscriber('/action', String, self.actioncallback)
		self.FSM_direction = rospy.Subscriber('/direction', String, self.directioncallback)

		# create loop
		rospy.Timer(rospy.Duration(self.dT), self.loop, oneshot=False)

		self.action = 'stand'
		self.direction = 'left'



	def loop(self,event):

		self.oldtime = self.timenow
		self.timenow = rospy.Time.now()

		myAngles = self.IK.JointAng(self.action, self.direction, self.timenow)
		self.servoAng.getServoAng(myAngles)


	def actioncallback(self,data):

		self.action = data.data

	def directioncallback(self,data):

		self.direction = data.data


# main function

def main(args):
	rospy.init_node('servo_control', anonymous=True)
	myNode = servoPublisher()

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	main(sys.argv) 




