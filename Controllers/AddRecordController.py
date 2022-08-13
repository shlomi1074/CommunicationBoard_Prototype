import os

from PyQt5 import uic, QtCore, QtWidgets, Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel

import Controllers.CommunicationBoardScreen
from CustomWidgets.AddRecordGridLabel import AddRecordGridLabel
from Database.DBQueries import *

global selected_icon
class AddRecordController(QMainWindow):
    def __init__(self, profile_name, category, parent):
        super().__init__()
        # LOAD UI FILE
        self.ui = uic.loadUi(r".\UI\AddRecordingScreen.ui", self)
        self.setFixedSize(1200, 900)
        self.profile_name = profile_name
        self.AddRecorButton.clicked.connect(self.add_record_to_db)
        self.parentScreen = parent
        self.ErrorMsgLabel.setVisible(False)
        self.row = 1
        self.col = 1
        self.icons_dir = r".\Resources\Icons"
        self.category = category
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setGeometry(40, 250, 1120, 500)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)
        self.load_grid()

    def add_record_to_db(self):
        if self.RecordName.text() is '' or self.RecordName.text() is "" or self.RecordName.text() is None:
            return
        if self.RecordText.text() is '' or self.RecordText.text() is "" or self.RecordText.text() is None:
            return
        records = get_user_records(self.profile_name)
        for record in records:
            if record[2] == self.RecordName.text():
                self.ErrorMsgLabel.setVisible(True)
                self.ErrorMsgLabel.setText(f"כבר קיימת הקלטה בשם {self.RecordName.text()}. אנא נסה שם אחר")
                return

        res = add_record(self.profile_name, self.RecordName.text(), self.RecordText.text(),
                         os.path.join(self.icons_dir, self.selectedIcon.text()), self.category)
        if res:
            print("added")
            self.parentScreen.close()
            main = Controllers.CommunicationBoardScreen.CommunicationBoardController(self.profile_name, self.category)
            main.show()
            self.close()
        else:
            self.ErrorMsgLabel.setVisible(True)
            self.ErrorMsgLabel.setText("הייתה בעיה בהוספת ההקלטה. אנא נסו שוב")

    def load_grid(self):
        for filename in os.listdir(self.icons_dir):
            f = os.path.join(self.icons_dir, filename)
            # checking if it is a file
            if os.path.isfile(f):
                self.add_grid_item(filename, f)

    def add_grid_item(self, label, image):
        if self.col >= 7:
            self.col = 1
            self.row += 1
        try:
            # vl = QVBoxLayout()
            ll = AddRecordGridLabel(label, image, self)
            ll.setFixedHeight(150)
            ll.setFixedWidth(150)
            ll.setScaledContents(True)
            ll.setAlignment(QtCore.Qt.AlignCenter)
            ll.setStyleSheet("border: 2px solid black;")

            # vl.addWidget(ll)
            # ll = QLabel(label, self)
            # ll.setAlignment(QtCore.Qt.AlignCenter)
            # vl.addWidget(ll)
            self.gridLayout.addWidget(ll, self.row, self.col, 1, 1)
            self.col += 1
        except Exception as e:
            print(e)







