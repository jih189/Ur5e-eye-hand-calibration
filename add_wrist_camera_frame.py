#!/usr/bin/env python  
import roslib
import rospy
import tf
import geometry_msgs.msg

import cv2
import glob
import math
import numpy as np


if __name__ == '__main__':
    video = cv2.VideoCapture(0)
    rot = tf.transformations.quaternion_from_euler(3.14, 1.068, -1.6627)
    rospy.init_node('fixed_tf_broadcaster')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    x = 0.006498722511
    y = 0.0 
    z = -0.05190468468 
    ux = 3.14 
    uy = 1.068
    uz = -1.57 
    while not rospy.is_shutdown():
         
        image = video.read()
        rot = tf.transformations.quaternion_from_euler(ux,uy,uz) 
        #br.sendTransform((x, y, z), rot, rospy.Time.now(), "wrist_cam", "ee_link")
        br.sendTransform((x, y, z), rot, rospy.Time.now(), "test_cam", "ee_link")
        #br.sendTransform((-0.0755382, 0.00675942, 0.570567), rot1, rospy.Time.now(), "object", "wrist_cam")
        cv2.imshow('image', image)
        keyinput = cv2.waitKey()
        print "input key: ", keyinput
        rate.sleep()
