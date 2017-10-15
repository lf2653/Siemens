# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from cv2 import *
import time
from math import *
import numpy as np
import configparser

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
            # 100毫秒发送一次信号
            time.sleep(0.1)

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stoped = True

    def isStoped(self):
        with QMutexLocker(self.mutex):
            return self.stoped


class Ui_Task3_1(QWidget):

    def __init__(self):
        super(Ui_Task3_1, self).__init__()
        self.setupUi1()
        self.setupUi2()
        self.setupUi3()
        self.setupUi4()

    #大部分按键和图像区域设置
    def setupUi1(self):
        self.resize(1020, 620)
        self.HminVal_horizontalSlider = QSlider(self)
        self.HminVal_horizontalSlider.setGeometry(QRect(790, 10, 220, 29))
        self.HminVal_horizontalSlider.setMaximum(180)
        self.HminVal_horizontalSlider.setOrientation(Qt.Horizontal)
        self.HmaxVal_horizontalSlider = QSlider(self)
        self.HmaxVal_horizontalSlider.setGeometry(QRect(790, 80, 220, 29))
        self.HmaxVal_horizontalSlider.setMaximum(180)
        self.HmaxVal_horizontalSlider.setOrientation(Qt.Horizontal)
        self.SminVal_horizontalSlider = QSlider(self)
        self.SminVal_horizontalSlider.setGeometry(QRect(790, 150, 220, 29))
        self.SminVal_horizontalSlider.setMaximum(255)
        self.SminVal_horizontalSlider.setOrientation(Qt.Horizontal)
        self.SmaxVal_horizontalSlider = QSlider(self)
        self.SmaxVal_horizontalSlider.setGeometry(QRect(790, 220, 220, 29))
        self.SmaxVal_horizontalSlider.setMaximum(255)
        self.SmaxVal_horizontalSlider.setOrientation(Qt.Horizontal)
        self.VminVal_horizontalSlider = QSlider(self)
        self.VminVal_horizontalSlider.setGeometry(QRect(790, 290, 220, 29))
        self.VminVal_horizontalSlider.setMaximum(255)
        self.VminVal_horizontalSlider.setOrientation(Qt.Horizontal)
        self.VmaxVal_horizontalSlider = QSlider(self)
        self.VmaxVal_horizontalSlider.setGeometry(QRect(790, 360, 220, 29))
        self.VmaxVal_horizontalSlider.setMaximum(255)
        self.VmaxVal_horizontalSlider.setOrientation(Qt.Horizontal)
        self.lcdNumber_HminVal = QLCDNumber(self)
        self.lcdNumber_HminVal.setGeometry(QRect(950, 40, 51, 41))
        self.lcdNumber_HmaxVal = QLCDNumber(self)
        self.lcdNumber_HmaxVal.setGeometry(QRect(950, 110, 51, 41))
        self.lcdNumber_SminVal = QLCDNumber(self)
        self.lcdNumber_SminVal.setGeometry(QRect(950, 180, 51, 41))
        self.lcdNumber_SmaxVal = QLCDNumber(self)
        self.lcdNumber_SmaxVal.setGeometry(QRect(950, 250, 51, 41))
        self.lcdNumber_VminVal = QLCDNumber(self)
        self.lcdNumber_VminVal.setGeometry(QRect(950, 320, 51, 41))
        self.lcdNumber_VmaxVal = QLCDNumber(self)
        self.lcdNumber_VmaxVal.setGeometry(QRect(950, 390, 51, 41))
        self.label_realtime = QLabel(self)
        self.label_realtime.setGeometry(QRect(10, 10, 66, 17))
        self.label_result = QLabel(self)
        self.label_result.setGeometry(QRect(500, 300, 66, 17))
        self.label_sampling = QLabel(self)
        self.label_sampling.setGeometry(QRect(10, 300, 66, 17))
        self.label_threshold = QLabel(self)
        self.label_threshold.setGeometry(QRect(500, 10, 66, 17))

        self.sampButton = QPushButton(self)
        self.sampButton.setGeometry(QRect(860, 580, 60, 27))
        self.exitButton = QPushButton(self)
        self.exitButton.setGeometry(QRect(930, 580, 60, 27))
        self.saveButton = QPushButton(self)
        self.saveButton.setGeometry(QRect(790, 580, 60, 27))

        self.label = QLabel(self)
        self.label.setGeometry(QRect(10, 280, 66, 17))
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(500, 280, 100, 17))
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QRect(10, 570, 80, 17))
        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QRect(500, 570, 66, 17))

        QObject.connect(self.HminVal_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber_HminVal.display)
        QObject.connect(self.HmaxVal_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber_HmaxVal.display)
        QObject.connect(self.SminVal_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber_SminVal.display)
        QObject.connect(self.SmaxVal_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber_SmaxVal.display)
        QObject.connect(self.VminVal_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber_VminVal.display)
        QObject.connect(self.VmaxVal_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber_VmaxVal.display)
        QMetaObject.connectSlotsByName(self)

        self.setWindowTitle("Task3-1")
        self.sampButton.setText("Samp")
        self.exitButton.setText("Exit")
        self.saveButton.setText("Save")

        self.label.setText("Realtime")
        self.label_2.setText("Threshold")
        self.label_3.setText("Sampling")
        self.label_4.setText("Result")
    # 自定义变量
    def setupUi2(self):
        self.HminVal = 24
        self.HmaxVal = 72
        self.SminVal = 12
        self.SmaxVal = 59
        self.VminVal = 149
        self.VmaxVal = 210

        self.HminVal_horizontalSlider.setValue(self.HminVal)
        self.HmaxVal_horizontalSlider.setValue(self.HmaxVal)
        self.SminVal_horizontalSlider.setValue(self.SminVal)
        self.SmaxVal_horizontalSlider.setValue(self.SmaxVal)
        self.VminVal_horizontalSlider.setValue(self.VminVal)
        self.VmaxVal_horizontalSlider.setValue(self.VmaxVal)

        self.lcdNumber_HminVal.display(self.HminVal)
        self.lcdNumber_HmaxVal.display(self.HmaxVal)
        self.lcdNumber_SminVal.display(self.SminVal)
        self.lcdNumber_SmaxVal.display(self.SmaxVal)
        self.lcdNumber_VminVal.display(self.VminVal)
        self.lcdNumber_VmaxVal.display(self.VmaxVal)

        self.image_realtime = QImage()
        self.image_threshold = QImage()
        self.image_sampling = QImage()
        self.image_result = QImage()
        self.temp_image = None  # 用于存取摄像头图像
        self.ROI = None  # 用于存取ROI
        self.device = VideoCapture(1)
        self.device.set(3, 1920)
        self.device.set(4, 1080)
        self.playTimer = Timer("updatePlay()")

        # 自定义连接
        # 将滑动条参数回传到系统里
        self.HminVal_horizontalSlider.valueChanged.connect(self.get_HminVal)
        self.HmaxVal_horizontalSlider.valueChanged.connect(self.get_HmaxVal)
        self.SminVal_horizontalSlider.valueChanged.connect(self.get_SminVal)
        self.SmaxVal_horizontalSlider.valueChanged.connect(self.get_SmaxVal)
        self.VminVal_horizontalSlider.valueChanged.connect(self.get_VminVal)
        self.VmaxVal_horizontalSlider.valueChanged.connect(self.get_VmaxVal)
        # 实时显示摄像头画面
        self.connect(self.playTimer, SIGNAL("updatePlay()"), self.show_Realtime)
        # 按下按键时
        self.sampButton.clicked.connect(self.clicked_GET)
        self.saveButton.clicked.connect(self.clicked_SAVE)
        self.exitButton.clicked.connect(QCoreApplication.instance().quit)
    # 设置ROI选择框
    def setupUi3(self):
        self.ROI_x = 635
        self.ROI_y = 130
        self.ROI_w = 900
        self.ROI_h = 900

        self.Label_ROI_x = QLabel(self)
        self.Label_ROI_y = QLabel(self)
        self.Label_ROI_w = QLabel(self)
        self.Label_ROI_h = QLabel(self)

        self.Label_ROI_x.setText(str(self.ROI_x))
        self.Label_ROI_y.setText(str(self.ROI_y))
        self.Label_ROI_w.setText(str(self.ROI_w))
        self.Label_ROI_h.setText(str(self.ROI_h))

        self.Label_ROI_x.setGeometry(QRect(790, 440, 50, 27))
        self.Label_ROI_y.setGeometry(QRect(790, 480, 50, 27))
        self.Label_ROI_w.setGeometry(QRect(895, 440, 50, 27))
        self.Label_ROI_h.setGeometry(QRect(895, 480, 50, 27))

        self.ROI_x_Button = QPushButton(self)
        self.ROI_y_Button = QPushButton(self)
        self.ROI_w_Button = QPushButton(self)
        self.ROI_h_Button = QPushButton(self)

        self.ROI_x_Button.setText("ROI_x")
        self.ROI_y_Button.setText("ROI_y")
        self.ROI_w_Button.setText("ROI_w")
        self.ROI_h_Button.setText("ROI_h")

        self.ROI_x_Button.setGeometry(QRect(825, 440, 70, 27))
        self.ROI_y_Button.setGeometry(QRect(825, 480, 70, 27))
        self.ROI_w_Button.setGeometry(QRect(930, 440, 70, 27))
        self.ROI_h_Button.setGeometry(QRect(930, 480, 70, 27))

        self.connect(self.ROI_x_Button, SIGNAL("clicked()"), self.slot_ROI_x)
        self.connect(self.ROI_y_Button, SIGNAL("clicked()"), self.slot_ROI_y)
        self.connect(self.ROI_w_Button, SIGNAL("clicked()"), self.slot_ROI_w)
        self.connect(self.ROI_h_Button, SIGNAL("clicked()"), self.slot_ROI_h)
    # 设置面积/长宽比范围输入框
    def setupUi4(self):
        self.maxarea = 10000
        self.minarea = 1500
        self.max_w_h_ratio=6
        self.min_w_h_ratio = 2.5

        self.Label_maxarea = QLabel(self)
        self.Label_minarea = QLabel(self)
        self.Label_max_w_h_ratio = QLabel(self)
        self.Label_min_w_h_ratio = QLabel(self)

        self.Label_maxarea.setText(str(self.maxarea))
        self.Label_minarea.setText(str(self.minarea))
        self.Label_max_w_h_ratio.setText(str(self.max_w_h_ratio))
        self.Label_min_w_h_ratio.setText(str(self.min_w_h_ratio))

        self.Label_maxarea.setGeometry(QRect(780, 510, 50, 27))
        self.Label_minarea.setGeometry(QRect(790, 550, 50, 27))
        self.Label_max_w_h_ratio.setGeometry(QRect(895, 510, 50, 27))
        self.Label_min_w_h_ratio.setGeometry(QRect(895, 550, 50, 27))

        self.maxarea_Button = QPushButton(self)
        self.minarea_Button = QPushButton(self)
        self.max_w_h_ratio_Button = QPushButton(self)
        self.min_w_h_ratio_Button = QPushButton(self)

        self.maxarea_Button.setText("maxarea")
        self.minarea_Button.setText("minarea")
        self.max_w_h_ratio_Button.setText("max_w_h")
        self.min_w_h_ratio_Button.setText("min_w_h")

        self.maxarea_Button.setGeometry(QRect(825, 510, 70, 27))
        self.minarea_Button.setGeometry(QRect(825, 550, 70, 27))
        self.max_w_h_ratio_Button.setGeometry(QRect(930, 510, 70, 27))
        self.min_w_h_ratio_Button.setGeometry(QRect(930, 550, 70, 27))

        self.connect(self.maxarea_Button, SIGNAL("clicked()"), self.slot_maxarea)
        self.connect(self.minarea_Button, SIGNAL("clicked()"), self.slot_minarea)
        self.connect(self.max_w_h_ratio_Button, SIGNAL("clicked()"), self.slot_max_w_h_ratio)
        self.connect(self.min_w_h_ratio_Button, SIGNAL("clicked()"), self.slot_min_w_h_ratio)

    #获取ROI
    def GET_ROI(self):
        self.ROI = self.temp_image[self.ROI_y:self.ROI_y + self.ROI_h, self.ROI_x:self.ROI_x + self.ROI_w].copy()
    # 读摄像头
    def show_Realtime(self):
        if self.device.isOpened():
            ret, frame = self.device.read()
            self.temp_image = frame.copy()
            self.GET_ROI()
        else:
            ret = False
        rectangle(frame, (self.ROI_x, self.ROI_y), (self.ROI_x + self.ROI_w, self.ROI_y + self.ROI_h), (0, 255, 0),3)
        height, width, bytesPerComponent = frame.shape
        bytesPerLine = bytesPerComponent * width
        res = resize(frame, (480, 270))
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        # 变换彩色空间顺序
        cvtColor(res, COLOR_BGR2RGB, res)
        # 转为QImage对象
        self.image_realtime = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # 显示图片
        self.label_realtime.setPixmap(QPixmap.fromImage(self.image_realtime))
        self.label_realtime.resize(self.image_realtime.size())
    # 获取图像并显示
    def clicked_GET(self):
        out=blur(self.ROI,(2,2))
        img_hsv = cvtColor(out, COLOR_RGB2HSV)
        drawing = np.zeros(self.ROI.shape, 'uint8')
        img_threshold = inRange(img_hsv, (self.HminVal, self.SminVal, self.VminVal), (self.HmaxVal, self.SmaxVal, self.VmaxVal))
        kernel = np.ones((3, 3), np.uint8)
        img_threshold = dilate(img_threshold, kernel, iterations=1)
        img_threshold = erode(img_threshold, kernel, iterations=1)
        _, contours, _ = findContours(img_threshold, RETR_TREE, CHAIN_APPROX_NONE)
        for c in contours:
            rect = minAreaRect(c)
            x, y = rect[0]
            w, h = rect[1]
            if (w > 0 and h > 0):
                area = w * h
                w_h_ratio = w / h
                angle = rect[2]
                box = boxPoints(rect)
                box = np.int0(box)
                if (area > self.minarea and area<self.maxarea and w_h_ratio > self.min_w_h_ratio and w_h_ratio < self.max_w_h_ratio ):
                    # print rect
                    drawContours(drawing, [box], 0, (0, 0, 255), 3)
                    drawContours(self.ROI, [box], 0, (0, 0, 255), 3)
            else:
                continue
        # 采样图显示
        res = resize(self.temp_image, (480, 270))
        # 变换彩色空间顺序
        cvtColor(res, COLOR_BGR2RGB, res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_sampling = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_sampling.setPixmap(QPixmap.fromImage(self.image_sampling))
        self.label_sampling.resize(self.image_sampling.size())

        # 结果图显示
        height, width = self.ROI.shape[:2]
        res = resize(self.ROI,(270, 270))
        # 变换彩色空间顺序
        cvtColor(res, COLOR_BGR2RGB, res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_result = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_result.setPixmap(QPixmap.fromImage(self.image_result))
        self.label_result.resize(self.image_result.size())

        #中间图显示
        res = resize(drawing,(270, 270))
        # 变换彩色空间顺序
        cvtColor(res, COLOR_BGR2RGB, res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_threshold = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_threshold.setPixmap(QPixmap.fromImage(self.image_threshold))
        self.label_threshold.resize(self.image_threshold.size())
    #保存当前参数
    def clicked_SAVE(self):
        config = configparser.ConfigParser()
        text_temp, ok = QInputDialog.getText(self, self.tr("Save"),
                                          self.tr("请输入保存文件名:"))
        if ok:
            print text_temp
            config.read(str(text_temp))
            config.add_section("hyperparms")
            config.set("hyperparms","HminVal",str(self.HminVal))
            config.set("hyperparms", "SminVal", str(self.SminVal))
            config.set("hyperparms", "VminVal", str(self.VminVal))
            config.set("hyperparms","HmaxVal",str(self.HmaxVal))
            config.set("hyperparms", "SmaxVal", str(self.SmaxVal))
            config.set("hyperparms", "VmaxVal", str(self.VmaxVal))
            config.set("hyperparms", "HminVal", str(self.HminVal))
            config.set("hyperparms", "maxarea", str(self.maxarea))
            config.set("hyperparms", "minarea", str(self.minarea))
            config.set("hyperparms", "max_w_h_ratio", str(self.max_w_h_ratio))
            config.set("hyperparms", "min_w_h_ratio", str(self.min_w_h_ratio))
            config.write(open(str(text_temp), "w"))
    # 从输入框输入参数
    def slot_maxarea(self):
        age, ok = QInputDialog.getInteger(self, self.tr("ROI_x"),
                                          self.tr("请输入数值:"),
                                          int(self.Label_maxarea.text()), self.minarea, 10000)
        if ok:
            self.Label_maxarea.setText(str(age))
            self.maxarea = age

    def slot_minarea(self):
        age, ok = QInputDialog.getInteger(self, self.tr("ROI_y"),
                                          self.tr("请输入数值:"),
                                          int(self.Label_minarea.text()), 50, self.maxarea)
        if ok:
            self.Label_minarea.setText(str(age))
            self.minarea = age

    def slot_max_w_h_ratio(self):
        age, ok = QInputDialog.getDouble(self, self.tr("ROI_w"),
                                          self.tr("请输入数值:"),
                                          float(self.Label_max_w_h_ratio.text()), self.min_w_h_ratio, 10)
        if ok:
            self.Label_max_w_h_ratio.setText(str(age))
            self.max_w_h_ratio= age
            print self.max_w_h_ratio

    def slot_min_w_h_ratio(self):
        age, ok = QInputDialog.getDouble(self, self.tr("ROI_h"),
                                          self.tr("请输入数值:"),
                                          float(self.Label_min_w_h_ratio.text()), 0, self.max_w_h_ratio)
        if ok:
            self.Label_min_w_h_ratio.setText(str(age))
            self.min_w_h_ratio = age

    def slot_ROI_x(self):
        age, ok = QInputDialog.getInteger(self, self.tr("ROI_x"),
                                          self.tr("请输入数值:"),
                                          int(self.Label_ROI_x.text()), 0, 1920)
        if ok:
            self.Label_ROI_x.setText(str(age))
            self.ROI_x = age

    def slot_ROI_y(self):
        age, ok = QInputDialog.getInteger(self, self.tr("ROI_y"),
                                          self.tr("请输入数值:"),
                                          int(self.Label_ROI_y.text()), 0, 1080)
        if ok:
            self.Label_ROI_y.setText(str(age))
            self.ROI_y = age

    def slot_ROI_w(self):
        age, ok = QInputDialog.getInteger(self, self.tr("ROI_w"),
                                          self.tr("请输入数值:"),
                                          int(self.Label_ROI_w.text()), 0, 1920)
        if ok:
            self.Label_ROI_w.setText(str(age))
            self.ROI_w = age

    def slot_ROI_h(self):
        age, ok = QInputDialog.getInteger(self, self.tr("ROI_h"),
                                          self.tr("请输入数值:"),
                                          int(self.Label_ROI_h.text()), 0, 1080)
        if ok:
            self.Label_ROI_h.setText(str(age))
            self.ROI_h = age

    #从滑动条获取参数
    def get_HminVal(self,num):
        self.HminVal=num

    def get_HmaxVal(self,num):
        self.HmaxVal=num

    def get_SminVal(self,num):
        self.SminVal=num

    def get_SmaxVal(self,num):
        self.SmaxVal=num

    def get_VminVal(self,num):
        self.VminVal=num

    def get_VmaxVal(self,num):
        self.VmaxVal=num

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myshow = Ui_Task3_1()
    myshow.playTimer.start()
    myshow.show()
    sys.exit(app.exec_())
