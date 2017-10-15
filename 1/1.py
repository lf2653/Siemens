# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from cv2 import *
import time
from math import *
import numpy as np

class mycsms(QWidget):
    def __init__(self):
        super(mycsms, self).__init__()
        self.initUI()

    def initUI(self):
        self.image = QImage()
        self.image2 = QImage()
        self.temp_image = None
        self.num=0;
        self.setGeometry(100, 100, 650, 600)

        #设置标签，从摄像头中持续读取图像
        self.label_src = QLabel(self)
        self.label_src.move(0,0)

        #设置标签，显示按键时采集的图像
        self.label_get = QLabel(self)
        self.label_get.move(0,330)

        #设置按键
        self.qbtn = QPushButton('GET', self)
        self.qbtn.resize(self.qbtn.sizeHint())
        self.qbtn.move(500, 300)

        self.qbtn_exit = QPushButton('exit', self)
        self.qbtn_exit.resize(self.qbtn.sizeHint())
        self.qbtn_exit.move(500, 350)

        #设置连接关系
        self.qbtn.clicked.connect(self.clicked_GET)
        self.qbtn_exit.clicked.connect(QCoreApplication.instance().quit)

        self.show_Or()

    # 读原始图
    def show_Or(self):
        self.temp_image = imread('2.jpg')
        height, width, bytesPerComponent = self.temp_image.shape
        bytesPerLine = bytesPerComponent * width
        res = resize(self.temp_image, (width / 8, height / 8))
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        # 变换彩色空间顺序
        cvtColor(res,COLOR_BGR2RGB,res)
        # 转为QImage对象
        self.image = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        #显示图片
        self.label_src.setPixmap(QPixmap.fromImage(self.image))
        self.label_src.resize(self.image.size())

    #获取图像并显示
    def clicked_GET(self):
        n = 0
        np.mean(self.temp_image[:, :, 0])
        averagecolor = (
        round(np.mean(self.temp_image[:, :, 0])), round(np.mean(self.temp_image[:, :, 1])), round(np.mean(self.temp_image[:, :, 2])))
        print("BGR", averagecolor)
        g_grayImage = cvtColor(self.temp_image, COLOR_BGR2GRAY)
        g_grayImage = blur(g_grayImage, (3, 3))
        g_dstImage = adaptiveThreshold(g_grayImage, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY_INV, 11, 2)
        _, g_vContours, g_vHierarchy = findContours(g_dstImage, RETR_EXTERNAL, CHAIN_APPROX_NONE)
        height, width, bytesPerComponent = self.temp_image.shape
        drawing = np.zeros(self.temp_image.shape,'uint8')
        print(self.temp_image.shape)
        mu = []
        mc = []
        mx = 0
        my = 0
        s = 0.0
        count = 0
        for c in g_vContours:
            count += 1
            M = moments(c)
            mu.append(moments(c))
            if M['m00'] != 0:
                mc = [int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])]
                color = (255, 255, 255)
                drawContours(drawing, c, -1, color, 1, 8)
                if (M["m00"] > 5 and M["m00"] < 10000 and np.max(abs(averagecolor - self.temp_image[mc[1], mc[0]])) > 100):
                    n += 1
                    contours_poly = approxPolyDP(c, 3, True)
                    x, y, w, h = boundingRect(contours_poly)
                    rectangle(drawing, (x, y), (x + w, y + h), (0, 255, 0), 1, 8, 0)
                    circle(drawing, (mc[0], mc[1]), 5, (0, 0, 255), -1, 8, 0)
                    rectangle(self.temp_image, (x, y), (x + w, y + h), (0, 0, 255), 1, 8, 0)

                    print("坏点位置：({0:>4},{1:>4})".format(mc[0], mc[1]))
                    print(
                    "坏点颜色：R={0:<3} G={1:<3} B={2:<3}".format(self.temp_image[mc[1], mc[0], 2], self.temp_image[mc[1], mc[0], 1],
                                                             self.temp_image[mc[1], mc[0], 0]))
        '''
        if n == 0:
            print("无坏点！")
        else:
            print("坏点个数：{0}".format(n))
        '''
        # 变换彩色空间顺序
        cvtColor(drawing, COLOR_BGR2RGB, drawing)
        height, width = drawing.shape[:2]
        res = resize(drawing, (width / 8, height / 8))
        print(res.shape)
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        # 转为QImage对象
        self.image2 = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        #显示图片
        self.label_get.setPixmap(QPixmap.fromImage(self.image2))
        self.label_get.resize(self.image2.size())

    #退出程序
    def clicked_EXIT(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myshow = mycsms()
    myshow.show()
    sys.exit(app.exec_())
