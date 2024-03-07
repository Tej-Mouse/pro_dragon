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
import subPYQTCustom as subPYCustom

LabelFont1 = QFont('Times', 15, QFont.Decorative)

LabelFont2 = QFont('Times', 12, QFont.Decorative)  # Attributes
LabelFont3 = QFont('Times', 10, QFont.Decorative)  # Skills



def create_frame(top_label_str:str, bottom_label_str:str):
    frame = QFrame()
    frame.setFrameShape(QFrame.Panel)
    frame.setMaximumHeight(100)

    layout = QVBoxLayout(frame)

    bottom_label = QLabel()
    bottom_label.setText(bottom_label_str)

    layout.addWidget(create_top_label(top_label_str), alignment=QtCore.Qt.AlignCenter)
    layout.addWidget(bottom_label, alignment=QtCore.Qt.AlignCenter)

    return frame, bottom_label


def create_top_label(string:str):
    top_label = QLabel()
    top_label.setText(string)
    top_label.setFont(LabelFont2)
    return top_label


def button_to_window(button, window):
    pass


class AllStatWidgets:

    def __init__(self, charecter):
        self.charecter = charecter
        self.attribute_labels = {
            'str': StatLayout(
                self.charecter.get_specific_attribute('str'), self.charecter.get_specific_skill_of_attribute('str')),
            'dex': StatLayout(
                self.charecter.get_specific_attribute('dex'), self.charecter.get_specific_skill_of_attribute('dex')),
            'con': StatLayout(
                self.charecter.get_specific_attribute('con'), self.charecter.get_specific_skill_of_attribute('con')),
            'int': StatLayout(
                self.charecter.get_specific_attribute('int'), self.charecter.get_specific_skill_of_attribute('int')),
            'wis': StatLayout(
                self.charecter.get_specific_attribute('wis'), self.charecter.get_specific_skill_of_attribute('wis')),
            'chr': StatLayout(
                self.charecter.get_specific_attribute('chr'), self.charecter.get_specific_skill_of_attribute('chr'))
        }

    def get_specific_layout(self,layout:str):
        return self.attribute_labels[layout]

    def add_widgets_to_layout(self,layout):
        for name in list(self.attribute_labels):
            layout.addWidget(self.attribute_labels[name].get_widget())

    def update(self):
        for name in list(self.attribute_labels):
            self.attribute_labels[name].update()


class StatLayout:

    def __init__(self, attribute: ruleTools.Stat, skills: list[ruleTools.Skill]):
        self.attribute = attribute
        self.skills = skills

        # widget to be returned to app
        self.main_widget = QWidget()

        # Widgets main layout
        outer_layout = QVBoxLayout(self.main_widget)

        # Separators for aestetic
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)

        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)

        outer_layout.addWidget(separator1)

        outer_layout.addWidget(separator2)

        # Layout for left and right side of stats
        main_layout = QHBoxLayout()
        outer_layout.addLayout(main_layout)

        # Frame for attribute labels
        frame1 = QFrame()
        frame1.setFrameShape(QFrame.Panel)
        # Frame for skill labels
        frame2 = QFrame()
        frame2.setFrameShape(QFrame.Panel)

        main_layout.addWidget(frame1)
        main_layout.addWidget(frame2)

        attribute_layout = QVBoxLayout(frame1)
        skill_layout = QVBoxLayout(frame2)

        # Attributes Labels___________
        self.att_labels = [
            QLabel(),
            QLabel()
        ]
        self.att_labels[0].setText(str(attribute.get_total_base()))

        bonus = attribute.get_total_bonus()

        sign = ruleTools.sign_string(bonus)

        self.att_labels[1].setText(sign + str(bonus))
        self.att_labels[1].setFont( QFont('Times', 20, QFont.Decorative))

        # Label for "Strength, Wisdom, etc"
        top_label = QLabel(attribute.get_type())
        top_label.setFont(LabelFont2)

        attribute_layout.addWidget(top_label, alignment=QtCore.Qt.AlignCenter)
        for i in range(len(self.att_labels)):
            attribute_layout.addWidget(self.att_labels[i], alignment=QtCore.Qt.AlignCenter)

        # Skill Labels___________
        self.skill_labels = []
        i = 0
        for name in list(skills):
            skill_string = skills[name].get_type()
            bonus = skills[name].get_total_bonus()
            sign = ruleTools.sign_string(bonus)

            skill_string += ': ' + sign + str(bonus)
            self.skill_labels += [QCheckBox(skill_string)]
            self.skill_labels[i].setFont(LabelFont3)
            self.skill_labels[i].toggled.connect(partial(self.skill_checked, skills[name], self.skill_labels[i]))
            skill_layout.addWidget(self.skill_labels[i], alignment=(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom))
            i += 1

    def get_widget(self):
        return self.main_widget

    def update(self):
        self.attribute.update()

        self.att_labels[0].setText(str(self.attribute.get_total_base()))

        bonus = self.attribute.get_total_bonus()
        sign = ruleTools.sign_string(bonus)
        self.att_labels[1].setText(sign + str(bonus))

        i = 0
        # Update Skills
        for name in list(self.skills):
            self.skills[name].update()
            skill_string = self.skills[name].get_type()
            bonus = self.skills[name].get_total_bonus()
            sign = ruleTools.sign_string(bonus)
            skill_string += ': ' + sign + str(bonus)

            self.skill_labels[i].setText(skill_string)
            i += 1

    def skill_checked(self, skill, button: QCheckBox):
        if button.isChecked():
            skill.give()
        else:
            skill.unlearn()

        self.update()


