import sys
from PySide2.QtWidgets import (QGraphicsView, QGraphicsScene, QApplication, QVBoxLayout, QPushButton, QHBoxLayout, QSlider,
                               QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem)
from PySide2.QtGui import QBrush, QPen, QPolygonF, QPixmap, QPainter
from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt, QPointF


if __name__ == '__main__':

    class Window(QWidget):
        def __init__(self):
            super().__init__()

            # Defining a scene rect of 400x200, with it's origin at 0,0.
            # If we don't set this on creation, we can set it later with .setSceneRect
            self.scene = QGraphicsScene(0, 0, 400, 200)

            # Draw a rectangle item, setting the dimensions.
            rect = QGraphicsRectItem(0, 0, 200, 50)

            # Set the origin (position) of the rectangle in the scene.
            rect.setPos(50, 20)

            # Define the brush (fill).
            brush = QBrush(Qt.red)
            rect.setBrush(brush)

            # Define the pen (line)
            pen = QPen(Qt.cyan)
            pen.setWidth(10)
            rect.setPen(pen)

            ellipse = QGraphicsEllipseItem(0, 0, 100, 100)
            ellipse.setPos(75, 30)

            brush = QBrush(Qt.blue)
            ellipse.setBrush(brush)

            pen = QPen(Qt.green)
            pen.setWidth(5)
            ellipse.setPen(pen)

            # Add the items to the scene. Items are stacked in the order they are added.
            self.scene.addItem(ellipse)
            self.scene.addItem(rect)

            ellipse.setFlag(QGraphicsItem.ItemIsMovable)
            ellipse.setFlag(QGraphicsItem.ItemIsSelectable)

            rect.setFlag(QGraphicsItem.ItemIsMovable)
            rect.setFlag(QGraphicsItem.ItemIsSelectable)

            textitem = self.scene.addText("QGraphics is fun!")
            textitem.setPos(100, 100)

            self.scene.addPolygon(
                QPolygonF(
                    [
                        QPointF(30, 60),
                        QPointF(270, 40),
                        QPointF(400, 200),
                        QPointF(20, 150),
                    ]),
                QPen(Qt.GlobalColor.darkGreen),
            )

            pixmap = QPixmap("../media/vendetta.png")
            pixmap_item = self.scene.addPixmap(pixmap)
            pixmap_item.setPos(250, 70)

            # Define our layout.
            vbox = QVBoxLayout()

            up = QPushButton("Up")
            up.clicked.connect(self.up)
            vbox.addWidget(up)

            down = QPushButton("Down")
            down.clicked.connect(self.down)
            vbox.addWidget(down)

            rotate = QSlider()
            rotate.setRange(0, 360)
            rotate.valueChanged.connect(self.rotate)
            vbox.addWidget(rotate)

            view = QGraphicsView(self.scene)
            view.setRenderHint(QPainter.RenderHint.Antialiasing)

            hbox = QHBoxLayout(self)
            hbox.addLayout(vbox)
            hbox.addWidget(view)

            self.setLayout(hbox)

        def up(self):
            """ Iterate all selected items in the view, moving them forward. """
            items = self.scene.selectedItems()
            for item in items:
                z = item.zValue()
                item.setZValue(z + 1)

        def down(self):
            """ Iterate all selected items in the view, moving them backward. """
            items = self.scene.selectedItems()
            for item in items:
                z = item.zValue()
                item.setZValue(z - 1)

        def rotate(self, value):
            """ Rotate the object by the received number of degrees. """
            items = self.scene.selectedItems()
            for item in items:
                item.setRotation(value)

    app = QApplication(sys.argv)

    w = Window()
    w.show()

    app.exec_()
