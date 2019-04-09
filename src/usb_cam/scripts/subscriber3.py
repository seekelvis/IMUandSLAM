# -*- coding: utf-8 -*-
#! /usr/bin/env python
import rospy
import serial
import time
from std_msgs.msg import String
# ser = serial.Serial("/dev/ttyAMA0", 9600)
ser = serial.Serial("/dev/ttyUSB3", 38400)

import re
import urllib,urllib2

count = 0
def callback(data):
    global count
    print count
    count +=1

    if data.data == '11':
        ser.write("KR-0,100,0;")
        time.sleep(0.1)
        ser.write("KR-0,0,0;")
    if data.data == '22':
        ser.write("KR-180,100,0;")
        time.sleep(0.1)
        ser.write("KR-0,0,0;")


    if data.data == 'ww':
        ser.write("KR-0,50,0;")
        time.sleep(0.1)
        ser.write("KR-0,0,0;")
    if data.data == 'ss':
        ser.write("KR-180,50,0;")
        time.sleep(0.1)
        ser.write("KR-0,0,0;")
    if data.data == 'aa':
        ser.write("KR-270,50,0;")
        time.sleep(0.1)
        ser.write("KR-0,0,0;")
    if data.data == 'dd':
        ser.write("KR-90,50,0;")
        time.sleep(0.1)
        ser.write("KR-0,0,0;")
    if data.data == 'qq':
        ser.write("KR-0,0,130;")
        time.sleep(0.1)
        ser.write("KR-0,0,0;")
    if data.data == 'ee':
        ser.write("KR-0,0,30;")
        time.sleep(0.1)
        ser.write("KR-0,0,0;")
    if data.data == 'begin':
        ser.write("KR-270,80,50;")
    if data.data == 'stop':
        ser.write("KR-0,0,0;")
def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("car_cmd", String, callback)

    rospy.spin()

if __name__ == '__main__':
    # listener()
    # ser.write("KR-0,10,0;")


    ser.write("AT+VERSION?\r\n")
    tmp=ser.read(22)
    print ser.name
    tmp.replace('','')
    tmp.replace('','')
    tmp.replace('\0','')
    tmp.replace('\n\r','')
    print "蓝牙硬件版本：",tmp

    ser.write("at+addr?\r\n")#地址
    tmp=ser.read(20)
    print "蓝牙地址...",tmp

    ser.write("at+role?\r\n")#
    tmp=ser.read(20)
    print "蓝牙角色...",tmp

    ser.write("at+uart?\r\n")#
    tmp=ser.read(20)
    print "蓝牙波特率...",tmp

    # ser.write("at+init\r\n")#初始化蓝牙
    # tmp=ser.read(20)
    # print "蓝牙初始化...",tmp

    ser.write("at+state?\r\n")#蓝牙状态？
    tmp=ser.read(20)
    print "蓝牙状态...",tmp

    # while 1:
    #     ser.timeout=10
    #     ser.write("AT+INQ\r\n")
    #     print "搜索周围设备..."
    #     tmp=ser.read(1000)
    #     print "设备列表..."
    #     tmp.strip('\n')
    #     tmp.strip('\r')
    #     tmp.strip('\r\n')
    #     tmp.strip('\n\r')
    #     print tmp
     
    #     print "地址匹配..."
    #     pattern = re.compile("(\+INQ:([A-Z]|\d){4}\W([A-Z]|\d){2}\W([A-Z]|\d){6}\W)|(\+INQ:([A-Z]|\d){2}:([A-Z]|\d){2}:([A-Z]|\d){5})\W")    #正则匹配
     
     
     
    #     i=0
    #     for m in pattern.finditer(tmp):
    #         print m.group()[5:-1]
    #         i=i+1
    #         print i#计数器
    #         str=m.group()[5:-1]
    #         url="http://192.168.43.146:8000/update_device/?address=%s&location=111"%str
    #         print url
    #         res=urllib2.urlopen(url)#提交
        
    #     time.sleep(10)
    # ser.close()


