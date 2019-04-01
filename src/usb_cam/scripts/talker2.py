#!/usr/bin/env python
# license removed for brevity
import rospy
import sys
import tty
import termios

from std_msgs.msg import String

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)
def talker():
    pub = rospy.Publisher('car_cmd', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        key=readkey()
        if key == 'w':
            cmd_str = 'ww'
            pub.publish(cmd_str)
            rate.sleep()
        elif key == 's':
            cmd_str = 'ss'
            pub.publish(cmd_str)
            rate.sleep()
        elif key == 'a':
            cmd_str = 'aa'
            pub.publish(cmd_str)
            rate.sleep()
        elif key == 'd':
            cmd_str = 'dd'
            pub.publish(cmd_str)
            rate.sleep()
        elif key == 'q':
            cmd_str = 'qq'
            pub.publish(cmd_str)
            rate.sleep()
        elif key == 'e':
            cmd_str = 'ee'
            pub.publish(cmd_str)
            rate.sleep()
        elif key == 'b':
            cmd_str = 'begin'
            pub.publish(cmd_str)
            rate.sleep()
        elif key == 'z':
            cmd_str = 'stop'
            pub.publish(cmd_str)
            rate.sleep()
        elif key == 'g':
            break
        else : 
            print "wait"
        

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
