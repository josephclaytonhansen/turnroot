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

def overlayTile(image, overlay, size):
    image = image.scaled(size,size, Qt.KeepAspectRatio)
    overlay = QPixmap(overlay)
    overlay = overlay.scaled(size,size, Qt.KeepAspectRatio)
    painter = QPainter()
    result = QPixmap(size, size)
    result.fill(Qt.transparent)
    painter.begin(result)
    painter.drawPixmap(0, 0, image)
    painter.drawPixmap(0, 0, overlay)
    painter.end()
    result = result.scaled(size, size, Qt.KeepAspectRatio)
    return result

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
        
        self.image = QPushButton()
        self.image.clicked.connect(self.change_icon)
        self.image.setMaximumHeight(150)
        self.image.setMaximumWidth(150)
        pixmap = QPixmap(135,135)
        pixmap.fill(Qt.transparent)
        p = overlayTile(pixmap, "src/skill_graphics/outer_gold.png", 135)
        g = overlayTile(p, "src/skill_graphics/inner_blue.png", 135)
        pixmap = QIcon(g)
        self.image.setIcon(pixmap)
        self.image.setIconSize(QSize(135,135))
        self.image.setToolTip("Edit icon")
        
        content_widget_layout.addWidget(self.image)
        
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
        self.outer = ["src/skill_graphics/outer_gold.png", "src/skill_graphics/outer_blue.png", "src/skill_graphics/outer_silver.png"]
        self.inner = ["src/skill_graphics/inner_blue.png", "src/skill_graphics/inner_dark_blue.png",
                 "src/skill_graphics/inner_dark_purple.png","src/skill_graphics/inner_dark_teal.png",
                 "src/skill_graphics/inner_gold.png","src/skill_graphics/inner_green.png",
                 "src/skill_graphics/inner_light_green.png","src/skill_graphics/inner_light_red.png",
                 "src/skill_graphics/inner_light_yellow.png","src/skill_graphics/inner_purple.png",
                 "src/skill_graphics/inner_red.png"]
        self.inner2 = ["src/skill_graphics/white_starburst.png","src/skill_graphics/dark_blue_starburst.png",
                       "src/skill_graphics/pink_star.png", "src/skill_graphics/white_star.png",]
        
        self.or_index = 0
        self.ir_index = 0
        self.ic_index = 0
        
        self.max_or_index = len(self.outer)
        self.max_ir_index = len(self.inner)
        self.max_ic_index = len(self.inner2)
        
        r = iconDialog(self.outer,self.inner,self.inner2,parent=self)
        r.exec_()
    
    def left_arrow(self):
        if self.sender().name == 0:
            #outer
            self.or_index -=1
            if self.or_index < 0:
                self.or_index = self.max_or_index-1
                
        elif self.sender().name == 1:
            #inner
            self.ir_index -=1
            if self.ir_index < 0:
                self.ir_index = self.max_ir_index-1
        
        elif self.sender().name == 2:
            #icon
            self.ic_index -=1
            if self.ic_index < 0:
                self.ic_index = self.max_ic_index-1
            
        pixmap = QPixmap(135,135)
        pixmap.fill(Qt.transparent)
        p = overlayTile(pixmap, self.outer[self.or_index], 135)
        g = overlayTile(p, self.inner[self.ir_index], 135)
        d = overlayTile(g, self.inner2[self.ic_index], 135)
        self.d_image.setPixmap(d)

    def right_arrow(self):
        if self.sender().name == 0:
            #outer
            self.or_index +=1
            if self.or_index == self.max_or_index:
                self.or_index = 0
        elif self.sender().name == 1:
            #inner
            self.ir_index +=1
            if self.ir_index == self.max_ir_index:
                self.ir_index = 0
        elif self.sender().name == 2:
            #icon
            self.ic_index +=1
            if self.ic_index == self.max_ic_index:
                self.ic_index = 0
    
        pixmap = QPixmap(135,135)
        pixmap.fill(Qt.transparent)
        p = overlayTile(pixmap, self.outer[self.or_index], 135)
        g = overlayTile(p, self.inner[self.ir_index], 135)
        d = overlayTile(g, self.inner2[self.ic_index], 135)
        self.d_image.setPixmap(d)
        
