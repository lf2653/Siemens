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
            # 40毫秒发送一次信号
            time.sleep(0.05)

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stoped = True

    def isStoped(self):
        with QMutexLocker(self.mutex):
            return self.stoped

class Ui_Task2(QWidget):
    def __init__(self):
        super(Ui_Task2, self).__init__()
        self.setupUi()
        
    def setupUi(self):
        self.resize(900, 540)
        #标定图像左上角位置
        self.label_realtime = QLabel(self)
        self.label_realtime.setGeometry(QRect(10, 10, 66, 17))
        self.label_BackGround = QLabel(self)
        self.label_BackGround.setGeometry(QRect(340, 10, 66, 17))
        self.label_Sampling = QLabel(self)
        self.label_Sampling.setGeometry(QRect(10, 270, 66, 17))
        self.label_result = QLabel(self)
        self.label_result.setGeometry(QRect(340, 270, 66, 17))
        #滑动块参数配置
        self.canny_thrs1_horizontalSlider = QSlider(self)
        self.canny_thrs1_horizontalSlider.setGeometry(QRect(670, 20, 221, 29))
        self.canny_thrs1_horizontalSlider.setMaximum(5000)
        self.canny_thrs1_horizontalSlider.setSingleStep(1)
        self.canny_thrs1_horizontalSlider.setProperty("value", 3500)
        self.canny_thrs1_horizontalSlider.setOrientation(Qt.Horizontal)
        self.gray_minVal_horizontalSlider = QSlider(self)
        self.gray_minVal_horizontalSlider.setGeometry(QRect(670, 250, 221, 29))
        self.gray_minVal_horizontalSlider.setMaximum(254)
        self.gray_minVal_horizontalSlider.setProperty("value", 210)
        self.gray_minVal_horizontalSlider.setOrientation(Qt.Horizontal)
        self.canny_thrs2_horizontalSlider = QSlider(self)
        self.canny_thrs2_horizontalSlider.setGeometry(QRect(670, 140, 221, 29))
        self.canny_thrs2_horizontalSlider.setMinimum(0)
        self.canny_thrs2_horizontalSlider.setMaximum(5000)
        self.canny_thrs2_horizontalSlider.setProperty("value", 3200)
        self.canny_thrs2_horizontalSlider.setOrientation(Qt.Horizontal)
        self.gray_maxVal_horizontalSlider = QSlider(self)
        self.gray_maxVal_horizontalSlider.setGeometry(QRect(670, 360, 221, 29))
        self.gray_maxVal_horizontalSlider.setMaximum(255)
        self.gray_maxVal_horizontalSlider.setProperty("value", 255)
        self.gray_maxVal_horizontalSlider.setOrientation(Qt.Horizontal)
        #LCD显示配置
        self.lcdNumber = QLCDNumber(self)
        self.lcdNumber.setGeometry(QRect(810, 60, 81, 31))
        self.lcdNumber_2 = QLCDNumber(self)
        self.lcdNumber_2.setGeometry(QRect(810, 180, 81, 31))
        self.lcdNumber_4 = QLCDNumber(self)
        self.lcdNumber_4.setGeometry(QRect(810, 290, 81, 31))
        self.lcdNumber_3 = QLCDNumber(self)
        self.lcdNumber_3.setGeometry(QRect(810, 400, 81, 31))
        #按键配置
        self.getbgButton = QPushButton(self)
        self.getbgButton.setGeometry(QRect(680, 460, 98, 27))
        self.samButton = QPushButton(self)
        self.samButton.setGeometry(QRect(790, 460, 98, 27))
        self.exitButton = QPushButton(self)
        self.exitButton.setGeometry(QRect(790, 500, 98, 27))
        #文字显示配置
        self.label_5 = QLabel(self)
        self.label_5.setGeometry(QRect(680, 60, 101, 31))
        self.label_6 = QLabel(self)
        self.label_6.setGeometry(QRect(680, 180, 101, 31))
        self.label_7 = QLabel(self)
        self.label_7.setGeometry(QRect(690, 290, 101, 31))
        self.label_8 = QLabel(self)
        self.label_8.setGeometry(QRect(690, 400, 101, 31))
        self.label = QLabel(self)
        self.label.setGeometry(QRect(10, 250, 66, 17))
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(340, 250, 100, 17))
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QRect(10, 510, 80, 17))
        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QRect(340, 510, 66, 17))

        #程序中出现的字符串
        self.setWindowTitle("Task2")
        self.getbgButton.setText("Get BG")
        self.samButton.setText("Sampling")
        self.exitButton.setText("Exit")
        self.label_5.setText("canny_thrs1")
        self.label_6.setText("canny_thrs2")
        self.label_7.setText("gray_minVal")
        self.label_8.setText("gray_maxVal")
        self.label.setText("Realtime")
        self.label_2.setText("BackGround")
        self.label_3.setText("Sampling")
        self.label_4.setText("Result")

        #自定义参量
        self.canny_thrs1=3500
        self.canny_thrs2 = 3200
        self.gray_minVal=210
        self.gray_maxVal=255
        self.image_realtime = QImage()
        self.image_BackGround = QImage()
        self.image_Sampling = QImage()
        self.image_result= QImage()
        self.temp_image = None  # 用于存取摄像头图像
        self.bg=None
        self.device = VideoCapture(1)
        self.playTimer = Timer("updatePlay()")

        QObject.connect(self.canny_thrs1_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber.display)
        self.lcdNumber.display(self.canny_thrs1)
        QObject.connect(self.canny_thrs2_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber_2.display)
        self.lcdNumber_2.display(self.canny_thrs2)
        QObject.connect(self.gray_minVal_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber_4.display)
        self.lcdNumber_4.display(self.gray_minVal)
        QObject.connect(self.gray_maxVal_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber_3.display)
        self.lcdNumber_3.display(self.gray_maxVal)
        QMetaObject.connectSlotsByName(self)

        #自定义连接
        #将滑动条参数回传到系统里
        self.canny_thrs1_horizontalSlider.valueChanged.connect(self.get_canny_thrs1)
        self.canny_thrs2_horizontalSlider.valueChanged.connect(self.get_canny_thrs2)
        self.gray_minVal_horizontalSlider.valueChanged.connect(self.get_gray_minVal)
        self.gray_maxVal_horizontalSlider.valueChanged.connect(self.get_gray_maxVal)
        #实时显示摄像头画面
        self.connect(self.playTimer, SIGNAL("updatePlay()"), self.show_Realtime)
        #按下按键时
        self.samButton.clicked.connect(self.clicked_GET)
        self.getbgButton.clicked.connect(self.BG_GET)
        self.exitButton.clicked.connect(QCoreApplication.instance().quit)

    def get_canny_thrs1(self,num):
        self.canny_thrs1=num

    def get_canny_thrs2(self,num):
        self.canny_thrs2=num

    def get_gray_minVal(self,num):
        self.gray_minVal=num

    def get_gray_maxVal(self,num):
        self.gray_maxVal=num

    # 读摄像头
    def show_Realtime(self):
        if self.device.isOpened():
            ret, frame = self.device.read()
            self.temp_image = frame
        else:
            ret = False

        height, width, bytesPerComponent = frame.shape
        bytesPerLine = bytesPerComponent * width
        res = resize(frame, (width / 2, height / 2))
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
        img = GET_ROI(self.temp_image)
        out = cvtColor(img, COLOR_RGB2GRAY)
        out = eye(out, 4, 1, -1, 10)
        _, out = apply_canny(out, img)
        out, draw = apply_contours(out, img, self.bg)

        #采样图显示
        height, width = self.temp_image.shape[:2]
        res = resize(self.temp_image, (width / 2, height / 2))
        # 变换彩色空间顺序
        cvtColor(res, COLOR_BGR2RGB, res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_Sampling = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_Sampling.setPixmap(QPixmap.fromImage(self.image_Sampling))
        self.label_Sampling.resize(self.image_Sampling.size())

        #结果图显示
        height, width = self.temp_image.shape[:2]
        res = resize(out, (width / 2, height / 2))
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
        bg_ROI = GET_ROI(self.temp_image)
        self.bg = getbg(bg_ROI)
        #背景图显示
        height, width = self.temp_image.shape[:2]
        res = resize(self.temp_image, (width / 2, height / 2))
        # 变换彩色空间顺序
        cvtColor(res ,COLOR_BGR2RGB,res)
        # 转为QImage对象
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        self.image_BackGround = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_BackGround.setPixmap(QPixmap.fromImage(self.image_BackGround))
        self.label_BackGround.resize(self.image_BackGround.size())


def getbg(img):
    flag = 1
    bg_temp = None
    space = img.shape[0] * img.shape[1]
    gray = cvtColor(img, COLOR_RGB2GRAY)
    img_enhanced = eye(gray, 4, 1, -1, 10)
    _, edge = apply_canny(img_enhanced, img)
    _, Contours, _ = findContours(edge, RETR_TREE, CHAIN_APPROX_NONE)
    count = 0
    n = 0
    for c in Contours:
        count += 1
        M = moments(c)
        if M['m00'] != 0:
            mc = [int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])]
            if (M["m00"] > 30 and M["m00"] < 1000):
                n += 1
                colorR = (img[mc[1], mc[0], 2]) / 255.0
                colorG = (img[mc[1], mc[0], 1]) / 255.0
                colorB = (img[mc[1], mc[0], 0]) / 255.0
                x = mc[1] / img.shape[1]
                y = mc[0] / img.shape[0]
                s = M["m00"] / space
                if flag:
                    bg_temp = np.array([colorR, colorG, colorB, x, y, s])
                    flag = 0
                else:
                    bg_temp = np.row_stack((bg_temp, np.array([colorR, colorG, colorB, x, y, s])))
    return bg_temp


