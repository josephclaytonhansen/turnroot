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

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

#update below when importing more color themes!
from src.UI_colorTheme import (
    midnight_spark,
    sand_dunes,
    rainforest,charcoal,
    ocean_waves
    ,chocolate,
    chili_pepper,custom)

color_themes_dict = [midnight_spark,
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

node_data = {"edge_type": EDGE_TYPE_BEZIER}

data = updateJSON()
dumpJSON(data)
   
with open("src/tmp/nesc.json", "r") as readfile:
    grid_const = json.load(readfile)
    GRID_SIZE = grid_const[4]
    GRID_ALT = grid_const[5]

with open("src/tmp/neec.json", "r") as readfile:
    edge_const = json.load(readfile)
    WIDTH = edge_const[0]
    SELECTED_WIDTH = edge_const[1]

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
        global node_data
        data = updateJSON()
        
        with open("src/tmp/node_preferences.json", "r") as r:
            node_data = json.load(r)

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
        
        self.ct = QLabel("Color theme")
        self.ct.setAlignment( Qt.AlignVCenter)
        self.aes_layout.addWidget(self.ct,4,0)
        self.color_theme_list = QListWidget()
        self.color_theme_list.setStyleSheet("background-color:"+self.active_theme.list_background_color+";")
        self.color_theme_list.addItems(color_themes)
        self.color_theme_list.setCurrentRow(active_index)
        self.current_theme_check = color_themes[active_index]
        self.current_font = data["font_size"]
        self.color_theme_list.currentTextChanged.connect(self.color_theme_changed)
        self.aes_layout.addWidget(self.color_theme_list,4,1)
        self.ct_edit = QPushButton("Edit color theme")
        self.ct_edit.clicked.connect(self.colorThemeDialog)
        self.aes_layout.addWidget(self.ct_edit,5,1)
        
        self.ls = QLabel("Node wire style")
        self.ls.setAlignment( Qt.AlignVCenter)
        self.aes_layout.addWidget(self.ls,6,0)
        
        self.radioGroup = QWidget()
        self.radioGroup_layout = QHBoxLayout()
        self.radioGroup.setLayout(self.radioGroup_layout)
        
        self.ls_radio_straight = QRadioButton("Straight")
        if node_data["edge_type"] == EDGE_TYPE_BEZIER:
            self.ls_radio_straight.setChecked(False)
        else:
            self.ls_radio_straight.setChecked(True)
        self.ls_radio_straight.edge_type = EDGE_TYPE_DIRECT
        self.ls_radio_straight.toggled.connect(self.changeWireType)
        self.radioGroup_layout.addWidget(self.ls_radio_straight)
        
        self.ls_radio_curved = QRadioButton("Curved")
        if node_data["edge_type"] == EDGE_TYPE_BEZIER:
            self.ls_radio_curved.setChecked(True)
        else:
            self.ls_radio_curved.setChecked(False)
        self.ls_radio_curved.edge_type = EDGE_TYPE_BEZIER
        self.ls_radio_curved.toggled.connect(self.changeWireType)
        self.radioGroup_layout.addWidget(self.ls_radio_curved)
        self.aes_layout.addWidget(self.radioGroup,6,1)
        
        self.gs = QLabel("Grid spacing")
        self.ls.setAlignment( Qt.AlignVCenter)
        self.aes_layout.addWidget(self.gs,7,0)
        self.gs_boxes = QWidget()
        self.gs_boxes_layout = QHBoxLayout()
        self.gs_boxes.setLayout(self.gs_boxes_layout)
        
        self.grid_size_box_label = QLabel("Small")
        self.grid_size_alt_box_label = QLabel("Large")
        self.grid_size_box = QSpinBox()
        self.grid_size_box.setStyleSheet("background-color:"+self.active_theme.list_background_color+";")
        self.grid_size_box.setRange(10,60)
        self.grid_size_box.setValue(GRID_SIZE)
        self.grid_size_box.valueChanged.connect(self.gridSmallChanged)
        self.grid_size_alt_box = QSpinBox()
        self.grid_size_alt_box.setStyleSheet("background-color:"+self.active_theme.list_background_color+";")
        self.grid_size_alt_box.setRange(2,10)
        self.grid_size_alt_box.setValue(GRID_ALT)
        self.grid_size_alt_box.valueChanged.connect(self.gridLargeChanged)
        
        self.gs_boxes_layout.addWidget(self.grid_size_box_label)
        self.gs_boxes_layout.addWidget(self.grid_size_box)
        self.gs_boxes_layout.addWidget(self.grid_size_alt_box_label)
        self.gs_boxes_layout.addWidget(self.grid_size_alt_box)
        self.aes_layout.addWidget(self.gs_boxes, 7,1)
        
        self.ww = QLabel("Wire width")
        self.ls.setAlignment( Qt.AlignVCenter)
        self.aes_layout.addWidget(self.ww,8,0)
        self.ww_boxes = QWidget()
        self.ww_boxes_layout = QHBoxLayout()
        self.ww_boxes.setLayout(self.ww_boxes_layout)
        
        self.wire_width_label = QLabel("Normal")
        self.wire_width_label_selected = QLabel("Selected")
        self.wire_width = QSpinBox()
        self.wire_width.setStyleSheet("background-color:"+self.active_theme.list_background_color+";")
        self.wire_width.setRange(1,20)
        self.wire_width.setValue(WIDTH)
        self.wire_width.valueChanged.connect(self.wireWidthChanged)
        self.wire_width_selected = QSpinBox()
        self.wire_width_selected.setStyleSheet("background-color:"+self.active_theme.list_background_color+";")
        self.wire_width_selected.setRange(2,30)
        self.wire_width_selected.setValue(SELECTED_WIDTH)
        self.wire_width_selected.valueChanged.connect(self.wireSelectedWidthChanged)
        
        self.ww_boxes_layout.addWidget(self.wire_width_label)
        self.ww_boxes_layout.addWidget(self.wire_width)
        self.ww_boxes_layout.addWidget(self.wire_width_label_selected)
        self.ww_boxes_layout.addWidget(self.wire_width_selected)
        self.aes_layout.addWidget(self.ww_boxes, 8,1)

        
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
    
    def gridLargeChanged(self):
        with open("src/tmp/nesc.json", "w") as write:
            grid_const[5] = self.sender().value()
            json.dump(grid_const, write)
    
    def gridSmallChanged(self):
        with open("src/tmp/nesc.json", "w") as write:
            grid_const[4] = self.sender().value()
            json.dump(grid_const, write)
    
    def wireWidthChanged(self):
        with open("src/tmp/neec.json", "w") as write:
            edge_const[0] = self.sender().value()
            json.dump(edge_const, write)
    
    def wireSelectedWidthChanged(self):
        with open("src/tmp/neec.json", "w") as write:
            edge_const[1] = self.sender().value()
            json.dump(edge_const, write)
        
    def cancel(self):
        self.close()
    
    def changeWireType(self):
        print(self.sender().edge_type)
        node_data["edge_type"] = self.sender().edge_type
        with open("src/tmp/node_preferences.json", "w") as wf:
            json.dump(node_data, wf)
        
    def colorThemeDialog(self):
        c = confirmAction(parent=self, s="edit this color theme")
        c.exec_()
        if(c.return_confirm):
            data["theme_changed"] == True
            dumpJSON(data)
            d= colorThemeEdit(parent=self)
            d.exec_()
        
    def category_change(self, s):
        data = updateJSON()
        for x in range(0, len(entries)):
            if (s == entries[x]):
                ind = x
                self.prefs_layout.setCurrentIndex(ind)
    
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
                
