from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor, QFont
from src.UI_updateJSON import updateJSON
import src.UI_colorTheme
import shutil, os, pickle, json, sys

class weaponTriangle(QDialog):
    def __init__(self, parent=None):
        data = updateJSON()
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        active_theme = self.active_theme
        super().__init__(parent)
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: white;color:black;")

        self.setFixedSize(1000,500)
        
        self.back = QLabel("",self)
        self.back.setPixmap(QPixmap("src/ui_images/triangle.png"))
        self.back.show()
        self.back.move(0,0)
        self.back.raise_()
        
        self.ok = QPushButton(QIcon(), "Ok", self)
        self.ok.setFont(parent.body_font)
        self.ok.setMinimumHeight(48)
        self.ok.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        self.ok.clicked.connect(self.ok_clicked)
        
        self.wt = QPushButton(QIcon(), "Edit Weapon Types", self)
        self.wt.setFont(parent.body_font)
        self.wt.setMinimumHeight(48)
        self.wt.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        self.wt.clicked.connect(self.ok_clicked)
        
        self.ok.show()
        self.ok.move(900, 420)
        self.ok.raise_()
        
        self.wt.show()
        self.wt.move(730, 420)
        self.wt.raise_()

        self.show()
        
    def ok_clicked(self):
        self.return_confirm = True
        self.close()

