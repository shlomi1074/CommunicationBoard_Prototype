import os
import shutil
from functools import partial

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from CustomWidgets.GridLabel import GridLabel
from Database.DBQueries import *
from Controllers.AddRecordController import AddRecordController


class CommunicationBoardController(QMainWindow):
    def __init__(self, profile_name):
        super().__init__()
        # LOAD UI FILE
        self.ui = uic.loadUi(r".\UI\CommunicationBoard.ui", self)
        self.setFixedSize(1100, 650)
        self.profile_name = profile_name
        self.label.setText(f'לוח התקשורת של {profile_name}')
        self.record_screen = None
        self.row = 1
        self.col = 1
        self.load_grid()
        self.AddAudioButton.clicked.connect(self.open_add_record_screen)

    def closeEvent(self, event):
        print('close event')
        self.delete_temp_content()
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

    def load_grid(self):
        # while self.gridLayout.count():
        #     try:
        #         item = self.gridLayout.takeAt(0)
        #         widget = item.widget()
        #         widget.setParent(None)
        #     except:
        #         pass
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)

        for x in range(1, 3):
            for y in range(1, 6):
                empty_label = QLabel("ריק", self)
                empty_label.setAlignment(QtCore.Qt.AlignCenter)
                self.gridLayout.addWidget(empty_label, x, y)

        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)

        records = get_user_records(self.profile_name)

        for record in records:
            self.add_grid_item(record[2], record[3], record[1])

    def open_add_record_screen(self):
        self.delete_temp_content()
        if self.record_screen is not None:
            self.record_screen.close()
        self.record_screen = AddRecordController(self.profile_name, self)
        self.record_screen.show()

    def add_grid_item(self, label, text, image):
        if self.col >= 6:
            self.col = 1
            self.row += 1
        if self.gridLayout.count() >= 10:
            return

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
            vl.addWidget(ll)
            ll = QLabel("מחק הקלטה", self)
            ll.setStyleSheet("color: red;")
            ll.mousePressEvent = partial(self.delete_record, label)
            ll.setAlignment(QtCore.Qt.AlignCenter)
            ll.setFixedWidth(150)
            vl.addWidget(ll)
            self.gridLayout.addWidget(v_widget, self.row, self.col, 1, 1)
            self.gridLayout.setColumnStretch(self.col % 5, 1)
            self.gridLayout.setRowStretch(self.row, 1)

            self.col += 1
        except Exception as e:
            print(e)

    def delete_record(self, record_name, event):
        print(record_name)
        RES = delete_user_record(self.profile_name, record_name)
        print(RES)
        self.load_grid()

