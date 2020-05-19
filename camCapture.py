import cv2
from PyQt5 import QtCore, QtGui, QtWidgets

from camCaptureUi import UiForm
from appORB import AppORB
import csv
import time
from ebay import EbaySeller


class MainWindow(QtWidgets.QDialog, UiForm):
    frameTimer = time.time()
    ebay_seller = EbaySeller()

    def __init__(self):
        super().__init__()

        self.setup_ui(self)

        self.control_bt.clicked.connect(self.start_webcam)
        self.scan_bt.clicked.connect(self.scan_card)

        self.add_bt.clicked.connect(self.add_bt_event)
        self.rem_bt.clicked.connect(self.rem_bt_event)
        self.sell_bt.clicked.connect(self.sell_bt_event)

        self.image_label.setScaledContents(True)

        self.cap = None

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(33)  # Approximately 30 frames per second
        self.timer.timeout.connect(self.update_frame)

    @QtCore.pyqtSlot()
    def sell_bt_event(self):
        EbaySeller.get_card_info_and_sell(self.ebay_seller, self.card_list.currentItem().text())

    @QtCore.pyqtSlot()
    def rem_bt_event(self):
        self.card_list.takeItem(self.card_list.currentRow())

        with open('cardList.csv', 'w+', newline='') as csvfile:
            csvfile.truncate()
            cardWriter = csv.writer(csvfile, delimiter=' ', quotechar='|')
            for i in range(self.card_list.count()):
                cardWriter.writerow(self.card_list.item(i).text())

    @QtCore.pyqtSlot()
    def add_bt_event(self):
        with open('cardList.csv', 'a+', newline='') as csvfile:
            card_writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
            card_writer.writerow(self.text_box.text())
        with open('cardList.csv', 'r', newline='') as csvfile:
            card_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            self.card_list.clear()
            for row in card_reader:
                self.card_list.addItem(''.join(row))

    @QtCore.pyqtSlot()
    def scan_card(self):
        if not self.cap is None:
            if not self.cap.isOpened():
                ret, camera_image = self.cap.read()
                AppORB.scan_card(self, camera_image)
        else:
            AppORB.scan_card(self, None)
            # self.msg = QtWidgets.QMessageBox()
            # self.msg.setWindowTitle("Error")
            # self.msg.setText("Card scan failed. Please ensure data set is valid and camera is connected.")
            # self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            # self.msg.exec()
        self.card_list.repaint()

    @QtCore.pyqtSlot()
    def start_webcam(self):

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)  # These parameters are different for each webcam, ymmv
        self.cap.set(4, 720)
        if self.cap.isOpened():
            self.timer.start()
        else:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Could not connect to camera")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.exec()

    @QtCore.pyqtSlot()
    def update_frame(self):
        ret, image = self.cap.read()
        self.display_image(image, True)

    def display_image(self, img, window=True):
        qformat = QtGui.QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QtGui.QImage.Format_RGBA8888
            else:
                qformat = QtGui.QImage.Format_RGB888
        outImage = QtGui.QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        if window:
            self.image_label.setPixmap(QtGui.QPixmap.fromImage(outImage))
