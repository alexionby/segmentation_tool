import os, glob
import shutil

from functools import partial

import sys
from PyQt5.QtWidgets import QApplication, QLayout, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QSlider, QMainWindow, QShortcut
from PyQt5.QtWidgets import QLineEdit, QRubberBand, QMessageBox
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtWidgets import QSizePolicy

from PyQt5.QtGui import QIcon, QIntValidator, QPixmap, QKeySequence

from PIL import ImageQt, Image


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        
        self.icon = QIcon(QPixmap('v.png'))
        self.idx = None
        self.main_label_size = 512

        self.initUI()


    def keyPressEvent(self, event):

        super().keyPressEvent(event)

        if event.key() == Qt.Key_Left:
            curr_value = self.rotate_slider.value()
            self.rotate_slider.valueChanged.emit(curr_value - 5)

        if event.key() == Qt.Key_Right:
            curr_value = self.rotate_slider.value()
            self.rotate_slider.valueChanged.emit(curr_value + 5)

        if event.key() == Qt.Key_Space:
            self.test_method()

    def test_method(self):
            print('Space key pressed')

    def test_message(self):
            QMessageBox.information(self, 'Message', 'Ctrl + M initiated')
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.msgSc = QShortcut(QKeySequence("Ctrl+M"), self)
        self.msgSc.activated.connect(self.test_message)

        rootLayout = QVBoxLayout()
        # rootLayout.setAlignment(Qt.AlignTop)

        self.imageDirLine = QLineEdit('test_images', self)
        self.imageDirLine.setPlaceholderText('Images folder')
        self.maskDirLine = QLineEdit('test_masks', self)
        self.maskDirLine.setPlaceholderText('Raw masks folder (optional)')
        self.outDirLine = QLineEdit('test_output', self)
        self.outDirLine.setPlaceholderText('Output folder')
        self.targetSizeLine = QLineEdit('768', self)
        self.targetSizeLine.setValidator(QIntValidator(64, 1024, self))
        self.targetSizeLine.setPlaceholderText('Target size (default: 512px)')
        self.rootBtn = QPushButton("Apply")
        self.resultLabel = QLabel("Num Files: 0")
        self.resultLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.resultLabel.setAlignment(Qt.AlignTop)
        
        rootLayout.addWidget(self.imageDirLine)
        rootLayout.addWidget(self.maskDirLine)
        rootLayout.addWidget(self.outDirLine)
        rootLayout.addWidget(self.targetSizeLine)
        rootLayout.addWidget(self.rootBtn)
        rootLayout.addWidget(self.resultLabel, 0)

        self.rootBtn.clicked.connect(self.apply_root_dir)

        control_layout = self.create_control_layout()

        ## Create widget
        self.label =  QMainLabel(self)
        self.label.load_pixmap('media/512.png')

        self.sh = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.sh.activated.connect(self.label.restore_original)
        
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        
        # self.resize(pixmap.width(),pixmap.height())

        rotate_slider, rotate_label = self.add_slider()
        
        rotate_layout = QVBoxLayout()
        rotate_layout.addWidget(rotate_label)
        rotate_layout.addWidget(rotate_slider)
        
        self.rotate_label = rotate_label
        self.rotate_slider = rotate_slider

        tools_layout = self.build_toolbox()

        layout = QHBoxLayout()
        btn_layout = QVBoxLayout()

        btn_layout.addLayout(rootLayout)
        btn_layout.addLayout(control_layout)
        btn_layout.addLayout(tools_layout)

        btn_layout.addLayout(rotate_layout)
        btn_layout.addWidget(QPushButton("Left-Most"), 1)
        btn_layout.addWidget(QPushButton("Center"), 1)
        btn_layout.addWidget(QPushButton("Right-Most"), 2)

        layout.addLayout(btn_layout)
        layout.addLayout(rootLayout)
        layout.addWidget(self.label)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        self.show()


    def add_slider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setMaximum(90)
        slider.setMinimum(-90)
        slider.setPageStep(5)

        rotate_label = QLabel('0')
        rotate_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        rotate_label.setMaximumHeight(20)

        slider.valueChanged.connect(self.updateLabel)

        return slider, rotate_label

    def updateLabel(self, value):
        self.rotate_label.setText(str(value))
        self.rotate_slider.setValue(value)

        image = ImageQt.fromqpixmap(self.label.original_image_pixmap)
        image = image.rotate(-1 * value)
        pixmap = ImageQt.toqpixmap(image)
        self.label.setPixmap(pixmap)


    def apply_root_dir(self):

        self.imageDirLine.setDisabled(True)
        self.maskDirLine.setDisabled(True)
        self.outDirLine.setDisabled(True)
        self.targetSizeLine.setDisabled(True)

        size = self.targetSizeLine.text()
        if size == '':
            size = self.targetSizeLine
        else:
            self.main_label_size = int(self.targetSizeLine.text())
            self.label.set_size(self.main_label_size)
        
        self.root_dir = self.imageDirLine.text()
        if self.root_dir == '':
            self.resultLabel.setText(f'Please, set root folder!')
            return None

        images = glob.glob(os.path.join(self.root_dir, '*.*'))
        num_images = len(images)

        if num_images == 0:
            self.resultLabel.setText(f'Num of images is Zero!')
            return None

        self.mask_dir = self.maskDirLine.text()
        masks = glob.glob(os.path.join(self.mask_dir, '*.*'))

        output_folder = self.outDirLine.text()

        if len(output_folder) == 0:
            self.resultLabel.setText(f'Wrong output folder name')
            return None

        self.resultLabel.setText(f'Sucess! Num images: {num_images}')

        try:
            os.mkdir(output_folder)
        except FileExistsError:
            print('recreating dir')
            shutil.rmtree(output_folder)
            os.mkdir(output_folder)

        self.images_list = sorted(images)
        self.masks_list = sorted(masks)
        self.idx = 0
        self.read_pad_show(self.images_list[self.idx])
        self.cur_pos_label.setText(f'Position: {self.idx + 1}')


    def read_pad_show(self, path):
        image = Image.open(path)
        image = pad_to_square(image, self.main_label_size)
        image = ImageQt.toqpixmap(image)
        self.label.load_pixmap(image)


    def create_control_layout(self):
        
        prev_btn = QPushButton('< Prev')
        next_btn = QPushButton('Next >')

        next_btn.clicked.connect(partial(self.direction_btn_press, True))
        prev_btn.clicked.connect(partial(self.direction_btn_press, False))

        self.cur_pos_label = QLabel(f'Position: {self.idx}')

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.cur_pos_label)
        control_layout.addWidget(prev_btn)
        control_layout.addWidget(next_btn)
        return control_layout


    def direction_btn_press(self, forward=True):

        folder = self.outDirLine.text()
        fname = self.images_list[self.idx]
        fname = os.path.basename(fname)
        fname = fname.split('.')[0] + '.png'
        image = ImageQt.fromqpixmap(self.label.pixmap())
        image.save(os.path.join(folder, fname))

        if forward:
            self.idx += 1
        else:
            self.idx -= 1

        if self.idx < 0:
            self.idx = 0
        elif self.idx > len(self.images_list) - 1:
            self.idx = self.idx - 1

        self.rotate_slider.valueChanged.emit(0)
        self.read_pad_show(self.images_list[self.idx])
        self.cur_pos_label.setText(f'Position: {self.idx + 1}')

