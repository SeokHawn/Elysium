import cv2
import pandas as pd

count = 0
click = 0
list = []
var = [0, 0, 0, 0, 0, 0]
# mouse handling
def onMouse(event, x, y, flags ,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        depth_ret = cv2.imread('C:/PycharmProjects/depth_img/{:0}.png' .format(count), cv2.IMREAD_ANYDEPTH)
        global click
        if click == 0:
            var[0] = x
            var[1] = y
            var[2] = depth_ret[var[1]][var[0]]
            # list.append([str('C:/PycharmProjects/depth_img/{:0}.png' .format(count+1)), x,y, depth_ret[y][x]])

            click += 1
        elif click == 1:
            var[3] = x
            var[4] = y
            var[5] = depth_ret[var[4]][var[3]]

            list.append([str('C:/PycharmProjects/depth_img/{:0}.png' .format(count)), var[0],var[1], var[2], var[3], var[4], var[5]])
            click = 0


# resize function
# def resize_image(img):
#     img_height = 240
#     img_width = 240
#     ret = cv2.resize(img, (img_width, img_height), fx = 1,fy =  1, interpolation = cv2.INTER_AREA)
#
#     return ret


while count < 99:
    ret_depth = cv2.imread('C:/PycharmProjects/depth_img/{:0}.png'.format(count+1), cv2.IMREAD_ANYDEPTH)
    ret_color = cv2.imread('C:/PycharmProjects/color_img/{:0}.png'.format(count+1))



    cv2.imshow('test', ret_color)
    cv2.setMouseCallback('test', onMouse, ret_depth)
    count += 1

    k = cv2.waitKey(0)
    if k == 27:  # esc key
        cv2.destroyAllWindows()

data = pd.DataFrame(list)
data.to_csv("C:/PycharmProjects/depth_img/data.csv",header = False, index = False,  mode='w')