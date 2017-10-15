# -*- coding: utf-8 -*-
from cv2 import *
from math import *
import numpy as np
from time import clock 
import os
import subprocess

def main():
	cam=VideoCapture(1)
	t_last=clock()
	t=clock()
	while (1):
		key = waitKey(1)
		if key == 27:
			break
		_,g_srcImage = cam.read()
		
		test(g_srcImage)
		t_last=t
		t=clock()
		print('fps',1/(t-t_last))
		os.system('cls')
		
def test(g_srcImage,i=0):
	n=0
	averagecolor=(round(np.mean(g_srcImage[:,:,0])),round(np.mean(g_srcImage[:,:,1])),round(np.mean(g_srcImage[:,:,2])))
	print("屏幕颜色(BGR)：",averagecolor)
	g_grayImage=cvtColor(g_srcImage,COLOR_BGR2GRAY)
	g_grayImage=blur(g_grayImage,(3,3))
	g_dstImage=adaptiveThreshold(g_grayImage,255,ADAPTIVE_THRESH_GAUSSIAN_C,THRESH_BINARY_INV,11,2)
	#imshow("adaptiveThreshold", g_dstImage)
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
			if(M["m00"]>3 and M["m00"]<10000 and np.max(abs(averagecolor-g_srcImage[mc[1],mc[0]]))>50):
				n+=1
				contours_poly=approxPolyDP(c,3,True)
				x, y, w, h=boundingRect(contours_poly)
				rectangle( drawing, (x, y), (x+w, y+h), (0,255,0), 1, 8, 0 )
				circle( drawing, (mc[0],mc[1]), 2,(0,0,255), -1, 8, 0 )
				g_hsvImage=cvtColor(g_srcImage,COLOR_BGR2HSV)
				print("坏点位置：({0:>4},{1:>4})".format(mc[0],mc[1]))
				print("坏点颜色：R={0:<3} G={1:<3} B={2:<3} H={3:<3} S={4:<3} V={5:<3}".format(g_srcImage[mc[1],mc[0],2],g_srcImage[mc[1],mc[0],1],g_srcImage[mc[1],mc[0],0],g_hsvImage[mc[1],mc[0],0],g_hsvImage[mc[1],mc[0],1],g_hsvImage[mc[1],mc[0],2]))
				rectangle( g_srcImage, (x, y), (x+w, y+h), (0,0,255), 1, 8, 0 )
	if n==0:
		print("无坏点！")
	else:
		print("坏点个数：{0}".format(n))
	
	imshow("Countours", drawing)
	imshow("Original", g_srcImage)

if __name__=='__main__':
	main()
