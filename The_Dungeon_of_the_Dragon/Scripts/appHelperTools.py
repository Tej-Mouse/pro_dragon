import sys

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
    QFrame
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5 import QtCore, Qt
import qdarktheme
from functools import partial

from PyQt5.sip import delete

from Scripts import objectsDnD, style, charManagers, ruleTools


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


def CreateLabel(text:str, font:QFont, style_sheet=None):
    label = QLabel()
    label.setText(text)
    label.setFont(font)

    if style_sheet is not None:
        label.setStyleSheet(style_sheet)
    return label


class ItemLabel(QFrame):

    def __init__(self, item:objectsDnD.Item, font:QFont):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setFrameShape(QFrame.Panel)
        # self.setMaximumSize(100,50)
        self.item = item
        self.text_label = QLabel()
        self.text_label.setFont(style.ItemLabelFont)
        self.text_label.setText(self.create_text())
        self.text_label.setStyleSheet(style.GreyLabel)
        self.layout.addWidget(self.text_label)
        # self.setMaximumWidth(300)
        self.setFixedHeight(80)
        self.setStyleSheet(style.ItemFrame)

    def create_text(self):
        text = ''
        text += self.item.get_name() + " " + str(self.item.get_amount()) + "x"
        text += "\n     "
        text += self.item.get_type() + "| "
        if self.item.get_amount() > 1:
            text += "(" + str(self.item.get_amount() * self.item.get_weight()) + ")"
        text += str(self.item.get_weight()) + " lbs" + " | "
        text += str(self.item.get_cost()[0]) + " " + self.item.get_cost()[1]
        return text

    def update(self):
        self.setText(self.create_text())


class EncumberanceLabel(QFrame):

    num_of_bars = 15

    def __init__(self, encumberance:ruleTools.Encumberance):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setFrameShape(QFrame.Panel)
        self.encumberance = encumberance

    def create_bar_widget(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.WinPanel)

        bar_layout = QGridLayout(frame)

        set_points = self.encumberance.get_encumberance_levels()
        max_weight = set_points[2]
        # TODO Fix
        if max_weight == 0:
            max_weight = 150
            set_points[1] = 50
            set_points[0] = 100
        lvl2 = int(np.ceil(max_weight * self.num_of_bars)) - 1  # minus for 0 index
        lvl1 = int((set_points[1] / max_weight) * self.num_of_bars) - 1
        lvl0 = int((set_points[0] / max_weight) * self.num_of_bars) - 1

        empty_color = ["#c7c7c7","#d8cd9c","#d8b69c","#c95e60"]
        fill_color = ["#919191","#e7d16f","#f000ba","#db292d"]
        current_weight = self.encumberance.get_weight()
        current_weight_bar = int((current_weight / max_weight) * self.num_of_bars)

        k = self.num_of_bars - 1

        for i in range(self.num_of_bars):
            current_level = 0
            if i > lvl0:
                current_level += 1

            if i > lvl1:
                current_level += 1

            if i > lvl2:
                current_level += 1

            if i < current_weight_bar:
                color = fill_color[current_level]
                print("FULL ",color)
            else:
                color = empty_color[current_level]
                print("Empty")


            bar = MakeColorWidget(color)

            bar_layout.addWidget(bar,k,0)
            k -= 1

        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.setSpacing(0)
        return frame

    def add_bars(self):
        self.layout.addWidget(self.create_bar_widget())

    def update(self):
        delete(self.layout)
        self.layout = QVBoxLayout(self)
        self.add_bars()


def MakeColorWidget(color):
    widget = QFrame()

    stylesheet =("QFrame {border-radius: 15px; background-color: " + color + "}"
     )
    widget.setStyleSheet(stylesheet)
    # widget.setAutoFillBackground(True)
    #
    # palette = widget.palette()
    # palette.setColor(QPalette.Window, QColor(color))
    # widget.setPalette(palette)
    # widget.setMinimumHeight(100)
    return widget



#
#

