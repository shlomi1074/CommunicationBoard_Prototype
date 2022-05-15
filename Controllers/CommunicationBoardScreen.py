from functools import partial

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout
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

        records = get_user_records(self.profile_name)
        for record in records:
            self.add_grid_item(record[2], record[3], record[0])

    def open_add_record_screen(self):
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
            vl = QVBoxLayout()
            ll = GridLabel(label, text, image, self)
            ll.setFixedHeight(200)
            ll.setFixedWidth(200)
            ll.setScaledContents(True)
            vl.addWidget(ll)
            ll = QLabel(label, self)
            ll.setAlignment(QtCore.Qt.AlignCenter)
            vl.addWidget(ll)
            ll = QLabel("מחק הקלטה", self)
            ll.setStyleSheet("color: red;")
            ll.mousePressEvent = partial(self.delete_record, label)
            ll.setAlignment(QtCore.Qt.AlignCenter)
            vl.addWidget(ll)
            self.gridLayout.addLayout(vl, self.row, self.col, 1, 1)
            self.col += 1
        except Exception as e:
            print(e)

    def delete_record(self, record_name, event):
        print(record_name)
        RES = delete_user_record(self.profile_name, record_name)
        print(RES)
        self.load_grid()

