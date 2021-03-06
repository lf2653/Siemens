# -*- coding: utf-8 -*-
from cv2 import *
import numpy as np

def main():
	filename=['c1-0.jpg','c1-1.jpg','c1-2.jpg','c1-3.jpg','c2-0.jpg','c2-1.jpg','c2-2.jpg','c2-3.jpg']
	for i in range(0,8):
		name=filename[i]
		print(name)
		img=imread(name)
		out=cvtColor(img,COLOR_RGB2GRAY)
		R=4
		r=1
		fac=10
		fac_R=1
		fac_r=fac
		out=eye(out,R,r,-fac_R,fac_r)
		vis,out=apply_canny(out,img)
		out,draw=apply_contours(out,img)
		imwrite('e'+name,out)
		imwrite('d'+name,draw)
		#显示效果
		height,width=out.shape[:2]
		res=resize(out,(width/4,height/4))
		imshow('out',res)
		res=resize(draw,(width/6,height/6))
		imshow('draw',res)
		res=resize(vis,(width/6,height/6))
		imshow('vis',res)
		waitKey(0)

def apply_canny(gray,img):
	thrs1=3500
	thrs2=3200
	edge=Canny(gray,thrs1,thrs2,apertureSize=5)
	vis=img.copy()
	vis=np.uint8(vis/2.)
	vis[edge!=0]=(0,255,0)
	return (vis,edge)

def apply_contours(gray,img):
	_,Contours,_=findContours(gray,RETR_TREE,CHAIN_APPROX_NONE)
	drawing=np.zeros(img.shape)
	mu=[]
	mc=[]
	mx=0
	my=0
	s=0.0
	count=0
	n=0
	for c in Contours:
		count+=1
		M=moments(c)
		if M['m00']!=0:
			mc=[int(M['m10']/M['m00']),int(M['m01']/M['m00'])]
			if (M["m00"]>70 and M["m00"]<1000):
				n+=1
				contours_poly=approxPolyDP(c,3,True)
				drawContours(drawing,c,-1,(255,255,255),1,8)
				drawContours(img,c,-1,(0,255,0),1,8)
	print(n)
	return (img,drawing)

def eye(img,R,r,fac_R,fac_r):
	x,y=np.meshgrid(np.linspace(1,R*2+1,R*2+1),np.linspace(1,R*2+1,R*2+1))
	dis=np.sqrt(np.multiply((x-(R+1)),(x-(R+1)))+np.multiply((y-(R+1)),(y-(R+1))))
	flag1=(dis<=r)
	flag2=(np.logical_and(dis>r,dis<=R))
	kernal=flag1*fac_r+flag2*fac_R
	#在python2.7中要加入float()
	kernal=kernal/float(kernal.sum())

	out=filter2D(img,-1,kernal)
	return out

if __name__=='__main__':
	main()
