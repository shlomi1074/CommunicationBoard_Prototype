import os
import shutil
from functools import partial

from PyQt5 import uic, QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QFileDialog

from Controllers.AddCategoryController import AddCategoryController
import Controllers.ProfileScreen
from CustomWidgets.CategoryGridLabel import CategoryGridLabel
from Database.DBQueries import *


class CategoryController(QMainWindow):
    def __init__(self, profile_name):
        super().__init__()
        # LOAD UI FILE
        self.ui = uic.loadUi(r".\UI\CategoryScreen.ui", self)
        self.setFixedSize(1200, 900)
        self.profile_name = profile_name
        self.label.setText(f'לוח התקשורת של {profile_name}')
        self.category_screen = None
        self.this_screen = None
        self.row = 1
        self.col = 1
        self.profile_picture_bytes = None
        self.load_profile_picture()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setGeometry(35, 200, 1125, 650)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)
        self.load_grid()
        self.AddCategoryButton.clicked.connect(self.open_add_category_screen)
        self.BackButton.clicked.connect(self.back_to_profile_screen)
        self.profileIcon.mousePressEvent = self.select_profile_picture

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

        self.add_grid_item("פעילויות יומיות", r".\Resources\Icons\alarm.png", False)
        self.add_grid_item("אוכל", r".\Resources\Icons\restaurant.png", False)
        self.add_grid_item("תקשורת", r".\Resources\Icons\icons8-communicate-80.png", False)


        records = get_user_categories(self.profile_name)

        for record in records:
            self.add_grid_item(record[1], record[2], record[1])

    def add_grid_item(self, label, image, is_deleteable=True):
        if self.col >= 6:
            self.col = 1
            self.row += 1

        try:
            v_widget = QWidget(self)
            v_widget.setFixedWidth(190)
            v_widget.setFixedHeight(235)
            vl = QVBoxLayout(v_widget)
            vl.setSpacing(5)

            ll = CategoryGridLabel(label, image, self)
            ll.setFixedHeight(180)
            ll.setFixedWidth(180)
            ll.setScaledContents(True)
            ll.setMargin(3)
            ll.setStyleSheet("border: 1px solid black;")
            ll.setAlignment(QtCore.Qt.AlignCenter)
            vl.addWidget(ll)
            ll = QLabel(label, self)
            ll.setAlignment(QtCore.Qt.AlignCenter)
            ll.setFixedWidth(180)
            ll.setFont(QtGui.QFont("MS Shell Dlg 2", 10, weight=QtGui.QFont.Bold))
            vl.addWidget(ll)
            if is_deleteable:
                ll = QLabel("מחק קטגוריה", self)
                ll.setStyleSheet("color: red;")
                ll.mousePressEvent = partial(self.delete_category, label)
                ll.setAlignment(QtCore.Qt.AlignCenter)
                ll.setFixedWidth(180)
                ll.setFont(QtGui.QFont("MS Shell Dlg 2", 10, weight=QtGui.QFont.Bold))
                vl.addWidget(ll)
            self.gridLayout.addWidget(v_widget, self.row, self.col, 1, 1)
            self.gridLayout.setColumnStretch(self.col % 6, 1)
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

    def select_profile_picture(self, event):
        image_path, _ = QFileDialog.getOpenFileName(self, 'Select Profile Picture', 'c:\\', "Image files (*.jpg *.png *.jpeg)")
        if image_path != '' and image_path is not None:
            update_user_profile_picture(self.profile_name, image_path)
            self.load_profile_picture()

    def load_profile_picture(self):
        try:
            self.profile_picture_bytes = get_user_profile_picture(self.profile_name)
            qp = QPixmap()
            qp.loadFromData(self.profile_picture_bytes)
            self.profileIcon.setPixmap(qp)
        except Exception as e:
            print("exp: " + str(e))

