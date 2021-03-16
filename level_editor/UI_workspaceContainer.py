import sys
import os
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap
import qtmodern.styles
import qtmodern.windows
from UI_updateJSON import updateJSON
from UI_ProxyStyle import ProxyStyle
from UI_Dialogs import confirmAction
import UI_colorTheme
from UI_color_test_widget import Color
import json
import math

current_tile = None
tiles = {0:{}, 1:{}, 2:{}, 3:{}}

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
                self.squares[self.count].setScaledContents( True )
                self.squares[self.count].clicked.connect(self.change_color)
                self.squares[self.count].right_clicked.connect(self.reset_color)
                self.squares[self.count].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.layout.addWidget(self.squares[self.count], x, y)
                if self.checker % 2 == 0:
                    self.squares[self.count].setStyleSheet("color: white; background-color: black;")
                else:
                    self.squares[self.count].setStyleSheet("color: white; background-color: #111111;")
                if x % 5 == 0 and y % 5 == 0:
                    self.squares[self.count].setText(str(self.squares[self.count].gridIndex))
        self.setLayout(self.layout)
    
    def change_color(self):
        global current_tile
        self.sender().setPixmap(current_tile)
        
    def reset_color(self):
        self.sender().clear()
        
class ClickableQLabel(QLabel):
    clicked=pyqtSignal()
    right_clicked=pyqtSignal()
    QLabel.gridIndex = 0
    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self.clicked.emit()
        elif ev.button() == Qt.RightButton:
            self.right_clicked.emit()

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
 
class Tiles(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        data = updateJSON()
        global tiles

        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: black;color: "+self.active_theme.window_text_color)
        self.pixmap = QPixmap("tiles/ple_grass_basic.png")
        self.label = QLabel()
        self.label.setPixmap(self.pixmap)
        self.layout = QGridLayout()
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        
        for x in range(0,14):
            for y in range(0,4):
                tiles[y][x] = ClickableQLabel()
                tiles[y][x].clicked.connect(self.assignCurrentTile)
                tiles[y][x].setPixmap(self.pixmap.copy(x*32, y*32, 32, 32).scaled(int(64), int(64), Qt.KeepAspectRatio))
                tiles[y][x].setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.layout.addWidget(tiles[y][x], y+1, x+1)
    
    def assignCurrentTile(self):
        global current_tile
        global tiles
        for x in range(0,14):
            for y in range(0,4):
                tiles[y][x].setStyleSheet("background-color: black;")
        current_tile = self.sender().pixmap()
        self.sender().setStyleSheet("background-color: "+self.active_theme.window_background_color+";")
        
                
    

            


    