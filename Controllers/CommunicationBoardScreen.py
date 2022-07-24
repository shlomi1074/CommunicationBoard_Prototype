import os
import shutil
from functools import partial

from PyQt5 import uic, QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from CustomWidgets.GridLabel import GridLabel
from Database.DBQueries import *
from Controllers.AddRecordController import AddRecordController
import Controllers.CategoryController

class CommunicationBoardController(QMainWindow):
    def __init__(self, profile_name, category):
        super().__init__()
        # LOAD UI FILE
        self.ui = uic.loadUi(r".\UI\CommunicationBoard.ui", self)
        self.setFixedSize(1100, 650)
        self.profile_name = profile_name
        self.label.setText(f'לוח התקשורת של {profile_name} - קטגוריית {category}')
        self.record_screen = None
        self.this_screen = None
        self.row = 1
        self.col = 1
        self.category = category

        self.layout = QtWidgets.QHBoxLayout(self)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setGeometry(35, 110, 1030, 500)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)
        self.load_grid()
        self.AddAudioButton.clicked.connect(self.open_add_record_screen)
        self.BackButton.clicked.connect(self.back_to_categories_screen)

    def closeEvent(self, event):
        print('close event')
        self.delete_temp_content()

        sound_name = os.getcwd() + r"\\output.mp3"
        sound_name = sound_name.replace("\\", "/")
        if os.path.exists(sound_name):
            os.remove(sound_name)
        event.accept()

    def delete_temp_content(self):
        folder = 'temp'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def back_to_categories_screen(self):
        profile_screen = Controllers.CategoryController.CategoryController(self.profile_name)
        profile_screen.show()
        self.close()

    def load_grid(self):
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)

        self.add_grid_item("כן", "כן", r".\Resources\Icons\yes.png", False)
        self.add_grid_item("לא", "לא", r".\Resources\Icons\no.png", False)

        records = get_user_category_records(self.profile_name, self.category)

        for record in records:
            self.add_grid_item(record[2], record[3], record[1])

    def open_add_record_screen(self):
        self.delete_temp_content()
        if self.record_screen is not None:
            self.record_screen.close()
        self.record_screen = AddRecordController(self.profile_name, self.category, self)
        self.record_screen.show()

    def add_grid_item(self, label, text, image, is_deleteable=True):
        if self.col >= 7:
            self.col = 1
            self.row += 1

        try:
            v_widget = QWidget(self)
            v_widget.setFixedWidth(160)
            v_widget.setFixedHeight(200)
            vl = QVBoxLayout(v_widget)
            vl.setSpacing(0)

            ll = GridLabel(label, text, image, self)
            ll.setFixedHeight(150)
            ll.setFixedWidth(150)
            ll.setScaledContents(True)
            ll.setAlignment(QtCore.Qt.AlignCenter)
            vl.addWidget(ll)
            ll = QLabel(label, self)
            ll.setAlignment(QtCore.Qt.AlignCenter)
            ll.setFixedWidth(150)
            ll.setFont(QtGui.QFont("MS Shell Dlg 2", 10, weight=QtGui.QFont.Bold))
            vl.addWidget(ll)
            if is_deleteable:
                ll = QLabel("מחק הקלטה", self)
                ll.setStyleSheet("color: red;")
                ll.mousePressEvent = partial(self.delete_record, label)
                ll.setAlignment(QtCore.Qt.AlignCenter)
                ll.setFixedWidth(150)
                ll.setFont(QtGui.QFont("MS Shell Dlg 2", 10, weight=QtGui.QFont.Bold))
                vl.addWidget(ll)
            self.gridLayout.addWidget(v_widget, self.row, self.col, 1, 1)
            self.gridLayout.setColumnStretch(self.col % 5, 1)
            self.gridLayout.setRowStretch(self.row, 1)

            self.col += 1
        except Exception as e:
            print(e)

    def delete_record(self, record_name, event):
        print(record_name)
        RES = delete_user_category_record(self.profile_name, record_name, self.category)
        print(RES)
        if RES:
            self.this_screen = CommunicationBoardController(self.profile_name, self.category)
            self.this_screen.show()
            self.close()

