import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QFrame

from Controllers.CommunicationBoardScreen import CommunicationBoardController


class CategoryGridLabel(QLabel):
    def __init__(self, name, pixmap,  parent=None):
        super().__init__(parent)
        self.name = name
        self.pixmap = pixmap
        self.setPixmap(QPixmap(self.pixmap))
        self.parent = parent

    def mouseReleaseEvent(self, event):
        board = CommunicationBoardController(self.parent.profile_name, self.name)
        board.show()
        self.parent.close()
        pass




