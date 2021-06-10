from src.img_overlay import overlayTileWithoutScaling
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.node_backend import getFiles, File

import json, math, os, random

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

from src.UI_Dialogs import confirmAction, popupInfo, infoClose
from src.game_directory import gameDirectory

class imageOverlayCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        self.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: 16")
        
        self.top_left = QWidget()
        self.top_left_layout = QVBoxLayout()
        self.top_left.setLayout(self.top_left_layout)
        
        self.right = QWidget()
        self.right_layout = QVBoxLayout()
        self.right.setLayout(self.right_layout)
        
        self.bottom = QWidget()
        self.bottom.setMinimumHeight(160)
        self.bottom.setMaximumHeight(160)
        self.bottom_layout = QHBoxLayout()
        self.bottom.setLayout(self.bottom_layout)
        
        self.layout.addWidget(self.top_left,0,0,2,2)
        self.layout.addWidget(self.right,0,3,1,1)
        self.layout.addWidget(self.bottom,3,0,1,1)
        
        self.canvas = QLabel()
        self.canvas.setAlignment(Qt.AlignCenter)
        self.canvas.setStyleSheet("background-color: white; border: 4px solid black; border-radius: 3px;")
        self.canvas.setMinimumWidth(512)
        self.canvas.setMaximumWidth(512)
        self.canvas.setMinimumHeight(512)
        self.canvas.setMaximumHeight(512)
        
        self.top_left_layout.addWidget(self.canvas)
        
        self.transform_pad = QWidget()
        self.transform_pad.setMaximumWidth(150)
        self.transform_pad.setMaximumHeight(150)
        self.transform_pad_layout = QGridLayout()
        self.transform_pad_layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.transform_pad.setLayout(self.transform_pad_layout)
        
        self.bottom_layout.addWidget(self.transform_pad)
        
        self.transform_pad_buttons = {}
        self.tpb_locs = [[0,1],[1,2],[2,1],[1,0]]
        index = -1
        
        self.timer = QTimer()
        
        for button in ["up", "right", "down", "left"]:
            index += 1
            self.transform_pad_buttons[button] = QPushButton()
            self.transform_pad_buttons[button].direction = button
            
            self.transform_pad_buttons[button].pressed.connect(self.on_press)
            self.transform_pad_buttons[button].released.connect(self.on_release)
            self.timer.timeout.connect(self.while_pressed)
            
            self.transform_pad_buttons[button].setMaximumWidth(50)
            self.transform_pad_buttons[button].setMaximumHeight(50)
            self.transform_pad_buttons[button].setIcon(QIcon(QPixmap("src/ui_icons/white/"+button+".png")))
            self.transform_pad_buttons[button].setIconSize(QSize(48,48))
            self.transform_pad_layout.addWidget(self.transform_pad_buttons[button], self.tpb_locs[index][0], self.tpb_locs[index][1], 1, 1)
        
        for x in [0,1,2]:
            self.transform_pad_layout.setColumnStretch(x, 1)
            self.layout.setColumnStretch(x, 1)
            
        ###TESTING ONLY###
        self.image1 = QPixmap("src/portrait_graphics/blue.png")
        self.image2 = QPixmap("src/portrait_graphics/yellow.png")
        self.overlay_dimensions = [self.image2.width(), self.image2.height()]
        self.pos = [256,256]
        composite = overlayTileWithoutScaling(self.image1, self.image2, 512, self.pos)
        self.canvas.setPixmap(composite)
        #self.canvas.setPixmap(composite).scaled(self.canvas_size, self.canvas_size, Qt.KeepAspectRatio, Qt.FastTransformation)
        
    def on_release(self):
        self.timer.stop()

    def on_press(self):
        self.timer.start(25)
        self.tmp_direction = self.sender().direction

    def while_pressed(self):
        self.move_overlay(self.tmp_direction)

    def move_overlay(self,direction):
        if direction == "up":
            self.pos[1] -= 1
            self.actually_move_overlay()
        elif direction == "right":
            self.pos[0] += 1
            self.actually_move_overlay()
        elif direction == "down":
            self.pos[1] += 1
            self.actually_move_overlay()
        elif direction == "left":
            self.pos[0] -= 1
            self.actually_move_overlay()
    
    def actually_move_overlay(self):
        if self.pos[0] > 512-self.overlay_dimensions[0]:
            self.pos[0] = 512-self.overlay_dimensions[0]
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[1] > 512-self.overlay_dimensions[1]:
            self.pos[1] = 512-self.overlay_dimensions[1]
        if self.pos[1] < 0:
            self.pos[1] = 0
        composite = overlayTileWithoutScaling(self.image1, self.image2, 512, self.pos)
        self.canvas.setPixmap(composite)