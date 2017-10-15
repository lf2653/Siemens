# -*- coding: utf-8 -*-
from cv2 import *
import numpy as np

IMAGE_WIDTH=1895
IMAGE_HEIGHT=1895
standard=[]
test=[]
test_flag=1
def test2(GaussianBlur_size):
    pass

def comparison(standard,test,img):
    draw_circle = []
    problem_flag=0
    n=len(standard)
    #用于标记是否标准样本参与过比较
    used_flag=np.zeros(n)
    m=len(test)
    for i in range(0 , n):
        for j in range(0,m):
            #中心点坐标距离
            bia1=(standard[i][0][0]-test[j][0][0])*(standard[i][0][0]-test[j][0][0])\
                 +(standard[i][0][1]-test[j][0][1])*(standard[i][0][1]-test[j][0][1])
            bia1=np.sqrt(bia1)
            if bia1>100:
                continue
            #如坐标中心点接近，则可认为是两幅图中相同位置的目标，才能够进行比较
            used_flag[i] = 1
            #包围矩形面积
            bia2=standard[i][1][0]*standard[i][1][1]-test[j][1][0]*test[j][1][1]
            #包围矩形旋转角度
            bia4=standard[i][2]-test[j][2]
            if (bia1>30 or abs(bia2) > 2800):
                draw_circle.append(standard[i])
                problem_flag=1
    #如有样本始终未参与过标记，则可认为在待测图中存在器件缺失
    for i in range(0, n):
        if used_flag[i] == 0:
            problem_flag = 1
            draw_circle.append(standard[i])
    #输出相关信息
    if problem_flag==0:
        font = FONT_HERSHEY_SIMPLEX
        putText(img, 'No Problem', (50, 100), font, 2, (255, 0, 0), 4)
    else:
        n = len(draw_circle)
        for i in range(0, n):
            if draw_circle[i][1][0]>draw_circle[i][1][1]:
                temp=draw_circle[i][1][0]
            else:
                temp = draw_circle[i][1][1]
            circle(img, (int(draw_circle[i][0][0]), int(draw_circle[i][0][1])), int(temp), (255, 0, 0), 3)



namedWindow('CONTROL')
createTrackbar('HminVal','CONTROL',63,180,test2)
createTrackbar('HmaxVal', 'CONTROL', 142, 180, test2)
createTrackbar('SminVal','CONTROL',0,255,test2)
createTrackbar('SmaxVal', 'CONTROL', 255, 255, test2)
createTrackbar('VminVal','CONTROL',0,255,test2)
createTrackbar('VmaxVal', 'CONTROL', 255, 255, test2)
filename = ['0.jpg', '1.jpg', '2.jpg']
for i in range(0, 3):
    name = filename[i]
    print(name)
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
            if (area > 1700 and w_h_ratio > 0.7 and w_h_ratio < 1.3):
                if (i==0):
                    drawContours(drawing, [box], 0, (0, 0, 255), 3)
                    drawContours(img, [box], 0, (0, 0, 255), 3)
                    standard.append(rect)
                    print standard
                else:
                    test.append(rect)
                    print test
        else:
            continue
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


