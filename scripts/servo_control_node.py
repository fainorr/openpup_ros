
# INVERSE KINEMATICS NODE


import roslib
import rospy
from numpy import *
roslib.load_manifest('openpup_ros')
from std_msgs.msg import String
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
		rospy.Timer(rospy.Duration(self.dT), self.timercallback, oneshot=False)

		self.action = 'stand'
		self.direction = 'left'



	def timercallback(self,data):

		self.oldtime = self.timenow
		self.timenow = rospy.Time.now()

		myAngles = self.IK.JointAng(self.action, self.direction, self.timenow)
		self.servo_angles.getServoAng(myAngles)

	def actioncallback(self,data):

		self.action = data.data




