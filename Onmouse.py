## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
count = 0
def onMouse(event, x, y, flags ,param):
    global count
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.imwrite('C:/PycharmProjects/saved_img/{:0}.png' .format(count), param)
        count += 1

def resize_image(img): # resize image to (240,240) and extract effective part of image

    img_height = 240
    img_width = 320
    ret = cv2.resize(img, (img_width, img_height), fx = 1,fy =  1, interpolation = cv2.INTER_AREA)

    return ret
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
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        res_depth = resize_image(depth_image)
        res_color_image = resize_image(color_image)
        res_depthcolor = resize_image(depth_colormap)

        # Stack both images horizontally
        images = np.hstack((res_depthcolor, res_color_image))


        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback('RealSense', onMouse, res_depth)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()