# -*- coding: utf-8 -*-
from cv2 import *
import numpy as np

def test(test):
    pass

def main():
    namedWindow('threshold')
    createTrackbar('minVal','threshold',0,255,test)
    createTrackbar('maxVal', 'threshold', 0, 255, test)
    img=imread('c1-0.jpg',1)
    gray=cvtColor(img,COLOR_RGB2GRAY)
    while(1):
        minVal = getTrackbarPos('minVal', 'threshold')
        maxVal = getTrackbarPos('maxVal', 'threshold')
        drawing = np.zeros(img.shape)
        ret,edges=threshold(gray,minVal,maxVal,THRESH_BINARY_INV)
        _,contours,_=findContours(edges,RETR_TREE,CHAIN_APPROX_NONE)
        count = 0
        n = 0
        maxm00=2000
        max_cnt=None
        for cnt in contours:
            count += 1
            M = moments(cnt)
            if M['m00'] != 0:
                mc = [int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])]
                if (M["m00"] > maxm00 ):
                    n += 1
                    max_cnt=cnt
                    drawContours(drawing, cnt, -1, (255, 0, 0), 5, 8)
        x,y,w,h=boundingRect(max_cnt)
        if (w > h):
            h = w
        else:
            w = h
        #到此为止,获得送入网络模型的ROI
        ROI = img[y:y + h, x:x + w]
        #显示效果
        height,width=img.shape[:2]
        res=resize(edges,(width/6,height/6))
        imshow('threshold',res)
        res=resize(drawing,(width/6,height/6))
        imshow('out',res)
        res=resize(img,(width/6,height/6))
        imshow('img',res)
        k=waitKey(1000)
        if k==27:
            break
    destroyAllWindows()


if __name__=='__main__':
    main()