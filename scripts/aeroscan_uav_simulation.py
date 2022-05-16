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

    z_pos = 100
    pos_x = 600
    pos_y = 500

    posx = [pos_x, pos_x, pos_x, -pos_x, -pos_x, pos_x, pos_x, -pos_x, -pos_x]
    posy = [pos_y, pos_y, -pos_y, -pos_y, pos_y, pos_y, -pos_y, -pos_y, pos_y]
    posz = [z_pos, z_pos, z_pos, z_pos, z_pos, -3*z_pos, -3*z_pos, -3*z_pos, -3*z_pos]

    i = 0

    pose = PoseStamped()
    pose.pose.position.x = 0.0
    pose.pose.position.y = 0.0
    pose.pose.position.z = 0.0
    # pose.pose.position.z = 125#-25

    pub.publish(pose)

    time.sleep(1)

    pub.publish(pose)

    while not rospy.is_shutdown():

        pose = PoseStamped()
        pose.pose.position.x = posx[i]
        pose.pose.position.y = posy[i]
        pose.pose.position.z = posz[i]

        pub.publish(pose)

        print(pose)

        time.sleep(45)

        rospy.wait_for_service('/c5/scan')
        try:
            proxy = rospy.ServiceProxy('/c5/scan', Scan)
            proxy('scan_sim', 512, 2048, 0.0, 0.0, 2.05, 2.05)
        except (rospy.ServiceException) as e:
            print("gazebo/reset_simulation service call failed")

        i += 1

        time.sleep(75)

        if (i == len(posx)):
            break
