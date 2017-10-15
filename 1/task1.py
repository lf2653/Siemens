# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from cv2 import *
import time
from math import *
import numpy as np

#相当于定时器
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

#打印信息在文本框使用
class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

#工作界面类
class Ui_Task1(QWidget):
    def __init__(self):
        super(Ui_Task1, self).__init__()
        self.setupUi1()
        self.setupUi2()
        self.setupUi3()
    #大部分图像和部件设置及自定义变量
    def setupUi1(self):
        self.setObjectName("Task1")
        self.setGeometry(300, 300, 1260, 400)
        self.adaptive_thr_C_lcdNumber = QLCDNumber(self)
        self.adaptive_thr_C_lcdNumber.setGeometry(QRect(10, 330, 91, 41))
        self.adaptive_thr_C_lcdNumber.display(2)
        self.adaptive_thr_C_Slider = QSlider(self)
        self.adaptive_thr_C_Slider.setGeometry(QRect(10, 300, 1245, 29))
        self.adaptive_thr_C_Slider.setMaximum(255)
        self.adaptive_thr_C_Slider.setValue(2)
        self.adaptive_thr_C_Slider.setOrientation(Qt.Horizontal)
        self.label_src = QLabel(self)
        self.label_src.setGeometry(QRect(0, 10, 66, 17))
        self.label_get = QLabel(self)
        self.label_get.setGeometry(QRect(490, 10, 66, 17))
        self.getButton = QPushButton(self)
        self.getButton.setGeometry(QRect(1150, 330, 98, 27))
        self.exitButton = QPushButton(self)
        self.exitButton.setGeometry(QRect(1150, 370, 98, 27))
        self.label = QLabel(self)
        self.label.setGeometry(QRect(10, 380, 191, 17))

        self.setWindowTitle("Task1")
        self.getButton.setText("GET")
        self.exitButton.setText("EXIT")
        self.label.setText("adaptive_thr_C:0~255")
        #自定义参量
        self.adaptive_thr_C=2
        self.image = QImage()
        self.image2 = QImage()
        self.temp_image = None  # 用于存取摄像头图像
        self.ROI = None  # 用于存取ROI
        self.device = VideoCapture(1)
        self.device.set(3,1920)
        self.device.set(4,1080)
        self.playTimer = Timer("updatePlay()")

        QObject.connect(self.adaptive_thr_C_Slider, SIGNAL("valueChanged(int)"), self.adaptive_thr_C_lcdNumber.display)
        QMetaObject.connectSlotsByName(self)
        
        #自定义连接
        #将滑动条参数回传到系统里
        self.adaptive_thr_C_Slider.valueChanged.connect(self.get_adaptive_thr_C)
        #实时显示摄像头画面
        self.connect(self.playTimer, SIGNAL("updatePlay()"), self.show_Realtime)
        #按下按键时
        self.getButton.clicked.connect(self.clicked_GET)
        self.exitButton.clicked.connect(QCoreApplication.instance().quit)
    # 设置ROI选择框
    def setupUi2(self):
        self.ROI_x = 320
        self.ROI_y = 30
        self.ROI_w = 1400
        self.ROI_h = 1000


        self.Label_ROI_x = QLabel(self)
        self.Label_ROI_y = QLabel(self)
        self.Label_ROI_w = QLabel(self)
        self.Label_ROI_h = QLabel(self)

        self.Label_ROI_x.setText(str(self.ROI_x))
        self.Label_ROI_y.setText(str(self.ROI_y))
        self.Label_ROI_w.setText(str(self.ROI_w))
        self.Label_ROI_h.setText(str(self.ROI_h))

        self.Label_ROI_x.setGeometry(QRect(210, 330, 50, 27))
        self.Label_ROI_y.setGeometry(QRect(210, 370, 50, 27))
        self.Label_ROI_w.setGeometry(QRect(380, 330, 50, 27))
        self.Label_ROI_h.setGeometry(QRect(380, 370, 50, 27))

        self.ROI_x_Button = QPushButton(self)
        self.ROI_y_Button = QPushButton(self)
        self.ROI_w_Button = QPushButton(self)
        self.ROI_h_Button = QPushButton(self)

        self.ROI_x_Button.setText("ROI_x")
        self.ROI_y_Button.setText("ROI_y")
        self.ROI_w_Button.setText("ROI_w")
        self.ROI_h_Button.setText("ROI_h")

        self.ROI_x_Button.setGeometry(QRect(260, 330, 98, 27))
        self.ROI_y_Button.setGeometry(QRect(260, 370, 98, 27))
        self.ROI_w_Button.setGeometry(QRect(430, 330, 98, 27))
        self.ROI_h_Button.setGeometry(QRect(430, 370, 98, 27))

        self.connect(self.ROI_x_Button, SIGNAL("clicked()"), self.slot_ROI_x)
        self.connect(self.ROI_y_Button, SIGNAL("clicked()"), self.slot_ROI_y)
        self.connect(self.ROI_w_Button, SIGNAL("clicked()"), self.slot_ROI_w)
        self.connect(self.ROI_h_Button, SIGNAL("clicked()"), self.slot_ROI_h)
    # 设置文本输出窗口
    def setupUi3(self):
        #def normalOutputWritten(self, text)，def __del__(self)也为输出窗口相关
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stder = EmittingStream(textWritten=self.normalOutputWritten)

        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(QRect(980, 10, 270, 270))
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
        rectangle(frame, (self.ROI_x, self.ROI_y), (self.ROI_x + self.ROI_w, self.ROI_y + self.ROI_h), (0, 255, 0),3)
        height, width, bytesPerComponent = frame.shape
        bytesPerLine = bytesPerComponent * width
        res = resize(frame, (480,270))
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        # 变换彩色空间顺序
        cvtColor(res, COLOR_BGR2RGB, res)
        # 转为QImage对象
        self.image = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # 显示图片
        self.label_src.setPixmap(QPixmap.fromImage(self.image))
        self.label_src.resize(self.image.size())

    # 对图像做处理并显示
    def clicked_GET(self):
        n = 0
        np.mean(self.ROI[:, :, 0])
        averagecolor = (
            round(np.mean(self.ROI[:, :, 0])), round(np.mean(self.ROI[:, :, 1])),
            round(np.mean(self.ROI[:, :, 2])))
        print("BGR", averagecolor)
        g_grayImage = cvtColor(self.ROI, COLOR_BGR2GRAY)
        g_grayImage = blur(g_grayImage, (3, 3))
        g_dstImage = adaptiveThreshold(g_grayImage, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY_INV, 11, self.adaptive_thr_C)
        _, g_vContours, g_vHierarchy = findContours(g_dstImage, RETR_EXTERNAL, CHAIN_APPROX_NONE)
        # 如不做特别声明，dtype=float64
        drawing = np.zeros(self.ROI.shape, 'uint8')
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
                if (M["m00"] > 1 and M["m00"] < 10000 and np.max(
                        abs(averagecolor - self.ROI[mc[1], mc[0]])) > 100):
                    n += 1
                    contours_poly = approxPolyDP(c, 3, True)
                    x, y, w, h = boundingRect(contours_poly)
                    rectangle(drawing, (x, y), (x + w, y + h), (0, 255, 0), 1, 8, 0)
                    circle(drawing, (mc[0], mc[1]), 5, (0, 0, 255), -1, 8, 0)
                    rectangle(self.ROI, (x, y), (x + w, y + h), (0, 0, 255), 1, 8, 0)

                    print("坏点位置：({0:>4},{1:>4})".format(mc[0], mc[1]))
                    print(
                        "坏点颜色：R={0:<3} G={1:<3} B={2:<3}".format(self.ROI[mc[1], mc[0], 2],
                                                                 self.ROI[mc[1], mc[0], 1],
                                                                 self.ROI[mc[1], mc[0], 0]))
        '''
        if n == 0:
            print("无坏点！")
        else:
            print("坏点个数：{0}".format(n))
        '''
        # 变换彩色空间顺序
        cvtColor(drawing, COLOR_BGR2RGB, drawing)
        #ROI图小，不必放大
        res=resize(drawing,(480,270))
        height, width, bytesPerComponent = res.shape
        bytesPerLine = bytesPerComponent * width
        # 转为QImage对象
        self.image2 = QImage(res.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # 显示图片
        self.label_get.setPixmap(QPixmap.fromImage(self.image2))
        self.label_get.resize(self.image2.size())
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

    def get_adaptive_thr_C(self,num):
        self.adaptive_thr_C=num
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myshow = Ui_Task1()
    myshow.playTimer.start()
    myshow.show()
    sys.exit(app.exec_())
