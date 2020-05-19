import os
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets  # uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget,
                             QLabel, QVBoxLayout)  # +++

from camCapture import MainWindow
from appORB import AppORB

ImageData = AppORB.ImageData
SetImages = AppORB.SetImages

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Card Capture')
    window.show()
    sys.exit(app.exec_())
