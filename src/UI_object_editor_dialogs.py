from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor, QFont
from src.UI_updateJSON import updateJSON
import src.UI_colorTheme
import shutil, os, pickle, json, sys, random
from src.UI_Dialogs import confirmAction
from src.node_backend import getFiles, GET_FILES
from src.img_overlay import overlayTile
from src.skeletons.unit_class import unitClass
from src.skeletons.unit import Unit
from src.skeletons.weapon_types import weaponTypes, expTypes

class combatDialog(QDialog):
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
        self.layout.setContentsMargins(8,8,8,8)
        self.setLayout(self.layout)
        
        self.values = {}
        
        q = QLabel("Combat Statistics")
        q.setFont(self.h_font)
        self.layout.addWidget(q, 0, 0, 1,2)
        
        r = 0
        for x in ["might", "hit", "crit", "range", "weight"]:
            r +=1 
            stat_label = QLabel(x)
            stat_label.setFont(self.body_font)
            
            stat_value = QSpinBox()
            stat_value.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
            stat_value.name = x
            stat_value.setFont(self.body_font)
            self.values[x] = stat_value
            stat_value.setRange(0,100)

            try:
                stat_value.setValue(getattr(self.parent.weapon, x))
            except:
                pass

            stat_value.valueChanged.connect(self.change_value)
                
            self.layout.addWidget(stat_label, r, 0, 1, 1)
            self.layout.addWidget(stat_value, r,1,1,1)
            
    def change_value(self):
        setattr(self.parent.weapon, self.sender().name, self.sender().value()) 
        if self.parent.weapon.path != None:
            self.parent.weapon.selfToJSON()