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

    posx = [-2.0, -2.0, 4.0]
    posy = [0.0, -7.0, -10.0]
    posz = [2.5, 2.5, 2.5]
    oriz = [0.0, math.pi/4, math.pi/2]

    i = 0

    pose = PoseStamped()
    pose.pose.position.x = 0.0
    pose.pose.position.y = 0.0
    pose.pose.position.z = 2.5

    pub.publish(pose)

    time.sleep(1)

    pub.publish(pose)

    while not rospy.is_shutdown():

        pose = PoseStamped()
        pose.pose.position.x = posx[i]
        pose.pose.position.y = posy[i]
        pose.pose.position.z = posz[i]

        wx, wy, wz, ww = quaternion_from_euler(0.0, 0.0, oriz[i])
        pose.pose.orientation.x = wx
        pose.pose.orientation.y = wy
        pose.pose.orientation.z = wz
        pose.pose.orientation.w = ww

        pub.publish(pose)

        print(pose)

        time.sleep(10)

        rospy.wait_for_service('/c5/scan')
        try:
            proxy = rospy.ServiceProxy('/c5/scan', Scan)
            proxy('scan_sim', 512, 1024, 0.0, 0.0, 2, 2)
        except (rospy.ServiceException) as e:
            print("gazebo/reset_simulation service call failed")

        i += 1

        time.sleep(45)

        if (i == len(posx)):
            break
