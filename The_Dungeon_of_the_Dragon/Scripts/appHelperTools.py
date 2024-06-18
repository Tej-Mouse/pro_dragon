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
    QFrame, QGraphicsOpacityEffect, QLineEdit, QSpinBox
)
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
from PyQt5 import QtCore, Qt
import qdarktheme
from functools import partial

from PyQt5.sip import delete

from Scripts import objectsDnD, style, charManagers, ruleTools, imageURLS


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def CreateTabButton(switch_tab_function, tab_value: int, label_font, style_sheet: str, label: str):
    tab_button = QPushButton()
    tab_button.setText(label)
    tab_button.clicked.connect(partial(switch_tab_function, tab_value))
    tab_button.setFont(label_font)
    tab_button.setStyleSheet(style_sheet)
    return tab_button


def CreateGenButton(text=None, font=None, stylesheet=None, function=None,function_list=None, minWidth=None,
                    minHeight=None, icon_url=None, icon_size: QIcon = None):
    button = QPushButton()
    if text is not None:
        button.setText(text)

    if font is not None:
        button.setFont(font)

    if stylesheet is not None:
        button.setStyleSheet(stylesheet)

    if minHeight is not None:
        button.setMinimumHeight(minHeight)

    if minWidth is not None:
        button.setMinimumWidth(minWidth)

    if function is not None:
        button.clicked.connect(function)

    if icon_url is not None:
        button.setIcon(QIcon(icon_url))
        if icon_size is not None:
            button.setIconSize(icon_size)

    if function_list is not None:
        for i in range(len(function_list)):
            button.clicked.connect(function_list[i])

    return button


def CreateSeperator():
    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    return separator


def CreateVSeperator():
    separator = QFrame()
    separator.setFrameShape(QFrame.VLine)
    return separator


def CreateLabel(text: str, font: QFont, style_sheet=None):
    label = QLabel()
    label.setText(text)
    label.setFont(font)

    if style_sheet is not None:
        label.setStyleSheet(style_sheet)
    return label


def deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.layout())


class ItemLabel(QFrame):

    def __init__(self,tinventory:charManagers.Inventory,item: objectsDnD.Item):
        super().__init__()
        self.tinventory = tinventory
        self.layout = QHBoxLayout(self)
        self.setFrameShape(QFrame.Panel)
        # self.setMaximumSize(100,50)
        self.item = item
        self.text_label = QLabel()
        self.button_layout = QHBoxLayout()

        self.default_state_creation()
        # self.setMaximumWidth(300)
        self.setFixedHeight(80)
        self.setStyleSheet(style.ItemFrame)
        self.edit_button_layout = None

    def default_state_creation(self):
        self.text_label.setFont(style.ItemLabelFont)
        self.text_label.setText(self.create_text())
        self.text_label.setStyleSheet(style.GreyLabel)
        self.layout.addWidget(self.text_label, stretch=3)
        self.layout.addLayout(self.button_layout)
        self.create_button_layout()

    def add_amount(self):
        self.clear_button_layout()
        line_edit = QSpinBox()
        # line_edit.setPlaceholderText("Enter a number")
        line_edit.setMaximumWidth(300)
        widget_for_info = {
            'addAmount': line_edit
        }
        line_edit.editings.connect(partial(self.create_confirm_button,'add',widget_for_info))
        oldfunc = line_edit.keyPressEvent
        line_edit.keyPressEvent = partial(self.LinekeyPressEvent,oldfunc)

        self.edit_button_layout = QHBoxLayout()
        self.button_layout.addWidget(line_edit)
        self.button_layout.addLayout(self.edit_button_layout)
        # self.create_confirm_button('add',widget_for_info)

        self.layout.addLayout(self.button_layout)

    def LinekeyPressEvent(self,func,QKeyEvent):
        func(QKeyEvent)

    def create_cancel_button(self):
        pass

    def create_confirm_button(self,function_string:str,suplimentary:dict=None):
        deleteItemsOfLayout(self.edit_button_layout)
        self.edit_button_layout = QHBoxLayout()
        if function_string == 'add':
            amount = suplimentary['addAmount'].text()
            if is_number(amount):
                function = partial(self.item.add_amount,int(amount))
                button = CreateGenButton(
                    stylesheet=style.ItemEditButton,
                    icon_url=imageURLS.CheckUrl,
                    icon_size=QtCore.QSize(20, 20),
                    function_list=[function,partial(self.refresh_button_layout)]
                                         )
                self.edit_button_layout.addWidget(button)
                # self.edit_button_layout.addWidget(QLineEdit())
                self.button_layout.addLayout(self.edit_button_layout)

            else:
                self.add_amount()


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

    def clear_button_layout(self):
        self.text_label.deleteLater()
        self.text_label = QLabel()
        deleteItemsOfLayout(self.button_layout)
        self.button_layout = QHBoxLayout()

    def refresh_button_layout(self):
        self.text_label.deleteLater()
        self.text_label = QLabel()
        deleteItemsOfLayout(self.button_layout)
        self.button_layout = QHBoxLayout()
        self.default_state_creation()

    def create_button_layout(self):
        edit_button = CreateGenButton(stylesheet=style.ItemEditButton,
                                           icon_url=imageURLS.IconUrl, icon_size=QtCore.QSize(20, 20))

        add_button = CreateGenButton(stylesheet=style.ItemEditButton,
                                          icon_url=imageURLS.AddUrl, icon_size=QtCore.QSize(20, 20),function=partial(self.add_amount))

        minus_button = CreateGenButton(stylesheet=style.ItemEditButton,
                                            icon_url=imageURLS.MinusUrl, icon_size=QtCore.QSize(20, 20))

        self.button_layout.addWidget(add_button, stretch=0)
        self.button_layout.addWidget(minus_button, stretch=0)
        self.button_layout.addWidget(edit_button, stretch=0)
        self.layout.addLayout(self.button_layout)

    def update(self):
        self.text_label.setText(self.create_text())


def MakeColorWidget(color, opacity):
    widget = QFrame()

    stylesheet = ("QFrame {border-radius: 5px; background-color: " + color + "}"
                  )
    widget.setStyleSheet(stylesheet)
    # creating a opacity effect
    widget.opacity_effect = QGraphicsOpacityEffect()

    # setting opacity level
    widget.opacity_effect.setOpacity(opacity)

    # adding opacity effect to the label
    widget.setGraphicsEffect(widget.opacity_effect)

    widget.setMinimumHeight(10)
    return widget

#
#
