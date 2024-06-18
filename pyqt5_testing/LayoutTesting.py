import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QPalette, QColor
import qdarktheme


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My App")


        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        layout4 = QGridLayout()

        layout1.setContentsMargins(10, 100, 10, 10)
        layout1.setSpacing(10)

        layout2.addWidget(Color('red'))
        layout2.addWidget(Color('Green'))
        layout2.addWidget(Color('grey'))

        layout1.addLayout(layout2)

        layout4.addWidget(Color('Purple'), 0, 0)
        layout4.addWidget(Color('green'), 1, 0)
        layout4.addWidget(Color('blue'), 1, 1)
        layout4.addWidget(Color('purple'), 2, 0)

        layout1.addLayout(layout4)

        layout3.addWidget(Color('red'))
        layout3.addWidget(Color('purple'))

        layout1.addLayout(layout3)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)


class Color(QWidget):

    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()