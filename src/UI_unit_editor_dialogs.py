from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor, QFont
from src.UI_updateJSON import updateJSON
import src.UI_colorTheme
import shutil, os, pickle, json, sys

class growthRateDialog(QDialog):
    def __init__(self, parent=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setMinimumWidth(500)
        
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        
        with open("src/skeletons/universal_stats.json", "r") as stats_file:
            universal_stats =  json.load(stats_file)
        
        for s in universal_stats:
            self.parent.unit.unit_class.growth_rates[s] = 60
        
        self.list = QListWidget()
        self.list.currentTextChanged.connect(self.list_change)
        self.list.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.list.addItems(universal_stats)
        
        self.layout.addWidget(self.list)
        
        row = QWidget()
        row_layout = QHBoxLayout()
        row.setLayout(row_layout)
        
        row_layout.addWidget(QLabel("0%\n(never increase)"))
        
        self.rate_slider = QSlider(Qt.Horizontal)
        self.rate_slider.name = 1
        self.rate_slider.valueChanged.connect(self.colorizeSlider)
        self.rate_slider.setValue(50)
        self.rate_slider.setRange(0,99)
        self.rate_slider.setSingleStep(1)
        
        row_layout.addWidget(self.rate_slider)
        
        row_layout.addWidget(QLabel("100%\n(always increase)"))
        
        self.layout.addWidget(row)
        
        self.setLayout(self.layout)
    
    def colorizeSlider(self, v):
        try:
            self.parent.unit.unit_class.growth_rates[self.list.currentItem().text()] = v
            self.parent.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.currentText()+".tructf")
        except:
            pass
            
        v = v / 100
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
    
    def list_change(self):
        self.rate_slider.setValue(self.parent.unit.unit_class.growth_rates[self.list.currentItem().text()])
        