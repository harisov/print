import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
import random


class Circle(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.show()
        self.paint = False
        self.pushButton.clicked.connect(self.circle)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.paint:
            painter = QPainter(self)
            x, y = [random.randint(10, 900) for i in range(2)]
            w, h = [random.randint(10, 100) for i in range(2)]
            painter.setPen(QPen(Qt.yellow, 5, Qt.SolidLine))
            painter.drawEllipse(x, y, w, h)

    def circle(self):
        self.paint = True
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qwe = Circle()
    qwe.show()
    sys.exit(app.exec_())
