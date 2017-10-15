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
            # 150毫秒发送一次信号
            time.sleep(0.15)

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stoped = True

    def isStoped(self):
        with QMutexLocker(self.mutex):
            return self.stoped

class Ui_Task3_2(QWidget):
    def __init__(self):
        super(Ui_Task3_2, self).__init__()
        self.setupUi1()
        self.setupUi2()
        self.setupUi3()
        self.setupUi4()

    #大部分按键和图像区域设置
    def setupUi1(self):
        self.resize(880, 400)
        self.label_realtime = QLabel(self)
        self.label_realtime.setGeometry(QRect(0, 0, 66, 17))
        self.label_Standard = QLabel(self)
        self.label_Standard.setGeometry(QRect(330, 0, 66, 17))
        self.Button_1 = QPushButton(self)
        self.Button_1.setGeometry(QRect(520, 10, 81, 41))
        self.Button_2 = QPushButton(self)
        self.Button_2.setGeometry(QRect(610, 10, 81, 41))
        self.Button_3 = QPushButton(self)
        self.Button_3.setGeometry(QRect(700, 10, 81, 41))
        self.Button_4 = QPushButton(self)
        self.Button_4.setGeometry(QRect(790, 10, 81, 41))
        self.Button_5 = QPushButton(self)
        self.Button_5.setGeometry(QRect(520, 160, 81, 41))
        self.Button_6 = QPushButton(self)
        self.Button_6.setGeometry(QRect(610, 160, 81, 41))
        self.Button_7 = QPushButton(self)
        self.Button_7.setGeometry(QRect(700, 160, 81, 41))
        self.Button_8 = QPushButton(self)
        self.Button_8.setGeometry(QRect(790, 160, 81, 41))

        self.loadButton_1 = QPushButton(self)
        self.loadButton_1.setGeometry(QRect(520, 70, 81, 41))
        self.loadButton_2 = QPushButton(self)
        self.loadButton_2.setGeometry(QRect(610, 70, 81, 41))
        self.loadButton_3 = QPushButton(self)
        self.loadButton_3.setGeometry(QRect(700, 70, 81, 41))
        self.loadButton_4 = QPushButton(self)
        self.loadButton_4.setGeometry(QRect(790, 70, 81, 41))
        self.loadButton_5 = QPushButton(self)
        self.loadButton_5.setGeometry(QRect(520, 210, 81, 41))
        self.loadButton_6 = QPushButton(self)
        self.loadButton_6.setGeometry(QRect(610, 210, 81, 41))
        self.loadButton_7 = QPushButton(self)
        self.loadButton_7.setGeometry(QRect(700, 210, 81, 41))
        self.loadButton_8 = QPushButton(self)
        self.loadButton_8.setGeometry(QRect(790, 210, 81, 41))

        self.label_realtime_samp = QLabel(self)
        self.label_realtime_samp.setGeometry(QRect(0, 200, 66, 17))
        self.label_result = QLabel(self)
        self.label_result.setGeometry(QRect(330, 200, 66, 17))

        #命名部分
        self.Button_4.setText("ELMENT4")
        self.Button_2.setText("ELMENT2")
        self.Button_3.setText("ELMENT3")
        self.Button_1.setText("ELMENT1")
        self.Button_5.setText("ELMENT5")
        self.Button_6.setText("ELMENT6")
        self.Button_7.setText("ELMENT7")
        self.Button_8.setText("ELMENT8")

        self.loadButton_4.setText("LOAD")
        self.loadButton_2.setText("LOAD")
        self.loadButton_3.setText("LOAD")
        self.loadButton_1.setText("LOAD")
        self.loadButton_5.setText("LOAD")
        self.loadButton_6.setText("LOAD")
        self.loadButton_7.setText("LOAD")
        self.loadButton_8.setText("LOAD")

        self.label_5 = QLabel(self)
        self.label_5.setGeometry(QRect(0, 180, 71, 17))
        self.label_5.setText("Realtime")

        self.label_6 = QLabel(self)
        self.label_6.setGeometry(QRect(330, 180, 71, 17))
        self.label_6.setText("Standard")

        self.label_7 = QLabel(self)
        self.label_7.setGeometry(QRect(0, 380, 71, 17))
        self.label_7.setText("Samp")

        self.label_8 = QLabel(self)
        self.label_8.setGeometry(QRect(330, 380, 71, 17))
        self.label_8.setText("Result")
    #ROI设置相关
    def setupUi2(self):
        #设置ROI选择框
        self.ROI_x = 30
        self.ROI_y = 30
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

        self.Label_ROI_x.setGeometry(QRect(520, 330, 50, 27))
        self.Label_ROI_y.setGeometry(QRect(520, 360, 50, 27))
        self.Label_ROI_w.setGeometry(QRect(625, 330, 50, 27))
        self.Label_ROI_h.setGeometry(QRect(625, 360, 50, 27))

        self.ROI_x_Button = QPushButton(self)
        self.ROI_y_Button = QPushButton(self)
        self.ROI_w_Button = QPushButton(self)
        self.ROI_h_Button = QPushButton(self)

        self.ROI_x_Button.setText("ROI_x")
        self.ROI_y_Button.setText("ROI_y")
        self.ROI_w_Button.setText("ROI_w")
        self.ROI_h_Button.setText("ROI_h")

        self.ROI_x_Button.setGeometry(QRect(555, 330, 70, 27))
        self.ROI_y_Button.setGeometry(QRect(555, 360, 70, 27))
        self.ROI_w_Button.setGeometry(QRect(660, 330, 70, 27))
        self.ROI_h_Button.setGeometry(QRect(660, 360, 70, 27))

        self.connect(self.ROI_x_Button, SIGNAL("clicked()"), self.slot_ROI_x)
        self.connect(self.ROI_y_Button, SIGNAL("clicked()"), self.slot_ROI_y)
        self.connect(self.ROI_w_Button, SIGNAL("clicked()"), self.slot_ROI_w)
        self.connect(self.ROI_h_Button, SIGNAL("clicked()"), self.slot_ROI_h)
    #自定义变量
    def setupUi3(self):
        #自定义变量
        self.image_realtime = QImage()
        self.image_standard = QImage()
        self.image_sampling = QImage()
        self.image_result= QImage()
        self.temp_image = None  # 用于存取摄像头图像
        self.ROI = None  # 用于存取ROI
        self.standard_image = None  # 用于存放标准图
        self.device = VideoCapture(1)
        self.device.set(3,1920)
        self.device.set(4,1080)
        self.playTimer = Timer("updatePlay()")

        self.elemnt1_flag = 0
        self.elemnt2_flag = 0
        self.elemnt3_flag = 0
        self.elemnt4_flag = 0
        self.elemnt5_flag = 0
        self.elemnt6_flag = 0
        self.elemnt7_flag = 0
        self.elemnt8_flag = 0

        self.standard1 = []
        self.standard2 = []
        self.standard3 = []
        self.standard4 = []
        self.standard5 = []
        self.standard6 = []
        self.standard7 = []
        self.standard8 = []
        self.test = []
        #功能按键
        self.pushButton_Standard = QPushButton(self)
        self.pushButton_Standard.setGeometry(QRect(760, 330, 111, 27))
        self.pushButton_EXIT = QPushButton(self)
        self.pushButton_EXIT.setGeometry(QRect(820, 360, 51, 27))
        self.pushButton_Samp = QPushButton(self)
        self.pushButton_Samp.setGeometry(QRect(760, 360, 51, 27))
        self.pushButton_Standard.setText("Standard")
        self.pushButton_EXIT.setText("EXIT")
        self.pushButton_Samp.setText("Samp")

        #按下按键时
        self.pushButton_Samp.clicked.connect(self.clicked_GET)
        self.pushButton_Standard.clicked.connect(self.Standard_GET)
        self.pushButton_EXIT.clicked.connect(QCoreApplication.instance().quit)

        self.Button_1.clicked.connect(self.elemnt1_USE)
        self.Button_2.clicked.connect(self.elemnt2_USE)
        self.Button_3.clicked.connect(self.elemnt3_USE)
        self.Button_4.clicked.connect(self.elemnt4_USE)
        self.Button_5.clicked.connect(self.elemnt5_USE)
        self.Button_6.clicked.connect(self.elemnt6_USE)
        self.Button_7.clicked.connect(self.elemnt7_USE)
        self.Button_8.clicked.connect(self.elemnt8_USE)

        self.loadButton_1.clicked.connect(self.load_data_1)
        self.loadButton_2.clicked.connect(self.load_data_2)
        self.loadButton_3.clicked.connect(self.load_data_3)
        self.loadButton_4.clicked.connect(self.load_data_4)
        self.loadButton_5.clicked.connect(self.load_data_5)
        self.loadButton_6.clicked.connect(self.load_data_6)
        self.loadButton_7.clicked.connect(self.load_data_7)
        self.loadButton_8.clicked.connect(self.load_data_8)

        self.connect(self.playTimer, SIGNAL("updatePlay()"), self.show_Realtime)
    #输入参数
    def setupUi4(self):
        self.maxarea=[10000,10000,10000,10000,10000,10000,10000,10000]
        self.minarea = [500,500,500,500,500,500,500,500]
        self.max_w_h_ratio=[10,10,10,10,10,10,10,10]
        self.min_w_h_ratio = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
        self.HminVal = [0,0,0,0,0,0,0,0]
        self.HmaxVal = [180, 180, 180, 180,180, 180, 180, 180]
        self.SminVal = [0,0,0,0,0,0,0,0]
        self.SmaxVal = [255, 255, 255, 255,255, 255, 255, 255]
        self.VminVal = [0,0,0,0,0,0,0,0]
        self.VmaxVal = [255, 255, 255, 255,255, 255, 255, 255]
        self.label_test=QLabel(self)
        self.label_test.setText(str(0))
    #用于比较样本情况
    def comparison(self,standard, test):
        draw_circle = []
        problem_flag = 0
        n = len(standard)
        # 用于标记是否标准样本参与过比较
        used_flag = np.zeros(n)
        m = len(test)
        for i in range(0, n):
            for j in range(0, m):
                # 中心点坐标距离
                bia1 = (standard[i][0][0] - test[j][0][0]) * (standard[i][0][0] - test[j][0][0]) \
                       + (standard[i][0][1] - test[j][0][1]) * (standard[i][0][1] - test[j][0][1])
                bia1 = np.sqrt(bia1)
                if bia1 > 100:
                    continue
                # 如坐标中心点接近，则可认为是两幅图中相同位置的目标，才能够进行比较
                used_flag[i] = 1
                # 包围矩形面积
                bia2 = standard[i][1][0] * standard[i][1][1] - test[j][1][0] * test[j][1][1]
                # 包围矩形旋转角度
                bia4 = standard[i][2] - test[j][2]
                if (bia1 > 30 or abs(bia2) > 2800):
                    draw_circle.append(standard[i])
                    problem_flag = 1
        # 如有样本始终未参与过标记，则可认为在待测图中存在器件缺失
        for i in range(0, n):
            if used_flag[i] == 0:
                problem_flag = 1
                draw_circle.append(standard[i])
        # 输出相关信息
        if problem_flag == 0:
            font = FONT_HERSHEY_SIMPLEX
            putText(self.ROI, 'No Problem', (50, 100), font, 2, (255, 0, 0), 4)
        else:
            n = len(draw_circle)
            for i in range(0, n):
                #取最大值
                if draw_circle[i][1][0] > draw_circle[i][1][1]:
                    temp = draw_circle[i][1][0]
                else:
                    temp = draw_circle[i][1][1]
                circle(self.ROI, (int(draw_circle[i][0][0]), int(draw_circle[i][0][1])), int(temp), (255, 0, 0), 3)
    #用于搜索对应目标
    def judgement(self,i,j):
        img_hsv = cvtColor(self.ROI, COLOR_RGB2HSV)
        img_threshold = inRange(img_hsv, (self.HminVal[i], self.SminVal[i], self.VminVal[i]),
                                (self.HmaxVal[i], self.SmaxVal[i], self.VmaxVal[i]))
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
                if (area > self.minarea[i] and area < self.maxarea[i] and
                            w_h_ratio > self.min_w_h_ratio[i] and w_h_ratio < self.min_w_h_ratio[i]):
                    if (j == 0):
                        if (i == 0):
                            self.standard1.append(rect)
                        if (i == 1):
                            self.standard2.append(rect)
                        if (i == 2):
                            self.standard3.append(rect)
                        if (i == 3):
                            self.standard4.append(rect)
                        if (i == 4):
                            self.standard5.append(rect)
                        if (i == 5):
                            self.standard6.append(rect)
                        if (i == 6):
                            self.standard7.append(rect)
                        if (i == 7):
                            self.standard8.append(rect)
                    else:
                        self.test.append(rect)
            else:
                continue
        #测试样本采集完毕，开始比较
        if j==1:
            if (i==0):
                self.comparison(self.standard1,self.test)
            if (i==1):
                self.comparison(self.standard2,self.test)
            if (i==2):
                self.comparison(self.standard3,self.test)
            if (i==3):
                self.comparison(self.standard4,self.test)
            if (i==4):
                self.comparison(self.standard1,self.test)
            if (i==5):
                self.comparison(self.standard2,self.test)
            if (i==6):
                self.comparison(self.standard3,self.test)
            if (i==7):
                self.comparison(self.standard4,self.test)
        #比较完毕，清空测试目标存储区域
        self.test=[]
    #获取ROI
    def GET_ROI(self):
        self.ROI = self.temp_image[self.ROI_y:self.ROI_y + self.ROI_h, self.ROI_x:self.ROI_x + self.ROI_w].copy()
    #读摄像头
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
        res = resize(frame, (320, 180))
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        # 变换彩色空间顺序
        cvtColor(res, COLOR_BGR2RGB, res)
        # 转为QImage对象
        self.image_realtime = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # 显示图片
        self.label_realtime.setPixmap(QPixmap.fromImage(self.image_realtime))
        self.label_realtime.resize(self.image_realtime.size())
    #采样动作
    def clicked_GET(self):
        self.ROI=resize(self.ROI, (900, 900))
        if self.elemnt1_flag==1:
            self.judgement(1-1,1)
        if self.elemnt2_flag==1:
            self.judgement(2-1,1)
        if self.elemnt3_flag==1:
            self.judgement(3-1,1)
        if self.elemnt4_flag==1:
            self.judgement(4-1,1)
        # 采样图显示
        height, width = self.temp_image.shape[:2]
        res = resize(self.temp_image, (320, 180))
        # 变换彩色空间顺序
        cvtColor(res, COLOR_BGR2RGB, res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_Sampling = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_realtime_samp.setPixmap(QPixmap.fromImage(self.image_Sampling))
        self.label_realtime_samp.resize(self.image_Sampling.size())

        #结果图显示
        height, width = self.ROI.shape[:2]
        res = resize(self.ROI, (180, 180))
        # 变换彩色空间顺序
        cvtColor(res, COLOR_BGR2RGB, res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_result = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_result.setPixmap(QPixmap.fromImage(self.image_result))
        self.label_result.resize(self.image_result.size())
    #标准图及标准量采集
    def Standard_GET(self):
        self.standard_image=self.ROI.copy()
        #采样标准图前先清空背景，再采集新样本
        if self.elemnt1_flag==1:
            self.standard1=[]
            self.judgement(1 - 1, 0)
        if self.elemnt2_flag==1:
            self.standard2 = []
            self.judgement(2 - 1, 0)
        if self.elemnt3_flag==1:
            self.standard3 = []
            self.judgement(3 - 1, 0)
        if self.elemnt4_flag==1:
            self.standard4 = []
            self.judgement(4 - 1, 0)
        #标准图显示
        height, width = self.ROI.shape[:2]
        res = resize(self.ROI, (180, 180))
        # 变换彩色空间顺序
        cvtColor(res ,COLOR_BGR2RGB,res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_standard = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_Standard.setPixmap(QPixmap.fromImage(self.image_standard))
        self.label_Standard.resize(self.image_standard.size())
    #选取参与检测的元素
    def elemnt1_USE(self):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to use elemnt1?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
        #测试函数的返回值。如果我们点击了Yes按钮，close这个事件将会被接受(accept)
        if reply == QMessageBox.Yes:
            self.elemnt1_flag=1
        if reply == QMessageBox.No:
            self.elemnt1_flag = 0

    def elemnt2_USE(self):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to use elemnt2?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
        #测试函数的返回值。如果我们点击了Yes按钮，close这个事件将会被接受(accept)
        if reply == QMessageBox.Yes:
            self.elemnt2_flag=1
        if reply == QMessageBox.No:
            self.elemnt2_flag = 0

    def elemnt3_USE(self):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to use elemnt3?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
        #测试函数的返回值。如果我们点击了Yes按钮，close这个事件将会被接受(accept)
        if reply == QMessageBox.Yes:
            self.elemnt3_flag=1
        if reply == QMessageBox.No:
            self.elemnt3_flag = 0

    def elemnt4_USE(self):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to use elemnt4?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
        #测试函数的返回值。如果我们点击了Yes按钮，close这个事件将会被接受(accept)
        if reply == QMessageBox.Yes:
            self.elemnt4_flag=1
        if reply == QMessageBox.No:
            self.elemnt4_flag = 0

    def elemnt5_USE(self):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to use elemnt5?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        # 测试函数的返回值。如果我们点击了Yes按钮，close这个事件将会被接受(accept)
        if reply == QMessageBox.Yes:
            self.elemnt5_flag = 1
        if reply == QMessageBox.No:
            self.elemnt5_flag = 0

    def elemnt6_USE(self):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to use elemnt6?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        # 测试函数的返回值。如果我们点击了Yes按钮，close这个事件将会被接受(accept)
        if reply == QMessageBox.Yes:
            self.elemnt6_flag = 1
        if reply == QMessageBox.No:
            self.elemnt6_flag = 0

    def elemnt7_USE(self):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to use elemnt7?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        # 测试函数的返回值。如果我们点击了Yes按钮，close这个事件将会被接受(accept)
        if reply == QMessageBox.Yes:
            self.elemnt7_flag = 1
        if reply == QMessageBox.No:
            self.elemnt7_flag = 0

    def elemnt8_USE(self):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to use elemnt8?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        # 测试函数的返回值。如果我们点击了Yes按钮，close这个事件将会被接受(accept)
        if reply == QMessageBox.Yes:
            self.elemnt8_flag = 1
        if reply == QMessageBox.No:
            self.elemnt8_flag = 0
    # 从输入框输入参数
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
    #读取参数
    def load_data_1(self):
        config = configparser.ConfigParser()
        text_temp, ok = QInputDialog.getText(self, self.tr("Load"),
                                          self.tr("请输入读取文件名:"))
        if ok:
            print text_temp
            config.read(str(text_temp))
            self.minarea[0] = int(config.get("hyperparms", "minarea"))
            self.maxarea[0] = int(config.get("hyperparms", "maxarea"))
            self.max_w_h_ratio[0] = float(config.get("hyperparms", "max_w_h_ratio"))
            self.min_w_h_ratio[0] = float(config.get("hyperparms", "min_w_h_ratio"))
            self.HminVal[0] = int(config.get("hyperparms", "HminVal"))
            self.SminVal[0] = int(config.get("hyperparms", "SminVal"))
            self.VminVal[0] = int(config.get("hyperparms", "VminVal"))
            self.HmaxVal[0] = int(config.get("hyperparms", "HmaxVal"))
            self.SmaxVal[0] = int(config.get("hyperparms", "SmaxVal"))
            self.VmaxVal[0] = int(config.get("hyperparms", "VmaxVal"))

    def load_data_2(self):
        config = configparser.ConfigParser()
        text_temp, ok = QInputDialog.getText(self, self.tr("Load"),
                                          self.tr("请输入读取文件名:"))
        if ok:
            print text_temp
            config.read(str(text_temp))
            self.minarea[1] = int(config.get("hyperparms", "minarea"))
            self.maxarea[1] = int(config.get("hyperparms", "maxarea"))
            self.max_w_h_ratio[1] = float(config.get("hyperparms", "max_w_h_ratio"))
            self.min_w_h_ratio[1] = float(config.get("hyperparms", "min_w_h_ratio"))
            self.HminVal[1] = int(config.get("hyperparms", "HminVal"))
            self.SminVal[1] = int(config.get("hyperparms", "SminVal"))
            self.VminVal[1] = int(config.get("hyperparms", "VminVal"))
            self.HmaxVal[1] = int(config.get("hyperparms", "HmaxVal"))
            self.SmaxVal[1] = int(config.get("hyperparms", "SmaxVal"))
            self.VmaxVal[1] = int(config.get("hyperparms", "VmaxVal"))

    def load_data_3(self):
        config = configparser.ConfigParser()
        text_temp, ok = QInputDialog.getText(self, self.tr("Load"),
                                          self.tr("请输入读取文件名:"))
        if ok:
            print text_temp
            config.read(str(text_temp))
            self.minarea[2] = int(config.get("hyperparms", "minarea"))
            self.maxarea[2] = int(config.get("hyperparms", "maxarea"))
            self.max_w_h_ratio[2] = float(config.get("hyperparms", "max_w_h_ratio"))
            self.min_w_h_ratio[2] = float(config.get("hyperparms", "min_w_h_ratio"))
            self.HminVal[2] = int(config.get("hyperparms", "HminVal"))
            self.SminVal[2] = int(config.get("hyperparms", "SminVal"))
            self.VminVal[2] = int(config.get("hyperparms", "VminVal"))
            self.HmaxVal[2] = int(config.get("hyperparms", "HmaxVal"))
            self.SmaxVal[2] = int(config.get("hyperparms", "SmaxVal"))
            self.VmaxVal[2] = int(config.get("hyperparms", "VmaxVal"))

    def load_data_4(self):
        config = configparser.ConfigParser()
        text_temp, ok = QInputDialog.getText(self, self.tr("Load"),
                                          self.tr("请输入读取文件名:"))
        if ok:
            print text_temp
            config.read(str(text_temp))
            self.minarea[3] = int(config.get("hyperparms", "minarea"))
            self.maxarea[3] = int(config.get("hyperparms", "maxarea"))
            self.max_w_h_ratio[3] = float(config.get("hyperparms", "max_w_h_ratio"))
            self.min_w_h_ratio[3] = float(config.get("hyperparms", "min_w_h_ratio"))
            self.HminVal[3] = int(config.get("hyperparms", "HminVal"))
            self.SminVal[3] = int(config.get("hyperparms", "SminVal"))
            self.VminVal[3] = int(config.get("hyperparms", "VminVal"))
            self.HmaxVal[3] = int(config.get("hyperparms", "HmaxVal"))
            self.SmaxVal[3] = int(config.get("hyperparms", "SmaxVal"))
            self.VmaxVal[3] = int(config.get("hyperparms", "VmaxVal"))

    def load_data_5(self):
        config = configparser.ConfigParser()
        text_temp, ok = QInputDialog.getText(self, self.tr("Load"),
                                             self.tr("请输入读取文件名:"))
        if ok:
            print text_temp
            config.read(str(text_temp))
            self.minarea[4] = int(config.get("hyperparms", "minarea"))
            self.maxarea[4] = int(config.get("hyperparms", "maxarea"))
            self.max_w_h_ratio[4] = float(config.get("hyperparms", "max_w_h_ratio"))
            self.min_w_h_ratio[4] = float(config.get("hyperparms", "min_w_h_ratio"))
            self.HminVal[4] = int(config.get("hyperparms", "HminVal"))
            self.SminVal[4] = int(config.get("hyperparms", "SminVal"))
            self.VminVal[4] = int(config.get("hyperparms", "VminVal"))
            self.HmaxVal[4] = int(config.get("hyperparms", "HmaxVal"))
            self.SmaxVal[4] = int(config.get("hyperparms", "SmaxVal"))
            self.VmaxVal[4] = int(config.get("hyperparms", "VmaxVal"))

    def load_data_6(self):
        config = configparser.ConfigParser()
        text_temp, ok = QInputDialog.getText(self, self.tr("Load"),
                                             self.tr("请输入读取文件名:"))
        if ok:
            print text_temp
            config.read(str(text_temp))
            self.minarea[5] = int(config.get("hyperparms", "minarea"))
            self.maxarea[5] = int(config.get("hyperparms", "maxarea"))
            self.max_w_h_ratio[5] = float(config.get("hyperparms", "max_w_h_ratio"))
            self.min_w_h_ratio[5] = float(config.get("hyperparms", "min_w_h_ratio"))
            self.HminVal[5] = int(config.get("hyperparms", "HminVal"))
            self.SminVal[5] = int(config.get("hyperparms", "SminVal"))
            self.VminVal[5] = int(config.get("hyperparms", "VminVal"))
            self.HmaxVal[5] = int(config.get("hyperparms", "HmaxVal"))
            self.SmaxVal[5] = int(config.get("hyperparms", "SmaxVal"))
            self.VmaxVal[5] = int(config.get("hyperparms", "VmaxVal"))

    def load_data_7(self):
        config = configparser.ConfigParser()
        text_temp, ok = QInputDialog.getText(self, self.tr("Load"),
                                             self.tr("请输入读取文件名:"))
        if ok:
            print text_temp
            config.read(str(text_temp))
            self.minarea[6] = int(config.get("hyperparms", "minarea"))
            self.maxarea[6] = int(config.get("hyperparms", "maxarea"))
            self.max_w_h_ratio[6] = float(config.get("hyperparms", "max_w_h_ratio"))
            self.min_w_h_ratio[6] = float(config.get("hyperparms", "min_w_h_ratio"))
            self.HminVal[6] = int(config.get("hyperparms", "HminVal"))
            self.SminVal[6] = int(config.get("hyperparms", "SminVal"))
            self.VminVal[6] = int(config.get("hyperparms", "VminVal"))
            self.HmaxVal[6] = int(config.get("hyperparms", "HmaxVal"))
            self.SmaxVal[6] = int(config.get("hyperparms", "SmaxVal"))
            self.VmaxVal[6] = int(config.get("hyperparms", "VmaxVal"))

    def load_data_8(self):
        config = configparser.ConfigParser()
        text_temp, ok = QInputDialog.getText(self, self.tr("Load"),
                                             self.tr("请输入读取文件名:"))
        if ok:
            print text_temp
            config.read(str(text_temp))
            self.minarea[7] = int(config.get("hyperparms", "minarea"))
            self.maxarea[7] = int(config.get("hyperparms", "maxarea"))
            self.max_w_h_ratio[7] = float(config.get("hyperparms", "max_w_h_ratio"))
            self.min_w_h_ratio[7] = float(config.get("hyperparms", "min_w_h_ratio"))
            self.HminVal[7] = int(config.get("hyperparms", "HminVal"))
            self.SminVal[7] = int(config.get("hyperparms", "SminVal"))
            self.VminVal[7] = int(config.get("hyperparms", "VminVal"))
            self.HmaxVal[7] = int(config.get("hyperparms", "HmaxVal"))
            self.SmaxVal[7] = int(config.get("hyperparms", "SmaxVal"))
            self.VmaxVal[7] = int(config.get("hyperparms", "VmaxVal"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myshow = Ui_Task3_2()
    myshow.playTimer.start()
    myshow.show()
    sys.exit(app.exec_())