# class ToolBox(QLayout):
#     def __init__(self, parentQWidget = None):
#         super(ToolBox, self).__init__(parentQWidget)

    def build_toolbox(self):

        layout = QHBoxLayout()

        crop = QPushButton(QIcon('media/scissors.png'), 'Crop')
        brush = QPushButton(QIcon('media/painting.png'), 'Draw')
        eraser = QPushButton(QIcon('media/eraser.png'), 'Erase')
        
        layout.addWidget(crop)
        layout.addWidget(brush)
        layout.addWidget(eraser)

        return layout


class QMainLabel(QLabel):
    def __init__(self, parentQWidget):
        super(QMainLabel, self).__init__(parentQWidget)
        self.original_image_pixmap = None
        self.original_mask_pixmap = None
        self.target_size = self.parent().main_label_size

    def set_size(self, size):
        self.target_size = size
    
    def load_pixmap(self, image_path, mask_path=None):
        self.original_image_pixmap = QPixmap(image_path)
        
        if mask_path:
            self.original_mask_pixmap = QPixmap(mask_path)
        
        self.setPixmap(self.original_image_pixmap)
        


    def restore_original(self):
        print('Ctrl+Z')
        if self.original_image_pixmap:
            self.setPixmap(self.original_image_pixmap)

    def mousePressEvent (self, eventQMouseEvent):
        self.originQPoint = eventQMouseEvent.pos()
        self.currentQRubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.currentQRubberBand.setGeometry(QRect(self.originQPoint, QSize()))
        self.currentQRubberBand.show()

    def mouseMoveEvent (self, eventQMouseEvent):
        self.currentQRubberBand.setGeometry(QRect(self.originQPoint, eventQMouseEvent.pos()).normalized())

    def mouseReleaseEvent (self, eventQMouseEvent):
        self.currentQRubberBand.hide()
        currentQRect = self.currentQRubberBand.geometry()
        self.currentQRubberBand.deleteLater()
        cropQPixmap = self.pixmap().copy(currentQRect)
        # cropQPixmap.save('output.png')

        crop_PIL = ImageQt.fromqpixmap(cropQPixmap)
        crop_PIL = pad_to_square(crop_PIL, self.target_size)
        cropQPixmap = ImageQt.toqpixmap(crop_PIL)
        self.setPixmap(cropQPixmap)
        

# https://jdhao.github.io/2017/11/06/resize-image-to-square-with-padding/
def pad_to_square(image, size=1024):
    
    orig_size = image.size
    ratio = size / max(orig_size)
    new_size = tuple([int(x*ratio) for x in orig_size])

    image = image.resize(new_size, Image.ANTIALIAS)

    new_im = Image.new("RGB", (size, size))
    new_im.paste(image, ((size-new_size[0])//2,
                        (size-new_size[1])//2))

    return new_im


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('media/vendetta.png'))
    ex = MainWindow()
    sys.exit(app.exec_())