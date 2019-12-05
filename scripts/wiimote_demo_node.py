#!/usr/bin/env python

import roslib; roslib.load_manifest('wiimote_demo')
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import * #import all of the standard message types
from numpy import *
import time;

#this node subscribes to a float and a string. The float represents the input to a first order system. The string represents a state.

class Node():
  def __init__(self):
    self.timenow = rospy.Time.now()#in case you need this
    
    #set up your publishers with appropriate topic types

    self.pub1 = rospy.Publisher("/What_Button_Was_Pressed",String,queue_size=1)
    #set up your subscribers
    self.sub1 = rospy.Subscriber("/joy",Joy,self.sub1Callback)

    #initialize any variables that the class "owns. these will be available in any function in the class.

    self.State = 'Waiting'

    self.dt = 0.1
    #set up timed loop to run like an arduino's "void loop" at a particular rate (100Hz)
    rospy.Timer(rospy.Duration(self.dt),self.loop,oneshot=False) 


  def sub1Callback(self,data):
    #the actual string is called by data.data. update the appropriate class-owned variable.
    print data.buttons[6]
    if data.buttons[6] == 1:
        self.State = "you pressed button 2"
    elif data.buttons[5] == 1: 
        self.State = "you pressed Button {5}" 
    elif data.buttons[4]== 1: 
        self.State = "you pressed Button {4}" 
    elif data.buttons[3]== 1: 
        self.State = "you pressed Button {3}" 
    elif data.buttons[2]== 1:
        self.State = "you pressed Button {2}"
    elif data.buttons[1]== 1: 
        self.State = "you pressed Button {1}" 
    elif data.buttons[0]== 1: 
        self.State = "you pressed Button {0}" 
    else:
        self.State = 'Waiting'
    



  def loop(self,event):
    #this function runs over and over again at dt.
    #do stuff based on states. 


    #set up a message to publish
    node_output = String()
    #fill in the data with self.x
    node_output.data = self.State
    #now publish the result of our loop into the ROS ether.
    self.pub1.publish(node_output)


    
      
#main function
def main(args):
  rospy.init_node('wiimote_demo_node', anonymous=True)
  my_node = Node()
  
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"

if __name__ == '__main__':
    main(sys.argv)