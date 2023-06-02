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
import openmesh as om
import numpy as np

models_list = []
models_list.append("/home/ricardo/catkin_ws/src/aeroscan_uav_simulation/models/oil_rig/meshes/8.obj")

# with open('/home/ricardo/file.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         models_list.append(str(row[0]))

print(models_list)

myCmd1 = "ps -ef | grep 'gazebo' | grep -v grep | awk '{print $2}' | xargs -r kill -9"
myCmd2 = "roslaunch aeroscan_uav_simulation launcher.launch mesh_file:="+models_list[0]+" &"

vehicle_pose = Pose()

def pose_callback(data):
    global vehicle_pose
    vehicle_pose = data

def goto_and_map(x,y,z):
    global vehicle_pose
    offset = 0
    pose = PoseStamped()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = z

    pub.publish(pose)

    while (True):
        if (abs(z-vehicle_pose.position.z)>0.25):
            offset += 0.2
            if (vehicle_pose.position.z - z > 0.25):
                pose.pose.position.z = z - offset
            elif (vehicle_pose.position.z - z < -0.25):
                pose.pose.position.z = z + offset
            else:
                print("Offset tested")
                break
            pub.publish(pose)

            time.sleep(2)
        else:
            print("Offset tested")
            break

    # print("Saving to disk")
    # with open('/home/ricardo/pos.csv', 'a') as csvfile:
    #     spamwriter = csv.writer(csvfile, delimiter=' ',
    #                     quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #
    #     spamwriter.writerow([vehicle_pose.position.x, vehicle_pose.position.y, vehicle_pose.position.z])

    rospy.wait_for_service('/c5/scan')
    try:
        proxy = rospy.ServiceProxy('/c5/scan', Scan)
        proxy('scan_sim', 512, 2048, 0.0, 0.0, 2.05, 2.05)
    except (rospy.ServiceException) as e:
        print("gazebo/reset_simulation service call failed")

    time.sleep(75)

if __name__ == "__main__":
    rospy.init_node("aeroscan_uav_simulation", anonymous=False)

    pub = rospy.Publisher('/c5/command/pose', PoseStamped, queue_size=10)

    rospy.Subscriber("/c5/odometry_sensor1/pose", Pose, pose_callback)

    # os.system(myCmd2)
    # print("gazebo launched")

    # modelo pra teste: 20160613office_model_CV2b_fordesign

    for i in range (0, len(models_list)):
        myCmd2 = "roslaunch aeroscan_uav_simulation launcher.launch mesh_file:="+models_list[i]+" &"

        os.system(myCmd2)
        print("gazebo launched")

        time.sleep(5)

        pose = PoseStamped()
        pose.pose.position.x = -100
        pose.pose.position.y = -100
        pose.pose.position.z = -100
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

        mesh = om.read_trimesh(models_list[i])

        max_x = -1000000
        min_x = 1000000
        max_y = -1000000
        min_y = 1000000
        max_z = -1000000
        min_z = 1000000
        offset = 10

        distance_between_points = 5

        for vh in mesh.points():
            # print(vh)
            if (vh[0] > max_x):
                max_x = vh[0]
            if(vh[0] < min_x):
                min_x = vh[0]
            if (vh[1] > max_y):
                max_y = vh[1]
            if(vh[1] < min_y):
                min_y = vh[1]
            if (vh[2] > max_z):
                max_z = vh[2]
            if(vh[2] < min_z):
                min_z = vh[2]

        # print(max_x, min_x, max_y, min_y, max_z, min_z)

        pos_x = np.arange(int(min_x-offset), int(max_x+offset), distance_between_points)
        pos_y = np.arange(int(min_y-offset), int(max_y+offset), distance_between_points)
        pos_z = np.arange(int(min_z-offset), int(max_z+offset), distance_between_points)

        # print(pos_x)
        # print(pos_y)
        # print(pos_z)

        # with open('/home/ricardo/pos.csv', 'a') as csvfile:
        #     spamwriter = csv.writer(csvfile, delimiter=' ',
        #                     quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #
        #     spamwriter.writerow([models_list[i]])

        for x in pos_x:
            for z in pos_z:
                print(x, pos_y[0], z)
                goto_and_map(x,pos_y[0],z)

        # pos_z = pos_z[::-1]
        #
        # for y in pos_y:
        #     for z in pos_z:
        #         print(pos_x[-1], y, z)
        #         goto_and_map(pos_x[-1], y, z)
        #
        # pos_x = pos_x[::-1]
        # pos_z = pos_z[::-1]
        #
        # for x in pos_x:
        #     for z in pos_z:
        #         print(x, pos_y[-1], z)
        #         goto_and_map(x, pos_y[-1], z)
        #
        # pos_z = pos_z[::-1]
        # pos_y = pos_y[::-1]
        #
        # for y in pos_y:
        #     for z in pos_z:
        #         print(pos_x[-1], y, z)
        #         goto_and_map(pos_x[-1], y, z)

        os.system(myCmd1)
        print("gazebo killed")

        time.sleep(60)

        break

    # pub = rospy.Publisher('/c5/command/pose', PoseStamped, queue_size=10)
    #
    # rospy.Subscriber("/c5/odometry_sensor1/pose", Pose, pose_callback)
    #
    # z_pos = 5
    # pos_x = 20
    # pos_y = 20
    #
    # posx = [pos_x, pos_x, pos_x, -pos_x, -pos_x, pos_x, pos_x, -pos_x, -pos_x]
    # posy = [pos_y, pos_y, -pos_y, -pos_y, pos_y, pos_y, -pos_y, -pos_y, pos_y]
    # posz = [z_pos, z_pos, z_pos, z_pos, z_pos, -z_pos, -z_pos, -z_pos, -z_pos]
    #
    # i = 0
    #
    # pose = PoseStamped()
    # pose.pose.position.x = pos_x
    # pose.pose.position.y = pos_y
    # pose.pose.position.z = z_pos
    # # pose.pose.position.z = 125#-25
    #
    # time.sleep(1)
    # pub.publish(pose)
    # time.sleep(1)
    # pub.publish(pose)
    # time.sleep(1)
    # pub.publish(pose)
    # time.sleep(1)
    # pub.publish(pose)
    # time.sleep(1)
    # pub.publish(pose)
    # time.sleep(1)
    # pub.publish(pose)
    #
    # time.sleep(60)
    #
    # os.system(myCmd1)
    # print("gazebo killed")

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
