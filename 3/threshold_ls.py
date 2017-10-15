# -*- coding: utf-8 -*-
from cv2 import *
import numpy as np


test={}
IMAGE_WIDTH=1895
IMAGE_HEIGHT=1895
def test2(GaussianBlur_size):
    pass

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
    test_flag = 1
    n = 0
    #roi=GET_ROI(img)
    #imshow('roi', roi)
    while (1):
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
                if(area > 1700 and w_h_ratio > 0.7 and w_h_ratio < 1.3 ):
                    drawContours(drawing, [box], 0, (0, 0, 255), 1)
                    drawContours(img, [box], 0, (0, 0, 255), 1)
                    if (n<5):
                        print box
                        print rect
                        n=n+1
            else:
                continue
        #drawContours(drawing, contours, -1, (255, 0, 0), 5, 8)
        # 显示效果
        res = resize(img_threshold, (450, 450))
        imshow('threshold', res)
        res=resize(img,(450,450))
        imshow('img', res)
        res = resize(drawing, (450, 450))
        imshow('drawing', res)
        k = waitKey(300)
        if k == 27:
            break
destroyAllWindows()
waitKey(0)
