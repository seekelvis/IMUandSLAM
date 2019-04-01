#!/usr/bin/env python
# license removed for brevity
#coding=utf-8

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

time_ = 0.0
stop_time_ = 0.0
yaw_ = 0.0
px_ = 0.0
py_ = 0.0
vx_ = 0.0
vy_ = 0.0
ax_ = 0.0
ay_ = 0.0
gz_ = 0.0
count_ = 0
# key_count = 0
# key_lastcount = 0
axmin = aymin = 30
axmax = aymax = -30
AXBIAS = (-0.126953125 + 0)/2
AXTHRE = abs(AXBIAS) #yuzhi
AYBIAS = (0.01171875 + 0.029541015625)/2
AYTHRE = abs(AYBIAS)

plt.close()  
fig=plt.figure()
fig_=fig.add_subplot(1,1,1)
# fig_.axis("equal") 
plt.grid(True) 
plt.ion()  #interactive mode on


def callback(imuMsg):
	global yaw_
	global px_
	global py_
	global vx_
	global vy_
	global ax_
	global ay_
	global gz_
	global time_
	global stop_time_
	global count_
	global axmin,axmax,aymin,aymax
	global AXBIAS,AXTHRE,AYBIAS,AYTHRE
	global fig_

	print "=================="+str(count_)
	count_ = count_ + 1
	rospy.loginfo(rospy.get_caller_id() )	
	if count_ > 2 and count_ < 30:
		time_ = imuMsg.header.stamp
		ax_ = imuMsg.linear_acceleration.x
		ay_ = imuMsg.linear_acceleration.y    	
		yaw_ = imuMsg.angular_velocity.z
		if ax_ < axmin:
			axmin = ax_
		if ay_ < aymin:
			aymin = ay_
		if ax_ > axmax:
			axmax = ax_
		if ay_ > aymax:
			aymax = ay_		
	elif count_ >= 30:
		####### Set the bias and threshold value #####################
		if count_ == 30:
			AXBIAS = (axmin + axmax)/2
			AXTHRE = abs(AXBIAS)/2 
			AYBIAS = (aymin + aymax)/2
			AYTHRE = abs(AYBIAS)/2
			# AXTHRE = 0
			# AYTHRE = 0
			stop_time_ = time_
		# print "ax: " + str(axmin) + "," + str(axmax)
		# print "ay: " + str(aymin) + "," + str(aymax)

		####### Update time #####################
		dt = float(imuMsg.header.stamp.nsecs - time_.nsecs)/1000000000		
		if dt < 0:
			dt = dt + 1		
		print "dt = ",dt
		time_ = imuMsg.header.stamp

		if stop_time_ > time_ : #It's not time to stop
		# if (stop_time_.secs > time_.secs) or (stop_time_.secs = time_.secs and stop_time_.nsecs >= time_.nsecs) :
			####### Update Gyroscopic data #####################
			gz = imuMsg.angular_velocity.z	
			# yaw_ = (yaw_ + imuMsg.angular_velocity.z * dt) % 360 
			yaw_ = (yaw_ + imuMsg.angular_velocity.z * dt * 12/13) % 360 
			r_yaw = math.radians(yaw_)

			###### deal with the bias of acc  ###################
			imuMsg.linear_acceleration.x = imuMsg.linear_acceleration.x - AXBIAS
			imuMsg.linear_acceleration.y = imuMsg.linear_acceleration.y - AYBIAS
			if abs(imuMsg.linear_acceleration.x) <= AXTHRE :
				ax_ = 0
			else:
				ax_ = imuMsg.linear_acceleration.x * math.cos(r_yaw) - imuMsg.linear_acceleration.y * math.sin(r_yaw)
				print "ax = ", ax_, " = ", imuMsg.linear_acceleration.x, " * ", math.cos(r_yaw), " - ", imuMsg.linear_acceleration.y, " * ",math.sin(r_yaw)
			if abs(imuMsg.linear_acceleration.y) <= AYTHRE :
				ay_ = 0
			else:
				ay_ = imuMsg.linear_acceleration.x * math.sin(r_yaw) + imuMsg.linear_acceleration.y * math.cos(r_yaw)
				print "ay = ", ay_, " = ", imuMsg.linear_acceleration.y, " * ", math.sin(r_yaw), " + ", imuMsg.linear_acceleration.x, " * ",math.cos(r_yaw)
			
			####### Integral operation #############################
			vx_ = vx_ + ax_ * dt
			vy_ = vy_ + ay_ * dt
			px_ = px_ + vx_ * dt /135 * 500
			py_ = py_ + vy_ * dt /135 * 500
			
			print "[[[[[update,,,,,,,,,,,,,,,,,,,,,,,,,,,,,]]]]]]"
		else :
			ax_ = 0
			ay_ = 0
			vx_ = 0
			vy_ = 0
			gz_ = 0
			print "[[[[[nothing changed|||||||||||||||||||||]]]]]]"
		print "ax: " + str(ax_) 
		print "ay: " + str(ay_) 	
		print "gz: " + str(imuMsg.angular_velocity.z)
		print "vx: " + str(vx_) 
		print "vy: " + str(vy_)		
		print "yaw = ", yaw_
		print "position = (", px_ , "," , py_ , ")"
		# fig_.scatter(count_, ax_, c='b', marker=".")
		# plt.pause(0.001)

	# rospy.loginfo(rospy.get_caller_id() + 'a0 (%f,%f, %f)', imuMsg.linear_acceleration.x, imuMsg.linear_acceleration.y, imuMsg.angular_velocity.z)
	
def key_action(data):
    # global yaw_
    # global vx_
    # global vy_
    # global ax_
    # global ay_
    # global key_count_
    global stop_time_
    if data.data == 'ww' or 'ss' or 'aa' or 'dd' or 'qq' or 'ee':
        #ax_ = 0
        #ay_ = 0
        #vx_ = 0
        #vy_ = 0
        #yaw_ = 0
        if stop_time_ <= time_ :
        	stop_time_ = time_ +  rospy.Duration(0.108 * 9)
       	else :
       		stop_time_ = stop_time_ +  rospy.Duration(0.108)
        	

def listener():
	global fig_

	print "listener begin"

    

	rospy.init_node('getting_position', anonymous=True)
	print "listener 1"
	rospy.Subscriber('IMU_data', Imu, callback)
	print "listener 1.5"
	rospy.Subscriber("car_cmd", String, key_action)
	print "listener 2"
    # spin() simply keeps python from exiting until this node is stopped
	
	while count_>= 0:
		if count_>30:
			fig_.scatter(float(count_)/10, ax_, c='b', marker=".")
			fig_.scatter(float(count_)/10, ay_, c='r', marker=".")
			plt.pause(0.1)


	rospy.spin()
	print "listener end"
if __name__ == '__main__':
	listener()
