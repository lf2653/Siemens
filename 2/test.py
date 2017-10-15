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
		#out=eye(out,R,r,-fac_R,fac_r)
		vis, out = apply_canny(out, img)
		#显示效果
		height,width=out.shape[:2]
		res=resize(out,(width/6,height/6))
		imshow('out',res)
		res=resize(vis,(width/6,height/6))
		imshow('vis',res)
		waitKey(0)

def apply_canny(gray,img):
	thrs2=4000
	thrs1=100
	edge=Canny(gray,thrs1,thrs2,apertureSize=5)
	vis=img.copy()
	vis=np.uint8(vis/2.)
	vis[edge!=0]=(0,255,0)
	return (vis,edge)


def eye(img,R,r,fac_R,fac_r):
	x,y=np.meshgrid(np.linspace(1,R*2+1,R*2+1),np.linspace(1,R*2+1,R*2+1))
	dis=np.sqrt(np.multiply((x-(R+1)),(x-(R+1)))+np.multiply((y-(R+1)),(y-(R+1))))
	flag1=(dis<=r)
	flag2=(np.logical_and(dis>r,dis<=R))
	kernal=flag1*fac_r+flag2*fac_R
	kernal=float(kernal)/kernal.sum()

	out=filter2D(img,-1,kernal)
	return out

if __name__=='__main__':
	main()
