# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from cv2 import *
import time
from math import *
import numpy as np

#打印信息在文本框使用
class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

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

class Ui_Task2(QWidget):
    def __init__(self):
        super(Ui_Task2, self).__init__()
        self.setupUi1()
        self.setupUi2()
        self.setupUi3()

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
        self.canny_thrs1_horizontalSlider = QSlider(self)
        self.canny_thrs1_horizontalSlider.setGeometry(QRect(780, 20, 221, 29))
        self.canny_thrs1_horizontalSlider.setMaximum(5000)
        self.canny_thrs1_horizontalSlider.setSingleStep(1)
        self.canny_thrs1_horizontalSlider.setProperty("value", 3500)
        self.canny_thrs1_horizontalSlider.setOrientation(Qt.Horizontal)
        self.canny_thrs2_horizontalSlider = QSlider(self)
        self.canny_thrs2_horizontalSlider.setGeometry(QRect(780, 140, 221, 29))
        self.canny_thrs2_horizontalSlider.setMinimum(0)
        self.canny_thrs2_horizontalSlider.setMaximum(5000)
        self.canny_thrs2_horizontalSlider.setProperty("value", 3200)
        self.canny_thrs2_horizontalSlider.setOrientation(Qt.Horizontal)
        self.a_horizontalSlider = QSlider(self)
        self.a_horizontalSlider.setGeometry(QRect(780, 260, 221, 29))
        self.a_horizontalSlider.setMaximum(110000)
        self.a_horizontalSlider.setMinimum(80000)
        self.a_horizontalSlider.setProperty("value", 95800)
        self.a_horizontalSlider.setOrientation(Qt.Horizontal)
        #LCD显示配置
        self.lcdNumber = QLCDNumber(self)
        self.lcdNumber.setGeometry(QRect(920, 60, 81, 31))
        self.lcdNumber_2 = QLCDNumber(self)
        self.lcdNumber_2.setGeometry(QRect(920, 180, 81, 31))
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
        self.label_5 = QLabel(self)
        self.label_5.setGeometry(QRect(790, 60, 101, 31))
        self.label_6 = QLabel(self)
        self.label_6.setGeometry(QRect(790, 180, 101, 31))
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
        self.label_5.setText("canny_thrs1")
        self.label_6.setText("canny_thrs2")
        self.label_8.setText("a")
        self.label.setText("Realtime")
        self.label_2.setText("BackGround")
        self.label_3.setText("Sampling")
        self.label_4.setText("Result")

        #自定义参量
        self.a=0.9580
        self.canny_thrs1=1000
        self.canny_thrs2 = 2000
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

        QObject.connect(self.canny_thrs1_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber.display)
        self.lcdNumber.display(self.canny_thrs1)
        QObject.connect(self.canny_thrs2_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber_2.display)
        self.lcdNumber_2.display(self.canny_thrs2)
        QObject.connect(self.a_horizontalSlider, SIGNAL("valueChanged(int)"), self.lcdNumber_3.display)
        self.lcdNumber_3.display(95800)
        QMetaObject.connectSlotsByName(self)

        #自定义连接
        #将滑动条参数回传到系统里
        self.canny_thrs1_horizontalSlider.valueChanged.connect(self.get_canny_thrs1)
        self.canny_thrs2_horizontalSlider.valueChanged.connect(self.get_canny_thrs2)
        self.a_horizontalSlider.valueChanged.connect(self.get_a)
        #实时显示摄像头画面
        self.connect(self.playTimer, SIGNAL("updatePlay()"), self.show_Realtime)
        #按下按键时
        self.samButton.clicked.connect(self.clicked_GET)
        self.getbgButton.clicked.connect(self.BG_GET)
        self.exitButton.clicked.connect(QCoreApplication.instance().quit)

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

    # 设置文本输出窗口
    def setupUi3(self):
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stder = EmittingStream(textWritten=self.normalOutputWritten)

        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(QRect(790, 440, 210, 100))

    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
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

    # 获取图像并显示
    def clicked_GET(self):
        out = cvtColor(self.ROI, COLOR_RGB2GRAY)
        out = eye(out, 4, 1, -1, 10)
        _, out = apply_canny(out, self.ROI)
        out, draw = apply_contours(out, self.ROI, self.bg)

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
        height, width = self.temp_image.shape[:2]
        res = resize(out, (270, 270))
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
        self.bg = getbg(self.ROI)
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

    def get_canny_thrs1(self,num):
        self.canny_thrs1=num

    def get_canny_thrs2(self,num):
        self.canny_thrs2=num

    def get_a(self,num):
        self.a=float(num/100000)
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
    edge = Canny(gray, myshow.canny_thrs1, myshow.canny_thrs2, apertureSize=5)
    vis = img.copy()
    vis = np.uint8(vis / 2.)
    vis[edge != 0] = (0, 255, 0)
    return (vis, edge)


def apply_contours(gray, img, bg):
    space = img.shape[0] * img.shape[1]
    _, Contours, _ = findContours(gray, RETR_TREE, CHAIN_APPROX_NONE)
    drawing = np.ones(img.shape) * 255
    imgdark = np.uint8(img / 2.).copy()
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
            if (M["m00"] > 30 and M["m00"] < 2000 and (bg is None or isbg(dis(bg, feature)))):
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
    if np.max(s) > myshow.a:
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
