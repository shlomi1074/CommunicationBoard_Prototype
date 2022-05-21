import os

from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel

import Controllers.CategoryController
from CustomWidgets.AddRecordGridLabel import AddRecordGridLabel
from Database.DBQueries import *


class AddCategoryController(QMainWindow):
    def __init__(self, profile_name, parent):
        super().__init__()
        # LOAD UI FILE
        self.ui = uic.loadUi(r".\UI\AddCategoryScreen.ui", self)
        self.setFixedSize(900, 765)
        self.profile_name = profile_name
        self.AddCategoryButton.clicked.connect(self.add_category_to_db)
        self.parentScreen = parent
        self.ErrorMsgLabel.setVisible(False)
        self.row = 1
        self.col = 1
        self.icons_dir = r"E:\python\BoardCommunication\Resources\Icons"

        self.layout = QtWidgets.QHBoxLayout(self)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setGeometry(40, 280, 820, 380)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)
        self.load_grid()

    def add_category_to_db(self):
        if self.CategoryName.text() is '' or self.CategoryName.text() is None or self.selectedIcon.text() is '':
            return
        if self.CategoryName.text() is '' or self.CategoryName.text() is None or self.selectedIcon.text() is '':
            return

        categories = get_user_categories(self.profile_name)
        for category in categories:
            if category[1] == self.CategoryName.text():
                self.ErrorMsgLabel.setVisible(True)
                self.ErrorMsgLabel.setText(f"כבר קיימת קטגוריה בשם {self.CategoryName.text()}. אנא נסה שם אחר")
                return

        res = add_category(self.profile_name, self.CategoryName.text(),
                           os.path.join(self.icons_dir, self.selectedIcon.text()))
        if res:
            print("added")
            self.parentScreen.close()
            main = Controllers.CategoryController.CategoryController(self.profile_name)
            main.show()
            self.close()
        else:
            self.ErrorMsgLabel.setVisible(True)
            self.ErrorMsgLabel.setText("הייתה בעיה בהוספת הקטגוריה. אנא נסו שוב")

    def load_grid(self):
        for filename in os.listdir(self.icons_dir):
            f = os.path.join(self.icons_dir, filename)
            # checking if it is a file
            if os.path.isfile(f):
                self.add_grid_item(filename, f)

    def add_grid_item(self, label, image):
        if self.col >= 8:
            self.col = 1
            self.row += 1
        try:
            # vl = QVBoxLayout()
            ll = AddRecordGridLabel(label, image, self)
            ll.setFixedHeight(100)
            ll.setFixedWidth(100)
            ll.setScaledContents(True)
            ll.setAlignment(QtCore.Qt.AlignCenter)
            self.gridLayout.addWidget(ll, self.row, self.col, 1, 1)
            self.col += 1
        except Exception as e:
            print(e)







