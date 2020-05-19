from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
import cv2 as cv2
import sys

app = QApplication([])
window = QWidget()
horizontalLayout = QHBoxLayout()
mainLayout = QVBoxLayout()
sideBarLayout = QVBoxLayout()

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
label = QLabel()

webcamComboBox = QComboBox()
webcamComboBox.addItem("<WEBCAM 1 REPLACE THIS>")
mainLayout.addWidget(webcamComboBox)
mainLayout.addWidget(label, 10)

sideBarLayout.addWidget(QPushButton('Top'))
sideBarLayout.addWidget(QPushButton('Bottom'))

horizontalLayout.addLayout(mainLayout, 5)
horizontalLayout.addLayout(sideBarLayout, 1)
window.setLayout(horizontalLayout)
window.show()
app.exec_()
