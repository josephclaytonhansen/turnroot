import sys
import os
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon
import qtmodern.styles
import qtmodern.windows
from UI_updateJSON import updateJSON
from UI_ProxyStyle import ProxyStyle
from UI_Dialogs import confirmAction
import UI_colorTheme
from UI_color_test_widget import Color
import json
import math
   
class workspaceContainer(QWidget):
        def __init__(self, workspace, layout):
            super().__init__()
            self.setAutoFillBackground(True)
            data = updateJSON()
            self.active_theme = getattr(UI_colorTheme, data["active_theme"])
            self.setStyleSheet("font-size: "+str(data["font_size"])+"px;color: "+self.active_theme.window_text_color)
            palette = self.palette()
            self.background_color = QColor(self.active_theme.workspace_background_color)
            palette.setColor(QPalette.Window, self.background_color)
            self.setPalette(palette)
            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(2,2,2,2)
            self.layout.setSpacing(4)
            self.label = QLabel("Label")
            font = self.label.font()
            font.setPointSize(int(data["icon_size"])/2)
            self.label.setFont(font)
            self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            self.layout.addWidget(self.label)
            self.layout.addWidget(Color(self.active_theme.window_background_color))
            self.layout.addWidget(Color(self.active_theme.list_background_color))
            self.setLayout(self.layout)

class showWorkspace(QPushButton):
    def __init__(self, workspace, layout):
        super().__init__()
        data = updateJSON()
        self.workspace = workspace
        self.layout = layout
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.setText("+")
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.setFixedSize((int(data["icon_size"]) -3), (int(data["icon_size"]) -3))
        
class hideWorkspace(QPushButton):
    def __init__(self, workspace, layout):
        super().__init__()
        data = updateJSON()
        self.workspace = workspace
        self.layout = layout
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.setText("—")
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.setFixedSize((int(data["icon_size"])-3), (int(data["icon_size"])-3))

class tileGridWorkspace(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.squares = {}
        self.count = 0
        self.checker = 0
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.width = self.geometry().width()
        self.height = self.geometry().height()
        self.setMinimumWidth(self.width)
        self.setMaximumHeight(self.height)
        self.ratio = self.width/self.height
        #each square is ratio width/1 height
        for x in range(0,int(int(self.height/(50*self.ratio))*4.4)):
            self.checker = self.checker + 1
            for y in range(0,int(int(self.width/50)*4.4)):
                
                self.count = self.count + 1
                self.checker = self.checker + 1
                self.squares[self.count] = ClickableQLabel()
                self.squares[self.count].gridIndex = self.count
                self.squares[self.count].clicked.connect(self.change_color)
                self.squares[self.count].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.layout.addWidget(self.squares[self.count], x, y)
                if self.checker % 2 == 0:
                    self.squares[self.count].setStyleSheet("color: white; background-color: black;")
                else:
                    self.squares[self.count].setStyleSheet("color: white; background-color: #222222;")
        self.setLayout(self.layout)
    
    def change_color(self):
        self.sender().setStyleSheet("color: white; background-color: red;")
        print(self.sender().gridIndex)
        
class ClickableQLabel(QLabel):
    clicked=pyqtSignal()
    QLabel.gridIndex = 0
    def mousePressEvent(self, ev):
        self.clicked.emit()

class toolsWorkspace(QWidget):
        def __init__(self, workspace, layout, labels):
            super().__init__()
            self.setAutoFillBackground(True)
            data = updateJSON()
            self.active_theme = getattr(UI_colorTheme, data["active_theme"])
            self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
            
            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(0,0,0,0)
            self.layout.setSpacing(0)
            self.k = QWidget()
            self.k.setMinimumHeight(0)
            self.k.setMinimumWidth(int(data["icon_size"])+6)
            self.layout.addWidget(self.k)
            for x in range(0, len(labels)):
                self.layout.addWidget(labels[x])
                labels[x].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                labels[x].setMinimumHeight(int(data["icon_size"]))
                labels[x].setMinimumWidth(int(data["icon_size"]))
            self.setLayout(self.layout)
            
    

            


    