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

        self.setFixedSize(1000,450)
        
        self.back = QLabel("",self)
        self.back.setPixmap(QPixmap("src/ui_images/triangle.png"))
        self.back.show()
        self.back.move(0,0)
        self.back.raise_()
        
        self.ok = QPushButton(QIcon(), "Save and Close", self)
        self.ok.setFont(parent.body_font)
        self.ok.setMinimumHeight(48)
        self.ok.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        self.ok.clicked.connect(self.ok_clicked)
        
        self.wt = QPushButton(QIcon(), "Edit Weapon Types", self)
        self.wt.setFont(parent.body_font)
        self.wt.setMinimumHeight(48)
        self.wt.setMinimumWidth(280)
        self.wt.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        self.wt.clicked.connect(self.ok_clicked)
        
        self.top_1 = QComboBox(self)
        self.top_1.setFont(parent.body_font)
        self.top_1.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        
        self.top_2 = QComboBox(self)
        self.top_2.setFont(parent.body_font)
        self.top_2.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        
        self.right_1 = QComboBox(self)
        self.right_1.setFont(parent.body_font)
        self.right_1.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        
        self.right_2 = QComboBox(self)
        self.right_2.setFont(parent.body_font)
        self.right_2.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        
        self.left_1 = QComboBox(self)
        self.left_1.setFont(parent.body_font)
        self.left_1.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        
        self.left_2 = QComboBox(self)
        self.left_2.setFont(parent.body_font)
        self.left_2.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        
        self.outliers_list = QListView(self)
        self.outliers_list.setFont(parent.body_font)
        self.outliers_list.setMaximumWidth(200)
        self.outliers_list.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        
        self.ok.show()
        self.ok.move(860, 380)
        self.ok.raise_()
        
        self.wt.show()
        self.wt.move(70, 380)
        self.wt.raise_()
        
        self.top_1.show()
        self.top_1.move(270, 50)
        self.top_1.raise_()
        
        self.top_2.show()
        self.top_2.move(360, 50)
        self.top_2.raise_()
        
        self.right_1.show()
        self.right_1.move(480, 300)
        self.right_1.raise_()
        
        self.right_2.show()
        self.right_2.move(570, 300)
        self.right_2.raise_()
        
        self.left_1.show()
        self.left_1.move(70, 300)
        self.left_1.raise_()
        
        self.left_2.show()
        self.left_2.move(160, 300)
        self.left_2.raise_()
        
        self.outliers_list.show()
        self.outliers_list.move(770, 50)
        self.outliers_list.raise_()

        self.show()
        
    def ok_clicked(self):
        self.return_confirm = True
        self.close()