class RPWidget:

    def __init__(self, top_stats: list[ruleTools.TopStatValue]):
        self.tp = top_stats

        # Main Widget to be given to app
        self.main_widget = QWidget()
        main_layout = QVBoxLayout(self.main_widget)

        # Upper layout has Name, Class and level
        upper_layout = QHBoxLayout()
        # Lower layout has background, race, alignment and exp
        lower_layout = QHBoxLayout()

        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)

        main_layout.addLayout(upper_layout)
        main_layout.addWidget(separator1)
        main_layout.addLayout(lower_layout)
        main_layout.addWidget(separator2)

        # names = ['name',
        #          'class',
        #          'level',
        #          'background',
        #          'race',
        #          'alignment',
        #          'experience']

        self.tp_values = {}

        # Name________________________
        frame = QFrame()
        frame.setFrameShape(QFrame.Panel)

        upper_layout.addWidget(frame)

        inner_label_layout = QVBoxLayout(frame)

        label = QLabel()
        label.setText(self.tp['name'].get_type())
        label.setFont(LabelFont1)

        self.tp_values['name'] = QPushButton()
        self.tp_values['name'].setText(self.tp['name'].get_value())
        self.tp_values['name'].clicked.connect(self.name_window)

        # self.tp_values['name'].setAutoFillBackground(True)
        self.tp_values['name'].setStyleSheet('QPushButton {color: white;}')
        # palette = QPalette()
        # palette.setColor(QPalette.WindowText, QColor('red'))
        # self.tp_values['name'].setPalette(palette)


        name_font = QFont('Times', 15, QFont.Bold)
        self.tp_values['name'].setFont(name_font)


        inner_label_layout.addWidget(label)
        inner_label_layout.addWidget(self.tp_values['name'])

        # Class and Level_______________
        frame = QFrame()
        frame.setFrameShape(QFrame.Panel)

        upper_layout.addWidget(frame)

        inner_label_layout0 = QVBoxLayout(frame)
        inner_label_layout1 = QHBoxLayout(frame)

        label = QLabel()
        label.setText(self.tp['class'].get_type() + ' & ' + self.tp['level'].get_type())
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFont(LabelFont1)

        self.tp_values['class'] = QLabel()
        self.tp_values['level'] = QLabel()
        self.tp_values['class'].setText(self.tp['class'].get_value())
        self.tp_values['class'].setAlignment(QtCore.Qt.AlignRight)
        self.tp_values['level'].setText(str(self.tp['level'].get_value()))
        self.tp_values['level'].setAlignment(QtCore.Qt.AlignLeft)

        inner_label_layout0.addWidget(label)
        inner_label_layout0.addLayout(inner_label_layout1)
        inner_label_layout1.addWidget(self.tp_values['class'])
        inner_label_layout1.addWidget(self.tp_values['level'])

        # Background_______________

        self.standard_label('background', lower_layout)

        # Race_______________

        self.standard_label('race', lower_layout)

        # Alignment_______________

        frame = QFrame()
        frame.setFrameShape(QFrame.Panel)

        lower_layout.addWidget(frame)

        inner_label_layout = QVBoxLayout(frame)

        label = QLabel()
        label.setText(self.tp['alignment'].get_type())
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFont(LabelFont1)

        self.tp_values['alignment'] = QPushButton()
        self.tp_values['alignment'].setText(self.tp['alignment'].get_value())
        self.tp_values['alignment'].clicked.connect(self.alignment_window)
        self.tp_values['alignment'].setStyleSheet('QPushButton {color: white;}')

        inner_label_layout.addWidget(label)
        inner_label_layout.addWidget(self.tp_values['alignment'])

        # Experience____________________
        self.standard_label('experience', lower_layout)

    def standard_label(self, label_name, lower_layout):

        frame = QFrame()
        frame.setFrameShape(QFrame.Panel)

        lower_layout.addWidget(frame)

        inner_label_layout = QVBoxLayout(frame)

        label = QLabel()
        label.setText(self.tp[label_name].get_type())
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFont(LabelFont1)

        self.tp_values[label_name] = QLabel()
        self.tp_values[label_name].setAlignment(QtCore.Qt.AlignCenter)
        self.tp_values[label_name].setText(str(self.tp[label_name].get_value()))

        inner_label_layout.addWidget(label)
        inner_label_layout.addWidget(self.tp_values[label_name])

    def get_widget(self):
        return self.main_widget

    def update(self):
        for name in list(self.tp_values):
            self.tp_values[name].setText(str(self.tp[name].get_value()))

    def name_window(self):
        self.name_w = PYCustomWindows.NameWindow(self.tp['name'].set, self.update)
        self.name_w.show()

    def alignment_window(self):
        self.alignment_w = PYCustomWindows.AlignmentWindow(self.tp['alignment'].set, self.update)
        self.alignment_w.show()