def apply_canny(gray, img):
    thrs1 = 3500
    thrs2 = 3200
    edge = Canny(gray, thrs1, thrs2, apertureSize=5)
    vis = img.copy()
    vis = np.uint8(vis / 2.)
    vis[edge != 0] = (0, 255, 0)
    return (vis, edge)


def apply_contours(gray, img, bg):
    space = img.shape[0] * img.shape[1]
    _, Contours, _ = findContours(gray, RETR_TREE, CHAIN_APPROX_NONE)
    drawing = np.ones(img.shape) * 255
    imgdark = np.uint8(img / 2.)
    count = 0
    n = 0
    totals = 0
    for c in Contours:
        count += 1
        M = moments(c)
        if M['m00'] != 0:
            mc = [int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])]
            colorR = (img[mc[1], mc[0], 2]) / 255
            colorG = (img[mc[1], mc[0], 1]) / 255
            colorB = (img[mc[1], mc[0], 0]) / 255
            x = mc[1] / img.shape[1]
            y = mc[0] / img.shape[0]
            s = M["m00"] / space
            feature = np.array([colorR, colorG, colorB, x, y, s])
            if (M["m00"] > 30 and M["m00"] < 2000 and isbg(dis(bg, feature))):
                n += 1
                drawContours(drawing, c, -1, (0, 0, 0), -1)
                drawContours(imgdark, c, -1, (0, 255, 0))
                totals += s
    if totals < 0.021 / 100:
        print('无裂纹和划痕')
    else:
        print('裂纹和划痕面积：{0:>.1f}，占画面比例：{1:>.6f}%'.format(totals * space, totals * 100))
    return (imgdark, drawing)


