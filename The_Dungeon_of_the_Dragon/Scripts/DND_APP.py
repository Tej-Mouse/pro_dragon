import sys
import subprocess
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
    QScrollArea, QFrame, QCheckBox
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5 import QtCore, Qt
from PyQt5.QtCore import (
    QSize
)
import qdarktheme
from functools import partial
import charecter
import pyqt5_Custom as PYCustom
import appHelperTools as aHT
from Scripts import objectsDnD, Reading, EZPaths
import style


class DnDWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.tcharecter = charecter.CharacterSheet()
        super().__init__()
        qdarktheme.setup_theme()
        self.setWindowTitle("Charecter Sheet")

        self.scroll = QScrollArea()

        main_outer_layout = QVBoxLayout()

        widget_scroll = QWidget()
        self.setCentralWidget(widget_scroll)
        widget_scroll.setLayout(main_outer_layout)

        # Scrolling_______________________________
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumSize(900,500)
        self.scroll.setWidget(widget_scroll)
        self.setCentralWidget(self.scroll)

        # Widget_Scroll -> Main_outer -> {buttons, stacked -> {base_widget/layout, others}}

        # Tab Widgets

        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        main_outer_layout.addLayout(button_layout)
        main_outer_layout.addLayout(self.stacklayout)

        # tab Widgets_________________________________________________________________________________________________
        base_widget = QWidget()
        base_layout = QVBoxLayout()
        base_widget.setLayout(base_layout)
        self.stacklayout.addWidget(base_widget)

        featTrait_widget = QWidget()
        featTraitLayout = QVBoxLayout()
        featTrait_widget.setLayout(featTraitLayout)
        self.stacklayout.addWidget(featTrait_widget)

        inventory_widget = QWidget()
        inventory_layout = QVBoxLayout()
        inventory_widget.setLayout(inventory_layout)
        self.stacklayout.addWidget(inventory_widget)

        options_widget = QWidget()
        options_layout = QVBoxLayout()
        options_widget.setLayout(options_layout)
        self.stacklayout.addWidget(options_widget)

        # Tab Buttons_________________________________________________________________________________________________

        button_layout.addWidget(aHT.CreateTabButton(self.switch_tab, 0, style.LabelFont2,
                                                    style.TabButtonSheet2, "Main Window"))
        button_layout.addWidget(aHT.CreateTabButton(self.switch_tab, 1, style.LabelFont2,
                                                    style.TabButtonSheet2, "Features && Traits"))
        button_layout.addWidget(aHT.CreateTabButton(self.switch_tab, 2, style.LabelFont2,
                                                    style.TabButtonSheet2, "Inventory"))
        button_layout.addWidget(aHT.CreateTabButton(self.switch_tab, 3, style.LabelFont2,
                                                    style.TabButtonSheet2, "Options"))

        """Base Menu_________________________________________________________________________________________________"""
        main_stats_layout = QHBoxLayout()

        # Left_layout_______________________________

        left_stats_layout = QVBoxLayout()

        self.attribute_labels = PYCustom.AllStatWidgets(self.tcharecter)

        # top_layout_______________________________
        self.top_widget = PYCustom.RPWidget(self.tcharecter.get_all_top())

        # Mid_layout_______________________________
        mid_layout = QVBoxLayout()
        self.mid_widget = PYCustom.MiddleWidget(self.tcharecter.get_all_mid_top(), self.tcharecter.get_all_mid_mid())
        mid_layout.addWidget(self.mid_widget.get_widget())

        test_button = QPushButton('test')
        test_button.clicked.connect(partial(self.test))

        # Attack Layout____________________________
        self.weapon_widget = PYCustom.WeaponWidget()
        mid_layout.addWidget(self.weapon_widget.get_widget(), alignment=QtCore.Qt.AlignCenter)

        # Right Layout_____________________________________
        right_layout = QVBoxLayout()

        # RP Trait Layout__________________________________
        self.rp_trait_widget = PYCustom.RPTraitWidget(self.tcharecter.get_all_rp_traits())

        # adding layouts
        left_stats_layout.addWidget(test_button)  # Test
        self.attribute_labels.add_widgets_to_layout(left_stats_layout)

        right_layout.addWidget(self.rp_trait_widget.get_widget())

        main_stats_layout.addLayout(left_stats_layout, stretch=2)
        main_stats_layout.addLayout(mid_layout, stretch=2)
        main_stats_layout.addLayout(right_layout, stretch=1)

        # Adding Main Layout
        base_layout.addWidget(self.top_widget.get_widget())
        base_layout.addLayout(main_stats_layout)

        """Feat & Trait Menu_________________________________________________________________________________________"""

        """Inventory_________________________________________________________________________________________________"""
        self.inventory_widget = PYCustom.InventoryWidget(self.tcharecter.get_inventory())

        inventory_layout.addWidget(self.inventory_widget.get_widget())
        """Options___________________________________________________________________________________________________"""
        saveButton = aHT.CreateGenButton("Save",style.LabelFont1,style.SubButtonSheet,self.save,minWidth=400)

        DarkModeToggle = QCheckBox()
        DarkModeToggle.setText("Dark Mode Toggled: On")
        DarkModeToggle.setFont(style.LabelFont1)
        DarkModeToggle.checked = True
        DarkModeToggle.clicked.connect(partial(self.dark_mode_toggle, DarkModeToggle.setText))
        DarkModeToggle.setStyleSheet(style.SubCheckedSheet)

        frame = QFrame()
        frame.setFrameShape(QFrame.Panel)
        frame.setMinimumWidth(600)
        options_sub_layout = QVBoxLayout(frame)
        options_sub_layout.addWidget(PYCustom.appHelperTools.CreateSeperator())
        options_sub_layout.addWidget(saveButton,alignment=QtCore.Qt.AlignCenter)
        options_sub_layout.addWidget(DarkModeToggle, alignment=QtCore.Qt.AlignCenter)
        options_sub_layout.addWidget(PYCustom.appHelperTools.CreateSeperator())

        options_layout.addWidget(frame,alignment=QtCore.Qt.AlignCenter)

        # options_widget.addLayout(options_layout)

    def test(self):
        # self.tcharecter.alter_attribute('prof','starter_level',
        #                                 self.tcharecter.get_specific_attribute('prof').get_total_base() + 3)
        self.tcharecter.alter_attribute('str','starter_level',800)
        self.tcharecter.alter_attribute('chr', 'starter_level', 8)
        self.tcharecter.alter_attribute('dex', 'starter_level',
                                        self.tcharecter.get_specific_attribute('dex').get_total_base() + 3)
        # self.tcharecter.get_specific_skills('sleight').give_expertise()
        # self.tcharecter.get_specific_top('name').set('Lucas Cyr')
        # self.tcharecter.get_specific_top('class').set('Killer')
        # self.tcharecter.get_specific_top('alignment').set('Neutral Evil')
        # self.tcharecter.get_specific_top('race').set('Other Kin')
        # self.tcharecter.get_specific_top('background').set('France')
        # self.tcharecter.get_specific_top('level').add(1000)
        # self.tcharecter.get_specific_top('experience').add(1000)
        # self.tcharecter.get_specific_mid_top('ac').alter_contrib_base("foo", 18)
        # self.tcharecter.get_specific_mid_mid('death').mark_failure()
        # self.tcharecter.get_specific_mid_mid('hd').set_total_hd(10)
        # self.tcharecter.get_specific_mid_mid('hd').set_d_type(10)
        # self.tcharecter.get_specific_mid_top('mhp').alter_contrib_base("god",1000000)
        # self.tcharecter.get_specific_mid_top('chp').alter_contrib_base("god", 1000000)
        # self.tcharecter.get_specific_rp_traits('ideals').set_text("Man, you don't wanna know")

        inventory = self.tcharecter.get_inventory()
        apple = objectsDnD.Item("Apple", 100, category="Food")
        pear = objectsDnD.Item("Pear", 1)
        ear = objectsDnD.Item("Ear", 10, cost=(100, "gp"))
        sword = objectsDnD.Weapon("Sword", 10, (10000, "gp"), (1, 4),
                                  "piercing", ["Throw"], "Simple")

        inventory.add_item(sword.get_key_name(), sword, 1)
        inventory.add_item(apple.get_key_name(), apple, 1)
        inventory.add_item(pear.get_key_name(), pear, 1)
        inventory.add_item(ear.get_key_name(), ear, 1)
        inventory.add_money(inventory.get_money("gp")[0] + 1, "gp")

        testWeapons = Reading.WeaponReader(EZPaths.Weapon_Path)
        list_weapons = testWeapons.get_all_weapons()
        for i in range(len(list_weapons)):
            inventory.add_item(list_weapons[i].get_key_name(), list_weapons[i], i+1)
        # self.update()
        self.tcharecter.alter_attribute('prof', 'starter_level',
                                        self.tcharecter.get_specific_attribute('prof').get_total_base() + 3)
        self.tcharecter.alter_attribute('chr', 'starter_level', 8)
        self.tcharecter.alter_attribute('dex', 'starter_level',
                                        self.tcharecter.get_specific_attribute('dex').get_total_base() + 3)
        self.tcharecter.get_specific_skills('sleight').give_expertise()
        self.tcharecter.get_specific_top('name').set('Christopher "Terror" Clark')
        self.tcharecter.get_specific_top('class').set('Killer')
        self.tcharecter.get_specific_top('alignment').set('True Evil')
        self.tcharecter.get_specific_top('race').set('Beyond Comprehension')
        self.tcharecter.get_specific_top('background').set('Cracker Barrel')
        self.tcharecter.get_specific_top('level').add(1000)
        self.tcharecter.get_specific_top('experience').add(1000)
        self.tcharecter.get_specific_mid_top('ac').alter_contrib_base("foo", 20)
        self.tcharecter.get_specific_mid_mid('death').mark_failure()
        self.tcharecter.get_specific_mid_mid('hd').set_total_hd(10)
        self.tcharecter.get_specific_mid_mid('hd').set_d_type(10)
        self.tcharecter.get_specific_mid_top('mhp').alter_contrib_base("god", 1000000)
        self.tcharecter.get_specific_mid_top('chp').alter_contrib_base("god", 1000000)
        self.tcharecter.get_specific_rp_traits('ideals').set_text("Man, you don't wanna know")
        self.update()

    def update(self):
        self.attribute_labels.update()
        self.top_widget.update()
        self.mid_widget.update()
        self.rp_trait_widget.update()
        self.inventory_widget.update()

    def switch_tab(self, index: int):
        self.stacklayout.setCurrentIndex(index)

    def dark_mode_toggle(self,set_text_function, isChecked:bool):
        if isChecked:
            set_text_function("Dark Mode Toggled: OFF PLEASE TURN IT BACK ON OH GOD")
            qdarktheme.setup_theme("light")
        else:
            qdarktheme.setup_theme()
            set_text_function("Dark Mode Toggled: On")

    def save(self):
        print("SAVED!!!!")



app = QApplication(sys.argv)

window = DnDWindow()
window.show()

app.exec()
