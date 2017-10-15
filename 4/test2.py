# -*- coding:utf-8 -*-
__author__ = 'Microcosm'

from cv2 import *
import numpy as np
from matplotlib import pyplot as plt

img4=imread("2.JPG")
w=img4.shape[0]
h=img4.shape[1]
img4 = resize(img4, (w / 3, h / 3))
img = imread("2.JPG", 0)
w, h = img.shape[::-1]
img = resize(img, (w / 3, h / 3))
img2 = img.copy()
img3 = imread("1.JPG", 0)
w, h = img3.shape[::-1]
img3 = resize(img3, (w / 3, h / 3))
w, h = img3.shape[::-1]
h_4 = int(h / 4)
w_4 = int(w / 4)
template = img3[h_4:h_4 * 3, w_4:w_4 * 3].copy()
w, h = template.shape[::-1]
img = img2.copy()

res = matchTemplate(img, template, TM_CCOEFF_NORMED)
threshold_temp=0.7
loc=np.where(res>=threshold_temp)
for pt in zip(*loc[::-1]):
    rectangle(img4,pt,(pt[0]+w,pt[1]+h),(0,0,255),1)

imshow('result',img4)
waitKey(0)


