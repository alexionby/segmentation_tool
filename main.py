import os, glob
import shutil

from functools import partial

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QSlider, QMainWindow
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy

from PyQt5.QtGui import QIcon, QPixmap

from PIL import ImageQt, Image


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.icon = QIcon(QPixmap('v.png'))

        self.idx = None

        self.initUI()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            curr_value = self.rotate_slider.value()
            self.rotate_slider.valueChanged.emit(curr_value + 1)

        if event.key() == Qt.Key_Right:
            curr_value = self.rotate_slider.value()
            self.rotate_slider.valueChanged.emit(curr_value - 1)

        if event.key() == Qt.Key_Space:
            self.test_method()

    def test_method(self):
            print('Space key pressed')
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)
        self.setGeometry(self.left, self.top, self.width, self.height)


        rootLayout = QVBoxLayout()
        self.rootLine = QLineEdit('media')
        self.rootLine.setPlaceholderText('images folder')
        self.outfLine = QLineEdit('output')
        self.outfLine.setPlaceholderText('output folder')
        self.rootBtn = QPushButton("Apply")
        self.resultLabel = QLabel("Num Files: 0")
        self.resultLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.resultLabel.setAlignment(Qt.AlignTop)
        
        rootLayout.addWidget(self.rootLine)
        rootLayout.addWidget(self.outfLine)
        rootLayout.addWidget(self.rootBtn)
        rootLayout.addWidget(self.resultLabel, 0)

        self.rootBtn.clicked.connect(self.apply_root_dir)

        control_layout = self.create_control_layout()

        # # Create widget
        self.label = QLabel(self)

        self.pixmap = QPixmap('media/p1024.png')
        self.label.setPixmap(self.pixmap)
        
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        
        # self.resize(pixmap.width(),pixmap.height())

        rotate_slider, rotate_label = self.add_slider()
        
        rotate_layout = QVBoxLayout()
        rotate_layout.addWidget(rotate_label)
        rotate_layout.addWidget(rotate_slider)
        
        self.rotate_label = rotate_label
        self.rotate_slider = rotate_slider

        layout = QHBoxLayout()
        btn_layout = QVBoxLayout()

        btn_layout.addLayout(rootLayout)
        btn_layout.addLayout(control_layout)

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

        image = ImageQt.fromqpixmap(self.pixmap)
        image = image.rotate(-1 * value)
        pixmap = ImageQt.toqpixmap(image)
        self.label.setPixmap(pixmap)

    
    def next_image(self):
        pass


    def apply_root_dir(self):

        self.root_dir = self.rootLine.text()
        if self.root_dir == '':
            self.resultLabel.setText(f'Please, set root folder!')
            return None

        images = glob.glob(os.path.join(self.root_dir, '*.*'))
        num_images = len(images)

        if num_images == 0:
            self.resultLabel.setText(f'Num of images is Zero!')
            return None

        output_folder = self.outfLine.text()

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
        self.idx = 0
        self.read_pad_show(self.images_list[self.idx])
        self.cur_pos_label.setText(f'Position: {self.idx + 1}')


    def read_pad_show(self, path):
        image = Image.open(path)
        image = pad_to_square(image)
        image = ImageQt.toqpixmap(image)
        self.pixmap = QPixmap(image)
        self.label.setPixmap(self.pixmap)


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

        folder = self.outfLine.text()
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
    ex = App()
    sys.exit(app.exec_())