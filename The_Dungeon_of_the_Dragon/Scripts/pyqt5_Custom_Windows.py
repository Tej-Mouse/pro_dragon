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
)
from PyQt5.QtGui import (
    QPalette,
    QColor,
    QFont,
)
from PyQt5.QtCore import (
    QSize
)
from PyQt5 import QtCore, Qt
import qdarktheme
import ruleTools as DT
from functools import partial


class NameWindow(QWidget):

    def __init__(self, name, update):
        super().__init__()
        mainLayout = QVBoxLayout()
        self.name_function = name
        self.update_function = update
        self.setWindowTitle('Name Your Charecter')
        self.setMinimumSize(300,100)
        self.setLayout(mainLayout)
        self.name_edit = QLineEdit()

        self.name_edit.editingFinished.connect(self.name_change)

        mainLayout.addWidget(self.name_edit)
        #
        # name_edit.textChanged.connect(self.tp['name'].set)

    def name_change(self):
        self.name_function(self.name_edit.text())
        self.update_function()
        self.close()


class AlignmentWindow(QWidget):

    def __init__(self, alignment, update):
        super().__init__()
        mainLayout = QGridLayout()
        self.alignment_function = alignment
        self.update_function = update
        self.setWindowTitle('Choose Your Charecters Alignment')
        self.setMinimumSize(300,300)
        self.setLayout(mainLayout)
        self.alignment_labels = [
            ["Lawful Good","Lawful Neutral","Lawful Evil"],
            ["Neutral Good","True Neutral","Neutral Evil"],
            ["Chaotic Good","Chaotic Neutral","Chaotic Evil"]
        ]
        self.buttons = []
        for i in range(3):
            this_row = []
            for j in range(3):
                this_row += [QPushButton()]
                this_row[j].setText(self.alignment_labels[i][j])
                mainLayout.addWidget(this_row[j], i, j)
                this_row[j].clicked.connect(partial(self.alignment_change,(i,j)))
            self.buttons += this_row

    def alignment_change(self,label_coords:tuple):
        new_alignment = self.alignment_labels[label_coords[0]][label_coords[1]]
        self.alignment_function(new_alignment)
        self.update_function()
        self.close()


