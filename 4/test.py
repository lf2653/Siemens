# -*- coding:utf-8 -*-  
__author__ = 'Microcosm'  
  
from cv2 import *
import numpy as np  
from matplotlib import pyplot as plt  
  
img = imread("4.JPG", 0)
w, h = img.shape[::-1]
img = resize(img, (w / 3, h / 3))
img2 = img.copy()
img3 = imread("4.JPG", 0)
w, h = img3.shape[::-1]
img3 = resize(img3, (w / 3, h / 3))
w, h = img3.shape[::-1]
h_4=int(h/4)
w_4=int(w/4)
template = img3[h_4:h_4*3,w_4:w_4*3].copy()
w, h = template.shape[::-1]

# 6 中匹配效果对比算法  
methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED', 'TM_CCORR',  
           'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED']  
  
for meth in methods:  
    img = img2.copy()  
  
    method = eval(meth)  
  
    res = matchTemplate(img,template,method)  
    min_val, max_val, min_loc, max_loc = minMaxLoc(res)  
    print min_val,max_val
    if method in [TM_SQDIFF, TM_SQDIFF_NORMED]:  
        top_left = min_loc  
    else:  
        top_left = max_loc  
    bottom_right = (top_left[0] + w, top_left[1] + h)  
  
    rectangle(img,top_left, bottom_right, 255, 4)
  
    print meth  
    plt.subplot(221), plt.imshow(img2,cmap= "gray")  
    plt.title('Original Image'), plt.xticks([]),plt.yticks([])  
    plt.subplot(222), plt.imshow(template,cmap= "gray")  
    plt.title('template Image'),plt.xticks([]),plt.yticks([])  
    plt.subplot(223), plt.imshow(res,cmap= "gray")  
    plt.title('Matching Result'), plt.xticks([]),plt.yticks([])  
    plt.subplot(224), plt.imshow(img,cmap= "gray")  
    plt.title('Detected Point'),plt.xticks([]),plt.yticks([])  
    plt.show()  
