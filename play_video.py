## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style

count = 800
# learningDigit_test =

def onMouse(event, x, y, flags ,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y, param[y][x])

def resize_image(img): # resize image to (240,240) and extract effective part of image

    img_height = 240
    img_width = 320
    ret = cv2.resize(img, (img_width, img_height), fx = 1,fy =  1, interpolation = cv2.INTER_AREA)
    # gray_ret = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    new_image = ret[90:150][0:240]
    return ret

# def learningDigit():
#     while count < 500:
#         img = cv2.imread('C:/PycharmProjects/images/frames{:0}.jpg'.format(count))
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        #주석처리
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.15), cv2.COLORMAP_JET)


        res_depth = resize_image(depth_image)
        res_depth_color = resize_image(depth_colormap)
        res_color_image = resize_image(color_image)
        # Stack both images horizontally
        images = np.hstack((res_depth_color, res_color_image))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback('RealSense', onMouse, res_depth_color)
        cv2.imshow('RealSense', images)
        # cv2.imwrite('C:/PycharmProjects/depth_img/frames{:0}.png'.format(count), res_depth)
        # cv2.imwrite('C:/PycharmProjects/depth_color_img/color_frames{:0}.png'.format(count), res_depth_color)
        # cv2.imwrite('C:/PycharmProjects/color_img/color_frames{:0}.png'.format(count), res_color_image)
        # count += 1
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()