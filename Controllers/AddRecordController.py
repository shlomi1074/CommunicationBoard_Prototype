from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

import Controllers.CommunicationBoardScreen
from Database.DBQueries import *


class AddRecordController(QMainWindow):
    def __init__(self, profile_name, parent):
        super().__init__()
        # LOAD UI FILE
        self.ui = uic.loadUi(r".\UI\AddRecordingScreen.ui", self)
        self.setFixedSize(600, 400)
        self.profile_name = profile_name
        self.AddRecorButton.clicked.connect(self.add_record_to_db)
        self.parentScreen = parent
        self.ErrorMsgLabel.setVisible(False)

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

        res = add_record(self.profile_name, self.RecordName.text(), self.RecordText.text(), "apple")
        if res:
            print("added")
            self.parentScreen.close()
            main = Controllers.CommunicationBoardScreen.CommunicationBoardController(self.profile_name)
            main.show()
            self.close()
        else:
            self.ErrorMsgLabel.setVisible(True)
            self.ErrorMsgLabel.setText("הייתה בעיה בהוספת ההקלטה. אנא נסו שוב")