class MiddleWidget:
    def __init__(self, top:list, middle:list):
        self.tp = top
        self.mdl= middle
        self.tp_values = {}
        self.mdl_values = {} # middle values
        # Main Widget to be given to app
        self.main_widget = QWidget()
        main_layout = QVBoxLayout(self.main_widget)



        first_layout_outer = QVBoxLayout()
        first_layout_inner = QHBoxLayout()

        first_layout_outer.addWidget(appHelperTools.CreateSeperator())
        first_layout_outer.addLayout(first_layout_inner)
        first_layout_outer.addWidget(appHelperTools.CreateSeperator())

        # AC_Layout_________________
        frame, self.tp_values["ac"] = create_frame(self.tp["ac"].get_type(),
                                                        str(self.tp["ac"].get_total_base()))
        first_layout_inner.addWidget(frame)

        # init_Layout_________________
        frame, self.tp_values["init"]  = create_frame(self.tp["init"].get_type(),
                                                           self.tp["init"].get_total_bonus_string())
        first_layout_inner.addWidget(frame)

        # Speed_Layout_________________
        frame, self.tp_values["speed"] = create_frame(self.tp["speed"].get_type(),
                                                           str(self.tp["speed"].get_total_base()))
        first_layout_inner.addWidget(frame)


        # Second inner layout_________________________________________________________________________________________

        second_layout_inner = QHBoxLayout()

        first_layout_outer.addWidget(appHelperTools.CreateSeperator())
        first_layout_outer.addLayout(second_layout_inner)
        first_layout_outer.addWidget(appHelperTools.CreateSeperator())

        # Hit Points Max_______________
        frame, self.tp_values["mhp"] = create_frame(self.tp["mhp"].get_type(),
                                                         str(self.tp["mhp"].get_total_base()))
        second_layout_inner.addWidget(frame)

        # Hit Points Current_______________

        frame, self.tp_values["chp"] = create_frame(self.tp["chp"].get_type(),
                                                         str(self.tp["chp"].get_total_base()))
        second_layout_inner.addWidget(frame)

        # Thirds inner layout_________________________________________________________________________________________

        third_layout_inner = QHBoxLayout()

        first_layout_outer.addWidget(appHelperTools.CreateSeperator())
        first_layout_outer.addLayout(third_layout_inner)
        first_layout_outer.addWidget(appHelperTools.CreateSeperator())


        # Total Hit dice_______________

        frame, self.mdl_values["thd"] = create_frame(self.mdl["hd"].get_total_hd_label(),
                                                    str(self.mdl["hd"].get_total_hd_string()))
        third_layout_inner.addWidget(frame)

        # Current Hit dice_______________

        frame, self.mdl_values["chd"] = create_frame(self.mdl["hd"].get_current_hd_label(),
                                                    str(self.mdl["hd"].get_current_hd_string()))
        third_layout_inner.addWidget(frame)

        # Death saving throws_______________

        frame1 = QFrame()
        frame1.setFrameShape(QFrame.Panel)
        frame1.setMaximumHeight(50)

        frame2 = QFrame()
        frame2.setFrameShape(QFrame.Panel)
        frame2.setMaximumHeight(100)

        first_layout_outer.addWidget(appHelperTools.CreateSeperator())
        first_layout_outer.addWidget(frame1)
        first_layout_outer.addWidget(frame2)
        first_layout_outer.addWidget(appHelperTools.CreateSeperator())

        second_outer_layout = QVBoxLayout(frame1)
        top_label = create_top_label(self.mdl["death"].get_type())
        second_outer_layout.addWidget(top_label,alignment=QtCore.Qt.AlignCenter)

        fourth_inner_layout = QHBoxLayout(frame2)

        success_layout = QVBoxLayout()

        success_layout.addWidget(create_top_label(self.mdl["death"].get_success_label()),
                                 alignment=QtCore.Qt.AlignCenter)
        success_checkbox_layout = QHBoxLayout()
        success_layout.addLayout(success_checkbox_layout)

        failure_layout = QVBoxLayout()
        failure_layout.addWidget(create_top_label(self.mdl["death"].get_failure_label()),
                                 alignment=QtCore.Qt.AlignCenter)
        failure_checkbox_layout = QHBoxLayout()
        failure_layout.addLayout(failure_checkbox_layout)

        fourth_inner_layout.addLayout(success_layout)
        fourth_inner_layout.addLayout(failure_layout)

        top_label = QLabel()
        top_label.setText(self.mdl["death"].get_success_label())
        top_label.setFont(LabelFont2)

        self.fcheckboxes = []
        self.wcheckboxes = []

        for i in range(3):
            self.fcheckboxes += [QCheckBox()]
            self.fcheckboxes[i].clicked.connect(partial(self.death_failure))
            failure_checkbox_layout.addWidget(self.fcheckboxes[i],alignment=QtCore.Qt.AlignCenter)

            self.wcheckboxes += [QCheckBox()]
            self.wcheckboxes[i].clicked.connect(partial(self.death_success))
            self.wcheckboxes[i].setStyleSheet('QPushButton {background-color: red; color: red;}')
            success_checkbox_layout.addWidget(self.wcheckboxes[i],alignment=QtCore.Qt.AlignCenter)

        # first_layout_outer.addWidget(frame1)
        # first_layout_outer.addWidget(frame2)

        # self.fcheckboxes[i].setStyleSheet("QCheckBox"
        #                                   "{"
        #                                   "background-color: lightblue"
        #                                   "}" )
        #                                   # "QCheckBox:hover:checked { color: white }"
        #                                   # "}")

        main_layout.addLayout(first_layout_outer)

    def get_widget(self):
        return self.main_widget

    def update(self):
        for name in list(self.tp_values):
            self.tp[name].update()
            self.tp_values[name].update()

            if name == "init":
                self.tp_values[name].setText(self.tp[name].get_total_bonus_string())
            else:
                self.tp_values[name].setText(str(self.tp[name].get_total_base()))

        self.mdl["hd"].update()
        self.mdl_values["thd"].setText(self.mdl["hd"].get_total_hd_string())
        self.mdl_values["chd"].setText(self.mdl["hd"].get_current_hd_string())

        self.mdl["death"].update()
        total_failures = self.mdl["death"].get_num_failure()
        total_successes = self.mdl["death"].get_num_success()

        f = 0
        w = 0
        for i in range(3):
            f += 1
            w += 1
            self.fcheckboxes[i].checked = False
            self.wcheckboxes[i].checked = False

            if f <= total_failures:
                self.fcheckboxes[i].checked = True

            if w <= total_successes:
                self.wcheckboxes[i].checked = True

            self.wcheckboxes[i].setChecked(self.wcheckboxes[i].checked)
            self.fcheckboxes[i].setChecked(self.fcheckboxes[i].checked)

    def death_failure(self,isChecked):

        if isChecked:
            self.mdl["death"].mark_failure()
        else:
            self.mdl["death"].reduce_failure()
        self.update()

    def death_success(self,isChecked):
        if isChecked:
            self.mdl["death"].mark_success()
        else:
            self.mdl["death"].reduce_success()
        self.update()




