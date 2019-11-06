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


def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (0,0,255), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (255,0,0), 5)
    return img

mtx = np.array(
[[676.39924541,0.0,         338.92297461],
 [  0.0,         674.54356227, 205.60241729],
 [  0.,           0.0,           1.0        ]]
)

dist = np.array(
[[0.0, 0.0, 0.0, 0.0, 0.0]]
)
 
if __name__ == '__main__':


    video = cv2.VideoCapture(0)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*8,3), np.float32)
    objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)
    objp *= 0.025
    axis = np.float32([[0.075, 0, 0],[0,0.075,0],[0,0,0.075]]).reshape(-1,3)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.


    rospy.init_node('fixed_tf_broadcaster')
    br = tf.TransformBroadcaster()

    x = 0.013498722511
    y = 0.0
    z = -0.04590468468

    ux = -1.02
    uy = 3.14
    uz = -1.57
    step = 0.01
    mstep = 0.001
    while(True):
        # read the image
        check, image = video.read()
        rot = tf.transformations.quaternion_from_euler(ux,uy,uz)
        br.sendTransform((x, y, z), rot, rospy.Time.now(), "test_cam", "ee_link")

        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        # save image to file, if pattern found
        ret, corners = cv2.findChessboardCorners(gray, (8,6), None)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(8,6),(-1,-1),criteria)
            ret, rvecs, tvecs = cv2.solvePnP(objp, corners2, mtx, dist)
            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
            image = draw(image, corners2, imgpts)

            rot1 = tf.transformations.quaternion_from_euler(rvecs[0],rvecs[1],rvecs[2])
            br.sendTransform((tvecs[0], tvecs[1], tvecs[2]), rot1, rospy.Time.now(), "object", "test_cam")

           
            imgpoints.append(corners2)

            # Draw and display the corners
            image = cv2.drawChessboardCorners(image, (8,6), corners2,ret)

        cv2.imshow('img',image)
        keyr = cv2.waitKey(1)
        if keyr != -1:
            if keyr & 0xFF == ord('w'):
                print "w"
                ux += step 
            elif keyr & 0xFF == ord('e'):
                print "e"
                ux -= step 
            elif keyr & 0xFF == ord('s'):
                print "s"
                uy += step 
            elif keyr & 0xFF == ord('d'):
                print "d"
                uy -= step
            elif keyr & 0xFF == ord('x'):
                print "x"
                uz += step 
            elif keyr & 0xFF == ord('c'):
                print "c"
                uz -= step
            elif keyr & 0xFF == ord('r'):
                print "r"
                x += mstep
            elif keyr & 0xFF == ord('t'):
                print "t"
                x -= mstep
            elif keyr & 0xFF == ord('f'):
                print "f"
                z += mstep
            elif keyr & 0xFF == ord('g'):
                print "g"
                z -= mstep
            elif keyr & 0xFF == ord('q'):
                break
            print "ux: ", ux, " uy: ", uy, " uz: ", uz, " x:", x, " z:", z

    cv2.destroyAllWindows()
