# -*- coding: utf-8 -*-
from cv2 import *
import numpy as np

def test2(GaussianBlur_size):
    pass


device = VideoCapture(1)
namedWindow('CONTROL')
createTrackbar('HminVal','CONTROL',0,180,test2)
createTrackbar('HmaxVal', 'CONTROL', 0, 180, test2)
createTrackbar('SminVal','CONTROL',0,255,test2)
createTrackbar('SmaxVal', 'CONTROL', 0, 255, test2)
createTrackbar('VminVal','CONTROL',0,255,test2)
createTrackbar('VmaxVal', 'CONTROL', 0, 255, test2)
while (1):
    if device.isOpened():
        ret, img = device.read()
        print img.shape
    else:
        ret = False
    img_hsv = cvtColor(img, COLOR_RGB2HSV)
    HminVal = getTrackbarPos('HminVal', 'CONTROL')
    HmaxVal = getTrackbarPos('HmaxVal', 'CONTROL')
    SminVal = getTrackbarPos('SminVal', 'CONTROL')
    SmaxVal = getTrackbarPos('SmaxVal', 'CONTROL')
    VminVal = getTrackbarPos('VminVal', 'CONTROL')
    VmaxVal = getTrackbarPos('VmaxVal', 'CONTROL')
    drawing = np.zeros(img.shape, 'uint8')
    img_threshold = inRange(img_hsv,(HminVal,SminVal,VminVal), (HmaxVal,SmaxVal,VmaxVal))
    _, contours, _ = findContours(img_threshold, RETR_TREE, CHAIN_APPROX_NONE)
    drawContours(drawing, contours, -1, (255, 0, 0))
    # 显示效果
    height, width = img.shape[:2]
    imshow('threshold', img_threshold)
    imshow('img', img)
    imshow('drawing', drawing)
    k = waitKey(50)
    if k == 27:
        break
destroyAllWindows()
waitKey(0)
