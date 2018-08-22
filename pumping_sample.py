import cv2
import math
import tensorflow as tf
import numpy as np
import pandas as pd

count = 0
click = 0
var = [0, 0, 0, 0, 0, 0]
theta = 5

#csv파일에서 받아온 경추(xy1), 요추(xy2) (x,y)값
df_xy1 = pd.read_csv('C:/PycharmProjects/depth_img/data.csv',usecols=[1,2],header = None)
df_xy2 = pd.read_csv('C:/PycharmProjects/depth_img/data.csv',usecols=[4,5], header = None)

#csv파일에서 받아온 경추, 요추 각각의 depth 값
df_depth1 = pd.read_csv('C:/PycharmProjects/depth_img/data.csv',usecols=[3],header = None)
df_depth2 = pd.read_csv('C:/PycharmProjects/depth_img/data.csv',usecols=[6],header = None)

# mouse handling 사진을 읽어서 마우스로 경추, 요추 순서대로 클릭하면 좌표를 리스트에 추가해줌
def onMouse(event, x, y, flags ,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        depth_ret = cv2.imread('C:/PycharmProjects/img_rotation/rot_img{:0}.png' .format(count), cv2.IMREAD_ANYDEPTH)
        global click
        if click == 0:
            var[0] = x
            var[1] = y
            var[2] = depth_ret[var[1]][var[0]]

            click += 1
        elif click == 1:
            var[3] = x
            var[4] = y
            var[5] = depth_ret[var[4]][var[3]]

            list.append([str(param .format(count)), var[0],var[1], var[2], var[3], var[4], var[5]])
            click = 0


# resize function
# def resize_image(img):
#     img_height = 240
#     img_width = 240
#     ret = cv2.resize(img, (img_width, img_height), fx = 1,fy =  1, interpolation = cv2.INTER_AREA)
#
#     return ret
while theta < 95:
    list = []
    angle = math.radians(theta)
    while count < 99 :
        ret_depth = cv2.imread('C:/PycharmProjects/depth_img/{:0}.png'.format(count+1),     cv2.IMREAD_ANYDEPTH)
        ret_color = cv2.imread('C:/PycharmProjects/color_img/{:0}.png'.format(count+1))
        rows = ret_color.shape[0] # 240
        cols = ret_color.shape[1] # 320

        x1 = df_xy1[1][count]
        y1 = df_xy1[2][count]
        x2 = df_xy2[4][count]
        y2 = df_xy2[5][count]

        #좌표 theta값에 따라 회전변환하는 공식
        rX1 = int((x1-cols/2)*math.cos(angle) - (y1-rows/2)*math.sin(angle)+cols/2)
        rY1 = int((x1-cols/2)*math.sin(angle) + (y1-rows/2)*math.cos(angle)+rows/2)
        rX2 = int((x2-cols/2)*math.cos(angle) - (y2-rows/2)*math.sin(angle)+cols/2)
        rY2 = int((x2-cols/2)*math.sin(angle) + (y2-rows/2)*math.cos(angle)+rows/2)

        # 이미지를 theta 각도에 따라 회전
        rot_color_img = cv2.getRotationMatrix2D((cols / 2, rows / 2), -1*theta, 1)
        changed_img = cv2.warpAffine(ret_color, rot_color_img, (cols, rows))
        cv2.imwrite('C:/PycharmProjects/rotation/rot_{:0}_img{:1}.png'.format(theta, (count+1)),changed_img)
        cv2.line(changed_img, (rX1,rY1), (rX2, rY2), (255, 255, 255),3)

        # cv2.imshow('test', changed_img)
        # k = cv2.waitKey(0)
        # if k == 27:  # esc key
        #     cv2.destroyAllWindows()
        # cv2.setMouseCallback('test', onMouse)
        list.append([str('C:/PycharmProjects/rotation/rot_{:0}_img{:1}.png'.format(theta, (count+1))), rX1, rY1, df_depth1[3][count], rX2, rY2, df_depth2[6][count]])
        count += 1

        # k = cv2.waitKey(0)
        # if k == 27:  # esc key
        #     cv2.destroyAllWindows()
    data = pd.DataFrame(list)
    data.to_csv("C:/PycharmProjects/rotation/rot_data{:0}.csv".format(theta),header = False, index = False,  mode='w')
    theta += 5
    count = 0
    print(theta)