def normalizeRows(x):
    if len(x.shape) > 1:
        a = np.sqrt(np.sum(np.multiply(x, x), 1))
        a = np.reshape(a, (x.shape[0], 1))
    else:
        a = np.sqrt(np.sum(np.multiply(x, x)))
    x = x / a
    return x


def dis(a, b):
    anorm = normalizeRows(a)
    bnorm = normalizeRows(b)
    return np.dot(anorm, bnorm.T)


def isbg(s):
    if np.max(s) > 0.9988:
        return False
    else:
        return True


def eye(img, R, r, fac_R, fac_r):
    x, y = np.meshgrid(np.linspace(1, R * 2 + 1, R * 2 + 1), np.linspace(1, R * 2 + 1, R * 2 + 1))
    dis = np.sqrt(np.multiply((x - (R + 1)), (x - (R + 1))) + np.multiply((y - (R + 1)), (y - (R + 1))))
    flag1 = (dis <= r)
    flag2 = (np.logical_and(dis > r, dis <= R))
    kernal = flag1 * fac_r + flag2 * fac_R
    kernal = kernal / float(kernal.sum())

    out = filter2D(img, -1, kernal)
    return out


def GET_ROI(img):
    minVal = 210
    maxVal = 255
    gray = cvtColor(img, COLOR_RGB2GRAY)
    ret, edges = threshold(gray, minVal, maxVal, THRESH_BINARY_INV)
    _, contours, _ = findContours(edges, RETR_TREE, CHAIN_APPROX_NONE)
    count = 0
    n = 0
    maxm00 = 0
    max_cnt = None
    for cnt in contours:
        count += 1
        M = moments(cnt)
        if M['m00'] != 0:
            if (M["m00"] > maxm00):
                n += 1
                maxm00 = M["m00"]
                max_cnt = cnt
    x, y, w, h = boundingRect(max_cnt)
    if w > h:
        h = w
    else:
        w = h
    ROI = img[y:y + h, x:x + w]
    return ROI




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myshow = Ui_Task2()
    myshow.playTimer.start()
    myshow.show()
    sys.exit(app.exec_())
