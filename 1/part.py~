# -*- coding: utf-8 -*-
from cv2 import *
from math import *
import numpy as np
from time import clock 
import os
import subprocess

def main():
	for i in range(1,5):
		g_srcImage=imread('{0}.jpg'.format(i))
		print(i)
		test(g_srcImage,i)
		key = waitKey(1)
		if key == 27:
			break
		
def test(g_srcImage,i):
	n=0
	averagecolor=(round(np.mean(g_srcImage[:,:,0])),round(np.mean(g_srcImage[:,:,1])),round(np.mean(g_srcImage[:,:,2])))
	print("BGR",averagecolor)
	g_grayImage=cvtColor(g_srcImage,COLOR_BGR2GRAY)
	g_grayImage=blur(g_grayImage,(3,3))
	g_dstImage=adaptiveThreshold(g_grayImage,255,ADAPTIVE_THRESH_GAUSSIAN_C,THRESH_BINARY_INV,11,2)
	_,g_vContours,g_vHierarchy=findContours(g_dstImage,RETR_EXTERNAL,CHAIN_APPROX_NONE)
	drawing= np.zeros(g_srcImage.shape)
	mu=[]
	mc=[]
	mx=0
	my=0
	s=0.0
	count=0
	for c in g_vContours:
		count+=1
		M=moments(c)
		mu.append(moments(c))
		if M['m00']!=0:
			mc=[int(M['m10'] / M['m00']),int(M['m01'] / M['m00'])]
			color = ( 255, 255,255 )
			drawContours( drawing, c, -1, color, 1, 8)
			if(M["m00"]>5 and M["m00"]<10000 and np.max(abs(averagecolor-g_srcImage[mc[1],mc[0]]))>100):
				n+=1
				contours_poly=approxPolyDP(c,3,True)
				x, y, w, h=boundingRect(contours_poly)
				rectangle( drawing, (x, y), (x+w, y+h), (0,255,0), 1, 8, 0 )
				circle( drawing, (mc[0],mc[1]), 5,(0,0,255), -1, 8, 0 )
				rectangle( g_srcImage, (x, y), (x+w, y+h), (0,0,255), 1, 8, 0 )
				
				print("坏点位置：({0:>4},{1:>4})".format(mc[0],mc[1]))
				print("坏点颜色：R={0:<3} G={1:<3} B={2:<3}".format(g_srcImage[mc[1],mc[0],2],g_srcImage[mc[1],mc[0],1],g_srcImage[mc[1],mc[0],0]))
	if n==0:
		print("无坏点！")
	else:
		print("坏点个数：{0}".format(n))
	height,width=drawing.shape[:2]
	res=resize(g_dstImage,(width/8,height/8))
	imshow("adaptiveThreshold", res)
	res=resize(drawing,(width/8,height/8))
	imshow("Countours", res)
	res=resize(g_srcImage,(width/8,height/8))
	imshow("Original", res)
	imwrite('c{0}.jpg'.format(i), g_srcImage)
	imwrite('d{0}.jpg'.format(i), drawing)
	waitKey(0)

if __name__=='__main__':
	main()
