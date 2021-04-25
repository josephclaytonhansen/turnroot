import sys, json, pickle, os, psutil
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon
from src.UI_updateJSON import updateJSON, dumpJSON
from src.UI_Dialogs import infoClose, colorThemeEdit, confirmAction

ind = 0
entries = ["Appearance", "System"]
returnv = False
import src.UI_colorTheme
    
#update below when importing more color themes!
from src.UI_colorTheme import (
    midnight_spark, midnight_spark_yellow,
    sand_dunes,
    rainforest,charcoal,
    ocean_waves
    ,chocolate,
    chili_pepper,custom)

color_themes_dict = [midnight_spark, midnight_spark_yellow,
    sand_dunes,
    rainforest,charcoal,
    ocean_waves
    ,chocolate,
    chili_pepper,custom]

data = {"font_size": 15, "rfont_size": 15,
        "active_theme": "midnight_spark_yellow",
        "active_layout": "right_lower", "icon_size": "26",
        "ah_rte": True, "ah_tasks": True, "ah_taskss": True,
        "ah_overlays": False, "theme_changed": False}

data = updateJSON()
dumpJSON(data)

active_theme = getattr(src.UI_colorTheme, data["active_theme"])

color_themes = []
for x in range(0, len(color_themes_dict)):
    color_themes.append(color_themes_dict[x].name)
if(active_theme.name in color_themes):
    active_index = color_themes.index(active_theme.name)
else:
    active_index = 0

class NodePreferencesDialog(QDialog):
    def __init__(self, parent=None):
        data = updateJSON()
        try:
            active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        except:
            active_theme = getattr(src.UI_colorTheme, "ocean_waves")
        self.active_theme = active_theme

        super().__init__()
        
        self.font_size = data["font_size"]
        self.setWindowTitle("Preferences")
        self.setMinimumHeight(340)
        self.setMaximumHeight(780)
        self.setMaximumWidth(900)
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        
        self.ok_label = "Apply changes"
        QBtn = QPushButton(self.ok_label)
        self.buttonBox = QBtn
        self.buttonBox.clicked.connect(self.accept)
        self.cancelBox = QPushButton("Cancel")
        self.cancelBox.clicked.connect(self.cancel)

        #the overall layout is a grid
        layout = QGridLayout()
        self.pref_categories = QListWidget()
        
        #list categories on the left
        self.pref_categories.addItems(entries)
        self.pref_categories.setMinimumWidth(120)
        self.pref_categories.setMaximumWidth(260)
        self.pref_categories.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.list_background_color)
        self.pref_categories.currentTextChanged.connect(self.category_change)
        
        #options on the right
        self.prefs = QWidget()
        self.prefs.setMinimumWidth(300)
        
        #options are stacked
        self.prefs_layout = QStackedLayout()
        
        self.aes = QWidget()
        self.aes_layout = QGridLayout()
        self.aes_layout.setSpacing(25)
        
        self.aes.setLayout(self.aes_layout)
        self.prefs_layout.addWidget(self.aes)
        
        self.prefs.setLayout(self.prefs_layout)
        
        self.sys = QWidget()
        self.sys_layout = QGridLayout()
        self.sys_layout.setSpacing(25)
        
        self.sys.setLayout(self.sys_layout)
        self.prefs_layout.addWidget(self.sys)

        layout.addWidget(self.pref_categories, 0, 0, 1, 1)
        layout.addWidget(self.prefs, 0, 1, 1, 3)
        layout.addWidget(self.buttonBox, 12, 1)
        layout.addWidget(self.cancelBox, 12, 2)
        
        self.setLayout(layout)
        
    def cancel(self):
        self.close()
        
    def category_change(self, s):
        data = updateJSON()
        for x in range(0, len(entries)):
            if (s == entries[x]):
                ind = x
                self.prefs_layout.setCurrentIndex(ind)
    
    def font_size_changed(self, i):
        data = updateJSON()
        font_size = i
        if (self.current_font != i):
            data["theme_changed"] = True
            self.buttonBox.setText("Apply changes and restart")
        self.pref_categories.setStyleSheet("font-size: "+str(font_size)+"px; background-color: "+self.active_theme.list_background_color)
        self.setStyleSheet("font-size: "+str(font_size)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        data["font_size"] = font_size
        dumpJSON(data)
    
    def rfont_size_changed(self, i):
        data = updateJSON()
        rfont_size = i
        data["rfont_size"] = rfont_size
        dumpJSON(data)

    def color_theme_changed(self, s):
        data = updateJSON()
        for x in range(0, len(color_themes_dict)):
            if (s == color_themes_dict[x].name):
                self.active_theme = color_themes_dict[x]
        data["active_theme"] = str(self.active_theme.tag)
        if (self.current_theme_check!= s):
            data["theme_changed"] = True
            self.buttonBox.setText("Apply changes and restart")
        dumpJSON(data)
                
        self.pref_categories.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.list_background_color)
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
                
