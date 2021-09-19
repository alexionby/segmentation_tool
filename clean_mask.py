import sys
from PySide2.QtWidgets import (QMainWindow, QApplication, QLabel, QWidget,
                            QHBoxLayout, QGraphicsItem, QGraphicsView, QGraphicsScene, QPushButton)
from PySide2.QtGui import QPixmap, QPainter, QImage
from PySide2.QtCore import Qt, QPoint


class View(QGraphicsView):

    def mousePressEvent(self, event):
        items = self.items(event.pos())
        for item in items:
            print(item.mapFromScene(self.mapToScene(event.pos())))


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        # self.label = QLabel()

        # image = QPixmap("test_images/002.png")
        # label = QPixmap("test_masks/002.png")

        # canvas = QPixmap(512,512)
        #
        # image = QImage("test_images/002.png")
        # label = QImage("test_masks/002.png")
        #
        # painter = QPainter()
        # painter.begin(canvas)
        # painter.drawImage(QPoint(0,0), label)
        # painter.drawImage(QPoint(0,0), image)
        # painter.end()
        #
        # self.label.setPixmap(canvas)
        # self.setCentralWidget(self.label)
        #
        self.scene = QGraphicsScene(0, 0, 400, 200)

        pixmap = QPixmap("test_images/002.png")
        pixmap_item = self.scene.addPixmap(pixmap)
        pixmap_item.setPos(0, 0)

        view = View(self.scene)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.view = view
        # self.view.setAlignment(Qt.AlignLeft)
        # self.view.setAlignment(Qt.AlignTop)
        self.view.setMinimumWidth(512)
        self.view.setMinimumHeight(512)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.view.ensureVisible(pixmap_item, 0, 0)

        btn = QPushButton("button")
        btn.clicked.connect(self.list_items())

        hbox = QHBoxLayout(self)
        hbox.addWidget(view)
        hbox.addWidget(btn)

        widget = QWidget()
        widget.setLayout(hbox)

        self.setCentralWidget(widget)

    def list_items(self):
        print(self.scene.items())
        item = self.scene.items()[0]
        pos = item.pos()
        x,y = pos.x(), pos.y()
        item.setPos(x+10, x+10)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
