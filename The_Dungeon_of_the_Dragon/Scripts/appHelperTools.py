import sys
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
    QFrame
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5 import QtCore, Qt
import qdarktheme
from functools import partial
import charecter as CSV2
import pyqt5_Custom as PYCustom


def CreateTabButton(switch_tab_function, tab_value:int, label_font, style_sheet:str, label:str):
    tab_button = QPushButton()
    tab_button.setText(label)
    tab_button.clicked.connect(partial(switch_tab_function, tab_value))
    tab_button.setFont(label_font)
    tab_button.setStyleSheet( style_sheet)
    return tab_button


def CreateGenButton(text, font, stylesheet, function, minWidth=None, minHeight=None):
    button = QPushButton()
    button.setText(text)
    button.setFont(font)
    button.setStyleSheet(stylesheet)
    if minHeight is not None:
        button.setMinimumHeight(minHeight)
    if minWidth is not None:
        button.setMinimumWidth(minWidth)
    button.clicked.connect(function)
    return button


def CreateSeperator():
    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    return separator

def CreateVSeperator():
    separator = QFrame()
    separator.setFrameShape(QFrame.VLine)
    return separator


def CreateLabel(text:str, font:QFont, style=None):
    label = QLabel()
    label.setText(text)
    label.setFont(font)

    if style is not None:
        label.setStyleSheet(style)
    return label



#
# def CreateFrame(top_label_str:str, bottom_label_str:str):
#     frame = QFrame()
#     frame.setFrameShape(QFrame.Panel)
#     frame.setMaximumHeight(100)
#
#     layout = QVBoxLayout(frame)
#
#     bottom_label = QLabel()
#     bottom_label.setText(bottom_label_str)
#
#     layout.addWidget(create_top_label(top_label_str), alignment=QtCore.Qt.AlignCenter)
#     layout.addWidget(bottom_label, alignment=QtCore.Qt.AlignCenter)
#
#     return frame, bottom_label
#
#
# def create_top_label(string:str):
#     top_label = QLabel()
#     top_label.setText(string)
#     top_label.setFont(LabelFont2)
#     return top_label
#
#

