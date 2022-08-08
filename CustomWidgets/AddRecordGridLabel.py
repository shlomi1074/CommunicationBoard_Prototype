import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QFrame


class AddRecordGridLabel(QLabel):
    def __init__(self,  name, pixmap,  parent=None):
        super().__init__(parent)
        self.name = name
        self.pixmap = pixmap
        self.setPixmap(QPixmap(self.pixmap))
        self.parent = parent

    def mouseReleaseEvent(self, event):
        for i in reversed(range(self.parent.gridLayout.count())):
            self.parent.gridLayout.itemAt(i).widget().setFrameStyle(QFrame.NoFrame)
            self.parent.gridLayout.itemAt(i).widget().setStyleSheet("border: 2px solid black;")

        self.setStyleSheet("border: 4px solid red;")

        self.parent.selectedIcon.setText(self.name)




