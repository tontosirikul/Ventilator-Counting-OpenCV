from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


#self = QMainWindow
class Mywindow(QMainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.setGeometry(200,200,300,300)
        self.setWindowTitle("Ventilator Counter")
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("status")
        self.label.move(50,50)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("start")
        self.b1.clicked.connect(start)
    
    def start(self):
        self.label.setText("Play video")
        self.update()
    
    def update(self):
        self.label.adjustSize()
        #automatically adjust the labal size


def start():
    print("clicked")


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.show()
    sys.exit(app.exec_())

window()