#!/usr/bin/env python3
import rospy
import os
from sensor_msgs.msg import CompressedImage
import numpy as np
import cv2

def streaming(msg, rate, stream, image_pub):
    while not rospy.is_shutdown():
        _, frame = stream.read()
        msg.header.stamp = rospy.Time.now()
        msg.format = 'jpeg'
        msg.data = np.array(cv2.imencode('.jpeg', frame)[1]).tostring()
        image_pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    src = 0 # 'http://[Pi IP]:8081/'
    stream = cv2.VideoCapture(src)

    hn = os.environ.get('HOSTNAME')
    hn = 'pi' if hn is None else hn

    image_pub = rospy.Publisher(f'/nautilus/{hn}/usbcam', CompressedImage, queue_size=1)
    rospy.init_node('compress_stream')
    rate = rospy.Rate(24)

    msg = CompressedImage()

    streaming(msg, rate, stream, image_pub)
