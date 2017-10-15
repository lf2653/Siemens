# -*- coding: utf-8 -*-
from cv2 import *
import numpy as np

roi=None
ROI_x=10
ROI_y=10
ROI_w=300
ROI_h=300
def test():
    pass

def GET_ROI(img):
    ROI = img[ROI_y:ROI_y + ROI_h, ROI_x:ROI_x + ROI_w]
    return ROI


if __name__ == "__main__":
    device = VideoCapture(0)
    createTrackbar('minVal','threshold',0,255,test)
    createTrackbar('maxVal', 'threshold', 0, 255, test)
    while(1):
        if device.isOpened():
            ret, frame = device.read()
        else:
            ret = False
        roi=GET_ROI(frame)
        rectangle(frame,(ROI_x,ROI_y),(ROI_x+ROI_w,ROI_y+ ROI_h),(0,255,0),3)
        imshow('src', frame)
        imshow('roi',roi)
        key = waitKey(150)
        if key==27:
            break
