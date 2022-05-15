import sys
from PyQt5.QtWidgets import QApplication
from Controllers.ProfileScreen import ProfileScreenController

if __name__ == '__main__':
    app = QApplication([])
    window = ProfileScreenController()
    window.show()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
