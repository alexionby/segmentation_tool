import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtGui import QBrush
from PySide2.QtCore import Qt

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PySide2")
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(400, 300)
        canvas.fill(Qt.green)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        # self.draw_something()

        pic = QtGui.QPixmap("../media/1k.jpg")
        print(pic)

        painter = QtGui.QPainter(self.label.pixmap())
        painter.drawPixmap(self.rect(), pic)

        print(self.rect())

        self.last_x, self.last_y = None, None

    def mouseMoveEvent(self, e):
        if self.last_x is None: # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return # Ignore the first time.

        painter = QtGui.QPainter(self.label.pixmap())
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawEllipse(self.last_x, self.last_y, 10, 10)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
