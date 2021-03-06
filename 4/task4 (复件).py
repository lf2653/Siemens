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
            time.sleep(0.2)

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
        self.label_Sampling = QLabel(self)
        self.label_Sampling.setGeometry(QRect(10, 300, 66, 17))
        self.label_result = QLabel(self)
        self.label_result.setGeometry(QRect(500, 300, 66, 17))
        #滑动块参数配置
        self.threshold_horizontalSlider = QSlider(self)
        self.threshold_horizontalSlider.setGeometry(QRect(780, 260, 221, 29))
        self.threshold_horizontalSlider.setMaximum(100000)
        self.threshold_horizontalSlider.setMinimum(50000)
        self.threshold_horizontalSlider.setProperty("value", 80000)
        self.threshold_horizontalSlider.setOrientation(Qt.Horizontal)
        #LCD显示配置
        self.lcdNumber_3 = QLCDNumber(self)
        self.lcdNumber_3.setGeometry(QRect(920, 300, 81, 31))
        #按键配置
        self.getbgButton = QPushButton(self)
        self.getbgButton.setGeometry(QRect(790, 550, 98, 27))
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
        self.setWindowTitle("Task2")
        self.getbgButton.setText("Get BG")
        self.samButton.setText("Sampling")
        self.exitButton.setText("Exit")
        self.label_8.setText("threshold")
        self.label.setText("Realtime")
        self.label_2.setText("BackGround")
        self.label_3.setText("Sampling")
        self.label_4.setText("Result")

        #自定义参量
        self.threshold_temp=0.80
        self.canny_thrs1=3500
        self.canny_thrs2 = 3200
        self.image_realtime = QImage()
        self.image_BackGround = QImage()
        self.image_Sampling = QImage()
        self.image_result= QImage()
        self.temp_image = None  # 用于存取摄像头图像
        self.ROI = None  # 用于存取ROI
        self.bg=None
        self.device = VideoCapture(1)
        self.device.set(3,1920)
        self.device.set(4,1080)
        self.playTimer = Timer("updatePlay()")

        QObject.connect(self.threshold_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber_3.display)
        self.lcdNumber_3.display(80000)
        QMetaObject.connectSlotsByName(self)

        #自定义连接
        #将滑动条参数回传到系统里
        self.threshold_horizontalSlider.valueChanged.connect(self.get_threshold_temp)
        #实时显示摄像头画面
        self.connect(self.playTimer, SIGNAL("updatePlay()"), self.show_Realtime)
        #按下按键时
        self.samButton.clicked.connect(self.clicked_GET)
        self.getbgButton.clicked.connect(self.BG_GET)
        self.exitButton.clicked.connect(QCoreApplication.instance().quit)
    # 设置ROI选择框
    def setupUi2(self):
        self.ROI_x = 900
        self.ROI_y = 100
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

    # 获取图像,完成图像匹配并显示并显示
    def clicked_GET(self):
        out = cvtColor(self.ROI, COLOR_RGB2GRAY)
        #out = eye(out, 4, 1, -1, 10)
        w,h=self.bg.shape
        h_4=int(h/4)
        w_4=int(w/4)
        template = out[h_4:h_4 * 3, w_4:w_4 * 3].copy()
        w, h = template.shape[::-1]
        res = matchTemplate(self.bg, template, TM_CCOEFF_NORMED)
        min_val,max_val,min_loc,max_loc=minMaxLoc(res)
        print max_val
        print self.threshold_temp
        if max_val>=self.threshold_temp:
            top_left=max_loc
            bottom_right=(top_left[0]+w,top_left[1]+h)
            rectangle(self.ROI,top_left,bottom_right,(0,0,255),3)
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

    # 获取背景图并显示
    def BG_GET(self):
        #out = cvtColor(self.ROI, COLOR_RGB2GRAY)
        #self.bg = eye(out, 4, 1, -1, 10)
        self.bg = cvtColor(self.ROI, COLOR_RGB2GRAY)
        #背景图显示
        height, width = self.ROI.shape[:2]
        res = resize(self.ROI, (270, 270))
        # 变换彩色空间顺序
        cvtColor(res ,COLOR_BGR2RGB,res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_BackGround = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_BackGround.setPixmap(QPixmap.fromImage(self.image_BackGround))
        self.label_BackGround.resize(self.image_BackGround.size())

    #获取ROI
    def GET_ROI(self):
        self.ROI = self.temp_image[self.ROI_y:self.ROI_y + self.ROI_h, self.ROI_x:self.ROI_x + self.ROI_w].copy()

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
        self.threshold_temp=float(num)/100000

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
