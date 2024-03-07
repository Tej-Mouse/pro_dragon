
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QStackedLayout,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QCheckBox,
    QFrame,
    QSizePolicy,
    QTextEdit,
    QLineEdit,
    QFrame,
)
from PyQt5.QtGui import (
    QPalette,
    QColor,
    QFont,
)
from PyQt5.QtCore import (
    QSize, QObject, pyqtSignal
)
from PyQt5 import QtCore, Qt
import qdarktheme
import ruleTools
from functools import partial
import pyqt5_Custom_Windows as PYCustomWindows
import charManagers
import appHelperTools
import objectsDnD


class ItemLabel(QFrame):

    def __init__(self, item:objectsDnD.Item, font:QFont):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setFrameShape(QFrame.Panel)
        # self.setMaximumSize(100,50)
        self.item = item
        self.text_label = QLabel()
        self.text_label.setFont(font)
        self.text_label.setText(self.create_text())
        self.layout.addWidget(self.text_label)

    def create_text(self):
        text = ''
        text += self.item.get_name() + " " + str(self.item.get_amount()) + "x"
        text += "\n     " + str(self.item.get_weight()) + " lbs"
        return text

    def update(self):
        self.setText(self.create_text())
