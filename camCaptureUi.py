from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
import csv
from os import path


class UiForm(object):
    def __init__(self):
        self.rem_bt = QPushButton()

    def setup_ui(self, Form):
        Form.setObjectName("Card Capture")
        self.vertical_layout = QtWidgets.QVBoxLayout(Form)
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setObjectName("horizontalLayout")
        self.main_layout = QVBoxLayout()
        self.webcam_combo_box_layout = QHBoxLayout()
        self.side_bar_layout = QVBoxLayout()

        self.webcam_combo_box = QComboBox(Form)
        self.webcam_combo_box.setObjectName("combo_box")
        self.webcam_combo_box.addItem("<WEBCAM 1 REPLACE THIS>")
        self.webcam_combo_box_layout.addWidget(self.webcam_combo_box, 4)

        self.control_bt = QtWidgets.QPushButton(Form)
        self.control_bt.setObjectName("control_bt")
        self.webcam_combo_box_layout.addWidget(self.control_bt)

        self.main_layout.addItem(self.webcam_combo_box_layout)

        ## Sidebar layout
        self.card_list = QListWidget(Form)
        if not path.exists('cardlist.csv'):
            open('cardList.csv', 'w+')
        with open('cardList.csv', newline='') as csvfile:
            card_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in card_reader:
                self.card_list.addItem(''.join(row))

        self.side_bar_layout.addWidget(self.card_list)
        self.text_box = QLineEdit()
        self.text_box.setObjectName("text_box")
        self.side_bar_layout.addWidget(self.text_box)

        self.side_bar_bottom_layout = QHBoxLayout()
        self.add_bt = QPushButton()
        self.add_bt.setObjectName("add_bt")
        self.add_bt.setText("Add")
        self.side_bar_bottom_layout.addWidget(self.add_bt)
        self.rem_bt.setObjectName("rem_bt")
        self.rem_bt.setText("Rem")
        self.side_bar_bottom_layout.addWidget(self.rem_bt)
        self.sell_bt = QPushButton()
        self.sell_bt.setObjectName("sell_bt")
        self.sell_bt.setText("Sell")
        self.side_bar_bottom_layout.addWidget(self.sell_bt)
        self.side_bar_layout.addLayout(self.side_bar_bottom_layout)

        ## Collect everything
        self.image_label = QtWidgets.QLabel(Form)
        self.image_label.setText("Nothing Captured")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setObjectName("image_label")
        self.image_label.setFixedWidth(1280)
        self.image_label.setFixedHeight(720)
        self.main_layout.addWidget(self.image_label)

        self.main_layout_bottom_buttons = QHBoxLayout(Form)
        self.scan_bt = QtWidgets.QPushButton(Form)
        self.scan_bt.setObjectName("scan_bt")
        self.scan_bt.setText("Scan 1")
        self.main_layout_bottom_buttons.addWidget(self.scan_bt)
        self.scan_multiple_bt = QtWidgets.QPushButton(Form)
        self.scan_multiple_bt.setObjectName("scanMultiple_bt")
        self.scan_multiple_bt.setText("Scan Multiple <ROBOT>")
        self.scan_multiple_bt.setEnabled(False)
        self.main_layout_bottom_buttons.addWidget(self.scan_multiple_bt)
        self.autoScan_bt = QtWidgets.QPushButton(Form)
        self.autoScan_bt.setObjectName("autoScan_bt")
        self.autoScan_bt.setText("Autoscan <ROBOT>")
        self.autoScan_bt.setEnabled(False)
        self.main_layout_bottom_buttons.addWidget(self.autoScan_bt)
        self.main_layout.addLayout(self.main_layout_bottom_buttons)

        self.horizontal_layout.addLayout(self.main_layout)
        self.horizontal_layout.addLayout(self.side_bar_layout)
        self.vertical_layout.addLayout(self.horizontal_layout)

        self.retranslate_ui(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslate_ui(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Cam view"))
        self.control_bt.setText(_translate("Form", "Start"))
