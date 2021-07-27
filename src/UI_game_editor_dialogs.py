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
        super().__init__(parent)
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)

        self.setFixedSize(900,600)
        
        self.back = QLabel("",self)
        self.back.setPixmap(QPixmap("src/ui_images/triangle.png"))
        self.back.show()
        self.back.move(0,0)
        self.back.raise_()
        
        self.ok = QPushButton(QIcon(), "Ok", self)    
        self.ok.clicked.connect(self.ok_clicked)
        
        self.ok.show()
        self.ok.move(50, 10)
        self.ok.raise_()

        self.show()
        
    def ok_clicked(self):
        self.return_confirm = True
        self.close()
