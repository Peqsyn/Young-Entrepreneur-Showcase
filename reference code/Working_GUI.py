# Gomi SHIFT prototype

# Libraries for file access 
import argparse
import io
import os
import time

# Libraries for webcam services
import cv2
import numpy

# Libraries for computer vision
from google.cloud import vision
from google.cloud.vision import types

# Libraries for user interface
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtCore, QtGui

file = "C:\Users\ericl\Documents\Gomi Technologies\oppfest\\vision_detect\\temp\\"

# This class defines all of the user interface functions and opperations
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1028, 844)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1001, 781))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")

        # Create a video stream in the window frame
        self.openVideoFrame()
        
        self.treeView = QtGui.QTreeView(self.horizontalLayoutWidget)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout.addLayout(self.verticalLayout)
        
        # Display the current food item
        self.listView = QtGui.QListWidget(self.horizontalLayoutWidget)
        self.listView.setObjectName("listView")
        
        self.horizontalLayout.addWidget(self.listView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1028, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))

    # grap image from webcam
    def setFrame(self, frame):
        pixmap = QPixmap.fromImage(frame)
        self.video_frame.setPixmap(pixmap)

    # initialize video frame
    def openVideoFrame(self):
        # Create Video Frame
        self.video_frame = QtGui.QLabel(self.horizontalLayoutWidget)
        self.video_frame.setObjectName("video_frame")
        self.verticalLayout.addWidget(self.video_frame)
        # Open up video stream
        self.video = videoThread()
        self.video.start()
        self.video_frame.connect(self.video, SIGNAL('newImage(QImage)'), self.setFrame)

    # returns the current frame for output
    def getCVImage(self):
        return self.video.getCVImage()

    def writeToList(self, data):
        self.listView.addItem(data)
            
 
class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.item_identification = identify_items()

    def keyPressEvent(self, e):

        # If the ENTER key is pressed, output what the item is
        if e.key() == 16777220:
            image_name = "image.jpeg"
            if (os.path.exists(image_name)):
                os.remove(image_name)
            cv2.imwrite(image_name, self.ui.getCVImage())
            self.ui.writeToList(self.item_identification.detect_label(file))
            

# This class creates a thread which streams the video footage
class videoThread(QThread):

    def __init__(self):
        super(videoThread,self).__init__()

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened():
            _,image = self.cap.read()
            # adjust width en height to the preferred values
            frame = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888).rgbSwapped()
            self.emit(SIGNAL('newImage(QImage)'), frame)
        

    def getCVImage(self):
        _,image = self.cap.read()
        return image


class identify_items():
    # This function takes in a path to an image and outputs a string describing that item
    def detect_label(self, path):
        """Detects labels in the file."""
        client = vision.ImageAnnotatorClient()

        # [START migration_label_detection]
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        response = client.label_detection(image=image)
        labels = response.label_annotations

        possible_labels = []
        label_description = []
        # puts the score and descroption of the items into their own list 
        # so that we can do operations
        for i in range(len(labels)):
            possible_labels.append(labels[i].score)
            label_description.append(labels[i].description)

        # finds the item with the highest score and the index in the list
        location = possible_labels.index(max(possible_labels))
        
        # displays result of what item was scanned
        return label_description[location]



def run_webcam():
    
    app = QtGui.QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())
       

if __name__ == '__main__':
	run_webcam()

