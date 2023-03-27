#! /usr/bin/env python3
import rospy
from std_msgs.msg import *
from geometry_msgs.msg import *
from leica_scanstation_msgs.srv import *
import math
import time
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import csv
import os

models_list = []

with open('/home/ricardo/file.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        models_list.append(str(row[0]))

print(models_list)

myCmd1 = "ps -ef | grep 'gazebo' | grep -v grep | awk '{print $2}' | xargs -r kill -9"
myCmd2 = "roslaunch aeroscan_uav_simulation launcher.launch mesh_file:="+models_list[0]+" &"
myCmd3 = "roslaunch aeroscan_uav_simulation launcher.launch mesh_file:="+models_list[1]+" &"

vehicle_pose = Pose()

def pose_callback(data):
    global vehicle_pose
    vehicle_pose = data

if __name__ == "__main__":
    rospy.init_node("aeroscan_uav_simulation", anonymous=False)

    os.system(myCmd2)
    print("gazebo launched")

    # modelo pra teste: 20160613office_model_CV2b_fordesign

    # time.sleep(5)
    #
    # os.system(myCmd3)
    # print("gazebo launched")
    #
    # time.sleep(30)
    #
    # os.system(myCmd1)
    # print("gazebo killed")

    pub = rospy.Publisher('/c5/command/pose', PoseStamped, queue_size=10)

    rospy.Subscriber("/c5/odometry_sensor1/pose", Pose, pose_callback)

    z_pos = 5
    pos_x = 20
    pos_y = 20

    posx = [pos_x, pos_x, pos_x, -pos_x, -pos_x, pos_x, pos_x, -pos_x, -pos_x]
    posy = [pos_y, pos_y, -pos_y, -pos_y, pos_y, pos_y, -pos_y, -pos_y, pos_y]
    posz = [z_pos, z_pos, z_pos, z_pos, z_pos, -z_pos, -z_pos, -z_pos, -z_pos]

    i = 0

    pose = PoseStamped()
    pose.pose.position.x = pos_x
    pose.pose.position.y = pos_y
    pose.pose.position.z = z_pos
    # pose.pose.position.z = 125#-25

    time.sleep(1)
    pub.publish(pose)
    time.sleep(1)
    pub.publish(pose)
    time.sleep(1)
    pub.publish(pose)
    time.sleep(1)
    pub.publish(pose)
    time.sleep(1)
    pub.publish(pose)
    time.sleep(1)
    pub.publish(pose)


    time.sleep(60)

    os.system(myCmd1)
    print("gazebo killed")



    # while not rospy.is_shutdown():
    #     offset = 0
    #     pose = PoseStamped()
    #     pose.pose.position.x = posx[i]
    #     pose.pose.position.y = posy[i]
    #     pose.pose.position.z = posz[i]

    #     pub.publish(pose)

    #     time.sleep(60)

    #     print("Testing offset")

    #     while (True):
    #         if (abs(posz[i]-vehicle_pose.position.z)>0.25):
    #             offset += 0.2
    #             if (vehicle_pose.position.z - posz[i] > 0.25):
    #                 pose.pose.position.z = posz[i] - offset
    #             elif (vehicle_pose.position.z - posz[i] < -0.25):
    #                 pose.pose.position.z = posz[i] + offset
    #             else:
    #                 print("Offset tested")
    #                 break

    #             pub.publish(pose)

    #             time.sleep(2)
    #         else:
    #             print("Offset tested")
    #             break

    #     print("Saving to disk")
    #     with open('/home/ricardo/pos.csv', 'a') as csvfile:
    #         spamwriter = csv.writer(csvfile, delimiter=' ',
    #                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #         if (i == 0):
    #             spamwriter.writerow(["Posx", "Posy", "Posz"])
    #         else:
    #             spamwriter.writerow([vehicle_pose.position.x, vehicle_pose.position.y, vehicle_pose.position.z])

    #     rospy.wait_for_service('/c5/scan')
    #     try:
    #         proxy = rospy.ServiceProxy('/c5/scan', Scan)
    #         proxy('scan_sim', 512, 2048, 0.0, 0.0, 2.05, 2.05)
    #     except (rospy.ServiceException) as e:
    #         print("gazebo/reset_simulation service call failed")

    #     i += 1

    #     time.sleep(75)

    #     if (i == len(posx)):
    #         break