class WeaponWidget:

    def __init__(self):
        self.main_widget = QFrame()
        self.main_widget.setFrameShape(QFrame.StyledPanel)

        main_layout = QVBoxLayout(self.main_widget )


        main_layout.addWidget(appHelperTools.CreateLabel("Attacks and SpellCasting", LabelFont2),
                              alignment=QtCore.Qt.AlignCenter)

        t = "QLabel {background-color: #a2a2a2;color: black}"
        # Grid Layout
        grid_layout = QGridLayout()
        # grid_layout.SetMaximuHeight
        grid_layout.addWidget(appHelperTools.CreateLabel("Name", LabelFont2, t), 0,0,alignment=QtCore.Qt.AlignCenter)
        grid_layout.addWidget(appHelperTools.CreateLabel("Attack Bonus", LabelFont2, t), 0, 1,alignment=QtCore.Qt.AlignCenter)
        grid_layout.addWidget(appHelperTools.CreateLabel("Damage/Type", LabelFont2, t), 0, 2,1,2,alignment=QtCore.Qt.AlignCenter)


        main_layout.addLayout(grid_layout)


    def get_widget(self):
        return self.main_widget


class FinishedSignal(QObject):
    finishedit = pyqtSignal()


class trait_box(QTextEdit):

    def __init__(self, text:str, font, connectingFunction):
        super().__init__()
        self.setFont(font)
        self.setText(text)
        self.signal = FinishedSignal()
        self.signal.finishedit.connect(connectingFunction)

    def focusOutEvent(self, e):
        super(trait_box,self).focusOutEvent(e)
        self.signal.finishedit.emit()
        self.setReadOnly(True)

    def mousePressEvent(self, e):
        self.setReadOnly(False)
        super(trait_box, self).mousePressEvent(e)