class iconDialog(QDialog):
    def __init__(self,outer,inner,inner2,parent=None):
        data = updateJSON()
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        
        self.outer = outer
        self.inner = inner
        self.inner2 = inner2
        self.parent = parent
        
        self.rc = False
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        self.parent.d_image = QLabel()
        self.parent.d_image.setAlignment(Qt.AlignHCenter)
        self.parent.d_image.setMaximumHeight(150)
        self.parent.d_image.setMaximumWidth(150)
        pixmap = QPixmap(135,135)
        pixmap.fill(Qt.transparent)
        p = overlayTile(pixmap, "src/skill_graphics/outer_gold.png", 135)
        g = overlayTile(p, "src/skill_graphics/inner_blue.png", 135)
        d = overlayTile(g, "src/skill_graphics/white_starburst.png", 135)
        self.parent.d_image.setPixmap(d)
        
        self.layout.addWidget(self.parent.d_image)
        
        row1 = QWidget()
        row1_layout = QHBoxLayout()
        row1.setLayout(row1_layout)
        
        row2 = QWidget()
        row2_layout = QHBoxLayout()
        row2.setLayout(row2_layout)
        
        row3 = QWidget()
        row3_layout = QHBoxLayout()
        row3.setLayout(row3_layout)
        
        #arrow, label, arrow
        self.left_arrows = {}
        self.right_arrows = {}
        label_dict = {row1_layout: "Outer Rim", row2_layout: "Background Color", row3_layout: "Icon"}
        lo = [row1_layout, row2_layout, row3_layout]
        for row in lo:
            self.left_arrows[row] = QPushButton("<")
            self.left_arrows[row].setMaximumWidth(24)
            self.left_arrows[row].name = lo.index(row)
            self.left_arrows[row].clicked.connect(self.parent.left_arrow)
            row.addWidget(self.left_arrows[row])
            
            row.addWidget(QLabel(label_dict[row]))
            
            self.right_arrows[row] = QPushButton(">")
            self.right_arrows[row].setMaximumWidth(24)
            self.right_arrows[row].name = lo.index(row)
            self.right_arrows[row].clicked.connect(self.parent.right_arrow)
            row.addWidget(self.right_arrows[row])
            
        self.layout.addWidget(row1)
        self.layout.addWidget(row2)
        self.layout.addWidget(row3)
        
        
        row4 = QWidget()
        row4_layout = QHBoxLayout()
        row4.setLayout(row4_layout)
        
        ok_button = QPushButton("Ok")
        ok_button.clicked.connect(self.ok)
        
        
        gfx_button = QPushButton()
        gfx_button.setIcon(QIcon(QPixmap("src/ui_icons/white/package-2-32.png").scaled(32,32, Qt.KeepAspectRatio)))
        gfx_button.setIconSize(QSize(32,32))
        gfx_button.setToolTip("Add different graphics")
        gfx_button.clicked.connect(self.gfx)
        row4_layout.addWidget(gfx_button)
        row4_layout.addWidget(ok_button)
        
        self.layout.addWidget(row4)
        
    def ok(self):
        self.close()
        pixmap = QPixmap(135,135)
        pixmap.fill(Qt.transparent)
        p = overlayTile(pixmap, self.parent.outer[self.parent.or_index], 135)
        g = overlayTile(p, self.parent.inner[self.parent.ir_index], 135)
        d = overlayTile(g, self.parent.inner2[self.parent.ic_index], 135)
        pixmap = QIcon(d)
        self.parent.image.setIcon(pixmap)
    
    def gfx(self):
        pass
    
    