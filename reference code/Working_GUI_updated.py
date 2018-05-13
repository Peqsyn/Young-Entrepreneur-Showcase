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
        self.listview.
        
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

    def closeVideo(self):
        self.video.stop()

    def writeToList(self, data):
        self.listView.addItem(data)
            
# Create an object which defines the main window
class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
        self.current_file = 1

        self.item_identification = identify_items()

        self.image_directory = "C:\Users\Peter\Documents\Work 2018\School 2018\MSE 410\Food Recognition Software\\"

    def keyPressEvent(self, e):

        # If the ENTER key is pressed, output what the item is
        if e.key() == 16777220:
            image_name = "image.jpeg"
            image = self.image_directory + image_name
            if (os.path.exists(image)):
                os.remove(image)
            cv2.imwrite(image, self.ui.getCVImage())

            file_name = ("C:\Users\ericl\Documents\Gomi Technologies\oppfest\\vision_detect\\temp2\\image_%d.jpeg" %(self.current_file))
            self.current_file += 1
            cv2.imwrite(file_name, self.ui.getCVImage())
            self.ui.writeToList(self.item_identification.detect_label(image))

    def closeEvent(self, e):
        self.ui.closeVideo()
        
    def setImageDirectory(self, directory):
        self.image_directory = directory
            

# This class creates a thread which streams the video footage
class videoThread(QThread):

    def __init__(self):
        super(videoThread,self).__init__()

    def run(self):
        self.cap = cv2.VideoCapture(1)
        while self.cap.isOpened():
            _,image = self.cap.read()
            # adjust width en height to the preferred values
            frame = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888).rgbSwapped()
            self.emit(SIGNAL('newImage(QImage)'), frame)
        
    def stop(self):
        self.cap.release()


    def getCVImage(self):
        _,image = self.cap.read()
        return image






class identify_items():
    # This function takes in a path to an image and outputs a string describing that item
    def detect_label(self, path):
        '''"""Detects labels in the file."""
        client = vision.ImageAnnotatorClient()

        # [START migration_label_detection]
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        response = client.web_detection(image=image).web_detection
        labels = response.web_entities

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
        return label_description[location]'''

        # Run 1
        """Detects web annotations given an image."""
        client = vision.ImageAnnotatorClient()

        # [START migration_web_detection]
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        response = client.web_detection(image=image)
        notes = response.web_detection.web_entities

        possible_entity = []
        entity_description = []
        # puts the score and descroption of the items into their own list 
        # so that we can do operations
        for i in range(len(notes)):
            possible_entity.append(notes[i].score)
            entity_description.append(notes[i].description)

        # finds the item with the highest score and the index in the list
        location = possible_entity.index(max(possible_entity))

        # Run 2
        # [START migration_web_detection]
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        response = client.web_detection(image=image)
        notes = response.web_detection.web_entities

        possible_entity = []
        entity_description = []
        # puts the score and descroption of the items into their own list 
        # so that we can do operations
        for i in range(len(notes)):
            possible_entity.append(notes[i].score)
            entity_description.append(notes[i].description)

        # finds the item with the highest score and the index in the list
        compare = possible_entity.index(max(possible_entity))
        count = 0;

        while (location != compare):
            with io.open(path, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

            response = client.web_detection(image=image)
            notes = response.web_detection.web_entities

            possible_labels = []
            label_description = []
            # puts the score and descroption of the items into their own list 
            # so that we can do operations
            for i in range(len(notes)):
                possible_labels.append(notes[i].score)
                label_description.append(notes[i].description)

            # finds the item with the highest score and the index in the list
            if count == 3:
                location = possible_labels.index(max(possible_labels))
                count = 0;
            else:
                compare = possible_labels.index(max(possible_labels))
                count = count + 1
        # displays result of what item was scanned
        return entity_description[compare]


def run_webcam():
    
    app = QtGui.QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.setImageDirectory("C:\Users\ericl\Documents\Gomi Technologies\oppfest\\vision_detect\\temp\\")
    MainWindow.show()
    
    sys.exit(app.exec_())
       

if __name__ == '__main__':
	run_webcam()