class RPTraitWidget:

    def __init__(self, rp_traits):
        self.main_widget = QWidget()
        main_layout = QVBoxLayout(self.main_widget)

        self.rp_traits = rp_traits

        frame1, ptext = self.create_trait_box("Peronality Trait", self.rp_traits["person"].get_text())
        frame2, itext = self.create_trait_box("Ideals", self.rp_traits["ideals"].get_text())
        frame3, btext = self.create_trait_box("Bonds", self.rp_traits["bonds"].get_text())
        frame4, ftext = self.create_trait_box("Flaws", self.rp_traits["flaws"].get_text())

        max_width = 400

        frame1.setMaximumWidth(max_width)
        frame2.setMaximumWidth(max_width)
        frame3.setMaximumWidth(max_width)
        frame4.setMaximumWidth(max_width)


        self.boxes = {
            "person": ptext,
            "ideals": itext,
            "bonds": btext,
            "flaws": ftext
        }

        main_layout.addWidget(appHelperTools.CreateSeperator())
        main_layout.addWidget(appHelperTools.CreateSeperator())
        main_layout.addWidget(frame1)
        main_layout.addWidget(frame2)
        main_layout.addWidget(frame3)
        main_layout.addWidget(frame4)
        main_layout.addWidget(appHelperTools.CreateSeperator())
        main_layout.addWidget(appHelperTools.CreateSeperator())

    def update(self):
        for name in list(self.boxes):
            self.boxes[name].setText(self.rp_traits[name].get_text())

    def get_widget(self):
        return self.main_widget

    def create_trait_box(self, label_input:str, text:str):
        frame = QFrame()
        frame.setFrameShape(QFrame.Panel)
        frame.setMaximumWidth(600)
        frame.setMinimumWidth(200)
        layout = QVBoxLayout(frame)

        font = QFont('Times', 15, QFont.StyleItalic)
        font.setWeight(12)
        font.setItalic(True)

        textbox = trait_box(text, font, partial(self.save_text))

        label = QLabel()
        label.setFont(LabelFont2)
        label.setText(label_input)

        layout.addWidget(textbox)
        layout.addWidget(label)

        return frame, textbox

    def save_text(self):
        for name in list(self.boxes):
            self.rp_traits[name].set_text(self.boxes[name].toPlainText())


