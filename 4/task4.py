# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from cv2 import *
import time
from math import *
import numpy as np


class Timer(QThread):
    def __init__(self, signal="updateTime()", parent=None):
        super(Timer, self).__init__(parent)
        self.stoped = False
        self.signal = signal
        self.mutex = QMutex()

    def run(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
        while True:
            if self.stoped:
                return
            self.emit(SIGNAL(self.signal))
            # 200毫秒发送一次信号
            time.sleep(0.4)

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stoped = True

    def isStoped(self):
        with QMutexLocker(self.mutex):
            return self.stoped

class Ui_Task2(QWidget):
    def __init__(self):
        super(Ui_Task2, self).__init__()
        self.setupUi1()
        self.setupUi2()

    # 大部分图像和部件设置及自定义变量
    def setupUi1(self):
        self.resize(1020, 620)
        #标定图像左上角位置
        self.label_realtime = QLabel(self)
        self.label_realtime.setGeometry(QRect(10, 10, 66, 17))
        self.label_BackGround = QLabel(self)
        self.label_BackGround.setGeometry(QRect(500, 10, 66, 17))
        self.label_BackGround1 = QLabel(self)
        self.label_BackGround1.setGeometry(QRect(500, 10, 66, 17))
        self.label_BackGround2 = QLabel(self)
        self.label_BackGround2.setGeometry(QRect(500, 145, 66, 17))
        self.label_BackGround3 = QLabel(self)
        self.label_BackGround3.setGeometry(QRect(635, 10, 66, 17))
        self.label_BackGround4 = QLabel(self)
        self.label_BackGround4.setGeometry(QRect(635, 145, 66, 17))
        self.label_Sampling = QLabel(self)
        self.label_Sampling.setGeometry(QRect(10, 300, 66, 17))
        self.label_result = QLabel(self)
        self.label_result.setGeometry(QRect(500, 300, 66, 17))
        #滑动块参数配置
        self.threshold_horizontalSlider = QSlider(self)
        self.threshold_horizontalSlider.setGeometry(QRect(780, 260, 221, 29))
        self.threshold_horizontalSlider.setMaximum(150000)
        self.threshold_horizontalSlider.setMinimum(0)
        self.threshold_horizontalSlider.setProperty("value", 30000)
        self.threshold_horizontalSlider.setOrientation(Qt.Horizontal)
        #LCD显示配置
        self.lcdNumber_3 = QLCDNumber(self)
        self.lcdNumber_3.setGeometry(QRect(920, 300, 81, 31))
        #按键配置
        self.clearbgButton = QPushButton(self)
        self.clearbgButton.setGeometry(QRect(790, 550, 98, 27))
        self.samButton = QPushButton(self)
        self.samButton.setGeometry(QRect(900, 550, 98, 27))
        self.exitButton = QPushButton(self)
        self.exitButton.setGeometry(QRect(900, 590, 98, 27))
        #文字显示配置
        self.label_8 = QLabel(self)
        self.label_8.setGeometry(QRect(790, 300, 101, 31))
        self.label = QLabel(self)
        self.label.setGeometry(QRect(10, 280, 66, 17))
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(500, 280, 100, 17))
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QRect(10, 570, 80, 17))
        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QRect(500, 570, 66, 17))

        #程序中出现的字符串
        self.setWindowTitle("Task2-2")
        self.clearbgButton.setText("Clear BG")
        self.samButton.setText("Sampling")
        self.exitButton.setText("Exit")
        self.label_8.setText("threshold")
        self.label.setText("Realtime")
        self.label_2.setText("BackGround")
        self.label_3.setText("Sampling")
        self.label_4.setText("Result")

        #自定义参量
        self.threshold_temp=30000
        self.canny_thrs1=3500
        self.canny_thrs2 = 3200
        self.image_realtime = QImage()
        #用于显示黑图
        self.image_BackGround = QImage()
        #显示背景图
        self.image_BackGround1 = QImage()
        self.image_BackGround2 = QImage()
        self.image_BackGround3 = QImage()
        self.image_BackGround4 = QImage()
        self.image_Sampling = QImage()
        self.image_result= QImage()
        self.temp_image = None  # 用于存取摄像头图像
        self.template=None
        self.ROI = None  # 用于存取ROI
        self.bg1 = None
        self.bg1_90 = None
        self.bg1_180 = None
        self.bg1_270 = None
        self.bg2 = None
        self.bg2_90 = None
        self.bg2_180 = None
        self.bg2_270 = None
        self.bg3 = None
        self.bg3_90 = None
        self.bg3_180 = None
        self.bg3_270 = None
        self.bg4 = None
        self.bg4_90 = None
        self.bg4_180 = None
        self.bg4_270 = None

        self.samp_hist=None
        self.bg1_hist = None
        self.bg2_hist = None
        self.bg3_hist = None
        self.bg4_hist = None

        self.bg1_90_hist = None
        self.bg1_180_hist = None
        self.bg1_270_hist = None

        self.bg2_90_hist = None
        self.bg2_180_hist = None
        self.bg2_270_hist = None

        self.bg3_90_hist = None
        self.bg3_180_hist = None
        self.bg3_270_hist = None

        self.bg4_90_hist = None
        self.bg4_180_hist = None
        self.bg4_270_hist = None

        self.bg1_dis = 0
        self.bg2_dis = 0
        self.bg3_dis = 0
        self.bg4_dis = 0
        self.bg1_flag = 0
        self.bg2_flag = 0
        self.bg3_flag = 0
        self.bg4_flag = 0
        #取得白色图
        self.black = np.zeros((270,270,3),np.uint8)
        height = self.black.shape[0]
        width = self.black.shape[1]
        for i in range(height):
            for j in range(width):
                self.black[i, j][0] =255
                self.black[i, j][1] = 255
                self.black[i, j][2] = 255
        self.device = VideoCapture(1)
        self.device.set(3,1920)
        self.device.set(4,1080)
        self.playTimer = Timer("updatePlay()")

        QObject.connect(self.threshold_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber_3.display)
        self.lcdNumber_3.display(30000)
        QMetaObject.connectSlotsByName(self)

        #自定义连接
        #将滑动条参数回传到系统里
        self.threshold_horizontalSlider.valueChanged.connect(self.get_threshold_temp)
        #实时显示摄像头画面
        self.connect(self.playTimer, SIGNAL("updatePlay()"), self.show_Realtime)
        #按下按键时
        self.samButton.clicked.connect(self.clicked_GET)
        self.clearbgButton.clicked.connect(self.CLEAR_BG)
        self.exitButton.clicked.connect(QCoreApplication.instance().quit)


        #取得背景图
        self.GET_BG1_Button = QPushButton(self)
        self.GET_BG2_Button = QPushButton(self)
        self.GET_BG3_Button = QPushButton(self)
        self.GET_BG4_Button = QPushButton(self)

        self.GET_BG1_Button.setText("GET_BG1")
        self.GET_BG2_Button.setText("GET_BG2")
        self.GET_BG3_Button.setText("GET_BG3")
        self.GET_BG4_Button.setText("GET_BG4")

        self.GET_BG1_Button.setGeometry(QRect(825, 440, 70, 27))
        self.GET_BG2_Button.setGeometry(QRect(825, 480, 70, 27))
        self.GET_BG3_Button.setGeometry(QRect(930, 440, 70, 27))
        self.GET_BG4_Button.setGeometry(QRect(930, 480, 70, 27))

        self.connect(self.GET_BG1_Button, SIGNAL("clicked()"), self.GET_BG1)
        self.connect(self.GET_BG2_Button, SIGNAL("clicked()"), self.GET_BG2)
        self.connect(self.GET_BG3_Button, SIGNAL("clicked()"), self.GET_BG3)
        self.connect(self.GET_BG4_Button, SIGNAL("clicked()"), self.GET_BG4)
    # 设置ROI选择框
    def setupUi2(self):
        self.ROI_x = 550
        self.ROI_y = 50
        self.ROI_w = 960
        self.ROI_h = 960

        self.Label_ROI_x = QLabel(self)
        self.Label_ROI_y = QLabel(self)
        self.Label_ROI_w = QLabel(self)
        self.Label_ROI_h = QLabel(self)

        self.Label_ROI_x.setText(str(self.ROI_x))
        self.Label_ROI_y.setText(str(self.ROI_y))
        self.Label_ROI_w.setText(str(self.ROI_w))
        self.Label_ROI_h.setText(str(self.ROI_h))

        self.Label_ROI_x.setGeometry(QRect(790, 360, 50, 27))
        self.Label_ROI_y.setGeometry(QRect(790, 400, 50, 27))
        self.Label_ROI_w.setGeometry(QRect(895, 360, 50, 27))
        self.Label_ROI_h.setGeometry(QRect(895, 400, 50, 27))

        self.ROI_x_Button = QPushButton(self)
        self.ROI_y_Button = QPushButton(self)
        self.ROI_w_Button = QPushButton(self)
        self.ROI_h_Button = QPushButton(self)

        self.ROI_x_Button.setText("ROI_x")
        self.ROI_y_Button.setText("ROI_y")
        self.ROI_w_Button.setText("ROI_w")
        self.ROI_h_Button.setText("ROI_h")

        self.ROI_x_Button.setGeometry(QRect(825, 360, 70, 27))
        self.ROI_y_Button.setGeometry(QRect(825, 400, 70, 27))
        self.ROI_w_Button.setGeometry(QRect(930, 360, 70, 27))
        self.ROI_h_Button.setGeometry(QRect(930, 400, 70, 27))

        self.connect(self.ROI_x_Button, SIGNAL("clicked()"), self.slot_ROI_x)
        self.connect(self.ROI_y_Button, SIGNAL("clicked()"), self.slot_ROI_y)
        self.connect(self.ROI_w_Button, SIGNAL("clicked()"), self.slot_ROI_w)
        self.connect(self.ROI_h_Button, SIGNAL("clicked()"), self.slot_ROI_h)
    # 读摄像头
    def show_Realtime(self):
        if self.device.isOpened():
            ret, frame = self.device.read()
            self.temp_image = frame.copy()
            self.GET_ROI()
        else:
            ret = False
        rectangle(frame, (self.ROI_x, self.ROI_y), (self.ROI_x + self.ROI_w, self.ROI_y + self.ROI_h), (0, 255, 0), 3)
        height, width, bytesPerComponent = frame.shape
        bytesPerLine = bytesPerComponent * width
        res = resize(frame, (480,270))
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        # 变换彩色空间顺序
        cvtColor(res, COLOR_BGR2RGB, res)
        # 转为QImage对象
        self.image_realtime = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # 显示图片
        self.label_realtime.setPixmap(QPixmap.fromImage(self.image_realtime))
        self.label_realtime.resize(self.image_realtime.size())

    #判断信息
    def judgement(self):
        fin_flag=0
        if not (self.bg1_flag or self.bg2_flag or self.bg3_flag or self.bg4_flag):
            putText(self.ROI, 'None of them', (50, 100), FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            return 0

        if self.bg1_flag:
            temp=np.sum((self.samp_hist-self.bg1_hist)**2)
            self.bg1_dis=np.sqrt(temp)
            print self.bg1_dis
            if self.bg1_dis <= self.threshold_temp:
                if fin_flag == 0:
                    fin_flag = 1
                    putText(self.ROI, '1', (50, 100), FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

        if self.bg2_flag:
            temp=np.sum((self.samp_hist-self.bg2_hist)**2)
            self.bg2_dis=np.sqrt(temp)
            print self.bg2_dis
            if self.bg2_dis <= self.threshold_temp:
                if fin_flag == 0:
                    fin_flag = 1
                    putText(self.ROI, '2', (50, 100), FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                else:
                    putText(self.ROI, 'error', (50, 100), FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

        if self.bg3_flag:
            temp=np.sum((self.samp_hist-self.bg3_hist)**2)
            self.bg3_dis=np.sqrt(temp)
            print self.bg3_dis
            if self.bg3_dis <= self.threshold_temp:
                if fin_flag == 0:
                    fin_flag = 1
                    putText(self.ROI, '3', (50, 100), FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                else:
                    putText(self.ROI, 'error', (50, 100), FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

        if self.bg4_flag:
            temp=np.sum((self.samp_hist-self.bg4_hist)**2)
            self.bg4_dis=np.sqrt(temp)
            print self.bg4_dis
            if self.bg4_dis <= self.threshold_temp:
                if fin_flag == 0:
                    fin_flag = 1
                    putText(self.ROI, '4', (50, 100), FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                else:
                    putText(self.ROI, 'error', (50, 100), FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

        if fin_flag == 0:
            putText(self.ROI, 'None of them', (50, 100), FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
    # 获取图像,完成图像匹配并显示并显示
    def clicked_GET(self):
        out = blur(self.ROI, (2, 2))
        out = cvtColor(out, COLOR_RGB2GRAY)
        print 'test'
        self.samp_hist=calcHist([out],[0],None,[246],[0,246])
        self.judgement()
        #采样图显示
        height, width = self.temp_image.shape[:2]
        res = resize(self.temp_image, (480,270))
        # 变换彩色空间顺序
        cvtColor(res, COLOR_BGR2RGB, res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_Sampling = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_Sampling.setPixmap(QPixmap.fromImage(self.image_Sampling))
        self.label_Sampling.resize(self.image_Sampling.size())

        #结果图显示
        res = resize(self.ROI, (270, 270))
        # 变换彩色空间顺序
        cvtColor(res, COLOR_BGR2RGB, res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_result = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_result.setPixmap(QPixmap.fromImage(self.image_result))
        self.label_result.resize(self.image_result.size())

    #清空背景
    def CLEAR_BG(self):
        #背景图相关清空状态
        self.bg1_flag = 0
        self.bg2_flag = 0
        self.bg3_flag = 0
        self.bg4_flag = 0
        #黑色图显示
        height, width, bytesPerComponent = self.black.shape
        bytesPerLine = bytesPerComponent * width
        self.image_BackGround = QImage(self.black.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_BackGround.setPixmap(QPixmap.fromImage(self.image_BackGround))
        self.label_BackGround.resize(self.image_BackGround.size())

    #获取ROI
    def GET_ROI(self):
        self.ROI = self.temp_image[self.ROI_y:self.ROI_y + self.ROI_h, self.ROI_x:self.ROI_x + self.ROI_w].copy()

    #获取背景
    def GET_BG1(self):
        self.bg1_flag = 1
        out = blur(self.ROI, (2, 2))
        self.bg1 = cvtColor(out, COLOR_RGB2GRAY)
        self.bg1_hist=calcHist([self.bg1],[0],None,[246],[0,246])
        w,h=self.bg1.shape
        M = getRotationMatrix2D((w, h), 90,1)
        self.bg1_90 =warpAffine(self.bg1, M, (w, h))
        self.bg1_90_hist = calcHist([self.bg1_90], [0], None, [246], [0, 246])
        M = getRotationMatrix2D((w, h), 180,1)
        self.bg1_180 = warpAffine(self.bg1, M, (w, h))
        self.bg1_180_hist = calcHist([self.bg1_180], [0], None, [246], [0, 246])
        M = getRotationMatrix2D((w, h), 270,1)
        self.bg1_270 = warpAffine(self.bg1, M, (w, h))
        self.bg1_270_hist = calcHist([self.bg1_270], [0], None, [246], [0, 246])
        #背景图显示
        height, width = self.ROI.shape[:2]
        res = resize(self.ROI, (135, 135))
        # 变换彩色空间顺序
        cvtColor(res ,COLOR_BGR2RGB,res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_BackGround1 = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_BackGround1.setPixmap(QPixmap.fromImage(self.image_BackGround1))
        self.label_BackGround1.resize(self.image_BackGround1.size())

    def GET_BG2(self):
        self.bg2_flag = 1
        out = blur(self.ROI, (2, 2))
        self.bg2 = cvtColor(out, COLOR_RGB2GRAY)
        self.bg2_hist=calcHist([self.bg2],[0],None,[246],[0,246])
        w,h=self.bg2.shape
        M = getRotationMatrix2D((w, h), 90,1)
        self.bg2_90 =warpAffine(self.bg2, M, (w, h))
        self.bg2_90_hist = calcHist([self.bg2_90], [0], None, [246], [0, 246])
        M = getRotationMatrix2D((w, h), 180,1)
        self.bg2_180 = warpAffine(self.bg2, M, (w, h))
        self.bg2_180_hist = calcHist([self.bg2_180], [0], None, [246], [0, 246])
        M = getRotationMatrix2D((w, h), 270,1)
        self.bg2_270 = warpAffine(self.bg2, M, (w, h))
        self.bg2_270_hist = calcHist([self.bg2_270], [0], None, [246], [0, 246])
        #背景图显示
        height, width = self.ROI.shape[:2]
        res = resize(self.ROI, (135, 135))
        # 变换彩色空间顺序
        cvtColor(res ,COLOR_BGR2RGB,res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_BackGround2 = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_BackGround2.setPixmap(QPixmap.fromImage(self.image_BackGround2))
        self.label_BackGround2.resize(self.image_BackGround2.size())

    def GET_BG3(self):
        self.bg3_flag = 1
        out = blur(self.ROI, (2, 2))
        self.bg3 = cvtColor(out, COLOR_RGB2GRAY)
        self.bg3_hist=calcHist([self.bg3],[0],None,[246],[0,246])
        w,h=self.bg3.shape
        M = getRotationMatrix2D((w, h), 90,1)
        self.bg3_90 =warpAffine(self.bg3, M, (w, h))
        self.bg3_90_hist = calcHist([self.bg3_90], [0], None, [246], [0, 246])
        M = getRotationMatrix2D((w, h), 180,1)
        self.bg3_180 = warpAffine(self.bg3, M, (w, h))
        self.bg3_180_hist = calcHist([self.bg3_180], [0], None, [246], [0, 246])
        M = getRotationMatrix2D((w, h), 270,1)
        self.bg3_270 = warpAffine(self.bg3, M, (w, h))
        self.bg3_270_hist = calcHist([self.bg3_270], [0], None, [246], [0, 246])
        #背景图显示
        height, width = self.ROI.shape[:2]
        res = resize(self.ROI, (135, 135))
        # 变换彩色空间顺序
        cvtColor(res ,COLOR_BGR2RGB,res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_BackGround3 = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_BackGround3.setPixmap(QPixmap.fromImage(self.image_BackGround3))
        self.label_BackGround3.resize(self.image_BackGround3.size())

    def GET_BG4(self):
        self.bg4_flag = 1
        out = blur(self.ROI, (2, 2))
        self.bg4 = cvtColor(out, COLOR_RGB2GRAY)
        self.bg4_hist=calcHist([self.bg4],[0],None,[246],[0,246])
        w,h=self.bg4.shape
        M = getRotationMatrix2D((w, h), 90,1)
        self.bg4_90 =warpAffine(self.bg4, M, (w, h))
        self.bg4_90_hist = calcHist([self.bg4_90], [0], None, [246], [0, 246])
        M = getRotationMatrix2D((w, h), 180,1)
        self.bg4_180 = warpAffine(self.bg4, M, (w, h))
        self.bg4_180_hist = calcHist([self.bg4_180], [0], None, [246], [0, 246])
        M = getRotationMatrix2D((w, h), 270,1)
        self.bg4_270 = warpAffine(self.bg4, M, (w, h))
        self.bg4_270_hist = calcHist([self.bg4_270], [0], None, [246], [0, 246])
        #背景图显示
        height, width = self.ROI.shape[:2]
        res = resize(self.ROI, (135, 135))
        # 变换彩色空间顺序
        cvtColor(res ,COLOR_BGR2RGB,res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_BackGround4 = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_BackGround4.setPixmap(QPixmap.fromImage(self.image_BackGround4))
        self.label_BackGround4.resize(self.image_BackGround4.size())
    #读取输入参数
    def slot_ROI_x(self):
        age, ok = QInputDialog.getInteger(self, self.tr("ROI_x"),
                                          self.tr("请输入数值:"),
                                          int(self.Label_ROI_x.text()), 0, 1920)
        if ok:
            self.Label_ROI_x.setText(str(age))
            self.ROI_x = age
            print self.ROI_x

    def slot_ROI_y(self):
        age, ok = QInputDialog.getInteger(self, self.tr("ROI_y"),
                                          self.tr("请输入数值:"),
                                          int(self.Label_ROI_y.text()), 0, 1080)
        if ok:
            self.Label_ROI_y.setText(str(age))
            self.ROI_y = age
            print self.ROI_y

    def slot_ROI_w(self):
        age, ok = QInputDialog.getInteger(self, self.tr("ROI_w"),
                                          self.tr("请输入数值:"),
                                          int(self.Label_ROI_w.text()), 0, 1920)
        if ok:
            self.Label_ROI_w.setText(str(age))
            self.ROI_w = age
            print self.ROI_w

    def slot_ROI_h(self):
        age, ok = QInputDialog.getInteger(self, self.tr("ROI_h"),
                                          self.tr("请输入数值:"),
                                          int(self.Label_ROI_h.text()), 0, 1080)
        if ok:
            self.Label_ROI_h.setText(str(age))
            self.ROI_h = age
            print self.ROI_h

    def get_threshold_temp(self,num):
        self.threshold_temp=num

#在这个任务里不好用
def eye(img, R, r, fac_R, fac_r):
    x, y = np.meshgrid(np.linspace(1, R * 2 + 1, R * 2 + 1), np.linspace(1, R * 2 + 1, R * 2 + 1))
    dis = np.sqrt(np.multiply((x - (R + 1)), (x - (R + 1))) + np.multiply((y - (R + 1)), (y - (R + 1))))
    flag1 = (dis <= r)
    flag2 = (np.logical_and(dis > r, dis <= R))
    kernal = flag1 * fac_r + flag2 * fac_R
    kernal = kernal / float(kernal.sum())

    out = filter2D(img, -1, kernal)
    return out





if __name__ == "__main__":
    app = QApplication(sys.argv)
    myshow = Ui_Task2()
    myshow.playTimer.start()
    myshow.show()
    sys.exit(app.exec_())
