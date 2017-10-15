# -*- coding: utf-8 -*-
from cv2 import *
import numpy as np

IMAGE_WIDTH=1895
IMAGE_HEIGHT=1895
standard=[]
test=[]
draw_circle=[]
test_flag=1
def test2(GaussianBlur_size):
    pass

def comparison(standard,test,img):
    problem_flag=0
    if len(standard)==len(test):
        n=len(test)
        for i in range(0 , n):
            #中心点坐标
            bia1=(standard[i][0][0]-test[i][0][0])*(standard[i][0][0]-test[i][0][0])\
                 +(standard[i][0][1]-test[i][0][1])*(standard[i][0][1]-test[i][0][1])
            #包围矩形长度
            bia2=standard[i][1][0]-test[i][1][0]

            #包围矩形宽度
            bia3=standard[i][1][1]-test[i][1][1]
            #包围矩形旋转角度
            bia4=standard[i][2]-test[i][2]
            if (bia1>200 or abs(bia2) > 5  or abs(bia3) > 5):
                draw_circle.append(standard[i])
                problem_flag=1
    else:
        problem_flag = 1
    #输出相关信息
    if problem_flag==0:
        font = FONT_HERSHEY_SIMPLEX
        putText(img, 'No Problem', (50, 100), font, 2, (255, 0, 0), 4)
    else:
        n = len(draw_circle)
        for i in range(0, n):
            temp = max(draw_circle[i][1][0], draw_circle[i][1][1])
            circle(img, (int(draw_circle[i][0][0]), int(draw_circle[i][0][1])), temp, (255, 0, 0), 3)


namedWindow('CONTROL')
createTrackbar('HminVal','CONTROL',111,180,test2)
createTrackbar('HmaxVal', 'CONTROL', 136, 180, test2)
createTrackbar('SminVal','CONTROL',0,255,test2)
createTrackbar('SmaxVal', 'CONTROL', 71, 255, test2)
createTrackbar('VminVal','CONTROL',0,255,test2)
createTrackbar('VmaxVal', 'CONTROL', 255, 255, test2)
filename = ['0.jpg', '1.jpg', '2.jpg']
for i in range(0, 3):
    name = filename[i]
    print(name)
    test_flag = 1
    #roi=GET_ROI(img)
    #imshow('roi', roi)
    img = imread(name, 1)
    img = blur(img, (5, 5))
    img = resize(img, (900, 900))
    img_hsv = cvtColor(img, COLOR_RGB2HSV)
    HminVal = getTrackbarPos('HminVal', 'CONTROL')
    HmaxVal = getTrackbarPos('HmaxVal', 'CONTROL')
    SminVal = getTrackbarPos('SminVal', 'CONTROL')
    SmaxVal = getTrackbarPos('SmaxVal', 'CONTROL')
    VminVal = getTrackbarPos('VminVal', 'CONTROL')
    VmaxVal = getTrackbarPos('VmaxVal', 'CONTROL')
    drawing = np.zeros(img.shape, 'uint8')
    img_threshold = inRange(img_hsv,(HminVal,SminVal,VminVal), (HmaxVal,SmaxVal,VmaxVal))
    kernel=np.ones((3,3),np.uint8)
    img_threshold = dilate(img_threshold,kernel,iterations=1)
    img_threshold = erode(img_threshold, kernel, iterations=1)
    _, contours, _ = findContours(img_threshold, RETR_TREE, CHAIN_APPROX_NONE)
    for c in contours:
        rect = minAreaRect(c)
        x,y=rect[0]
        w,h=rect[1]
        if(w>0 and h>0):
            area=w*h
            w_h_ratio=w/h
            angle=rect[2]
            box = boxPoints(rect)
            box = np.int0(box)
            if(area > 2000 and w_h_ratio > 1.5 and w_h_ratio < 2.5 ):
                drawContours(drawing, [box], 0, (0, 0, 255), 1)
                drawContours(img, [box], 0, (0, 0, 255), 1)
                if (test_flag==1):
                    if (i==0):
                        standard.append(rect)
                        print standard
                    else:
                        test.append(rect)
                        print test
        else:
            continue
    if (test_flag == 1):
        test_flag=0
    #drawContours(drawing, contours, -1, (255, 0, 0), 5, 8)
    # 显示效果
    if i!=0:
        comparison(standard,test,img)
        test=[]
    res = resize(img_threshold, (450, 450))
    imshow('threshold', res)
    res = resize(img, (450, 450))
    imshow('img', res)
    res = resize(drawing, (450, 450))
    imshow('drawing', res)
    k = waitKey(0)

destroyAllWindows()
waitKey(0)


