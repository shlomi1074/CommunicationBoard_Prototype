from PyQt5 import uic, Qt, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Controllers.CategoryController import CategoryController
from Database.DBMgmt import *
from Database.DBQueries import *


class ProfileScreenController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main = None
        # LOAD UI FILE
        import os
        directory = os.getcwd()

        print(directory)
        self.ui = uic.loadUi(r".\UI\ProfileScreen.ui", self)
        self.setFixedSize(800, 600)
        # LOAD TAB WIDGET CSS FILE
        with open('Resources/CSS/ComboBox.css', "r") as fh:
            tw = fh.read()
            self.ProfileComboBox.setStyleSheet(tw)
        create_database()
        self.load_combobox_data()

        self.ErrorLabel.setVisible(False)

        self.AddProfileButton.clicked.connect(self.add_profile_button_click)
        self.DeleteProfileButton.clicked.connect(self.delete_profile_button_click)
        self.LoadBoardButton.clicked.connect(self.load_categories_button_click)

    def add_profile_button_click(self):
        self.ErrorLabel.setVisible(True)
        if self.ProfileLineEdit.text() is None or self.ProfileLineEdit.text() == '':
            return

        profile_names = get_profile_names()
        for profile_name in profile_names:
            if profile_name == self.ProfileLineEdit.text():
                print("profile already exist")
                self.ErrorLabel.setText("פרופיל קיים כבר. נא לבחור שם אחר")
                return

        res = add_profile(self.ProfileLineEdit.text())
        if res:
            print("profile created")
            self.ErrorLabel.setText("הפרופיל נוצר בהצלחה")
            self.ProfileLineEdit.setText("")

        else:
            self.ErrorLabel.setText("אירעה שגיאה ביצירת הפרופיל")
        self.load_combobox_data()

    def delete_profile_button_click(self):
        self.ErrorLabel.setVisible(True)
        if self.ProfileLineEdit.text() is None or self.ProfileLineEdit.text() == '':
            return

        profile_names = get_profile_names()
        for profile_name in profile_names:
            if profile_name == self.ProfileLineEdit.text():
                res = delete_profile(self.ProfileLineEdit.text())
                if res:
                    print("profile deleted")
                    self.ErrorLabel.setText("הפרופיל נמחק בהצלחה")
                    self.ProfileLineEdit.setText("")
                    for p in get_profile_names():
                        print(p)
                else:
                    self.ErrorLabel.setText("אירעה שגיאה במחיקת הפרופיל")
                    print("profile does not deleted")
                self.load_combobox_data()
                return
        self.ErrorLabel.setText(f"אין פרופיל בשם {self.ProfileLineEdit.text()}")

    def load_combobox_data(self):
        self.ProfileComboBox.clear()
        self.ProfileComboBox.setEditable(True)
        # getting the line edit of combo box
        line_edit = self.ProfileComboBox.lineEdit()

        # setting line edit alignment to the center
        line_edit.setAlignment(QtCore.Qt.AlignCenter)

        profile_names = get_profile_names()
        profile_names.insert(0, 'בחר פרופיל')
        self.ProfileComboBox.addItems(profile_names)

        for i in range(self.ProfileComboBox.count()):
            self.ProfileComboBox.setItemData(i, QtCore.Qt.AlignCenter, QtCore.Qt.ItemDataRole.TextAlignmentRole)

        # setting line edit to read only
        line_edit.setReadOnly(True)


    def load_categories_button_click(self):
        content = self.ProfileComboBox.currentText()
        if content is None or content == '' or content == 'בחר פרופיל':
            return
        self.main = CategoryController(content)
        self.main.show()
        self.close()



