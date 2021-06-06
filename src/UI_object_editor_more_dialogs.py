from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor, QFont
from src.UI_updateJSON import updateJSON
import src.UI_colorTheme
import shutil, os, pickle, json, sys, random
from src.UI_Dialogs import confirmAction, popupInfo
from src.node_backend import getFiles, GET_FILES
from src.img_overlay import overlayTile
from src.skeletons.unit_class import unitClass
from src.skeletons.unit import Unit
from src.skeletons.weapon_types import weaponTypes, expTypes
from src.skeletons.Object import (Object,usableItem,Key,healItem,statIncreaseItem,expIncreaseItem,
                                  classChangeItem,summoningItem,levelEffectItem,equippableItem,Weapon,Shield)

class chooseUnitStatDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setMinimumWidth(200)
        self.body_font = font
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)
        
        with open("src/skeletons/universal_stats.json", "r") as stats_file:
            universal_stats =  json.load(stats_file)
        
        self.list = QListWidget()
        self.list.currentTextChanged.connect(self.returnData)
        self.list.setFont(self.body_font)
        self.list.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.list.addItems(universal_stats)
        self.layout.addWidget(self.list)
                
        self.close_button = QPushButton("Close")
        self.close_button.setFont(self.body_font)
        self.layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.close)
    
    def returnData(self):
        self.data = self.sender().currentItem().text()

class forgingDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.body_font = font
        self.h_font = QFont(self.body_font)
        self.h_font.setPointSize(20)
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        active_theme = self.active_theme
        super().__init__(parent)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)
        
        repair_cost_per = QSpinBox()
        repair_items_amounts = QSpinBox()
        self.spinners = [repair_cost_per,repair_items_amounts]
        self.att = ["repair_cost_per","repair_items_amounts"]
        labels = ["Repair Price Per Use","Repair Item Quantity Per 5 Uses*"]
        r = 0
        for x in self.spinners:
            r+=1
            x.setFont(self.body_font)
            x.setRange(0,1000)
            x.name = self.att[self.spinners.index(x)]
            try:
                x.setValue(getattr(self.parent.weapon, self.att[self.spinners.index(x)]))
            except:
                pass
            x.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
            x.valueChanged.connect(self.change_value)
            self.layout.addWidget(x, r, 1, 1, 1)
            label = QLabel(labels[r-1])
            label.setFont(self.body_font)
            self.layout.addWidget(label,r,0,1,1)
        
        self.rate_slider = QSlider(Qt.Horizontal)
        self.rate_slider.name = 1
        self.rate_slider.valueChanged.connect(self.colorizeSlider)
        self.rate_slider.setValue(int(self.parent.weapon.full_durability/2))
        self.rate_slider.setRange(0,self.parent.weapon.full_durability)
        self.rate_slider.setSingleStep(1)
        
        self.layout.addWidget(self.rate_slider,r+5,0,1,3)
        
        h = QLabel("Used, this weapon would cost X to repair...")
        h.setFont(self.h_font)
        self.layout.addWidget(h,r+3,0,1,2)
        t = QLabel("Change used amount")
        t.setToolTip("Durability must be greater than 0. Set with the Combat button")
        t.setFont(self.body_font)
        self.layout.addWidget(t,r+4,0,1,2)
        
        self.used_uses = QLabel("Remaining Uses: ")
        self.used_uses.setFont(self.body_font)
        self.cost = QLabel(" Cost: ")
        self.cost.setFont(self.body_font)
        self.layout.addWidget(self.used_uses, r+6, 0, 1,1)
        self.layout.addWidget(self.cost,r+6,1,1,1)
        self.item_cost = QLabel(" Item Cost: ")
        self.item_cost.setFont(self.body_font)
        self.layout.addWidget(self.item_cost,r+6,2,1,1)
        
        i = QLabel("*Set to 0 if this weapon doesn't require items to repair")
        self.layout.addWidget(i,r+2,0,1,1)
        
    def change_value(self):
        self.cost.setText(" Cost: ")
        self.item_cost.setText(" Item Cost: ")
        setattr(self.parent.weapon, self.sender().name, self.sender().value()) 
        if self.parent.weapon.path != None:
            self.parent.weapon.selfToJSON()
    
    def colorizeSlider(self, v):
        try:
            self.cost_at_use = ((v) * self.parent.weapon.repair_cost_per)
            self.used_uses.setText("Remaining Uses: "+str(self.parent.weapon.full_durability-v))
            self.cost.setText(" Price: "+str(self.cost_at_use))
            self.item_cost.setText(" Item Cost: "+str(round(v/5) * self.parent.weapon.repair_items_amounts))
        except:
            pass
            
        v = v / self.parent.weapon.full_durability
        color_left = QColor(self.active_theme.unit_editor_slider_color_0)
        color_right = QColor(self.active_theme.unit_editor_slider_color_1)
        color_left_c = [color_left.red(), color_left.green(), color_left.blue()]
        color_right_c = [color_right.red(), color_right.green(), color_right.blue()]
        
        distances = [(color_right.red() - color_left.red()),
                     (color_right.green() - color_left.green()),
                     (color_right.blue() - color_left.blue())]
        
        
        new_color = [int(color_left.red() + v * distances[0]),
                     int(color_left.green() + v * distances[1]),
                     int(color_left.blue()+ v * distances[2])]
        
        self.sender().setStyleSheet(
            "QSlider::handle:horizontal {\nbackground-color: "+str(QColor(new_color[0],new_color[1],new_color[2]).name())+";border-radius: 2px;width:40px;height:40px;}"
            )
        
