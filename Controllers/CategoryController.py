import os
import shutil
from functools import partial

from PyQt5 import uic, QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

from Controllers.AddCategoryController import AddCategoryController
import Controllers.ProfileScreen
from CustomWidgets.CategoryGridLabel import CategoryGridLabel
from Database.DBQueries import *


class CategoryController(QMainWindow):
    def __init__(self, profile_name):
        super().__init__()
        # LOAD UI FILE
        self.ui = uic.loadUi(r".\UI\CategoryScreen.ui", self)
        self.setFixedSize(1100, 650)
        self.profile_name = profile_name
        self.label.setText(f'לוח התקשורת של {profile_name}')
        self.category_screen = None
        self.this_screen = None
        self.row = 1
        self.col = 1

        self.layout = QtWidgets.QHBoxLayout(self)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setGeometry(35, 110, 1030, 500)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)
        self.load_grid()
        self.AddCategoryButton.clicked.connect(self.open_add_category_screen)
        self.BackButton.clicked.connect(self.back_to_profile_screen)

    def closeEvent(self, event):
        print('close event')
        event.accept()

    def open_add_category_screen(self):
        if self.category_screen is not None:
            self.category_screen.close()
        self.category_screen = AddCategoryController(self.profile_name, self)
        self.category_screen.show()

    def back_to_profile_screen(self):
        profile_screen = Controllers.ProfileScreen.ProfileScreenController()
        profile_screen.show()
        self.close()

    def load_grid(self):
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)

        records = get_user_categories(self.profile_name)

        for record in records:
            self.add_grid_item(record[1], record[2], record[1])

    def add_grid_item(self, label, image, is_deleteable=True):
        if self.col >= 7:
            self.col = 1
            self.row += 1

        try:
            v_widget = QWidget(self)
            v_widget.setFixedWidth(160)
            v_widget.setFixedHeight(200)
            vl = QVBoxLayout(v_widget)
            vl.setSpacing(0)

            ll = CategoryGridLabel(label, image, self)
            ll.setFixedHeight(150)
            ll.setFixedWidth(150)
            ll.setScaledContents(True)
            ll.setAlignment(QtCore.Qt.AlignCenter)
            vl.addWidget(ll)
            ll = QLabel(label, self)
            ll.setAlignment(QtCore.Qt.AlignCenter)
            ll.setFixedWidth(150)
            ll.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))
            vl.addWidget(ll)
            if is_deleteable:
                ll = QLabel("מחק קטגוריה", self)
                ll.setStyleSheet("color: red;")
                ll.mousePressEvent = partial(self.delete_category, label)
                ll.setAlignment(QtCore.Qt.AlignCenter)
                ll.setFixedWidth(150)
                ll.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))
                vl.addWidget(ll)
            self.gridLayout.addWidget(v_widget, self.row, self.col, 1, 1)
            self.gridLayout.setColumnStretch(self.col % 5, 1)
            self.gridLayout.setRowStretch(self.row, 1)

            self.col += 1
        except Exception as e:
            print(e)

    def delete_category(self, category_name, event):
        RES = delete_user_category(self.profile_name, category_name)
        if RES:
            RES = delete_category(self.profile_name, category_name)
        print(RES)
        if RES:
            self.this_screen = CategoryController(self.profile_name)
            self.this_screen.show()
            self.close()

