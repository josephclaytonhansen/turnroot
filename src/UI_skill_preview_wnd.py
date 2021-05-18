from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.skeletons.weapon_types import weaponTypes
from src.skeletons.unit_class import unitClass
from src.UI_TableModel import TableModel
from src.node_backend import getFiles, File

import json, math, random

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

class skillPreview(QWidget):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.path = None
        
        self.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        content_widget = QWidget()
        content_widget_layout = QHBoxLayout()
        content_widget_layout.setContentsMargins(10,10,10,10)
        content_widget_layout.setSpacing(0)
        content_widget.setLayout(content_widget_layout)
        
        self.layout.addWidget(content_widget)
        
        #from left to right: skill icon, skill name/skill desciption
        
        image = QPushButton()
        image.clicked.connect(self.change_icon)
        image.setMaximumHeight(150)
        image.setMaximumWidth(150)
        pixmap = QPixmap(135,135)
        pixmap.fill(QColor("white"))
        pixmap = QIcon(pixmap)
        image.setIcon(pixmap)
        image.setIconSize(QSize(135,135))
        image.setToolTip("Edit icon")
        
        content_widget_layout.addWidget(image)
        
        text_area = QWidget()
        text_area_layout = QVBoxLayout()
        text_area.setLayout(text_area_layout)
        
        self.skill_name = QLabel("Skill Name")
        self.skill_name.setAlignment(Qt.AlignCenter)
        self.skill_name_font = self.skill_name.font()
        self.skill_name_font.setPointSize(22)
        self.skill_name.setFont(self.skill_name_font)
        
        text_area_layout.addWidget(self.skill_name)
        
        desc_name = QLineEdit()
        desc_name.setAlignment(Qt.AlignCenter)
        desc_name.setPlaceholderText("Skill description")
        desc_name_font = desc_name.font()
        desc_name_font.setPointSize(15)
        desc_name.setFont(desc_name_font)
        
        text_area_layout.addWidget(desc_name)
        
        content_widget_layout.addWidget(text_area)

    def change_icon(self):
        pass