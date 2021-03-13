import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon
import json
from UI_updateJSON import updateJSON

ind = 0
entries = ["Appearance", "System", "Keyboard Shortcuts"]
returnv = False

#update below when importing more color themes!
from UI_colorTheme import (
    midnight_spark, midnight_spark_yellow,
    coral_reef,sand_dunes,
    rainforest,charcoal,
    system_light,ocean_waves,
    clouds,chocolate,
    chili_pepper,garden_morning)

color_themes_dict = [midnight_spark, midnight_spark_yellow,
    coral_reef,sand_dunes,
    rainforest,charcoal,
    system_light,ocean_waves,
    clouds,chocolate,
    chili_pepper,garden_morning]
#update portion ends here

data = {"font_size": 15, "rfont_size": 15,
        "active_theme": "midnight_spark_yellow",
        "active_layout": "right_lower", "icon_size": "26",
        "ah_rte": True, "ah_tasks": True, "ah_taskss": True,
        "ah_overlays": False, "theme_changed": False}

data = updateJSON()

with open("preferences.json", "w") as write_file:
    json.dump(data, write_file)
    write_file.close()
    
import UI_colorTheme

active_theme = getattr(UI_colorTheme, data["active_theme"])

#update below when importing more layouts!
from UI_layoutOption import (right_lower,left_lower,lower_lower,left_left,right_right,simple)
layout_dict = [right_lower,left_lower,lower_lower,left_left,right_right,simple]
#update portion ends here

color_themes = []
for x in range(0, len(color_themes_dict)):
    color_themes.append(color_themes_dict[x].name)
if(active_theme.name in color_themes):
    active_index = color_themes.index(active_theme.name)

layout_names = []
for x in range(0, len(layout_dict)):
    layout_names.append(layout_dict[x].name)

class PreferencesDialog(QDialog):

    def __init__(self, parent=None):
        data = updateJSON()
        active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.active_theme = active_theme
        self.active_layout = right_lower

        #sizing options
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
        
        #each stack looks like this
        self.aes = QWidget()
        self.aes_layout = QGridLayout()
        self.aes_layout.setSpacing(25)
        
        self.mfs = QLabel("Label font size")
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
        self.ct.setAlignment( Qt.AlignVCenter)
        self.aes_layout.addWidget(self.ct,4,0)
        self.color_theme_list = QListWidget()
        self.color_theme_list.addItems(color_themes)
        self.color_theme_list.setCurrentRow(active_index)
        self.current_theme_check = color_themes[active_index]
        self.current_font = data["font_size"]
        self.color_theme_list.currentTextChanged.connect(self.color_theme_changed)
        self.aes_layout.addWidget(self.color_theme_list,4,1)
        
        self.ah = QLabel("Auto-hide")
        self.ah.setAlignment(Qt.AlignVCenter)
        self.aes_layout.addWidget(self.ah,5,0,3,0)
        self.ah_rte = QCheckBox("Rules/text editor")
        self.ah_rte.setCheckState(Qt.Checked)
        self.ah_rte.stateChanged.connect(self.ah_rte_changed)
        self.aes_layout.addWidget(self.ah_rte,5,1)
        self.ah_tasks = QCheckBox("Task selector")
        self.ah_tasks.setCheckState(Qt.Checked)
        self.ah_tasks.stateChanged.connect(self.ah_tasks_changed)
        self.aes_layout.addWidget(self.ah_tasks,6,1)
        self.ah_taskss = QCheckBox("Task settings")
        self.ah_taskss.setCheckState(Qt.Checked)
        self.ah_taskss.stateChanged.connect(self.ah_taskss_changed)
        self.aes_layout.addWidget(self.ah_taskss,7,1)
        self.ah_overlays = QCheckBox("Editor overlay buttons")
        self.ah_overlays.setCheckState(0)
        self.ah_overlays.stateChanged.connect(self.ah_overlays_changed)
        self.aes_layout.addWidget(self.ah_overlays,8,1)
        
        self.lo = QPushButton("Layout (click for reference)")
        self.aes_layout.addWidget(self.lo,9,0)
        self.lo_list = QListWidget()
        self.lo_list.addItems(layout_names)
        self.lo_list.setCurrentRow(0)
        self.lo_list.currentTextChanged.connect(self.layout_changed)
        self.aes_layout.addWidget(self.lo_list,9,1)
                
        self.tis = QLabel("Toolbar icon size")
        self.tis.setAlignment(Qt.AlignVCenter)
        self.aes_layout.addWidget(self.tis,10,0)
        self.tis_slider = QSlider(Qt.Horizontal)
        self.tis_slider.setTickPosition(3)
        self.tis_slider.setTickInterval(4)
        self.tis_slider.setValue(int(data["icon_size"]))
        self.tis_slider.setRange(16,48)
        self.tis_slider.setSingleStep(4)
        self.tis_slider.valueChanged.connect(self.tis_size_changed)
        self.aes_layout.addWidget(self.tis_slider,10,1)
        
        self.aes.setLayout(self.aes_layout)
        self.prefs_layout.addWidget(self.aes)
        
        #new stack
        self.sys = QWidget()
        self.sys_layout = QGridLayout()
        self.sys_layout.setSpacing(25)
        
        self.updates = QLabel("Check for updates")
        self.updates.setAlignment(Qt.AlignVCenter)
        self.sys_layout.addWidget(self.updates,0,0)
        self.c_updates = QPushButton("Check for Updates")
        self.c_updates.clicked.connect(self.check_updates)
        self.sys_layout.addWidget(self.c_updates, 0, 1)
        
        self.sys.setLayout(self.sys_layout)
        self.prefs_layout.addWidget(self.sys)
        
        #new stack
        self.shortcuts = QLabel("blue")
        self.prefs_layout.addWidget(self.shortcuts)
        
        self.prefs.setLayout(self.prefs_layout)

        self.prefs_layout.setCurrentIndex(2)

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
        with open("preferences.json", "w") as write_file:
            json.dump(data, write_file)
            write_file.close()
    
    def rfont_size_changed(self, i):
        data = updateJSON()
        rfont_size = i
        data["rfont_size"] = rfont_size
        with open("preferences.json", "w") as write_file:
            json.dump(data, write_file)
            write_file.close()


    def color_theme_changed(self, s):
        data = updateJSON()
        for x in range(0, len(color_themes_dict)):
            if (s == color_themes_dict[x].name):
                self.active_theme = color_themes_dict[x]
        data["active_theme"] = str(self.active_theme.tag)
        if (self.current_theme_check!= s):
            data["theme_changed"] = True
            self.buttonBox.setText("Apply changes and restart")
        with open("preferences.json", "w") as write_file:
            json.dump(data, write_file)
            write_file.close()
                
        self.pref_categories.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.list_background_color)
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)

    
    def ah_rte_changed(self, s):
        pass
    
    def ah_tasks_changed(self, s):
        pass
    
    def ah_taskss_changed(self, s):
        pass
    
    def tis_size_changed(self, i):
        icon_size = i
        data["icon_size"] = str(i)
        with open("preferences.json", "w") as write_file:
            json.dump(data, write_file)
            write_file.close()
    
    def ah_overlays_changed(self, s):
        pass

    def layout_changed(self, s):
        for x in range(0, len(layout_dict)):
            if (s == layout_dict[x].name):
                self.active_layout = layout_dict[x]
    
    def check_updates(self):
        #check for updates
        self.c_updates.setText("No updates found")
        self.c_updates.setEnabled(False)
        
        
