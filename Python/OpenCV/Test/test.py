# -*- coding: utf-8 -*-

import sys
import cv2 as cv
from PIL import Image
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.uic import loadUi

class Main(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        loadUi('sample.ui',self)

        self.capture = cv.VideoCapture(0)

        self.image = None
        self.start.clicked.connect(self.start_cam)
        self.is_static = False

        self.setStatic.clicked.connect(self.set_motion_image)
        self.motionFrame = None

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.stop.clicked.connect(self.timer.stop)

    def set_motion_image(self):
        self.is_static = True
        gray = cv.cvtColor(self.image.copy(), cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (21,21), 0)
        self.motionFrame = gray

    def start_cam(self):
        try:
            self.capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
            self.capture.set(cv.CAP_PROP_FRAME_WIDTH, 640)
            self.timer.start(5)
        except Exception as e:print(e)

    def update(self):
        try:
            ret, self.image = self.capture._read()
            detected_image = self.detect_motion(self.image)
            self.displayImage(detected_image)    
        except Exception as e:print(e)

    def detect_motion(self,input_img):
        try:
            if self.is_static:
                gray = cv.cvtColor(input_img, cv.COLOR_BGR2GRAY)
                gray = cv.GaussianBlur(gray, (21,21), 0)

                frameDif = cv.absdiff(self.motionFrame,gray)
                thresh = cv.threshold(frameDif, 40, 255, cv.THRESH_BINARY)[1]
                thresh = cv.dilate(thresh, None, iterations = 5)
                im2, cnts, hierarchy = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, 
                                                        cv.CHAIN_APPROX_SIMPLE)
                try: hierarchy = hierarchy[0]
                except: hierarchy = []

                
                height, width, channels = input_img.shape

                min_x, min_y = width, height
                max_x = max_y = 0
                for contour, heir in zip(cnts, hierarchy):
                    (x, y, w, h) = cv.boundingRect(contour)
                    min_x, max_x = min(x, min_x), max(x+w, max_x)
                    min_y, max_y = min(y, min_y), max(y+h, max_y)

                if max_x - min_x > 80 and max_y - min_y > 80:
                    cv.rectangle(input_img, (min_x, min_y), (max_x, max_y), (0,255,0), 3)
        except Exception as e: 
            self.timer.stop()
            print(e)
        return input_img

    def displayImage(self, img):
        try:            
            qformat = QtGui.QImage.Format_RGB888
            outImage = QtGui.QImage(img,img.shape[1], img.shape[0],
                                    img.strides[0] , qformat)
            outImage = outImage.rgbSwapped()
            self.display.setPixmap(QtGui.QPixmap.fromImage(outImage))
            self.display.setScaledContents(True)
        except Exception as e:print('display',e)

app = QtWidgets.QApplication(sys.argv)   
exe = Main()
exe.show()
sys.exit(app.exec_())