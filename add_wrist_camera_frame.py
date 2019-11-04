#!/usr/bin/env python  
import roslib
import rospy
import tf

if __name__ == '__main__':
    #rot1 = tf.transformations.quaternion_from_euler(0.324503, -0.405354, 0.037618)
    rospy.init_node('fixed_tf_broadcaster')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    x = 0.006498722511
    y = -0.03829518105 
    z = -0.05190468468 
    ux = 0.0
    uy = 0.0
    uz = 0.0
    val = ""
    while not rospy.is_shutdown():
        rot = tf.transformations.quaternion_from_euler(ux, uy, uz)
        #br.sendTransform((x, y, z), rot, rospy.Time.now(), "wrist_cam", "ee_link")
        br.sendTransform((x, y, z), (0.5951821, 0.6211687, 0.3691586, 0.35161), rospy.Time.now(), "wrist_cam", "ee_link")
        #br.sendTransform((-0.0755382, 0.00675942, 0.570567), rot1, rospy.Time.now(), "object", "wrist_cam")
        rate.sleep()