class InventoryWidget:

    def __init__(self,tinventory:charManagers.Inventory):
        self.main_widget = QFrame()
        self.main_widget.setFrameShape(QFrame.Panel)

        inventory_layout = QVBoxLayout(self.main_widget)

        top_sub_layout = QHBoxLayout()

        money_style = "QLabel { border-radius: 9px}"

        money_layout = QGridLayout()

        money_text = ["CP", "SP","EP","GP","PP"]


        self.tinventory = tinventory
        money_value = self.tinventory.get_money()

        self.widgets = {}
        for i in range(5):
            money_layout.addWidget(appHelperTools.CreateSeperator(), 0, i)

        self.widgets["currency_amounts"] = []
        for i in range(1,2*len(money_text)+1,2):
            # CURRENTY DENOMINATION LABELS
            money_layout.addWidget(appHelperTools.CreateLabel(money_text[int(i / 2)], LabelFont1, money_style), i, 1)
            money_layout.addWidget(appHelperTools.CreateSeperator(), i + 1, 1)

            # CURRENCY AMOUNT LABELS
            self.widgets["currency_amounts"] += [appHelperTools.CreateLabel(str(money_value[int(i / 2)]), LabelFont1, money_style)]
            money_layout.addWidget(self.widgets["currency_amounts"][int(i/2)], i, 3)
            money_layout.addWidget(appHelperTools.CreateSeperator(), i + 1, 3)
            # V SEPERATORS

            money_layout.addWidget(appHelperTools.CreateVSeperator(), i, 0)
            money_layout.addWidget(appHelperTools.CreateVSeperator(), i + 1, 0)
            money_layout.addWidget(appHelperTools.CreateVSeperator(), i, 2)
            money_layout.addWidget(appHelperTools.CreateVSeperator(), i + 1, 2)
            money_layout.addWidget(appHelperTools.CreateVSeperator(), i, 4)
            money_layout.addWidget(appHelperTools.CreateVSeperator(), i + 1, 4)

        # Inventory Options________________________________________________________

        inventory_options_widget = QFrame()
        inventory_options_layout = QVBoxLayout(inventory_options_widget)
        inventory_options_widget.setFrameShape(QFrame.WinPanel)

        inventory_proper_widget = QFrame()
        inventory_proper_layout = QHBoxLayout(inventory_proper_widget)
        inventory_proper_widget.setFrameShape(QFrame.Box)


        top_sub_layout.addLayout(money_layout,stretch=1)
        top_sub_layout.addWidget(inventory_options_widget, stretch=2)
        inventory_layout.addLayout(top_sub_layout, stretch=1)
        inventory_layout.addWidget(inventory_proper_widget, stretch=3)

        # Inventory ________________________________________________________
        self.left_inventory_layout = QGridLayout()
        self.right_inventory_layout = QGridLayout()


        inventory_proper_layout.addLayout(self.left_inventory_layout)
        inventory_proper_layout.addLayout(self.right_inventory_layout)



        self.create_item_labels()

    def get_widget(self):
        return self.main_widget

    def update(self):
        money_value = self.tinventory.get_money()
        for i in range(len(self.widgets["currency_amounts"])):
            self.widgets["currency_amounts"][i].setText(str(money_value[i]))
        self.create_item_labels()

    def create_item_labels(self, order="alphabetical", reverse=False):
        items = self.tinventory.get_all_items(order, reverse)
        halfway = int(len(items) / 2)

        k = 0
        for i in range(0,halfway):
            self.left_inventory_layout.addWidget(subPYCustom.ItemLabel(items[i], LabelFont2), i, 0)
            k += 1

        self.left_inventory_layout.setRowStretch(k + 2, 1)


        k = 0
        for i in range(halfway,len(items)):
            self.right_inventory_layout.addWidget(subPYCustom.ItemLabel(items[i], LabelFont2), k, 0)
            k += 1

        self.right_inventory_layout.setRowStretch(k + 2, 1)







