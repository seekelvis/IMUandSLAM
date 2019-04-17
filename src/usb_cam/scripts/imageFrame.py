#!/usr/bin/env python
# license removed for brevity
#coding=utf-8
from sensor_msgs.msg import Image

import os
import rospy
import re
import math
import struct
import time
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion, Vector3
import matplotlib.pyplot as plt
# from matplotlib.patches import Circle
# import numpy as np

begin=-1
now=0
fps=0       	
       	
def countting(data):
	global begin,now,fps

	rostime = rospy.get_rostime()
	print rostime
	if begin == -1:
		begin = rostime.secs
		now = begin
		fps = 1
	elif now == rostime.secs:
		fps = fps + 1
	else:
		print "---",now,"-----------",fps,"fps"
		now = rostime.secs
		fps = 1     



def listener():
	global fig_,fig2_,fig3_

	print "listener begin"

    

	rospy.init_node('getting_fps', anonymous=True)
	print "getting_fps"
	rospy.Subscriber('usb_cam/image_raw', Image, countting)



	rospy.spin()
	print "listener end"
if __name__ == '__main__':
	listener()
