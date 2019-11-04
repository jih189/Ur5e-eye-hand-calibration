#!/usr/bin/env_python
import sys
import roslib
import rospy
import math
import tf
import geometry_msgs.msg

import cv2
import glob
import numpy as np
import math


 
if __name__ == '__main__':

    poseindex = sys.argv[1]
    print "pose index = " , poseindex
    print "press t to take the image"

    video = cv2.VideoCapture(0)
    video.set(3, 2592)
    video.set(4, 1944)
    video.set(5, 15)
    codec = cv2.VideoWriter_fourcc("M","J","P","G")
    video.set(6, codec)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*8,3), np.float32)
    objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    rospy.init_node('tf_listener')

    listener = tf.TransformListener()

    while(True):
        # get the position of end effector
        try:
            (trans,rot) = listener.lookupTransform('/base_link', '/ee_link', rospy.Time(0))

            posematrix = np.dot(tf.transformations.translation_matrix(trans), tf.transformations.quaternion_matrix(rot))
            print "current pose"
            print posematrix
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
   
        # read the image
        check, image = video.read()
        savedimage = image.copy()

        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        # save image to file, if pattern found
        ret, corners = cv2.findChessboardCorners(gray, (8,6), None)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            image = cv2.drawChessboardCorners(image, (8,6), corners2,ret)

            cv2.imshow('img',image)
            keyr = cv2.waitKey()
            if keyr & 0xFF == ord('t'):
                break       
            elif keyr & 0xFF == ord('q'):
                exit (0)
            else:
                continue
        else:
            cv2.imshow('img',image)
            keyr = cv2.waitKey(5)
            if keyr & 0xFF == ord('q'):
                exit(0)
            else:
                continue

    if ret == True:
        print "found board"
        filename = "image-" + poseindex + ".jpg"
        cv2.imwrite(filename, savedimage)
        posefilename = "pose_fPe_" + poseindex + ".yaml"
        f = open(posefilename, "w")
        f.write("rows: 6\n")
        f.write("cols: 1\n")
        f.write("data:\n")
        for t in trans:
            f.write("  - [")
            f.write(str(t))
            f.write("]\n")
        print "please copy following number:\n"
        print rot[0], " ", rot[1], " ", rot[2], " ", rot[3] 
    else:
        print "found no board"
    cv2.destroyAllWindows()
