#!/usr/bin/env python
# license removed for brevity
#coding=utf-8
import os
import rospy
import datetime
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

time_str = datetime.datetime.strftime(datetime.datetime.now(),'%d-%H-%M-%S')
# file = open('./'+time_str+'.csv', 'w')
file1 = open('/home/elvis/catkin_ws/imuTestData/'+time_str+'.csv', 'w')
file1.write("stamp,time,ax,ay,vx,vy,px,py,gz,yaw\n")
realtime_ = 0
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
AXBIAS = 0
AXTHRE = abs(AXBIAS) #yuzhi
AYBIAS = 0
AYTHRE = abs(AYBIAS)

STATE = 0  #0 stop ; 1 run
stop_count = 0

plt.close()  
fig=plt.figure()
fig_=fig.add_subplot(3,1,1)
fig2_=fig.add_subplot(3,1,2)
fig3_=fig.add_subplot(3,1,3)
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
	global realtime_
	global time_
	global stop_time_
	global count_
	global axmin,axmax,aymin,aymax
	global AXBIAS,AXTHRE,AYBIAS,AYTHRE
	global fig_
	global file
	global STATE
	global stop_count

	# os.system("clear")
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
		stop_time_ = time_	

	elif count_ >= 30:
		####### Set the bias and threshold value #####################
		
			# AXTHRE = 0
			# AYTHRE = 0
			
		# print "ax: " + str(axmin) + "," + str(axmax)
		# print "ay: " + str(aymin) + "," + str(aymax)

		####### Update time #####################
		dt = float(imuMsg.header.stamp.nsecs - time_.nsecs)/1000000000 		
		if dt < 0:
			dt = (dt + 1) * 12/13
		else :		
			dt = dt * 12/13 #time offset

		# print "dt = ",dt
		time_ = imuMsg.header.stamp
		realtime_ = realtime_ + float(dt) 
		print "<<time = ",realtime_ , " >>"

		# print "~~~~~~~~~",stop_time_.secs,"~~~~~~~~~~~~~~",time_.secs
		# if 2 > 1 :
		if stop_time_ > time_ : #It's not time to stop

			if STATE == 0:
				STATE = 1
				AXBIAS = (axmin + axmax)/2
				# AXTHRE = abs(AXBIAS)/2 
				AYBIAS = (aymin + aymax)/2
				# AYTHRE = abs(AYBIAS)/2


			####### Update Gyroscopic data #####################
			gz = imuMsg.angular_velocity.z			
			yaw_ = (yaw_ + imuMsg.angular_velocity.z * dt ) % 360 
			r_yaw = math.radians(yaw_)

			###### deal with the bias of acc  ###################
			imuMsg.linear_acceleration.x = imuMsg.linear_acceleration.x - AXBIAS
			imuMsg.linear_acceleration.y = imuMsg.linear_acceleration.y - AYBIAS
			if abs(imuMsg.linear_acceleration.x) <= AXTHRE :
				ax_ = 0
			else:
				ax_ = imuMsg.linear_acceleration.x * math.cos(r_yaw) - imuMsg.linear_acceleration.y * math.sin(r_yaw)
				# print "ax = ", ax_, " = ", imuMsg.linear_acceleration.x, " * ", math.cos(r_yaw), " - ", imuMsg.linear_acceleration.y, " * ",math.sin(r_yaw)
			if abs(imuMsg.linear_acceleration.y) <= AYTHRE :
				ay_ = 0
			else:
				ay_ = imuMsg.linear_acceleration.x * math.sin(r_yaw) + imuMsg.linear_acceleration.y * math.cos(r_yaw)
				# print "ay = ", ay_, " = ", imuMsg.linear_acceleration.y, " * ", math.sin(r_yaw), " + ", imuMsg.linear_acceleration.x, " * ",math.cos(r_yaw)
			
			####### Integral operation #############################
			vx_ = vx_ + ax_ * dt
			vy_ = vy_ + ay_ * dt
			px_ = px_ + vx_ * dt 
			py_ = py_ + vy_ * dt 
			# px_ = px_ + vx_ * dt /135 * 500
			# py_ = py_ + vy_ * dt /135 * 500
			
			# print "+++++++++++++++++++ update ++++++++++++++++"
		else :		

			stop_count = stop_count + 1	
			if STATE == 1:
				STATE = 0
				axmin = imuMsg.linear_acceleration.x
				axmax = imuMsg.linear_acceleration.x
				aymin = imuMsg.linear_acceleration.y   
				aymax = imuMsg.linear_acceleration.y  
				stop_count = 0 
			elif stop_count > 10 and stop_count < 40 :
				if imuMsg.linear_acceleration.x < axmin:
					axmin = imuMsg.linear_acceleration.x
				if imuMsg.linear_acceleration.y < aymin:
					aymin = imuMsg.linear_acceleration.y
				if imuMsg.linear_acceleration.x > axmax:
					axmax = imuMsg.linear_acceleration.x
				if imuMsg.linear_acceleration.y > aymax:
					aymax = imuMsg.linear_acceleration.y	

			

			ax_ = 0
			ay_ = 0
			vx_ = 0
			vy_ = 0
			gz_ = 0
			
			# print "&&&&&&&&&&&& nothing changed &&&&&&&&&&&&&&&&"
		# print "ax: " + str(ax_) 
		# print "ay: " + str(ay_) 	
		# print "gz: " + str(imuMsg.angular_velocity.z)
		# print "vx: " + str(vx_) 
		# print "vy: " + str(vy_)		
		print "yaw = ", yaw_
		# print "position = (", px_ , "," , py_ , ")"
		file1.write(str(time_.secs)+"."+str(time_.nsecs)+",")
		file1.write(str(realtime_)+","+str(ax_) + ","+ str(ay_) + "," + str(vx_) + "," + str(vy_)+ ","+ str(px_)+ ","+ str(py_)+ "," + str(imuMsg.angular_velocity.z) + ","+ str(yaw_)+"\n")
		# file1.write(ax_, ",", ay_, ",", vx_, ",", vy_, ",", px_, ",", py_, ",", imuMsg.angular_velocity.z, ",", yaw_)
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
    # print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    global stop_time_
    if data.data == 'ww' or 'ss' or 'aa' or 'dd' or 'qq' or 'ee' or '11' or '22':
        #ax_ = 0
        #ay_ = 0
        #vx_ = 0
        #vy_ = 0
        #yaw_ = 0
        if stop_time_ <= time_ :
        	stop_time_ = time_ + rospy.Duration(0.108 * 9)
       	else :
       		stop_time_ = stop_time_ + rospy.Duration(0.108)
        	

def listener():
	global file1
	global fig_,fig2_,fig3_
	try:		

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
				fig_.scatter(realtime_, ax_, c='b', marker=".")
				fig_.scatter(realtime_, ay_, c='r', marker=".")
				fig2_.scatter(realtime_, vx_, c='b', marker=".")
				fig2_.scatter(realtime_, vy_, c='r', marker=".")
				fig3_.scatter(realtime_, px_, c='b', marker=".")
				fig3_.scatter(realtime_, py_, c='r', marker=".")
				plt.pause(0.001)


		rospy.spin()

	finally:
		if file1:
			file1.close()
		print "listener end"

if __name__ == '__main__':
	listener()
