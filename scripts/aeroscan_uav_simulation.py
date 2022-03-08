#! /usr/bin/env python
import rospy
from std_msgs.msg import *
from geometry_msgs.msg import *
from leica_scanstation_msgs.srv import *
import math
import time
from tf.transformations import euler_from_quaternion, quaternion_from_euler

if __name__ == "__main__":

    rospy.init_node("aeroscan_uav_simulation", anonymous=False)

    pub = rospy.Publisher('/c5/command/pose', PoseStamped, queue_size=10)

    posx = [150.0        , 115.0    , 125.0,     25.0,     25.0,     25.0,          15.0,       0.0,       -15.0,     -30.0,      -45.0,      -60.0,        -75.0, -90.0, -90.0,   -90.0,     -75.0,     -60.0,     -35.0,     -10.0]
    posy = [-200.0       , -93.0    , -85.0,     30.0,     40.0,     65.0,          70.0,       70.0,       70.0,      70.0,       70.0,       70.0,         70.0,  60.0,  30.0,    0.0,      -10.0,     -10.0,     -10.0,     -10.0]
    oriz = [3*math.pi/4, math.pi, math.pi, math.pi, math.pi, -3*math.pi/4, -math.pi/2, -math.pi/2, -math.pi/2, -math.pi/2, -math.pi/2, -math.pi/2, -math.pi/4, 0.0,   0.0,   0.0,   math.pi/4, math.pi/2, math.pi/2,   math.pi/2]

    i = 0

    pose = PoseStamped()
    pose.pose.position.x = 0.0
    pose.pose.position.y = 0.0
    pose.pose.position.z = 110

    pub.publish(pose)

    time.sleep(1)

    pub.publish(pose)

    while not rospy.is_shutdown():

        pose = PoseStamped()
        pose.pose.position.x = posx[i]
        pose.pose.position.y = posy[i]
        pose.pose.position.z = 110

        wx, wy, wz, ww = quaternion_from_euler(0.0, 0.0, oriz[i])
        pose.pose.orientation.x = wx
        pose.pose.orientation.y = wy
        pose.pose.orientation.z = wz
        pose.pose.orientation.w = ww

        pub.publish(pose)

        print(pose)

        time.sleep(45)

        rospy.wait_for_service('/c5/scan')
        try:
            proxy = rospy.ServiceProxy('/c5/scan', Scan)
            proxy('scan_sim', 512, 2048, 0.0, 0.0, 2.0, 2.0)
        except (rospy.ServiceException) as e:
            print("gazebo/reset_simulation service call failed")

        i += 1

        time.sleep(75)

        if (i == len(posx)):
            break

        break
