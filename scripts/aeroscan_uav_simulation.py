#! /usr/bin/env python
import rospy
from std_msgs.msg import *
from geometry_msgs.msg import *
from leica_scanstation_msgs.srv import *
import math
import time
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import csv

vehicle_pose = Pose()

def pose_callback(data):
    global vehicle_pose
    vehicle_pose = data

if __name__ == "__main__":
    rospy.init_node("aeroscan_uav_simulation", anonymous=False)

    pub = rospy.Publisher('/c5/command/pose', PoseStamped, queue_size=10)

    rospy.Subscriber("/c5/odometry_sensor1/pose", Pose, pose_callback)

    z_pos = 10
    pos_x = 15
    pos_y = 15

    posx = [pos_x, pos_x, pos_x, -pos_x, -pos_x, pos_x, pos_x, -pos_x, -pos_x]
    posy = [pos_y, pos_y, -pos_y, -pos_y, pos_y, pos_y, -pos_y, -pos_y, pos_y]
    posz = [z_pos, z_pos, z_pos, z_pos, z_pos, -z_pos, -z_pos, -z_pos, -z_pos]

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
        offset = 0
        pose = PoseStamped()
        pose.pose.position.x = posx[i]
        pose.pose.position.y = posy[i]
        pose.pose.position.z = posz[i]

        pub.publish(pose)

        time.sleep(15)

        print("Testing offset")

        while (True):
            if (abs(posz[i]-vehicle_pose.position.z)>0.25):
                offset += 0.2
                if (vehicle_pose.position.z - posz[i] > 0.25):
                    pose.pose.position.z = posz[i] - offset
                elif (vehicle_pose.position.z - posz[i] < -0.25):
                    pose.pose.position.z = posz[i] + offset
                else:
                    print("Offset tested")
                    break

                pub.publish(pose)

                time.sleep(2)
            else:
                print("Offset tested")
                break

        print("Saving to disk")
        with open('/home/ricardo/pos.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            if (i == 0):
                spamwriter.writerow(["Posx", "Posy", "Posz"])
            else:
                spamwriter.writerow([vehicle_pose.position.x, vehicle_pose.position.y, vehicle_pose.position.z])

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
