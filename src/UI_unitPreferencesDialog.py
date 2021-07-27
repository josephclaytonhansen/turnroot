import sys, json, pickle, os, psutil
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon
from src.UI_updateJSON import updateJSON, dumpJSON
from src.UI_Dialogs import infoClose, colorThemeEdit, confirmAction

ind = 0
entries = ["Appearance"]
returnv = False
import src.UI_colorTheme
    
#update below when importing more color themes!
from src.UI_colorTheme import (
    midnight_spark,
    sand_dunes,
    rainforest,charcoal,
    ocean_waves
    ,chocolate,
    chili_pepper,turnroot,custom)

color_themes_dict = [midnight_spark,
    sand_dunes,
    rainforest,charcoal,
    ocean_waves
    ,chocolate,
    chili_pepper,turnroot,custom]
  
#update portion ends here

data = {"font_size": 15, "rfont_size": 15,
        "active_theme": "midnight_spark_yellow",
        "active_layout": "right_lower", "icon_size": "26",
        "ah_rte": True, "ah_tasks": True, "ah_taskss": True,
        "ah_overlays": False, "theme_changed": False}

data = updateJSON()
dumpJSON(data)

active_theme = getattr(src.UI_colorTheme, data["active_theme"])

from src.UI_layoutOption import (right_lower,left_lower,left_left,right_right)
layout_dict = [right_lower,left_lower,left_left,right_right]

color_themes = []
for x in range(0, len(color_themes_dict)):
    color_themes.append(color_themes_dict[x].name)
if(active_theme.name in color_themes):
    active_index = color_themes.index(active_theme.name)
else:
    active_index = 0

class unitOptionsDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        try:
            active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        except:
            active_theme = getattr(src.UI_colorTheme, "ocean_waves")
        self.active_theme = active_theme

        #sizing options
        super().__init__()
        self.body_font = font
        self.setWindowTitle("Preferences")
        self.setMinimumHeight(340)
        self.setMaximumHeight(780)
        self.setMaximumWidth(900)
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.ok_label = "Apply changes"
        QBtn = QPushButton(self.ok_label)
        self.buttonBox = QBtn
        self.buttonBox.clicked.connect(self.accept)
        self.buttonBox.setFont(self.body_font)
        self.cancelBox = QPushButton("Cancel")
        self.cancelBox.clicked.connect(self.cancel)
        self.cancelBox.setFont(self.body_font)

        #the overall layout is a grid
        layout = QGridLayout()
        self.pref_categories = QListWidget()
        self.pref_categories.setFont(self.body_font)
        
        #list categories on the left
        self.pref_categories.addItems(entries)
        self.pref_categories.setMinimumWidth(120)
        self.pref_categories.setMaximumWidth(260)
        self.pref_categories.setStyleSheet("background-color: "+self.active_theme.list_background_color)
        self.pref_categories.currentTextChanged.connect(self.category_change)
        
        #options on the right
        self.prefs = QWidget()
        self.prefs.setMinimumWidth(300)
        
        #options are stacked
        self.prefs_layout = QStackedLayout()
        
        #each stack looks like this
        self.aes = QWidget()
        self.aes_layout = QGridLayout()
        self.aes_layout.setSpacing(25)
        
        self.mfs = QLabel("Label font size")
        self.mfs.setFont(self.body_font)
        self.mfs.setAlignment(Qt.AlignVCenter)
        self.aes_layout.addWidget(self.mfs,0,0)
        self.font_slider = QSlider(Qt.Horizontal)
        self.font_slider.setTickPosition(3)
        self.font_slider.setTickInterval(2)
        self.font_slider.setValue(data["font_size"])
        self.font_slider.setRange(8,30)
        self.font_slider.setSingleStep(1)
        self.font_slider.valueChanged.connect(self.font_size_changed)
        self.aes_layout.addWidget(self.font_slider,0,1)
        
        self.rfs = QLabel("Text editor font size")
        self.rfs.setFont(self.body_font)
        self.rfs.setAlignment( Qt.AlignVCenter)
        self.aes_layout.addWidget(self.rfs,2,0)
        self.rfont_slider = QSlider(Qt.Horizontal)
        self.rfont_slider.setTickPosition(3)
        self.rfont_slider.setTickInterval(2)
        self.rfont_slider.setValue(data["rfont_size"])
        self.rfont_slider.setRange(8,30)
        self.rfont_slider.setSingleStep(1)
        self.rfont_slider.valueChanged.connect(self.rfont_size_changed)
        self.aes_layout.addWidget(self.rfont_slider,2,1)
        
        self.ct = QLabel("Color theme\n (will automatically restart)")
        self.ct.setFont(self.body_font)
        self.ct.setAlignment( Qt.AlignVCenter)
        self.aes_layout.addWidget(self.ct,4,0)
        self.color_theme_list = QListWidget()
        self.color_theme_list.setFont(self.body_font)
        self.color_theme_list.setStyleSheet("background-color:"+self.active_theme.list_background_color+";")
        self.color_theme_list.addItems(color_themes)
        self.color_theme_list.setCurrentRow(active_index)
        self.current_theme_check = color_themes[active_index]
        self.current_font = data["font_size"]
        self.color_theme_list.currentTextChanged.connect(self.color_theme_changed)
        self.aes_layout.addWidget(self.color_theme_list,4,1)
        self.ct_edit = QPushButton("Edit color theme")
        self.ct_edit.setFont(self.body_font)
        self.ct_edit.clicked.connect(self.colorThemeDialog)
        self.aes_layout.addWidget(self.ct_edit,5,1)
        
        self.tis = QLabel("Toolbar icon size")
        self.tis.setFont(self.body_font)
        self.tis.setAlignment(Qt.AlignVCenter)
        self.aes_layout.addWidget(self.tis,11,0)
        self.tis_slider = QSlider(Qt.Horizontal)
        self.tis_slider.setTickPosition(3)
        self.tis_slider.setTickInterval(4)
        self.tis_slider.setValue(int(data["icon_size"]))
        self.tis_slider.setRange(16,48)
        self.tis_slider.setSingleStep(4)
        self.tis_slider.valueChanged.connect(self.tis_size_changed)
        self.aes_layout.addWidget(self.tis_slider,11,1)
        
        self.de_label = QLabel("Default editor")
        self.de_label.setFont(self.body_font)
        self.de = QComboBox()
        self.de.setFont(self.body_font)
        self.de.currentTextChanged.connect(self.default_editor_changed)
        self.de.addItems(["Unit/Class Editor","Skill Editor", "Portrait Editor", "Object Editor", "Level Editor"])
        self.de.setCurrentText(data["default_editor"])
        self.de_label.setAlignment(Qt.AlignVCenter)
        self.aes_layout.addWidget(self.de_label,12,0)
        self.aes_layout.addWidget(self.de,12,1)
        
        self.aes.setLayout(self.aes_layout)
        self.prefs_layout.addWidget(self.aes)
        
        #finalize layout
        
        self.prefs.setLayout(self.prefs_layout)

        self.prefs_layout.setCurrentIndex(2)

        layout.addWidget(self.pref_categories, 0, 0, 1, 1)
        layout.addWidget(self.prefs, 0, 1, 1, 3)
        layout.addWidget(self.buttonBox, 12, 1)
        layout.addWidget(self.cancelBox, 12, 2)
        self.setLayout(layout)

    def cancel(self):
        self.close()

    def colorThemeDialog(self):
        c = confirmAction(parent=self, s="edit this color theme")
        c.exec_()
        if(c.return_confirm):
            d= colorThemeEdit(parent=self)
            d.exec_()

        
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
        
    def default_editor_changed(self,s):
        data["default_editor"] = s
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
    
    def tis_size_changed(self, i):
        icon_size = i
        data["icon_size"] = str(i)
        self.buttonBox.setText("Apply changes and restart")
        dumpJSON(data)
    
    


